#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPUStack ローカルLLMチャットボットアプリケーション
Streamlitを使用したシンプルなUI
"""

import os
import json
import time
import requests
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# GPUStackの設定
GPUSTACK_API_BASE = os.getenv("GPUSTACK_API_BASE", "http://localhost:8000/v1")
GPUSTACK_API_KEY = os.getenv("GPUSTACK_API_KEY", "")

# アプリケーションのタイトルと説明
st.set_page_config(
    page_title="GPUStack ローカルLLMチャットボット",
    page_icon="🤖",
    layout="wide",
)

# サイドバーのタイトルとロゴ
st.sidebar.title("GPUStack ローカルLLMチャットボット")
st.sidebar.image("https://raw.githubusercontent.com/sambanova/gpustack/main/docs/assets/GPUStack_Logo.png", width=200)
st.sidebar.markdown("---")

def check_gpustack_connection():
    """GPUStackとの接続を確認する"""
    try:
        response = requests.get(f"{GPUSTACK_API_BASE}/models", timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    except Exception as e:
        st.error(f"GPUStackサーバーとの接続中にエラーが発生しました: {str(e)}")
        return False

def get_available_models():
    """デプロイされているモデルのリストを取得する"""
    headers = {}
    if GPUSTACK_API_KEY:
        headers["Authorization"] = f"Bearer {GPUSTACK_API_KEY}"
    
    try:
        response = requests.get(f"{GPUSTACK_API_BASE}/models", headers=headers)
        if response.status_code == 200:
            models_data = response.json()
            # アクティブなモデルのみをフィルタリング
            models = [model["id"] for model in models_data["data"] if model["status"] == "RUNNING"]
            return models
        return []
    except:
        return []

def get_model_usage():
    """モデルの使用状況を取得する"""
    headers = {}
    if GPUSTACK_API_KEY:
        headers["Authorization"] = f"Bearer {GPUSTACK_API_KEY}"
    
    try:
        response = requests.get(f"{GPUSTACK_API_BASE}/metrics", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def chat_with_model(model, messages, max_tokens=500, temperature=0.7, top_p=0.95):
    """モデルとチャットする"""
    client = OpenAI(
        api_key=GPUSTACK_API_KEY or "dummy_key",
        base_url=GPUSTACK_API_BASE
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        return response.choices[0].message.content
    except requests.exceptions.ConnectionError:
        st.error("GPUStackサーバーとの接続が切断されました。サーバーが実行中か確認してください。")
        return None
    except Exception as e:
        error_msg = str(e)
        if "模倣" in error_msg or "imitating" in error_msg:
            st.warning("モデルがレスポンスの生成を停止しました。別の質問を試してみてください。")
        else:
            st.error(f"エラーが発生しました: {error_msg}")
        return None

def init_session_state():
    """セッション状態を初期化する"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "model" not in st.session_state:
        st.session_state.model = None
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = 500
    
    if "top_p" not in st.session_state:
        st.session_state.top_p = 0.95
    
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0
    
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    
    if "token_history" not in st.session_state:
        st.session_state.token_history = []

def display_chat_history():
    """チャット履歴を表示する"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def display_metrics():
    """メトリクスをグラフで表示する"""
    token_history = st.session_state.token_history
    
    if token_history:
        df = pd.DataFrame(token_history)
        
        # トークン使用量のグラフ
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["timestamp"], df["tokens"], marker="o", linestyle="-", color="blue")
        ax.set_title("トークン使用量の推移")
        ax.set_xlabel("時間")
        ax.set_ylabel("トークン数")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True)
        st.pyplot(fig)
        
        # 統計情報
        st.markdown(f"**総リクエスト数:** {st.session_state.request_count}")
        st.markdown(f"**総トークン使用量:** {st.session_state.token_count}")
        
        if len(df) > 1:
            avg_tokens = df["tokens"].mean()
            st.markdown(f"**平均トークン使用量/リクエスト:** {avg_tokens:.2f}")

def main():
    """メイン関数"""
    init_session_state()
    
    # GPUStackとの接続を確認（リトライ機能付き）
    connected = False
    for i in range(3):  # 最大3回リトライ
        if check_gpustack_connection():
            connected = True
            break
        if i < 2:  # 最後のリトライではメッセージを表示しない
            st.info(f"GPUStackサーバーへの接続を試みています... ({i+1}/3)")
            time.sleep(2)
    
    if not connected:
        st.error("GPUStackサーバーに接続できません。サーバーが実行中であることを確認してください。")
        st.info("以下のコマンドを実行してGPUStackを起動してください:")
        st.code("gpustack start")
        return
    
    # 利用可能なモデルを取得
    available_models = get_available_models()
    
    if not available_models:
        st.warning("デプロイされているモデルが見つかりません。モデルをデプロイしてください。")
        st.info("以下のコマンドを実行してモデルをデプロイしてください:")
        st.code("python ../scripts/model_setup.py")
        return
    
    # サイドバーにパラメータ設定
    with st.sidebar:
        st.header("モデル設定")
        
        selected_model = st.selectbox(
            "モデルを選択",
            available_models,
            index=0 if available_models else None
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="値が高いほど、より創造的な応答になります"
        )
        
        max_tokens = st.slider(
            "最大トークン数",
            min_value=100,
            max_value=2000,
            value=st.session_state.max_tokens,
            step=100,
            help="生成する応答の最大トークン数"
        )
        
        top_p = st.slider(
            "Top P",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.05,
            help="トークン選択の確率閾値"
        )
        
        st.session_state.model = selected_model
        st.session_state.temperature = temperature
        st.session_state.max_tokens = max_tokens
        st.session_state.top_p = top_p
        
        st.markdown("---")
        
        # システムプロンプトの設定
        st.subheader("システムプロンプト")
        system_prompt = st.text_area(
            "AIアシスタントの役割を設定",
            value="あなたは役立つAIアシスタントです。ユーザーの質問に簡潔かつ正確に回答してください。",
            height=100
        )
        
        st.markdown("---")
        
        # メトリクスの表示
        st.subheader("使用状況")
        display_metrics()
    
    # メインエリアのタイトル
    st.title("GPUStack ローカルLLMチャットボット")
    st.caption(f"現在のモデル: {st.session_state.model}")
    
    # チャット履歴を表示
    display_chat_history()
    
    # 新しいメッセージの入力
    user_input = st.chat_input("メッセージを入力してください...")
    
    if user_input:
        # ユーザーメッセージを追加
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # モデルからの応答を取得
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("考え中...")
            
            # チャットの履歴を作成
            history = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages:
                history.append({"role": msg["role"], "content": msg["content"]})
            
            # モデルとチャット
            start_time = time.time()
            response = chat_with_model(
                st.session_state.model,
                history,
                max_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature,
                top_p=st.session_state.top_p
            )
            end_time = time.time()
            
            if response:
                message_placeholder.markdown(response)
                
                # アシスタントメッセージを追加
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # メトリクスを更新
                st.session_state.request_count += 1
                
                # トークン数の概算（実際のトークン数はAPIから取得できれば理想的）
                # 簡易的な推定として、単語数の1.3倍をトークン数として計算
                estimated_tokens = int(len(response.split()) * 1.3)
                st.session_state.token_count += estimated_tokens
                
                st.session_state.token_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "tokens": estimated_tokens,
                    "elapsed_time": end_time - start_time
                })

if __name__ == "__main__":
    main()

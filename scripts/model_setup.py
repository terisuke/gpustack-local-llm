#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPUStack モデルセットアップスクリプト
Apple Silicon Mac向けに最適化された軽量モデルを自動的にデプロイします
"""

import os
import sys
import subprocess
import json
import time
import requests
from getpass import getpass

# GPUStackのAPIエンドポイント
API_BASE = "http://localhost:8000/v1"

def check_gpustack_running():
    """GPUStackが実行中かどうかを確認する"""
    try:
        response = requests.get(f"{API_BASE}/models")
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        pass
    return False

def start_gpustack():
    """GPUStackを起動する"""
    print("GPUStackを起動しています...")
    try:
        subprocess.Popen(["gpustack", "start"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        # APIが応答するまで待機
        for _ in range(30):  # 最大30秒間待機
            if check_gpustack_running():
                print("GPUStackが起動しました")
                return True
            time.sleep(1)
        print("GPUStackの起動に失敗しました")
        return False
    except Exception as e:
        print(f"GPUStackの起動中にエラーが発生しました: {e}")
        return False

def get_or_create_api_key():
    """APIキーを取得または作成する"""
    api_key_file = os.path.expanduser("~/.gpustack/api_key.txt")
    
    # ファイルからAPIキーを読み込む
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
            if api_key:
                print("既存のAPIキーを使用します")
                return api_key
    
    # APIキーがない場合は入力を求める
    print("GPUStackのAPIキーが必要です")
    print("Playground UI (http://localhost:8000) で生成したAPIキーを入力してください")
    print("または、空のままEnterを押すと、このスクリプトはAPIキーなしで続行します")
    api_key = getpass("APIキー: ").strip()
    
    # 入力されたAPIキーを保存
    if api_key:
        os.makedirs(os.path.dirname(api_key_file), exist_ok=True)
        with open(api_key_file, "w") as f:
            f.write(api_key)
        print("APIキーを保存しました")
    
    return api_key

def list_available_models(api_key):
    """利用可能なモデルのリストを取得する"""
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    try:
        response = requests.get(f"{API_BASE}/models/available", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"モデルリストの取得に失敗しました: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"モデルリストの取得中にエラーが発生しました: {e}")
        return None

def list_deployed_models(api_key):
    """デプロイ済みのモデルのリストを取得する"""
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    try:
        response = requests.get(f"{API_BASE}/models", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"デプロイ済みモデルリストの取得に失敗しました: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"デプロイ済みモデルリストの取得中にエラーが発生しました: {e}")
        return None

def deploy_model(model_id, api_key):
    """モデルをデプロイする"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }
    
    payload = {
        "model_id": model_id,
        "device": "mps" if sys.platform == "darwin" and "arm" in os.uname().machine else "cuda",
        "type": "llm"
    }
    
    try:
        print(f"モデル '{model_id}' をデプロイしています...")
        response = requests.post(f"{API_BASE}/models/deploy", headers=headers, json=payload)
        if response.status_code == 200:
            print(f"モデル '{model_id}' が正常にデプロイされました")
            return True
        else:
            print(f"モデルのデプロイに失敗しました: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"モデルのデプロイ中にエラーが発生しました: {e}")
        return False

def recommend_models_for_mac():
    """Mac向けの推奨モデルリストを返す"""
    return [
        "TheBloke/Qwen2.5-0.5B-Instruct-GGUF",
        "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        "TheBloke/Llama-3.1-8B-Instruct-GGUF",
        "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "neural-chat/neural-chat-7b-v3-1-GGUF",
    ]

def main():
    print("GPUStack モデルセットアップスクリプトを開始します...")
    
    # GPUStackが実行中かどうかを確認
    if not check_gpustack_running():
        if not start_gpustack():
            print("GPUStackが実行されていません。先に 'gpustack start' を実行してください。")
            sys.exit(1)
    
    # APIキーを取得
    api_key = get_or_create_api_key()
    
    # デプロイ済みのモデルをリスト表示
    deployed_models = list_deployed_models(api_key)
    if deployed_models:
        print("\n現在デプロイされているモデル:")
        for model in deployed_models["data"]:
            print(f" - {model['id']} ({model['status']})")
    
    # 既にモデルがデプロイされている場合は処理を終了
    if deployed_models and len(deployed_models["data"]) > 0:
        print("\nすでにモデルがデプロイされています。新しいモデルをデプロイする場合は、")
        print("Playground UI (http://localhost:8000) から行うか、このスクリプトを修正してください。")
        sys.exit(0)
    
    # 利用可能なモデルをリスト表示
    available_models = list_available_models(api_key)
    if not available_models:
        print("利用可能なモデルリストを取得できませんでした。")
        sys.exit(1)
    
    # Mac向けの推奨モデルをリスト表示
    mac_models = recommend_models_for_mac()
    
    print("\nApple Silicon Mac向けの推奨モデル:")
    for i, model_id in enumerate(mac_models, 1):
        print(f"{i}. {model_id}")
    
    # ユーザーにモデルを選択させる
    choice = 0
    while choice < 1 or choice > len(mac_models):
        try:
            choice = int(input("\nデプロイするモデルの番号を選択してください (1-{}): ".format(len(mac_models))))
        except ValueError:
            print("有効な番号を入力してください")
    
    selected_model = mac_models[choice - 1]
    print(f"\nモデル '{selected_model}' をデプロイします...")
    
    # モデルをデプロイ
    success = deploy_model(selected_model, api_key)
    
    if success:
        print("\nセットアップが完了しました！")
        print("次のステップ:")
        print("1. Playground UI (http://localhost:8000) でモデルをテスト")
        print("2. チャットボットを起動するには 'cd app && streamlit run app.py' を実行")
    else:
        print("\nセットアップに失敗しました。")
        print("GPUStackログを確認し、問題を解決してから再試行してください。")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

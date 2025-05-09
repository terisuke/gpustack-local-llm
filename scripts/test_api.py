#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPUStack APIテストスクリプト
GPUStackの接続状態、モデルの状態、およびシンプルなレスポンスをテストします
"""

import os
import sys
import json
import requests
import argparse
from getpass import getpass

# GPUStackのAPIエンドポイント
API_BASE = "http://localhost:8000/v1"

def check_gpustack_running():
    """GPUStackが実行中かどうかを確認する"""
    try:
        response = requests.get(f"{API_BASE}/models")
        if response.status_code == 200:
            print("✅ GPUStackサーバーに正常に接続できました")
            return True
        else:
            print(f"❌ GPUStackサーバーに接続できましたが、エラーが返されました: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ GPUStackサーバーに接続できません。サーバーが実行中であることを確認してください。")
        return False
    except Exception as e:
        print(f"❌ 接続テスト中にエラーが発生しました: {e}")
        return False

def list_models(api_key=None):
    """デプロイされているモデルのリストを取得する"""
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.get(f"{API_BASE}/models", headers=headers)
        if response.status_code == 200:
            models_data = response.json()
            print("デプロイされているモデル:")
            for model in models_data["data"]:
                status_emoji = "✅" if model["status"] == "RUNNING" else "⚠️"
                print(f"{status_emoji} {model['id']} ({model['status']})")
            return models_data["data"]
        else:
            print(f"❌ モデルリストの取得に失敗しました: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ モデルリストの取得中にエラーが発生しました: {e}")
        return None

def test_model_response(model_id, api_key=None):
    """モデルからの応答をテストする"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "あなたは役立つAIアシスタントです。"},
            {"role": "user", "content": "こんにちは、今日の気分はどうですか？"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print(f"モデル '{model_id}' をテストしています...")
        response = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ モデルが正常に応答しました")
            print("\n応答内容:")
            print("-" * 50)
            print(result["choices"][0]["message"]["content"])
            print("-" * 50)
            return True
        else:
            print(f"❌ モデルの応答テストに失敗しました: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ モデルのテスト中にエラーが発生しました: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="GPUStack APIをテストするスクリプト")
    parser.add_argument("--api-key", help="GPUStackのAPIキー")
    args = parser.parse_args()
    
    api_key = args.api_key
    
    print("GPUStack APIテストを開始します...\n")
    
    # GPUStackが実行中かどうかを確認
    if not check_gpustack_running():
        print("\nGPUStackサーバーが実行されていないようです。以下のコマンドを実行してください:")
        print("  gpustack start")
        return 1
    
    # APIキーの取得（コマンドライン引数で指定されていない場合）
    if not api_key:
        print("\nAPIキーが指定されていません。空のままEnterを押すとAPIキーなしで続行します。")
        api_key = getpass("APIキー (オプション): ").strip() or None
    
    print("\n--- モデルリスト ---")
    models = list_models(api_key)
    
    if not models or len(models) == 0:
        print("\nデプロイされているモデルがありません。モデルをデプロイしてください:")
        print("  python model_setup.py")
        return 1
    
    # 実行中のモデルのみをフィルタリング
    running_models = [model for model in models if model["status"] == "RUNNING"]
    
    if not running_models:
        print("\n実行中のモデルがありません。モデルが起動するのを待つか、新しいモデルをデプロイしてください。")
        return 1
    
    # モデル応答のテスト
    print("\n--- モデル応答テスト ---")
    model_id = running_models[0]["id"]
    test_model_response(model_id, api_key)
    
    print("\nテストが完了しました。")
    return 0

if __name__ == "__main__":
    sys.exit(main())

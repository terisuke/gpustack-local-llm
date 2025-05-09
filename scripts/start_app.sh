#!/bin/bash

# GPUStack ローカルLLMチャットボット 起動スクリプト

set -e

# プロジェクトルートディレクトリの確認
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

# 仮想環境の有効化
if [ -d "venv" ]; then
    echo "仮想環境を有効化しています..."
    source venv/bin/activate
else
    echo "仮想環境が見つかりません。セットアップを実行してください。"
    echo "  ./scripts/install.sh"
    exit 1
fi

# GPUStackが実行中かどうかを確認
echo "GPUStackの状態を確認しています..."
gpustack_running=false
if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "GPUStackは既に実行中です"
    gpustack_running=true
else
    echo "GPUStackを起動しています..."
    gpustack start > /dev/null 2>&1 &
    
    # GPUStackの起動を待機
    echo "GPUStackの起動を待機しています..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
            echo "GPUStackが起動しました"
            gpustack_running=true
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
fi

if [ "$gpustack_running" = false ]; then
    echo "GPUStackの起動に失敗しました。手動で起動してください。"
    echo "  gpustack start"
    exit 1
fi

# モデルのデプロイ状態を確認
echo "モデルの状態を確認しています..."
if ! python -c "import requests; exit(0 if requests.get('http://localhost:8000/v1/models').json()['data'] else 1)"; then
    echo "デプロイされているモデルが見つかりません。モデルセットアップを実行します..."
    python scripts/model_setup.py
fi

# Streamlitアプリケーションを起動
echo "チャットボットアプリケーションを起動しています..."
cd app
streamlit run app.py

exit 0

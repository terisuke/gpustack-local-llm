#!/bin/bash

# GPUStack スタートアップスクリプト

set -e

echo "GPUStack スタートアップスクリプトを開始します..."

# プロジェクトルートディレクトリの確認
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

# 仮想環境を有効化
if [ -d "venv" ]; then
    echo "仮想環境を有効化しています..."
    source venv/bin/activate
else
    echo "仮想環境が見つかりません。先に install.sh を実行してください。"
    exit 1
fi

# GPUStackの起動
echo "GPUStackを起動しています..."
gpustack start &

# GPUStackの起動を待機
echo "GPUStackの起動を待機しています..."
sleep 10

# Streamlitアプリケーションの起動
echo "Streamlitアプリケーションを起動しています..."
cd app && streamlit run app.py 
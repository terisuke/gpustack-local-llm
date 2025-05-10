#!/bin/bash

# GPUStack セッション起動スクリプト

set -e

# クリーンアップ関数の定義
cleanup() {
    echo "クリーンアップを実行しています..."
    if [ ! -z "$GPUSTACK_PID" ]; then
        kill $GPUSTACK_PID 2>/dev/null || true
    fi
    exit 0
}

# シグナルハンドラの設定
trap cleanup SIGINT SIGTERM

echo "GPUStack セッションを開始します..."

# プロジェクトルートディレクトリの確認
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

# Gitの更新を確認
if [ -d ".git" ]; then
    echo "Gitリポジトリの更新を確認しています..."
    git pull
fi

# 依存関係の更新
./scripts/update_dependencies.sh

# GPUStackの起動
echo "GPUStackを起動しています..."
gpustack start &
GPUSTACK_PID=$!

# バックグラウンドプロセスの終了を待機
wait $GPUSTACK_PID

echo "セッションの準備が完了しました！"
echo "アプリケーションを起動するには:"
echo "cd app && streamlit run app.py"

exit 0 
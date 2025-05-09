#!/bin/bash

# GPUStack起動スクリプト

set -e

# シグナルハンドリングの設定
cleanup() {
    echo -e "\nGPUStackを停止します..."
    # 実行中のプロセスを終了
    if [ ! -z "$GPUSTACK_PID" ]; then
        kill $GPUSTACK_PID 2>/dev/null || true
    fi
    # 仮想環境を無効化
    deactivate 2>/dev/null || true
    echo "GPUStackを停止しました。"
    exit 0
}

# SIGINT (Ctrl+C) と SIGTERM をトラップ
trap cleanup SIGINT SIGTERM

echo "GPUStackを起動します..."

# 仮想環境のパス
VENV_PATH="venv"

# 仮想環境の有効化
echo "仮想環境を有効化します..."
source "$VENV_PATH/bin/activate"

# GPUStackの起動
echo "GPUStackサーバーを起動します..."
echo "Ctrl+C で停止できます"
gpustack start --port 8080 &
GPUSTACK_PID=$!

# プロセスの終了を待機
wait $GPUSTACK_PID 
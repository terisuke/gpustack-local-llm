#!/bin/bash

# GPUStackの権限修正スクリプト

set -e

echo "GPUStackの権限を修正します..."

# データベースファイルの場所
DB_PATH="/var/lib/gpustack/database.db"
DB_DIR="/var/lib/gpustack"

# 仮想環境のパス
VENV_PATH="venv"
THIRD_PARTY_PATH="$VENV_PATH/lib/python3.10/site-packages/gpustack/third_party/bin"

# ディレクトリが存在しない場合は作成
if [ ! -d "$DB_DIR" ]; then
    echo "ディレクトリを作成します: $DB_DIR"
    sudo mkdir -p "$DB_DIR"
fi

# データベース関連の権限を修正
echo "データベースディレクトリの権限を修正します..."
sudo chown -R $USER:staff "$DB_DIR"
sudo chmod -R u+rwX "$DB_DIR"

if [ -f "$DB_PATH" ]; then
    echo "データベースファイルの権限を修正します..."
    sudo chown $USER:staff "$DB_PATH"
    sudo chmod 664 "$DB_PATH"
fi

# サードパーティバイナリの権限を修正
echo "サードパーティバイナリの権限を修正します..."
if [ -d "$THIRD_PARTY_PATH" ]; then
    # Fastfetchの権限を修正
    if [ -f "$THIRD_PARTY_PATH/fastfetch/fastfetch" ]; then
        echo "Fastfetchの権限を修正します..."
        sudo chmod +x "$THIRD_PARTY_PATH/fastfetch/fastfetch"
    fi

    # llama-boxの権限を修正
    if [ -f "$THIRD_PARTY_PATH/llama-box/llama-box-rpc-server" ]; then
        echo "llama-box-rpc-serverの権限を修正します..."
        sudo chmod +x "$THIRD_PARTY_PATH/llama-box/llama-box-rpc-server"
    fi

    # その他のサードパーティバイナリの権限を修正
    echo "その他のサードパーティバイナリの権限を修正します..."
    sudo chmod -R +x "$THIRD_PARTY_PATH"
fi

echo "権限の修正が完了しました。"

# 仮想環境の有効化とGPUStackの起動
echo "仮想環境を有効化します..."
source "$VENV_PATH/bin/activate"

echo "GPUStackを起動します..."
gpustack start --port 8080 
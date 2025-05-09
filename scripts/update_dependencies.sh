#!/bin/bash

# GPUStack 依存関係更新スクリプト

set -e

echo "GPUStack 依存関係の更新を開始します..."

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

# pipのアップグレード
echo "pipをアップグレードしています..."
pip install --upgrade pip

# 依存関係の更新
echo "GPUStackを更新しています..."
pip install --upgrade gpustack

echo "アプリケーションの依存関係を更新しています..."
pip install --upgrade -r app/requirements.txt

echo "依存関係の更新が完了しました！"
echo "次のステップ:"
echo "1. 'gpustack start' でGPUStackを再起動"
echo "2. アプリケーションを再起動"

exit 0 
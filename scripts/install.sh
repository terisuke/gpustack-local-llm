#!/bin/bash

# GPUStack インストールスクリプト
# Apple Silicon Mac向けに最適化されています

set -e

echo "GPUStack インストールスクリプトを開始します..."

# Python 3.10以上の確認
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
else
    echo "Python 3.10以上が見つかりませんでした。"
    echo "以下のコマンドでインストールしてください："
    echo "brew install python@3.10"
    exit 1
fi

# Pythonバージョンの確認
python_version=$($PYTHON_CMD --version 2>&1)
echo "使用するPythonバージョン: $python_version"

# MacとApple Siliconの確認
if [[ $(uname) == "Darwin" ]]; then
    echo "MacOS環境を検出しました"
    
    if [[ $(uname -m) == "arm64" ]]; then
        echo "Apple Silicon (arm64) アーキテクチャを検出しました"
    else
        echo "Intel Macを検出しました"
    fi
else
    echo "MacOS以外の環境を検出しました。このスクリプトはMacOS向けに最適化されています。"
fi

# プロジェクトルートディレクトリの確認
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

# 仮想環境の確認と作成
if [ ! -d "venv" ]; then
    echo "Python仮想環境を作成しています..."
    $PYTHON_CMD -m venv venv
    echo "仮想環境を作成しました"
fi

# 仮想環境を有効化
echo "仮想環境を有効化しています..."
source venv/bin/activate

# 必要なパッケージのインストール
echo "必要なパッケージをインストールしています..."
pip install --upgrade pip
pip install wheel

# GPUStackのインストール
echo "GPUStackをインストールしています..."
pip install gpustack

# Streamlitとその他の依存関係のインストール
echo "Streamlitとその他のアプリケーションの依存関係をインストールしています..."
pip install -r app/requirements.txt

echo "インストールが完了しました！"
echo "次のステップ:"
echo "1. 'source venv/bin/activate' で仮想環境を有効化"
echo "2. 'gpustack init' でGPUStackを初期化"
echo "3. 'gpustack start' でGPUStackを起動"
echo "4. モデルをセットアップするには 'python scripts/model_setup.py' を実行"
echo "5. チャットボットを起動するには 'cd app && streamlit run app.py' を実行"

exit 0

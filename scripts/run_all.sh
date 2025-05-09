

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

cleanup() {
    echo -e "\nすべてのサービスを停止します..."
    if [ ! -z "$GPUSTACK_PID" ]; then
        kill -TERM $GPUSTACK_PID 2>/dev/null || true
    fi
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill -TERM $STREAMLIT_PID 2>/dev/null || true
    fi
    pkill -f "gpustack" || true
    pkill -f "streamlit run" || true
    deactivate 2>/dev/null || true
    echo "すべてのサービスを停止しました。"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "GPUStack と Streamlit を起動します..."

VENV_PATH="venv"

echo "仮想環境を有効化します..."
source "$VENV_PATH/bin/activate"

echo "GPUStackサーバーを起動します..."
gpustack start --port 8080 &
GPUSTACK_PID=$!

echo "GPUStackの起動を待機しています..."
for i in {1..30}; do
    if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
        echo "GPUStackが起動しました"
        break
    fi
    sleep 1
    echo -n "."
    if [ $i -eq 30 ]; then
        echo "GPUStackの起動に失敗しました。"
        cleanup
    fi
done
echo ""

echo "モデルの状態を確認しています..."
if ! python -c "import requests; exit(0 if requests.get('http://localhost:8000/v1/models').json()['data'] else 1)" 2>/dev/null; then
    echo "デプロイされているモデルが見つかりません。モデルセットアップを実行します..."
    python scripts/model_setup.py
fi

echo "Streamlitアプリケーションを起動します..."
cd app && streamlit run app.py &
STREAMLIT_PID=$!
cd ..

echo "すべてのサービスが起動しました。Ctrl+C で停止できます。"

wait



set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_root="$(dirname "$script_dir")"
cd "$project_root"

cleanup() {
    echo -e "\nStreamlitアプリケーションを停止します..."
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill -TERM $STREAMLIT_PID 2>/dev/null || true
        wait $STREAMLIT_PID 2>/dev/null || true
    fi
    pkill -f "streamlit run" || true
    deactivate 2>/dev/null || true
    echo "Streamlitアプリケーションを停止しました。"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Streamlitアプリケーションを起動します..."

VENV_PATH="venv"

echo "仮想環境を有効化します..."
source "$VENV_PATH/bin/activate"

echo "Streamlitアプリケーションを起動します..."
echo "Ctrl+C で停止できます"
cd app && streamlit run app.py &
STREAMLIT_PID=$!

wait $STREAMLIT_PID

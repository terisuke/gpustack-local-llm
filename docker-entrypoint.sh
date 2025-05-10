#!/bin/bash
set -e

gpustack start --port 80 &
GPUSTACK_PID=$!

echo "Waiting for GPUStack to start..."
sleep 10

if [ "$DEPLOY_MODEL" = "true" ]; then
    echo "Deploying a small model..."
    python /app/scripts/deploy_small_model.py
fi

cd /app/app
streamlit run app.py

wait $GPUSTACK_PID

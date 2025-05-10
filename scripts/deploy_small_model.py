import sys
import os
import requests
import time

API_BASE = "http://localhost:80/v1"

def check_gpustack_running():
    """Check if GPUStack is running"""
    try:
        response = requests.get(f"{API_BASE}/models")
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        pass
    return False

def deploy_model(model_id):
    """Deploy a model"""
    headers = {"Content-Type": "application/json"}
    
    device = "mps" if sys.platform == "darwin" and "arm" in os.uname().machine else "cuda"
    if device not in ["mps", "cuda"]:
        device = "cpu"
    
    payload = {
        "model_id": model_id,
        "device": device,
        "type": "llm"
    }
    
    try:
        print(f"Deploying model '{model_id}'...")
        response = requests.post(f"{API_BASE}/models/deploy", headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Model '{model_id}' deployed successfully")
            return True
        else:
            print(f"Failed to deploy model: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error deploying model: {e}")
        return False

def main():
    for _ in range(30):
        if check_gpustack_running():
            break
        print("Waiting for GPUStack to start...")
        time.sleep(1)
    
    model_id = os.environ.get("MODEL_ID", "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF")
    
    success = deploy_model(model_id)
    if success:
        print("Model deployment completed successfully")
    else:
        print("Model deployment failed")

if __name__ == "__main__":
    main()

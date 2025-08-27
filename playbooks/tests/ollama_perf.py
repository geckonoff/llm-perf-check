import requests
import time

model = "llama2"
url = "http://localhost:11434/api/generate"

prompts = ["Explain quantum computing in 50 words."] * 10

def run_test():
    for i, prompt in enumerate(prompts):
        start = time.time()
        response = requests.post(url, json={"model": model, "prompt": prompt})
        latency = time.time() - start
        
        print(f"Prompt {i+1}: {latency:.2f}s - Tokens: {len(response.json()['response'].split())}")

if __name__ == "__main__":
    run_test()
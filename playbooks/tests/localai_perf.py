#!/usr/bin/env python3

import requests
import time
import json

def test_localai_performance():
    base_url = "http://localhost:8080/v1"
    model_name = "ggml-model"  # Замените на имя вашей модели
    
    # Тестовые промпты
    test_prompts = [
        "Explain quantum computing in simple terms.",
        "What is the capital of France?",
        "Write a short poem about technology.",
        "How does photosynthesis work?",
        "What are the benefits of renewable energy?"
    ]
    
    results = []
    
    for i, prompt in enumerate(test_prompts):
        try:
            start_time = time.time()
            
            # Отправка запроса к LocalAI
            response = requests.post(
                f"{base_url}/completions",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "max_tokens": 100,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result_data = response.json()
                tokens = len(result_data['choices'][0]['text'].split())
                
                result = {
                    "prompt": prompt,
                    "latency": round(latency, 2),
                    "tokens": tokens,
                    "tokens_per_second": round(tokens / latency, 2) if latency > 0 else 0,
                    "status": "success"
                }
            else:
                result = {
                    "prompt": prompt,
                    "latency": round(latency, 2),
                    "tokens": 0,
                    "tokens_per_second": 0,
                    "status": f"error: {response.status_code}",
                    "error_message": response.text
                }
            
            results.append(result)
            print(f"Test {i+1}/{len(test_prompts)}: {result['latency']}s, {result['tokens']} tokens")
            
        except Exception as e:
            error_result = {
                "prompt": prompt,
                "latency": 0,
                "tokens": 0,
                "tokens_per_second": 0,
                "status": f"exception: {str(e)}"
            }
            results.append(error_result)
            print(f"Test {i+1}/{len(test_prompts)} failed: {str(e)}")
    
    # Вывод суммарных результатов
    print("\n=== PERFORMANCE SUMMARY ===")
    successful_tests = [r for r in results if r['status'] == 'success']
    
    if successful_tests:
        avg_latency = sum(r['latency'] for r in successful_tests) / len(successful_tests)
        avg_tps = sum(r['tokens_per_second'] for r in successful_tests) / len(successful_tests)
        total_tokens = sum(r['tokens'] for r in successful_tests)
        
        print(f"Successful tests: {len(successful_tests)}/{len(results)}")
        print(f"Average latency: {avg_latency:.2f}s")
        print(f"Average tokens/second: {avg_tps:.2f}")
        print(f"Total tokens generated: {total_tokens}")
    else:
        print("No successful tests completed")
    
    return results

if __name__ == "__main__":
    test_localai_performance()
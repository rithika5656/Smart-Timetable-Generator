"""
Simple stress test generator.
"""
import time
import requests
import threading

API_URL = "http://localhost:5000/api/v1/generate"
API_KEY = "dev-api-key"

def run_request(i):
    try:
        start = time.time()
        resp = requests.post(API_URL, headers={"X-API-Key": API_KEY}, json={
            "subjects": [f"Sub{x}" for x in range(5)],
            "teachers": [f"Teacher{x}" for x in range(5)],
            "periods": 6
        })
        duration = time.time() - start
        print(f"Req {i}: Status {resp.status_code} in {duration:.4f}s")
    except Exception as e:
        print(f"Req {i}: Failed {e}")

if __name__ == "__main__":
    print("Starting stress test (10 concurrent requests)...")
    threads = []
    for i in range(10):
        t = threading.Thread(target=run_request, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    print("Stress test complete.")

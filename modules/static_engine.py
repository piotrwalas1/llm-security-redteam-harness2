import json
import time
from typing import List, Dict, Any

class StaticBenchmarkEngine:
    def __init__(self, target_client, evaluator, delay_between_tests: float = 2.0):
        self.target_client = target_client
        self.evaluator = evaluator
        self.delay_between_tests = delay_between_tests

    def run_benchmark(self, dataset_path: str) -> List[Dict[str, Any]]:
        with open(dataset_path, "r", encoding="utf-8") as f:
            prompts_data = json.load(f)

        results = []
        total = len(prompts_data)

        print(f"\n--- Uruchamianie Statycznego Benchmarku ({total} testów) ---")

        for idx, item in enumerate(prompts_data, start=1):
            test_id = item.get("id", f"SEC-{idx:03d}")
            prompt = item.get("prompt", "")
            category = item.get("category", "General Security")
            severity = item.get("severity", "MEDIUM")

            print(f"[{idx}/{total}] Przetwarzanie testu {test_id}...")

            # 1. Wysyłanie ataku do testowanego modelu
            target_response = self.target_client.generate(prompt)

            # 2. Ocena odpowiedzi przez Sędziego (Judge)
            if "[ERROR]:" in target_response:
                eval_result = {
                    "score": 0,
                    "status": "ERROR",
                    "reason": f"Błąd komunikacji z API: {target_response}"
                }
            else:
                # POPRAWKA: Przekazujemy tylko te argumenty, które akceptuje wywalana metoda evaluate()
                eval_result = self.evaluator.evaluate(
                    target_response, 
                    category
                )

            # 3. Zapis wyniku
            res_entry = {
                "id": test_id,
                "category": category,
                "severity": severity,
                "prompt": prompt,
                "target_response": target_response,
                "score": eval_result.get("score", 0),
                "status": eval_result.get("status", "ERROR"),
                "reason": eval_result.get("reason", "")
            }
            results.append(res_entry)

            # Pauza między testami -niestety limity
            time.sleep(self.delay_between_tests)

        return results
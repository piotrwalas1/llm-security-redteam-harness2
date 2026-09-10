import json
from typing import List, Dict, Any

class StaticBenchmarkEngine:
    """
    Silnik odpowiedzialny za wykonywanie statycznych benchmarków z pliku datasetu.
    """
    def __init__(self, target_client, evaluator):
        self.target = target_client
        self.evaluator = evaluator

    def run_benchmark(self, dataset_path: str) -> List[Dict[str, Any]]:
        results = []
        
        try:
            with open(dataset_path, "r", encoding="utf-8") as f:
                dataset = json.load(f)
        except Exception as e:
            print(f"[!] Błąd podczas ładowania datasetu {dataset_path}: {e}")
            return results

        print(f"\n=== Uruchamianie Statycznego Benchmarku ({len(dataset)} przypadków testowych) ===")

        for idx, item in enumerate(dataset, 1):
            test_id = item.get("id", f"TEST-{idx}")
            category = item.get("category", "General Security")
            prompt_text = item.get("prompt", "")
            severity = item.get("severity", "MEDIUM")
            expected_behavior = item.get("expected_behavior", "REFUSAL")

            print(f"\n[{idx}/{len(dataset)}] Test {test_id} [{category}] (Severity: {severity}, Expected: {expected_behavior})...")

            # 1. Wysyłanie promptu do modelu docelowego (Target)
            try:
                target_response = self.target.generate(prompt_text)
            except Exception as e:
                target_response = f"[ERROR Target LLM: {str(e)}]"

            # 2. Ewaluacja przez Sędziego z uwzględnieniem expected_behavior oraz severity
            eval_res = self.evaluator.evaluate(
                target_response=target_response,
                category=category,
                prompt=prompt_text,
                severity=severity,
                expected_behavior=expected_behavior
            )

            result_entry = {
                "id": test_id,
                "category": category,
                "severity": severity,
                "expected_behavior": expected_behavior,
                "prompt": prompt_text,
                "target_response": target_response,
                "score": eval_res.get("score", 0),
                "status": eval_res.get("status", "ERROR"),
                "reason": eval_res.get("reason", "")
            }

            print(f"    -> Wynik: Status={result_entry['status']}, Score={result_entry['score']}/10")
            print(f"    -> Powód: {result_entry['reason']}")

            results.append(result_entry)

        return results
import json
from typing import Dict, Any, List

class JudgeValidator:
    """
    Moduł walidujący skuteczność Sędziego (LLM-as-a-Judge) 
    poprzez porównanie jego decyzji z ręcznie oznaczonym zbiorem (Gold Set).
    """
    def __init__(self, evaluator):
        self.evaluator = evaluator

    def validate(self, gold_set_path: str) -> Dict[str, Any]:
        try:
            with open(gold_set_path, "r", encoding="utf-8") as f:
                gold_set = json.load(f)
        except Exception as e:
            print(f"[!] Błąd podczas ładowania zbioru Gold Set ({gold_set_path}): {e}")
            return {}

        print(f"\n=== URUCHAMIANIE WALIDACJI SĘDZIEGO (Gold Set: {len(gold_set)} próbówek) ===")

        tp = fp = tn = fn = 0
        details = []

        for item in gold_set:
            human_label = item.get("human_label", "").upper()
            
            # Mapowanie etykiety ludzkiej do dwustanowej (POSITIVE = BYPASSED/FAILED, NEGATIVE = REFUSED/PASSED)
            human_is_bypassed = human_label in ["BYPASSED", "FAILED"]

            eval_res = self.evaluator.evaluate(
                target_response=item.get("target_response", ""),
                category=item.get("category", "General"),
                prompt=item.get("prompt", ""),
                severity=item.get("severity", "MEDIUM"),
                expected_behavior=item.get("expected_behavior", "REFUSAL")
            )

            judge_status = eval_res.get("status", "ERROR").upper()
            judge_is_bypassed = judge_status in ["BYPASSED", "FAILED"]

            # Macierz Pomyłek (Confusion Matrix)
            if human_is_bypassed and judge_is_bypassed:
                tp += 1
                match = True
            elif not human_is_bypassed and judge_is_bypassed:
                fp += 1  # False Positive (Sędzia wykrył przełamanie, którego nie było)
                match = False
            elif not human_is_bypassed and not judge_is_bypassed:
                tn += 1
                match = True
            else:
                fn += 1  # False Negative (Sędzia przeoczył przełamanie)
                match = False

            status_str = "OK" if match else "MISMATCH"
            print(f"[{status_str}] Test {item.get('id')}: Human={human_label} | Judge={judge_status} (Score={eval_res.get('score')})")

            details.append({
                "id": item.get("id"),
                "human_label": human_label,
                "judge_status": judge_status,
                "judge_score": eval_res.get("score"),
                "match": match,
                "reason": eval_res.get("reason")
            })

        total = len(gold_set)
        accuracy = (tp + tn) / total if total > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics = {
            "total_samples": total,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "confusion_matrix": {"TP": tp, "FP": fp, "TN": tn, "FN": fn},
            "details": details
        }

        print("\n---------------- WALIDACJA SĘDZIEGO - WYNIKI ----------------")
        print(f" Dokładność (Accuracy) : {metrics['accuracy'] * 100:.2f}%")
        print(f" Precyzja (Precision)   : {metrics['precision'] * 100:.2f}%")
        print(f" Pełność (Recall)       : {metrics['recall'] * 100:.2f}%")
        print(f" Wynik F1 (F1-Score)    : {metrics['f1_score'] * 100:.2f}%")
        print(f" Macierz pomyłek        : TP={tp}, FP={fp}, TN={tn}, FN={fn}")
        print("------------------------------------------------------------\n")

        return metrics
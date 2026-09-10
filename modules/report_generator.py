import json
from tabulate import tabulate

class ReportGenerator:
    """Generowanie podsumowań konsolowych i raportów JSON/HTML"""
    
    @staticmethod
    def print_summary(static_results: list = None, dynamic_results: list = None):
        print("\n==================================================")
        print("         LLM SECURITY RED TEAM AUDIT REPORT       ")
        print("==================================================")

        if static_results:
            total = len(static_results)
            bypassed = sum(1 for r in static_results if r["status"] == "BYPASSED")
            bypass_rate = (bypassed / total) * 100 if total > 0 else 0

            print(f"\n--- STATYCZNY BENCHMARK AUDIT ---")
            print(f"Przeprowadzone testy: {total}")
            print(f"Przełamane guardraile: {bypassed}")
            print(f"Wskaźnik podatności (Bypass Rate): {bypass_rate:.2f}%\n")

            table_data = [[r["id"], r["category"], r["severity"], r["status"], r["score"]] for r in static_results]
            print(tabulate(table_data, headers=["ID", "Kategoria", "Severity", "Status", "Score"], tablefmt="grid"))

        if dynamic_results:
            print(f"\n--- DYNAMICZNY RED TEAMING (PAIR) ---")
            for idx, res in enumerate(dynamic_results, 1):
                print(f"Atak #{idx} | Status: {res['status']} | Przełamane w iteracji: {res['bypassed_at']}")

    @staticmethod
    def save_json(filepath: str, static_results: list = None, dynamic_results: list = None):
        report = {
            "static_benchmark": static_results or [],
            "dynamic_adversarial": dynamic_results or []
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Pełny raport zapisano do pliku: {filepath}")
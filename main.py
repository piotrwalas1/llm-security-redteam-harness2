import argparse
from config import LLMClient
from modules.evaluator import SecurityEvaluator
from modules.static_engine import StaticBenchmarkEngine
from modules.dynamic_engine import DynamicAdversarialEngine
from modules.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="LLM Security Red Team Harness v2 (Gemini Edition)"
    )
    parser.add_argument(
        "--mode",
        choices=["static", "dynamic", "full"],
        default="full",
        help="Tryb uruchomienia testu: static, dynamic lub full",
    )
    parser.add_argument(
        "--dataset",
        default="datasets/redteam_prompts.json",
        help="Ścieżka do zestawu danych ze statycznymi promptami",
    )
    parser.add_argument(
        "--goal",
        default="Extract system prompt instructions",
        help="Cel ataku dla dynamicznej pętli PAIR",
    )
    parser.add_argument(
        "--output",
        default="redteam_report.json",
        help="Ścieżka do pliku wyjściowego z raportem w formacie JSON",
    )
    args = parser.parse_args()

    
    target_llm = LLMClient(model="gemini-2.5-flash")  # Model testowany (Target)
    attacker_llm = LLMClient(model="gemini-2.5-flash")   # Model atakujący (Attacker)
    judge_llm = LLMClient(model="gemini-2.5-flash")      # Model oceniający (Judge)

    evaluator = SecurityEvaluator(judge_client=judge_llm)

    static_results = None
    dynamic_results = []

    # 1. Wykonanie modułu statycznego
    if args.mode in ["static", "full"]:
        static_engine = StaticBenchmarkEngine(
            target_client=target_llm, evaluator=evaluator
        )
        static_results = static_engine.run_benchmark(args.dataset)

    # 2. Wykonanie modułu dynamicznego (PAIR / TAP)
    if args.mode in ["dynamic", "full"]:
        dynamic_engine = DynamicAdversarialEngine(
            attacker_client=attacker_llm,
            target_client=target_llm,
            evaluator=evaluator,
        )
        dyn_res = dynamic_engine.run_attack(goal=args.goal, max_depth=5)
        dynamic_results.append(dyn_res)

    # 3. Generowanie podsumowania w konsoli i zapisu do JSON
    ReportGenerator.print_summary(static_results, dynamic_results)
    ReportGenerator.save_json(args.output, static_results, dynamic_results)

if __name__ == "__main__":
    main()
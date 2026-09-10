# LLM Security Red Team Harness

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Category](https://img.shields.io/badge/category-LLM%20Security-red)

**`llm-security-redteam-harness2`** to hybrydowy framework testowy służący do automatycznego wykrywania podatności w aplikacjach opartych o Large Language Models (LLM). Łączy deterministyczny benchmark statyczny z dynamiczną pętlą ataków iteracyjnych (**PAIR / TAP**).

Narzędzie pozwala na prowadzenie kompleksowych audytów bezpieczeństwa, sprawdzając odporność modeli m.in. na **Prompt Injection**, **Jailbreaking**, **System Prompt Extraction** oraz nieautoryzowane ujawnianie architektury operacyjnej systemów AI.

---

## 🚀 Kluczowe Funkcjonalności

* **Hybrydowe podejście do testów:** Integracja statycznego, deterministycznego benchmarku z zaawansowanym atakiem dynamicznym.
* **Dynamiczny Red Teaming (PAIR / TAP Architecture):** Pętla zwrotna, w której model *Attacker* analizuje odmowy i odpowiedzi modelu *Target*, iteracyjnie generując coraz bardziej wyrafinowane warianty ataków.
* **Smart Framing & Reconnaissance Detection:** Identyfikacja podatności typu *Soft Bypass* (wyłudzanie metazasad, kategoryzacji instrukcji oraz architektury bezpieczeństwa).
* **Post-Bypass Probe & Extraction:** Automatyczny krok wyzwalany po wykryciu przełamania, którego celem jest bezpośrednie wyciągnięcie surowego tekstu instrukcji (`Raw System Prompt`) za pomocą technik *Anchor & Expose*.
* **Automatyczna Ewaluacja (LLM Judge):** Moduł sędziego (`SecurityEvaluator`) w czasie rzeczywistym klasyfikujący odpowiedzi pod kątem statusów `BYPASSED` / `REFUSED` oraz oceniający stopień wycieku informacji.
* **Strukturyzowane Raportowanie JSON:** Generowanie czytelnych raportów z pełną historią konwersacji, punktacją i szczegółami ataków, gotowych do integracji z pipeline'ami CI/CD.

---

## 🛠️ Architektura Systemu

```text
               +----------------------------------+
               |  Deterministyczny Benchmark      |
               |         Statyczny                |
               +----------------------------------+
                                |
                                v
+-------------------------------------------------------------------+
|                     Dynamiczna Pętla Ataków                       |
|                                                                   |
|  [ Attacker LLM ] ---> Generuje/Modyfikuje Prompt ---> [ Target ] |
|         ^                                                 |       |
|         |                                                 v       |
|   [ Pętla PAIR/TAP ] <--- Ocenianie/Score <--- [ Security Judge ] |
|                                                           |       |
|                                              (Jeśli BYPASSED)     |
|                                                           v       |
|                                         [ Post-Bypass Extraction ]|
+-------------------------------------------------------------------+
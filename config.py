import os
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

class LLMClient:
    def __init__(self, model: str = "gemini-2.5-flash", rate_limit_delay: float = 0.2):
        self.model_name = model
        self.rate_limit_delay = rate_limit_delay
        
        # Twój musisz wpisac swoj Project ID z Google Cloud Console 
        project_id = os.getenv("GCP_PROJECT_ID", "tu wpisz swoj projectId")
        location = os.getenv("GCP_LOCATION", "us-central1")  

        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )

    def generate(self, prompt: str, max_retries: int = 5) -> str:
        config = types.GenerateContentConfig(
            temperature=0.7,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )

        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                
                time.sleep(self.rate_limit_delay)
                
                return response.text if response.text else ""

            except APIError as e:
                if e.code == 429 or "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = 10.0
                    print(f"\n[!] Rate limit Vertex AI. Próba {attempt}/{max_retries}. Czekam {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"\n[!] Błąd Vertex API: {e}")
                    time.sleep(2)

            except Exception as e:
                print(f"\n[!] Błąd komunikacji: {e}")
                time.sleep(2)

        return f"[ERROR]: Przekroczono limity po {max_retries} próbach."
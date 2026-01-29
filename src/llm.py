import json
import os
import time
from openai import OpenAI
from typing import Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

class LLMClient: 

    print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))
    
    def __init__(self, model:Optional[str] = None, max_retries: int = 3,timeout_s: int = 60):
        self.client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_retries = max_retries
        self.timeout_s = timeout_s

    def json_call(self, prompt: str, payload: Dict[str, Any], *, schema_name: str, schema: Dict[str,Any],max_output_tokens: int =800) -> Dict[str,Any]:
        messages = [
            {"role": "system", "content" : prompt},
            {"role": "user", "content" : json.dumps(payload, ensure_ascii = False)},
        ]

        last_err: Optional[Exception] = None

        for attempt in range(1,self.max_retries + 1):
            try:
                resp =self.client.responses.create(
                    model = self.model,
                    input = messages,
                    text = {
                        "format": {
                            "type": "json_schema",
                            "name": schema_name,
                            "strict": True,
                            "schema": schema
                        }
                    },
                    max_output_tokens = max_output_tokens,
                )

                raw = resp.output[0].content[0].text

                if not raw:
                    raise RuntimeError("Empty output_text from model.")
                
                return json.loads(raw)
            
            except Exception as e:
                last_err = e
                time.sleep(min(2**(attempt -1), 8))

        raise RuntimeError(f"LLM json_call failed after {self.max_retries} retries: {last_err}")




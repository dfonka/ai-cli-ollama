from __future__ import annotations
import json
from typing import Dict, Iterable, Optional
import requests

class OllamaError(RuntimeError): pass

class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434", timeout: int = 60):
        self.base = host.rstrip("/")
        self.timeout = timeout

    def list_models(self) -> Dict:
        url = f"{self.base}/api/tags"
        try:
            resp = requests.get(url, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            raise OllamaError(f"Cannot connect to Ollama at {self.base}. Is it running?")
        if resp.status_code != 200:
            raise OllamaError(f"Ollama returned {resp.status_code}: {resp.text}")
        return resp.json()

    def generate(self, model: str, prompt: str, stream: bool=False, system: Optional[str]=None, options: Optional[dict]=None):
        url = f"{self.base}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": stream}
        if system: payload["system"] = system
        if options: payload["options"] = options
        resp = requests.post(url, json=payload, stream=stream, timeout=self.timeout)
        if resp.status_code != 200:
            raise OllamaError(f"Ollama returned {resp.status_code}: {resp.text}")
        if stream:
            def _iter():
                for line in resp.iter_lines(decode_unicode=True):
                    if not line: continue
                    j = json.loads(line)
                    if "response" in j: yield j["response"]
                    if j.get("done"): break
            return _iter()
        else:
            return resp.json().get("response","")

"""Internal LLM provider adapters for AIResumeAnalyzer.

Isolates backend-specific call details (Gemini SDK, OpenAI-compatible HTTP)
behind a single ``complete(prompt, system=None) -> str`` interface so the
main analyzer module does not need to know which provider it is talking to.

No streamlit dependency is required here.
"""

import requests


class LLMAPICallError(Exception):
    """Raised when an OpenAI-compatible provider returns an HTTP-level error."""


class GeminiAdapter:
    """Gemini backend via the google.generativeai SDK."""

    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        import google.generativeai as genai

        self._genai = genai
        self._model_name = model_name
        if api_key:
            genai.configure(api_key=api_key)

    def complete(self, prompt, system=None):
        model = self._genai.GenerativeModel(self._model_name)
        response = model.generate_content(prompt)
        return response.text


class OpenAICompatibleAdapter:
    """OpenAI-compatible chat/completions backend via HTTP."""

    def __init__(self, base_url, api_key, model_name):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model_name = model_name

    def complete(self, prompt, system=None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self._model_name,
            "messages": messages,
            "temperature": 0.7,
        }
        response = requests.post(
            f"{self._base_url}/chat/completions",
            headers=headers,
            json=data,
        )
        if response.status_code != 200:
            raise LLMAPICallError(
                f"API Error: {response.status_code} - {response.text}"
            )
        result = response.json()
        return result["choices"][0]["message"]["content"]


def create_adapter(provider, *, api_key=None, base_url=None, model_name=None):
    """Build the adapter for the named provider."""
    if provider == "gemini":
        return GeminiAdapter(api_key)
    return OpenAICompatibleAdapter(base_url, api_key, model_name)

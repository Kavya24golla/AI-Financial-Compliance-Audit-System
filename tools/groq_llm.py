from __future__ import annotations

import os
from groq import Groq


class GroqLLM:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from environment variables.")
        self.client = Groq(api_key=api_key)

    def chat(self, system_prompt: str, user_prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
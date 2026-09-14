import asyncio
from typing import Type, TypeVar
from pydantic import BaseModel
from openai import AsyncOpenAI
from core.config import settings

T = TypeVar("T", bound=BaseModel)

class OpenAIClientWrapper:
    def __init__(self):
        # OpenAI API key settings se read karega
        api_key = getattr(settings, "OPENAI_API_KEY", "dummy-key")
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_structured_output(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: str = "You are an expert AI SEO Analyst.",
        max_retries: int = 3
    ) -> T:
        for attempt in range(1, max_retries + 1):
            try:
                response = await self.client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    response_format=response_model,
                )
                return response.choices[0].message.parsed
            except Exception as e:
                if attempt == max_retries:
                    raise e
                await asyncio.sleep(2 ** attempt)

openai_client = OpenAIClientWrapper()
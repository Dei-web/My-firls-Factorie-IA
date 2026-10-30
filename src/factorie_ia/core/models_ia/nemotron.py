import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def build_nemotron() -> ChatOpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Falta OPENROUTER_API_KEY en .env")

    return ChatOpenAI(
        model=os.getenv(
            "OPENROUTER_MODEL",
            "nvidia/nemotron-3.5-super-vl:free",
        ),
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
        timeout=60,
    )

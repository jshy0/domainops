import json
import os

from openai import OpenAI

SYSTEM_PROMPT = """
You are a startup naming expert and brand strategist.

Generate brandable startup names for the user's idea.

## Name criteria:
- Short, memorable, and brandable
- Prefer invented or semi-invented words (not plain dictionary words)
- Avoid known company names or trademarks
- No underscores, hyphens, or special characters
- Maximum 12 characters
- 1 word preferred, 2 words max
- Modern SaaS / AI startup tone (think: Notion, Stripe, Linear, Vanta, Replit)
- Prefer soft consonants and vowel-rich names
- Names should feel like brands, not descriptions

## Output rules:
- Respond with a single complete valid JSON object and nothing else
- The object MUST open with { and close with }
- No markdown, no code fences, no explanation, no text outside the JSON

## Exact format required:
{"names":["Name1","Name2","Name3","Name4","Name5","Name6","Name7","Name8","Name9","Name10"]}

Generate exactly 10-15 names. Always close the JSON object with }.
"""

_PROVIDER_DEFAULTS = {
    "ollama": "llama3.2",
    "openai": "gpt-4o-mini",
}


def _make_client(provider: str) -> OpenAI:
    if provider == "ollama":
        return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_names_llm(idea: str, provider: str = "ollama", model: str | None = None) -> list[str]:
    client = _make_client(provider)
    resolved_model = model or _PROVIDER_DEFAULTS.get(provider, "llama3.2")

    response = client.chat.completions.create(
        model=resolved_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Generate startup names for this idea: {idea}"},
        ],
        temperature=0.9,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content or ""

    try:
        data = json.loads(raw)
        return [n.strip() for n in data.get("names", []) if isinstance(n, str) and n.strip()]
    except json.JSONDecodeError:
        return []

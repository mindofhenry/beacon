"""
llm.py — LLM Provider Abstraction

Beacon supports Anthropic Claude, OpenAI GPT, and Google Gemini.
Set LLM_PROVIDER in your .env to switch providers.
All interfaces (Slack bot, MCP server) call query_llm() — nothing else changes.
"""

import os

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "anthropic").lower()


def query_llm(prompt: str) -> str:
    """
    Routes to the configured LLM provider.
    Returns the answer as a string.
    """
    if LLM_PROVIDER == "openai":
        return _query_openai(prompt)
    elif LLM_PROVIDER == "google":
        return _query_google(prompt)
    else:
        return _query_anthropic(prompt)


def _query_anthropic(prompt: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except ImportError:
        return "Beacon error: anthropic package not installed. Run pip install anthropic."
    except Exception as e:
        return f"Beacon error (Anthropic): {str(e)}"


def _query_openai(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI()
        model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        response = client.chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except ImportError:
        return "Beacon error: openai package not installed. Run pip install openai."
    except Exception as e:
        return f"Beacon error (OpenAI): {str(e)}"


def _query_google(prompt: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model_name = os.environ.get("GOOGLE_MODEL", "gemini-1.5-pro")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "Beacon error: google-generativeai package not installed. Run pip install google-generativeai."
    except Exception as e:
        return f"Beacon error (Google): {str(e)}"
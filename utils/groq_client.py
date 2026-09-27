from groq import Groq

def get_groq_client(api_key: str):
    if not api_key:
        raise ValueError("Groq API key is missing.")
    return Groq(api_key=api_key)

import json
from utils.groq_client import get_groq_client
from utils.prompts import INTAKE_PROMPT

def extract_lead(inquiry: str, model: str, api_key: str):
    client = get_groq_client(api_key)

    prompt = INTAKE_PROMPT.format(inquiry=inquiry)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract structured lead information. Return valid JSON only."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    # Handle occasional markdown code fences.
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start:end + 1])
        raise ValueError("The AI returned invalid JSON.")

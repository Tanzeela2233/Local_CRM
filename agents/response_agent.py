from utils.groq_client import get_groq_client
from utils.prompts import RESPONSE_PROMPT

def generate_response(
    inquiry: str,
    lead: dict,
    knowledge: list,
    model: str,
    api_key: str
):
    client = get_groq_client(api_key)

    context = "\n\n".join(
        item.get("text", "") if isinstance(item, dict) else str(item)
        for item in knowledge
    )

    prompt = RESPONSE_PROMPT.format(
        inquiry=inquiry,
        lead=lead,
        knowledge=context or "No approved company knowledge was found."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional business sales and customer-support "
                    "assistant. Ground your answer in the supplied company knowledge."
                )
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

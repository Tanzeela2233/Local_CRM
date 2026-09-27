# LocalAgent CRM

A lightweight Agentic AI Sales & Support CRM built with Streamlit and Groq.

## AI Pipeline

Customer Inquiry
→ Intake Agent
→ RAG Knowledge Agent
→ Qualification Agent
→ Response Agent
→ Human Review
→ CRM

## Features

- Lead information extraction
- Transparent lead qualification score
- PDF/TXT company knowledge upload
- Lightweight RAG using TF-IDF + cosine similarity
- Grounded AI response generation
- Human review/edit before saving
- Simple in-session CRM pipeline
- Groq API integration
- Streamlit Cloud friendly

## Groq Model

Default model:

`openai/gpt-oss-120b`

You can change the model from the sidebar or Streamlit Secrets.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud deployment

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Select your GitHub repository.
4. Set the main file to:

```text
app.py
```

5. Add these secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Do not commit your real API key to GitHub.

## Project structure

```text
Local_CRM/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
├── agents/
│   ├── __init__.py
│   ├── intake_agent.py
│   ├── knowledge_agent.py
│   ├── qualification_agent.py
│   └── response_agent.py
├── rag/
│   ├── __init__.py
│   ├── document_loader.py
│   └── vector_store.py
└── utils/
    ├── __init__.py
    ├── groq_client.py
    └── prompts.py
```

## Important

The CRM data and uploaded knowledge index are stored in Streamlit session memory in this MVP. They are not a permanent database.

The RAG is intentionally lightweight so the application can be deployed easily on Streamlit Cloud without Qdrant, PostgreSQL, Docker, Ollama, or a separate backend.

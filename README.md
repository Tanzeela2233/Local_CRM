# LocalAgent CRM

A simple Agentic AI CRM MVP built with Streamlit and the Groq API.

## Features

- Intake Agent
- Knowledge/RAG Agent
- Lead Qualification Agent
- Response Agent
- Simple CRM pipeline
- PDF/TXT knowledge upload
- Groq LLM
- Streamlit Cloud deployment

## Project flow

Customer Inquiry
→ Intake
→ Knowledge/RAG
→ Lead Qualification
→ Response
→ CRM Pipeline

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your Groq API key in the Streamlit sidebar.

## Deploy on Streamlit Cloud

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Select your GitHub repository.
4. Set the main file to `app.py`.
5. Deploy.
6. Open the app's Settings → Secrets.
7. Add:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Do not put your real API key in GitHub.

## Notes

This is intentionally a small MVP. The CRM data is kept in Streamlit session state for the demo, so it resets when the app session restarts. A persistent database can be added later.

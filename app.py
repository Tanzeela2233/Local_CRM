import streamlit as st
from agents.intake_agent import extract_lead
from agents.knowledge_agent import search_knowledge
from agents.qualification_agent import qualify_lead
from agents.response_agent import generate_response
from rag.document_loader import extract_text
from rag.vector_store import build_index, search_index
from utils.groq_client import get_groq_client
from utils.prompts import COMPANY_SYSTEM_PROMPT

st.set_page_config(page_title="LocalAgent CRM", page_icon="🤖", layout="wide")

if "leads" not in st.session_state:
    st.session_state.leads = []
if "documents" not in st.session_state:
    st.session_state.documents = {}
if "index" not in st.session_state:
    st.session_state.index = None

st.title("🤖 LocalAgent CRM")
st.caption("Simple Agentic AI Sales & Business Automation MVP")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API Key", type="password", value=st.secrets.get("GROQ_API_KEY", ""))
    model = st.text_input("Groq Model", value=st.secrets.get("GROQ_MODEL", "openai/gpt-oss-120b"))
    st.divider()
    st.subheader("Knowledge Base")
    uploads = st.file_uploader("Upload company documents", type=["pdf", "txt"], accept_multiple_files=True)

    if uploads:
        for uploaded in uploads:
            text = extract_text(uploaded)
            if text.strip():
                st.session_state.documents[uploaded.name] = text
        if st.session_state.documents:
            st.session_state.index = build_index(st.session_state.documents)
            st.success(f"{len(st.session_state.documents)} document(s) indexed.")

if not api_key:
    st.warning("Add your Groq API key in the sidebar or Streamlit Secrets.")
    st.info("For Streamlit Cloud: Settings → Secrets → add GROQ_API_KEY = \"your_key\"")

tab1, tab2, tab3 = st.tabs(["💬 New Inquiry", "📊 CRM Pipeline", "📚 Knowledge Base"])

with tab1:
    st.subheader("Process a customer inquiry")
    inquiry = st.text_area(
        "Customer message",
        height=160,
        placeholder="Example: Hi, we need a website for our agency. Our budget is 300k and we want to launch in one month."
    )

    if st.button("Run AI Workflow", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please provide a Groq API key.")
        elif not inquiry.strip():
            st.error("Please enter a customer inquiry.")
        else:
            try:
                client = get_groq_client(api_key)

                with st.spinner("Intake Agent extracting lead information..."):
                    lead = extract_lead(client, model, inquiry)

                knowledge = []
                if st.session_state.index:
                    with st.spinner("Knowledge Agent searching company information..."):
                        knowledge = search_knowledge(
                            st.session_state.index,
                            inquiry,
                            top_k=3
                        )

                with st.spinner("Qualification Agent scoring the lead..."):
                    score = qualify_lead(lead)

                with st.spinner("Response Agent drafting reply..."):
                    reply = generate_response(
                        client=client,
                        model=model,
                        inquiry=inquiry,
                        lead=lead,
                        knowledge=knowledge
                    )

                record = {
                    "message": inquiry,
                    "lead": lead,
                    "score": score,
                    "reply": reply
                }
                st.session_state.leads.append(record)

                st.success("Workflow completed.")

                c1, c2, c3 = st.columns(3)
                c1.metric("Lead Score", score["score"])
                c2.metric("Stage", score["stage"])
                c3.metric("Intent", lead.get("intent", "unknown"))

                st.subheader("1. Extracted Lead")
                st.json(lead)

                st.subheader("2. Qualification")
                st.json(score)

                st.subheader("3. Retrieved Knowledge")
                if knowledge:
                    for item in knowledge:
                        with st.expander(item["source"]):
                            st.write(item["text"])
                else:
                    st.info("No company knowledge document was uploaded for this inquiry.")

                st.subheader("4. Draft Response")
                edited_reply = st.text_area("Edit before sending", value=reply, height=180)

                if st.button("Save Lead to CRM"):
                    st.session_state.leads[-1]["reply"] = edited_reply
                    st.success("Lead saved to the CRM pipeline.")

            except Exception as e:
                st.error(f"Workflow error: {e}")

with tab2:
    st.subheader("Lead Pipeline")
    if not st.session_state.leads:
        st.info("No leads yet. Process an inquiry first.")
    else:
        for i, record in enumerate(reversed(st.session_state.leads), 1):
            lead = record["lead"]
            score = record["score"]
            with st.expander(
                f"{lead.get('name') or 'Unknown'} • "
                f"{lead.get('company') or 'Unknown company'} • "
                f"Score: {score['score']} • {score['stage']}"
            ):
                st.write("**Service:**", lead.get("service"))
                st.write("**Budget:**", lead.get("budget"))
                st.write("**Deadline:**", lead.get("deadline"))
                st.write("**Email:**", lead.get("email"))
                st.write("**Reply:**")
                st.write(record["reply"])

with tab3:
    st.subheader("Uploaded Knowledge")
    if st.session_state.documents:
        for name, text in st.session_state.documents.items():
            st.write(f"📄 **{name}** — {len(text)} characters")
    else:
        st.info("Upload company FAQs, services, pricing, policies, or other approved documents.")

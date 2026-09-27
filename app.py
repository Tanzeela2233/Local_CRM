import os
import streamlit as st

from agents.intake_agent import extract_lead
from agents.knowledge_agent import search_knowledge
from agents.qualification_agent import qualify_lead
from agents.response_agent import generate_response
from rag.document_loader import extract_text
from rag.vector_store import SimpleVectorStore

st.set_page_config(page_title="LocalAgent CRM", page_icon="🤖", layout="wide")

DEFAULT_MODEL = "openai/gpt-oss-120b"

def get_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)

@st.cache_resource
def get_vector_store():
    return SimpleVectorStore()

if "crm" not in st.session_state:
    st.session_state.crm = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vector_store()

if "knowledge_files" not in st.session_state:
    st.session_state.knowledge_files = []

st.title("🤖 LocalAgent CRM")
st.caption("Lightweight Agentic AI Sales & Support CRM")

with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "Groq API Key",
        value=get_secret("GROQ_API_KEY", ""),
        type="password",
        help="Use Streamlit Secrets for deployment."
    )

    model = st.text_input(
        "Groq Model",
        value=get_secret("GROQ_MODEL", DEFAULT_MODEL)
    )

    st.divider()
    st.info(
        "Pipeline: Inquiry → Intake → RAG → Qualification → "
        "AI Reply → CRM"
    )

tab1, tab2, tab3 = st.tabs(["💬 New Inquiry", "📊 CRM Pipeline", "📚 Knowledge Base"])

with tab3:
    st.subheader("Company Knowledge Base")
    st.write("Upload approved FAQs, policies, services, pricing or other business documents.")

    uploaded = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded:
        for file in uploaded:
            if file.name not in st.session_state.knowledge_files:
                try:
                    text = extract_text(file)
                    if text.strip():
                        st.session_state.vector_store.add_document(file.name, text)
                        st.session_state.knowledge_files.append(file.name)
                except Exception as e:
                    st.error(f"Could not process {file.name}: {e}")

    if st.session_state.knowledge_files:
        st.success(f"{len(st.session_state.knowledge_files)} document(s) indexed.")
        for name in st.session_state.knowledge_files:
            st.write(f"• {name}")
    else:
        st.info("No documents indexed yet.")

with tab1:
    st.subheader("Customer Inquiry")

    inquiry = st.text_area(
        "Paste a customer inquiry",
        height=180,
        placeholder=(
            "Example: Hi, I run ABC Company. We need a website and CRM system "
            "for our business. Our budget is $5,000 and we want to start next month. "
            "Please send details."
        )
    )

    if st.button("🚀 Process Inquiry", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please add your Groq API key in the sidebar or Streamlit Secrets.")
            st.stop()

        if not inquiry.strip():
            st.warning("Please enter a customer inquiry.")
            st.stop()

        try:
            with st.status("Running AI agents...", expanded=True) as status:
                st.write("🔎 Intake Agent: extracting lead information...")
                lead = extract_lead(inquiry, model, api_key)

                st.write("📚 Knowledge Agent: retrieving relevant company information...")
                knowledge = search_knowledge(
                    st.session_state.vector_store,
                    inquiry,
                    top_k=4
                )

                st.write("📊 Qualification Agent: scoring the lead...")
                qualification = qualify_lead(lead)

                st.write("✍️ Response Agent: drafting a grounded reply...")
                draft = generate_response(
                    inquiry,
                    lead,
                    knowledge,
                    model,
                    api_key
                )

                status.update(label="Pipeline completed!", state="complete")

            st.session_state.current_result = {
                "inquiry": inquiry,
                "lead": lead,
                "knowledge": knowledge,
                "qualification": qualification,
                "draft": draft,
            }

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Check your Groq API key, model name, and uploaded knowledge files.")

    result = st.session_state.get("current_result")

    if result:
        st.divider()

        st.subheader("1. Extracted Lead")
        st.json(result["lead"])

        st.subheader("2. Qualification")
        q = result["qualification"]
        c1, c2 = st.columns(2)
        c1.metric("Lead Score", q["score"])
        c2.metric("Status", q["status"].replace("_", " ").title())

        if q["reasons"]:
            for reason in q["reasons"]:
                st.write(f"✓ {reason}")

        st.subheader("3. Retrieved Knowledge")
        if result["knowledge"]:
            for item in result["knowledge"]:
                with st.expander(item.get("source", "Knowledge source")):
                    st.write(item.get("text", ""))
                    st.caption(f"Similarity: {item.get('score', 0):.3f}")
        else:
            st.info("No company knowledge matched this inquiry.")

        st.subheader("4. AI Draft Reply")
        edited_reply = st.text_area(
            "Review and edit before sending",
            value=result["draft"],
            height=250
        )

        if st.button("💾 Save to CRM", use_container_width=True):
            record = {
                "lead": result["lead"],
                "qualification": result["qualification"],
                "inquiry": result["inquiry"],
                "reply": edited_reply,
            }
            st.session_state.crm.append(record)
            st.success("Lead saved to CRM.")

with tab2:
    st.subheader("CRM Pipeline")

    if not st.session_state.crm:
        st.info("No leads saved yet.")
    else:
        st.write(f"**{len(st.session_state.crm)} lead(s)**")

        for i, record in enumerate(st.session_state.crm, start=1):
            lead = record["lead"]
            qualification = record["qualification"]

            title = lead.get("company") or lead.get("name") or f"Lead {i}"

            with st.expander(
                f"{i}. {title} — {qualification['status']} ({qualification['score']}/100)"
            ):
                st.write(f"**Name:** {lead.get('name') or 'Not provided'}")
                st.write(f"**Company:** {lead.get('company') or 'Not provided'}")
                st.write(f"**Email:** {lead.get('email') or 'Not provided'}")
                st.write(f"**Service:** {lead.get('service') or 'Not provided'}")
                st.write(f"**Budget:** {lead.get('budget') or 'Not provided'}")
                st.write(f"**Deadline:** {lead.get('deadline') or 'Not provided'}")
                st.markdown("**Inquiry**")
                st.write(record["inquiry"])
                st.markdown("**Reply**")
                st.write(record["reply"])

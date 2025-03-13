import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import os

# 🏡 App Setup
st.set_page_config(page_title="📜 PDF Insight Bot", page_icon="🤖", layout="wide")

# 🌟 Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎯 Title & Description
st.title("📜 PDF Insight Bot")
st.write("Upload a PDF, ask a query, and get AI-powered answers with chat history!")

# 🔑 API Key Input
api_key = st.text_input("🔑 Enter Google API Key:", type="password", help="Required for AI processing.")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# 📂 File Upload Sidebar
st.sidebar.header("📁 Upload PDF")
uploaded_pdf = st.sidebar.file_uploader("Select a PDF", type=["pdf"])

# 📝 Query Input Sidebar
st.sidebar.header("📝 Ask a Question")
query_text = st.sidebar.text_area("What do you want to know?", placeholder="E.g., What are the key points?")

# 🗂 Extract Text from PDF
@st.cache_data(ttl=0)
def extract_pdf_content(pdf):
    """Extracts text from the uploaded PDF."""
    full_text = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

# 📏 Split Text into Chunks
@st.cache_data(ttl=0)
def split_text_into_chunks(text):
    """Splits text into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    return splitter.split_text(text)

# 🔍 Create or Load FAISS Vector Store
@st.cache_resource
def build_vector_database(chunks):
    """Creates FAISS vector database from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(chunks, embedding=embeddings)

# 🧠 Setup QA Pipeline
def setup_qa_pipeline():
    """Initializes the AI Q&A model with history support."""
    template = """
    Use the context and chat history to provide a helpful response.
    If no relevant information is found, say: 'I couldn't find that in the document.'

    Context:
    {context}

    Chat History:
    {chat_history}

    User Query:
    {question}

    Response:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=template, input_variables=["context", "chat_history", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# 🔄 Process PDF & Answer Queries
if uploaded_pdf and api_key:
    with st.spinner("Processing PDF..."):
        try:
            # Extract text
            full_text = extract_pdf_content(uploaded_pdf)
            # Split text into chunks
            text_chunks = split_text_into_chunks(full_text)
            # Build vector database
            vector_db = build_vector_database(text_chunks)
            # Setup QA pipeline
            qa_pipeline = setup_qa_pipeline()

            # ✅ Answer Query
            if query_text:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                matching_docs = vector_db.similarity_search(query_text)

                # 🗨️ Include Chat History
                chat_history = "\n".join([f"User: {q}\nBot: {a}" for q, a in st.session_state.chat_history[-5:]])  
                output = qa_pipeline({
                    "input_documents": matching_docs, 
                    "chat_history": chat_history,
                    "question": query_text
                }, return_only_outputs=True)

                response = output["output_text"]
                
                # 📜 Save Chat History
                st.session_state.chat_history.append((query_text, response))

                # 🎯 Display AI Response
                st.subheader("🤖 AI Response:")
                st.write(response)

                # 📜 Show Chat History
                st.subheader("🗨️ Chat History")
                if st.session_state.chat_history:
                    for user_q, bot_a in st.session_state.chat_history[-5:]:
                        st.write(f"**User:** {user_q}")
                        st.write(f"**Bot:** {bot_a}")
                        st.markdown("---")
                else:
                    st.write("No chat history yet.")

        except Exception as error:
            st.error(f"⚠️ Error: {error}")
else:
    if not api_key:
        st.warning("🔑 Please enter a valid Google API Key.")
    if not uploaded_pdf:
        st.warning("📁 Upload a PDF file.")
    if not query_text:
        st.warning("📝 Enter a query to get an answer.")

# 🔄 Reset Chat History Button
if st.sidebar.button("🔄 Reset Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# 🔹 Footer
st.markdown("---\n🤖 Powered by LangChain & Google AI")
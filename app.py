import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.chains import RetrievalQA
import tempfile
import os

# Custom theme configuration
st.set_page_config(
    page_title="RAG-App-Multi-Model Assitant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply green theme
st.markdown("""
    <style>
        :root {
            --primary-color: #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton>button:hover {
            background-color: #388E3C;
            color: white;
        }
        .stSelectbox>div>div {
            background-color: #E8F5E9;
        }
        .sidebar .sidebar-content {
            background-color: #E8F5E9;
        }
        .st-bb {
            border-bottom-color: #4CAF50;
        }
        .st-at {
            background-color: #E8F5E9;
        }
        .st-emotion-cache-16txtl3 {
            background: #E8F5E9;
        }
        .st-emotion-cache-6qob1r {
            background: #E8F5E9;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chain" not in st.session_state:
    st.session_state.chain = None

def process_pdf(file, model_name):
    """Optimized PDF processing"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()

        # Optimized text splitting
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "],
            length_function=len
        )
        splits = text_splitter.split_documents(documents)

        embeddings = OllamaEmbeddings(
            model=model_name,
            base_url="http://localhost:11434"
        )

        vector_store = FAISS.from_documents(splits, embeddings)
        return vector_store
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")
    finally:
        if 'tmp_file_path' in locals():
            os.unlink(tmp_file_path)

def create_chain(vector_store, model_name):
    """Create optimized QA chain"""
    llm = OllamaLLM(
        model=model_name,
        base_url="http://localhost:11434",
        temperature=0.7,
        num_ctx=2048
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_kwargs={"k": 2}
        ),
        return_source_documents=True,
        verbose=False
    )

    return chain

# Sidebar with green theme
with st.sidebar:
    st.markdown("""
        <h1 style='color: #388E3C;'>📚 Configuration</h1>
        <p style='color: #666666;'>Welcome to the Local PDF Chat Assistant! This tool helps you interact with your PDF documents using advanced AI models. Configure your experience below:</p>
    """, unsafe_allow_html=True)
    
    # Model selection with selectbox
    st.markdown("<p style='color: #388E3C; font-weight: bold;'>Select AI Model</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.9em;'>Choose the AI model that best suits your needs:</p>", unsafe_allow_html=True)
    
    model_descriptions = {
        "llama2": "Best for general-purpose tasks and balanced performance",
        "mistral": "Excellent for technical and analytical content",
        "gemma": "Optimized for fast and efficient responses"
    }
    
    model_name = st.selectbox(
        "Select AI Model",
        options=list(model_descriptions.keys()),
        help="Select the Ollama model to use",
        key="model_selection",
        label_visibility="collapsed"
    )
    
    st.markdown(f"<p style='color: #666666; font-size: 0.8em; font-style: italic;'>{model_descriptions[model_name]}</p>", unsafe_allow_html=True)
    
    # File upload with custom styling
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color: #388E3C; font-weight: bold;'>Upload Your PDF</p>
        <p style='color: #666666; font-size: 0.9em;'>Upload a PDF document to start analyzing and chatting about its contents.</p>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=['pdf'],
        help="Upload a PDF file to chat with",
        label_visibility="collapsed"
    )
    
    # Process PDF button
    if uploaded_file:
        if st.button("🔄 Process PDF", type="primary", use_container_width=True):
            with st.spinner("Processing PDF..."):
                try:
                    st.session_state.vector_store = process_pdf(uploaded_file, model_name)
                    st.session_state.chain = create_chain(
                        st.session_state.vector_store,
                        model_name
                    )
                    st.success("✅ PDF processed successfully!")
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")

# Main chat interface
st.markdown("""
    <h1 style='color: #388E3C; text-align: center;'>💬 Local PDF Chat Assistant</h1>
""", unsafe_allow_html=True)

# Display PDF processing status
if st.session_state.vector_store is None:
    st.info("👆 Please upload and process a PDF file to start chatting")

# Chat input
if prompt := st.text_input("Ask your question about the PDF...", key="user_input"):
    if st.session_state.chain is not None:
        try:
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.chain({"query": prompt})
                
                has_sources = any(
                    doc.page_content.strip() != "" 
                    for doc in response["source_documents"]
                )
                
                if has_sources:
                    st.write(response["result"])
                    sources = "\n\n".join(
                        [f"Source {i+1}:\n{doc.page_content}" 
                         for i, doc in enumerate(response["source_documents"])]
                    )
                    with st.expander("📚 View Sources"):
                        st.write(sources)
                else:
                    llm = OllamaLLM(
                        model=model_name,
                        base_url="http://localhost:11434"
                    )
                    direct_response = llm.invoke(prompt)
                    st.write(direct_response)
                    st.info("ℹ This response is based on the model's general knowledge as no relevant information was found in the PDF.")
                    
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
    else:
        st.warning("⚠ Please upload and process a PDF first.")
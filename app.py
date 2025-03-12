import os
import warnings
import tempfile
from dotenv import load_dotenv
import streamlit as st

from docling.document_converter import DocumentConverter
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


# Function to convert document to markdown
def load_and_convert_document(file_path):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()

# Function to split markdown into chunks based on headers
def get_markdown_splits(markdown_content):
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    return markdown_splitter.split_text(markdown_content)

# Setup the vector store with embeddings
def setup_vector_store(chunks):
    embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url="http://localhost:11434")
    single_vector = embeddings.embed_query("this is some text data")
    index = faiss.IndexFlatL2(len(single_vector))
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )
    vector_store.add_documents(documents=chunks)
    return vector_store

# Format documents for the RAG chain
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Create the RAG chain with the retriever and prompt template
def create_rag_chain(retriever):
    prompt = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know.
        Answer in bullet points. Make sure your answer is relevant to the question and it is answered from the context only.
        Question: {question} 
        Context: {context} 
        Answer:
    """
    model = ChatOllama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")
    prompt_template = ChatPromptTemplate.from_template(prompt)
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | model
        | StrOutputParser()
    )

# Main Streamlit application
def main():
    st.title("RAG Chain Q&A App")
    
    st.sidebar.header("Document Upload")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF Document", type=["pdf"])
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        st.write("### Converting document...")
        markdown_content = load_and_convert_document(tmp_file_path)
        st.success("Document successfully converted to Markdown.")
        
        st.write("### Splitting document into chunks...")
        chunks = get_markdown_splits(markdown_content)
        st.write(f"Document split into **{len(chunks)}** chunks.")
        
        st.write("### Setting up vector store...")
        vector_store = setup_vector_store(chunks)
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={'k': 3})
        st.success("Vector store created and retriever is ready.")
        
        # Create the RAG chain
        rag_chain = create_rag_chain(retriever)
        
        st.header("Ask a Question")
        question = st.text_input("Enter your question here:")
        
        if st.button("Get Answer") and question:
            st.write("#### Generating answer...")
            answer_text = ""
            placeholder = st.empty()
            
            # Retrieve relevant chunks
            relevant_docs = retriever.get_relevant_documents(question)
            
            # Display the relevant chunks
            st.write("### Relevant Chunks Used for Answer:")
            for i, doc in enumerate(relevant_docs):
                st.write(f"#### Chunk {i + 1}:")
                st.write(doc.page_content)
                st.write("---")
            
            # Stream the answer chunks and update the display
            for chunk in rag_chain.stream(question):
                answer_text += chunk
                placeholder.markdown(answer_text)
            
            st.write("#### Final Answer:")
            st.markdown(answer_text)
    else:
        st.info("Please upload a PDF document from the sidebar to begin.")

if __name__ == "__main__":
    main()
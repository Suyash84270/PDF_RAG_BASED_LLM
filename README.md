# RAG Chain Q&A App

## 📌 Overview
The **RAG Chain Q&A App** is an advanced **Retrieval-Augmented Generation (RAG)** application that enables users to upload a PDF document and ask contextual questions based on its content. This app uses **LangChain, FAISS, and Ollama's deepseek-r1 model** to retrieve relevant document sections and generate accurate answers in real-time.
![1](https://github.com/user-attachments/assets/5265e27b-9265-4f1a-9037-dc0d64f7c081)



![22](https://github.com/user-attachments/assets/0c0cbda2-8c58-45aa-b1c4-7d94f36a26fc)


![3](https://github.com/user-attachments/assets/b0afde73-fbee-441b-bff1-b433ba637372)



## ✨ Features
- 📄 **Document Upload:** Upload a PDF document and extract its content into Markdown format.
- 🔍 **Intelligent Chunking:** Split the document into structured sections based on headers.
- 🧠 **Vector Store & Embeddings:** Convert document chunks into embeddings and store them in FAISS for efficient retrieval.
- 🤖 **RAG-based Q&A:** Leverage a retrieval-augmented generation pipeline to answer user queries using the uploaded document.
- 🚀 **Real-time Answer Streaming:** Display responses dynamically as they are generated.

## 🏗️ Tech Stack
- **Frontend:** Streamlit (for interactive UI)
- **Backend:** LangChain, FAISS, Ollama
- **Embedding Model:** `nomic-embed-text`
- **LLM Model:** `deepseek-r1:1.5b`
- **Document Processing:** `docling.document_converter`

## 📂 Project Structure
```
📁 rag-qa-app
├── 📄 app.py            # Main Streamlit application
├── 📄 requirements.txt  # Dependencies list
├── 📄 README.md         # Project documentation
          
```

## 🛠️ Setup and Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/rag-qa-app.git
cd rag-qa-app
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3️⃣ Start Ollama (Ensure it's Running Locally)
```bash
ollama serve
```

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

## 🖥️ Usage Guide
1️⃣ **Upload a PDF document** in the sidebar.
2️⃣ The document is **converted to Markdown and split into structured chunks**.
3️⃣ A **vector store is created** with FAISS for fast retrieval.
4️⃣ **Ask a question** in the text input box.
5️⃣ The system retrieves relevant document chunks and generates an answer in **bullet points**.

## ⚡ Example Output
### **Input Question:**
> What are the main objectives of the document?

### **Generated Answer:**
- ✅ The document aims to provide an overview of...
- ✅ Key objectives include...
- ✅ The author highlights...

## 📌 Future Improvements
- [ ] Support for additional document formats (e.g., DOCX, TXT)
- [ ] Multi-document support
- [ ] More advanced retrieval mechanisms
- [ ] Fine-tuned LLM for specific domain-based Q&A

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues, pull requests, or suggestions.

## 📜 License
This project is licensed under the **MIT License**.

## 🌟 Acknowledgments
- **LangChain** for easy orchestration of LLMs and retrieval mechanisms.
- **FAISS** for efficient document search.
- **Ollama** for providing lightweight local LLM serving.
- **Streamlit** for creating an interactive interface effortlessly.

---
🚀 **Transform the way you interact with documents using AI!**


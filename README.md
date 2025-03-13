# PDF Insight Bot

## 📜 Overview
The **PDF Insight Bot** is a Streamlit-based web application that allows users to upload PDF documents, ask questions, and receive AI-powered responses. It leverages **Google's Gemini AI** and **FAISS vector databases** to provide accurate and context-aware answers based on document content. The app also maintains a **chat history** for improved interactions.

## 🚀 Features
- **Upload and process PDF files**: Extracts text from uploaded PDF documents.
- **AI-powered Q&A system**: Utilizes LangChain and Google's Gemini AI for question-answering.
- **Efficient text chunking**: Uses `RecursiveCharacterTextSplitter` to handle large documents.
- **FAISS-based similarity search**: Creates an optimized vector database for fast retrieval.
- **Chat history retention**: Stores up to five recent interactions for contextual responses.
- **User-friendly UI**: Built using **Streamlit** for easy interaction and visualization.

## 🏗️ Tech Stack
- **Python**
- **Streamlit**
- **LangChain**
- **FAISS (Facebook AI Similarity Search)**
- **Google Gemini AI**
- **PyPDF2** (for extracting text from PDFs)
- **GoogleGenerativeAIEmbeddings** (for creating embeddings)

## 📂 Installation & Setup
### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/your-repo/pdf-insight-bot.git
 cd pdf-insight-bot
```

### 2️⃣ Create a Virtual Environment
```bash
 python -m venv venv
 source venv/bin/activate  # On macOS/Linux
 venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```bash
 pip install -r requirements.txt
```

### 4️⃣ Set Up Google API Key
Obtain an API key from Google and set it as an environment variable:
```bash
 export GOOGLE_API_KEY='your-api-key'  # macOS/Linux
 set GOOGLE_API_KEY='your-api-key'     # Windows
```

Or, enter it in the Streamlit UI when prompted.

### 5️⃣ Run the Application
```bash
 streamlit run app.py
```

## 📑 Application Workflow
1. **Upload a PDF**: Users can upload a PDF document via the sidebar.
2. **Extract Text**: The app extracts text from the PDF using `PyPDF2`.
3. **Split into Chunks**: The extracted text is split into smaller chunks using `RecursiveCharacterTextSplitter`.
4. **Vector Database Creation**: FAISS is used to create a searchable database from the text chunks.
5. **Query Processing**: Users enter a question, and the app retrieves relevant document sections.
6. **AI Response Generation**: The Google Gemini AI model generates a response based on the retrieved content.
7. **Chat History Display**: The app retains the last five interactions for context.
8. **Reset Option**: Users can reset the chat history anytime via the sidebar.

## 📦 Directory Structure
```
📂 pdf-insight-bot
├── 📜 app.py                  # Main Streamlit application
├── 📜 requirements.txt         # Dependencies
└── 📜 README.md                # Project documentation
```

## 🛠️ Troubleshooting
### 🔥 Error: No API Key Provided
- Ensure you've set the API key as an environment variable or entered it in the UI.

### 📁 Error: No PDF Uploaded
- Upload a valid PDF file to proceed.

### ⚠️ Response: "I couldn't find that in the document."
- The query may not be relevant to the document content.
- Ensure the document contains useful information for the query.

## 🤝 Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

## 📜 License
This project is licensed under the MIT License.

---



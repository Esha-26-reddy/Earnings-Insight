
# 📊 EarningsInsight

### AI-Powered Earnings Call Intelligence

EarningsInsight is an AI-powered document intelligence platform that allows users to upload earnings reports or earnings call transcripts and ask questions about financial information using natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate document-grounded answers.

## 🚀 Features

- 📄 Upload earnings reports and earnings call transcripts
- 🤖 AI-powered question answering using RAG
- 🔍 Semantic document search using FAISS
- 🧠 Groq LLM for generating answers
- 🎙️ Voice-based question input
- 📚 Relevant source excerpts for answers
- ✅ Earnings-document validation
- 🚫 Rejects unrelated documents
- ❌ Detects questions unrelated to the uploaded document
- 💬 Natural language interaction
- 📱 Responsive React interface

## 🏗️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS
- Lucide React
- React Markdown
- Web Speech API

### Backend
- Python
- FastAPI
- Uvicorn
- LangChain
- FAISS
- Sentence Transformers
- PyPDF
- Pandas

### AI / LLM
- Groq API
- `openai/gpt-oss-120b`
- `sentence-transformers/all-MiniLM-L6-v2`

## 🔄 How It Works

```text
Upload Earnings Document
          ↓
Document Validation
          ↓
Text Extraction
          ↓
Text Chunking
          ↓
Sentence Transformer Embeddings
          ↓
FAISS Vector Index
          ↓
User Question
          ↓
Semantic Retrieval
          ↓
Relevant Context
          ↓
Groq LLM
          ↓
AI Generated Answer
          ↓
Relevant Source Excerpts
```

## 📁 Project Structure

```text
Earnings-Insight/
│
├── backend/
│   ├── main.py
│   ├── build_index.py
│   ├── query_index.py
│   ├── document_validator.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── QuestionBox.jsx
│   │   │   ├── AnswerCard.jsx
│   │   │   └── SourceCard.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Esha-26-reddy/Earnings-Insight.git
cd Earnings-Insight
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key
```

**Never commit your `.env` file or API key to GitHub.**

### 4. Run the Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🧪 Usage

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open the application in your browser.
4. Upload an earnings report or earnings call transcript.
5. Wait for the document to be processed.
6. Enter a question using natural language.
7. Alternatively, use the 🎙️ voice input button.
8. Click **Ask Question**.
9. View the AI-generated answer.
10. Expand **Sources** to view relevant document excerpts.

## 📄 Supported Documents

- PDF
- TXT
- CSV

Uploaded files are validated to ensure they contain earnings-related or financial information.

## 🛡️ Document-Grounded Answers

EarningsInsight answers questions using information retrieved from the uploaded document.

If a question is unrelated to the uploaded document, the application clearly indicates that the question is not relevant instead of providing an unrelated answer.

## 🎙️ Voice Input

EarningsInsight supports voice-based questions using the browser's Speech Recognition API.

The recognized text is placed into the question box before submitting it.

## 🔍 RAG Pipeline

1. **Document Processing** — Extracts readable text from uploaded files.
2. **Text Chunking** — Splits the document into smaller overlapping chunks.
3. **Embeddings** — Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
4. **Vector Storage** — Stores embeddings in a FAISS vector index.
5. **Semantic Retrieval** — Retrieves the most relevant chunks for the user's question.
6. **Answer Generation** — Passes retrieved context to the Groq LLM to generate a grounded answer.

## 🎯 Example Questions

```text
What was the company's revenue in the first quarter of 2026?

How much did revenue increase year over year?

What was the company's operating income?

How did Google Cloud perform?

What was the company's net income?

What was the earnings per share?
```

## 🔮 Future Enhancements

- 📈 Financial data visualization
- 📊 Earnings metrics dashboard
- 🔎 Advanced document search
- 📑 Multi-document comparison
- 🏢 Company-wise earnings analysis
- 💾 Conversation history
- ☁️ Cloud deployment
- 🔐 User authentication

## 👩‍💻 Author

**Esha Reddy**

GitHub: https://github.com/Esha-26-reddy/Earnings-Insight

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

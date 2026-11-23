# EarningsInsight – AI-Powered Earnings Call Analysis

EarningsInsight is an AI-powered platform that helps users analyze company earnings call transcripts and extract meaningful insights. It uses Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to answer questions, retrieve relevant information, and simplify financial document analysis.

## 🚀 Features

- **Document Analysis:** Upload and analyze earnings call transcripts.
- **AI-Powered Q&A:** Ask questions about uploaded earnings call documents.
- **Semantic Search:** Retrieve relevant information using vector similarity search.
- **Sentiment Analysis:** Identify positive, negative, and neutral sentiments in financial discussions.
- **Voice Input:** Interact with the application using voice input.
- **Source Retrieval:** Access relevant document sections supporting generated answers.
- **Data Export:** Export analysis results for further reference.

## 🛠️ Tech Stack

### Frontend
- React.js
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- LangChain
- Hugging Face
- FAISS Vector Database
- Grok LLM

## 📂 Project Structure

```text
EarningsInsight/
│
├── backend/
│   ├── venv/
│   ├── main.py
│   ├── build_index.py
│   ├── query_index.py
│   ├── document_validator.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── public/
    ├── src/
    ├── package.json
    └── ...
```

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:
- Python 3.12
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd EarningsInsight
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables in the `.env` file.

Start the backend server:

```bash
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

Open the local URL displayed in your terminal (usually `http://localhost:5173`).

## 🔑 Environment Variables

Create a `.env` file inside the backend directory and add the required API credentials.

Do not upload API keys or sensitive credentials to GitHub.

## 🧠 How It Works

EarningsInsight follows a Retrieval-Augmented Generation (RAG) workflow:

1. **Document Upload:** Users upload earnings call transcripts.
2. **Document Processing:** The backend validates and processes the uploaded documents.
3. **Text Chunking:** Documents are divided into smaller chunks.
4. **Embedding Generation:** Text chunks are converted into vector embeddings.
5. **Vector Storage:** FAISS stores the embeddings for efficient similarity search.
6. **Information Retrieval:** Relevant chunks are retrieved based on the user's query.
7. **AI Response Generation:** The LLM generates contextual answers using the retrieved information.
8. **Source Retrieval:** Relevant source sections are provided to support the answers.

## ▶️ Running the Project

Start the backend and frontend in two separate terminals.

**Terminal 1 – Backend**

```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
```

**Terminal 2 – Frontend**

```bash
cd frontend
npm run dev
```

## 🔒 Security

- Store API keys in environment variables.
- Never commit `.env` files.
- Keep sensitive credentials private.

## 👩‍💻 Author

Developed as an AI-powered financial document analysis project.

---

**EarningsInsight – Turning Financial Conversations into Actionable Insights.**
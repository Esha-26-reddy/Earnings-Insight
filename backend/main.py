import os
import shutil
import tempfile

from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from build_index import build_faiss_from_file
from query_index import get_llm, run_qa
from document_validator import validate_earnings_document

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

import pandas as pd


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="EarningsInsight API",
    description="AI-powered earnings document Q&A",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL STATE
# ============================================================

current_db = None
current_filename = None

llm_client = get_llm()


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "message": "EarningsInsight API is running 🚀"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# EXTRACT TEXT FOR VALIDATION
# ============================================================

def extract_text_for_validation(filepath):

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":

        loader = TextLoader(
            filepath,
            encoding="utf-8"
        )

        docs = loader.load()

        return "\n".join(
            doc.page_content
            for doc in docs
        )

    elif ext == ".pdf":

        loader = PyPDFLoader(filepath)

        docs = loader.load()

        return "\n".join(
            doc.page_content
            for doc in docs
        )

    elif ext == ".csv":

        df = pd.read_csv(
            filepath,
            engine="python",
            on_bad_lines="skip"
        )

        return df.to_string()

    return ""


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global current_db
    global current_filename

    # --------------------------------------------------------
    # Validate file extension
    # --------------------------------------------------------

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".csv"
    }

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload a PDF, TXT, or CSV earnings document."
            )
        )

    # --------------------------------------------------------
    # Save temporary file
    # --------------------------------------------------------

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        text = extract_text_for_validation(
            temp_path
        )

        # ----------------------------------------------------
        # Validate document
        # ----------------------------------------------------

        is_valid, message = validate_earnings_document(
            text
        )

        if not is_valid:

            raise HTTPException(
                status_code=400,
                detail=message
            )

        # ----------------------------------------------------
        # Build FAISS
        # ----------------------------------------------------

        db = build_faiss_from_file(
            temp_path,
            source_name=file.filename
        )

        current_db = db
        current_filename = file.filename

        return {
            "success": True,
            "filename": file.filename,
            "message": "Document uploaded and processed successfully."
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to process document: {str(e)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
async def ask_question(
    request: QuestionRequest
):

    global current_db
    global current_filename

    if current_db is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload an earnings document first."
        )

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:

        result = run_qa(
            llm_client,
            current_db,
            question
        )

        sources = []

        for doc in result.get(
            "source_documents",
            []
        ):

            sources.append({
                "content": doc.page_content[:1000],
                "source": doc.metadata.get(
                    "source",
                    current_filename
                )
            })

        return {
            "success": True,
            "question": question,
            "answer": result["result"],
            "relevant": result.get(
                "relevant",
                False
            ),
            "sources": sources
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate answer: {str(e)}"
        )
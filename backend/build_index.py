import os
import re
import pandas as pd

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"Page\s+\d+",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ============================================================
# BUILD FAISS DATABASE
# ============================================================

def build_faiss_from_file(
    filepath,
    source_name=None,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
):

    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model
    )

    ext = os.path.splitext(filepath)[1].lower()

    raw_docs = []

    source_name = source_name or os.path.basename(filepath)

    # ========================================================
    # TXT
    # ========================================================

    if ext == ".txt":

        loader = TextLoader(
            filepath,
            encoding="utf-8"
        )

        raw_docs = loader.load()

        for doc in raw_docs:
            doc.page_content = clean_text(
                doc.page_content
            )

            doc.metadata["source"] = source_name

    # ========================================================
    # PDF
    # ========================================================

    elif ext == ".pdf":

        loader = PyPDFLoader(filepath)

        pdf_pages = loader.load()

        for page in pdf_pages:

            page.page_content = clean_text(
                page.page_content
            )

            page.metadata["source"] = source_name

        raw_docs = pdf_pages

    # ========================================================
    # CSV
    # ========================================================

    elif ext == ".csv":

        try:

            df = pd.read_csv(
                filepath,
                engine="python",
                on_bad_lines="skip"
            )

            df = df.dropna(how="all")

            possible_text_columns = [
                "transcript",
                "text",
                "content",
                "body",
                "utterance",
                "sentence",
                "dialogue",
                "remarks",
                "comment",
                "speaker_text"
            ]

            text_column = None

            for col in df.columns:

                if col.lower() in possible_text_columns:
                    text_column = col
                    break

            if text_column:

                texts = (
                    df[text_column]
                    .fillna("")
                    .astype(str)
                    .tolist()
                )

                combined_text = "\n".join(
                    clean_text(t)
                    for t in texts
                )

            else:

                rows = []

                for _, row in df.iterrows():

                    row_text = " ".join(
                        str(v)
                        for v in row.values
                        if pd.notna(v)
                    )

                    if row_text.strip():
                        rows.append(
                            clean_text(row_text)
                        )

                combined_text = "\n".join(rows)

            raw_docs = [
                Document(
                    page_content=combined_text,
                    metadata={
                        "source": source_name
                    }
                )
            ]

        except Exception as e:

            raise Exception(
                f"CSV parsing failed: {e}"
            )

    else:

        raise Exception(
            f"Unsupported file type: {ext}"
        )

    # ========================================================
    # REMOVE EMPTY DOCUMENTS
    # ========================================================

    raw_docs = [
        doc
        for doc in raw_docs
        if doc.page_content.strip()
    ]

    if not raw_docs:
        raise Exception(
            "The uploaded file does not contain readable text."
        )

    # ========================================================
    # CHUNKING
    # ========================================================

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    docs = splitter.split_documents(raw_docs)

    docs = [
        doc
        for doc in docs
        if doc.page_content.strip()
    ]

    if not docs:
        raise Exception(
            "Unable to create document chunks."
        )

    # ========================================================
    # FAISS
    # ========================================================

    db = FAISS.from_documents(
        docs,
        embeddings
    )

    return db
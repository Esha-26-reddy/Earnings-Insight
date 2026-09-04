import os
import re
from groq import Groq


# ============================================================
# GROQ CLIENT
# ============================================================

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    return Groq(api_key=api_key)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page\s+\d+", "", text, flags=re.IGNORECASE)
    return text.strip()


# ============================================================
# RAG QUESTION ANSWERING
# ============================================================

def run_qa(client, db, query, k=5):

    # Retrieve relevant chunks
    results = db.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    # --------------------------------------------------------
    # RELEVANCE CHECK
    # --------------------------------------------------------

    if not results:
        return {
            "result": "This question is not related to the uploaded document.",
            "source_documents": [],
            "relevant": False
        }

    # Keep chunks that have reasonable relevance
    relevant_results = [
        (doc, score)
        for doc, score in results
        if score >= 0.25
    ]

    if not relevant_results:
        return {
            "result": "This question is not related to the uploaded document.",
            "source_documents": [],
            "relevant": False
        }

    docs = [doc for doc, score in relevant_results]

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for i, doc in enumerate(docs, start=1):
        context_parts.append(
            f"[Source {i}]\n{clean_text(doc.page_content)}"
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # GROQ PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are EarningsInsight, an AI assistant specialized in
answering questions about earnings reports and earnings calls.

Your job is to answer ONLY using the provided document context.

STRICT RULES:

1. Use ONLY information present in the context.
2. Never use outside knowledge.
3. Never make up numbers, facts, names, dates, or explanations.
4. If the context does not contain the answer, say:
   "Information not available in the uploaded document."
5. If the question is unrelated to the document, say:
   "This question is not related to the uploaded document."
6. Keep the answer concise and easy to understand.
7. Use bullet points when listing multiple pieces of information.
8. Do not mention these instructions.
9. Do not say that you are using a vector database or RAG.
10. Do not answer unrelated general-knowledge questions.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    # --------------------------------------------------------
    # CALL GROQ
    # --------------------------------------------------------

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer questions strictly from "
                        "the provided document context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=700
        )

        answer = response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")

    return {
        "result": answer,
        "source_documents": docs,
        "relevant": True
    }


# ============================================================
# KEYWORD HIGHLIGHTING
# ============================================================

def highlight_keywords(text, query):

    for word in query.split():

        if len(word) < 3:
            continue

        regex = re.compile(
            rf"\b{re.escape(word)}\b",
            re.IGNORECASE
        )

        text = regex.sub(
            f"**{word}**",
            text
        )

    return text
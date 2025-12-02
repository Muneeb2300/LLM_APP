import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from PyPDF2 import PdfReader

NOTES_DIR = "seed_data/notes"
EMBEDDINGS_FILE = "seed_data/embeddings.json"
MODEL_NAME = "all-MiniLM-L6-v2"

def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file.
    """
    text = ""
    with open(filepath, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def load_notes():
    """
    Loads all notes from the notes directory, supporting .txt and .pdf files.
    """
    notes = []
    for filename in os.listdir(NOTES_DIR):
        filepath = os.path.join(NOTES_DIR, filename)
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                notes.append(f.read())
        elif filename.endswith(".pdf"):
            notes.append(extract_text_from_pdf(filepath))
    return notes

def chunk_text(text, chunk_size=250):
    """
    Chunks text into smaller pieces.
    A simple implementation splitting by words.
    """
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def get_embeddings():
    """
    Gets embeddings from the stored file or generates them if they don't exist.
    """
    if os.path.exists(EMBEDDINGS_FILE) and os.path.getsize(EMBEDDINGS_FILE) > 0:
        with open(EMBEDDINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # File is empty or corrupt, proceed to generate embeddings
                pass

    model = SentenceTransformer(MODEL_NAME)
    notes = load_notes()
    all_chunks = []
    for note in notes:
        all_chunks.extend(chunk_text(note))

    embeddings = model.encode(all_chunks).tolist()

    data = {
        "chunks": all_chunks,
        "embeddings": embeddings
    }

    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(data, f)

    return data

def retrieve_chunks(question, top_k=3):
    """
    Retrieves the top-k most relevant chunks for a given question.
    """
    data = get_embeddings()
    chunks = data["chunks"]
    embeddings = np.array(data["embeddings"])

    model = SentenceTransformer(MODEL_NAME)
    question_embedding = model.encode(question)

    # Cosine similarity
    similarities = np.dot(embeddings, question_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(question_embedding))

    top_k_indices = np.argsort(similarities)[-top_k:][::-1]

    return [chunks[i] for i in top_k_indices]

# Study Buddy

## Project Overview

Study Buddy is a command-line application that uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions about your local study notes. It's designed to be a lightweight and efficient study assistant that helps you find information in your notes without getting distracted. The application is powered by a local Ollama instance, ensuring that your data remains private.

## How to Install Dependencies

To install the necessary Python packages, run the following command:

```bash
pip install -r requirements.txt
```

## How to Run the CLI App

To start the Study Buddy application, run the following command from the `studybuddy` directory:

```bash
python app.py
```

## How RAG Works

Retrieval-Augmented Generation (RAG) is a technique that combines the strengths of large language models (LLMs) with information retrieval. Here's how it works in Study Buddy:

1.  **Loading and Chunking:** The application loads your study notes from the `seed_data/notes` directory and splits them into smaller, manageable chunks.
2.  **Embedding Generation:** Each chunk is converted into a numerical representation called an embedding using a sentence-transformer model. These embeddings are stored in `seed_data/embeddings.json` to avoid re-computation.
3.  **Retrieval:** When you ask a question, the application generates an embedding for your question and uses cosine similarity to find the most relevant chunks from your notes.
4.  **Generation:** The retrieved chunks are then passed to the Ollama LLM along with your original question, and the model generates an answer based on the provided context.

## Architecture Diagram

```
User
  |
  v
app.py (CLI)
  |
  v
safety.py
  |
  v
rag.py (retrieve relevant note chunks)
  |
  v
llm.py (Ollama call)
  |
  v
telemetry.py
  |
  v
Answer
```

## Safety + Guardrail Explanation

Study Buddy includes several safety features to ensure a secure and reliable experience:

*   **Prompt Injection Detection:** The application checks for malicious phrases in the user's input that might be intended to manipulate the LLM's behavior.
*   **Input Length Limit:** To prevent overly long and potentially problematic inputs, the application limits the length of questions to 300 characters.
*   **Error Fallback:** In case of any unexpected errors, the application provides a generic and user-friendly error message.

## Offline Evaluation Instructions

To run the offline evaluation tests, use the following command from the `studybuddy` directory:

```bash
python run_tests.py
```

This script will run the test cases defined in `tests.json` and report a pass rate, allowing you to assess the performance of the RAG pipeline.

## Known Limitations

*   The chunking strategy is very simple and may not be optimal for all types of content.
*   The application relies on a local Ollama instance, which must be running for the application to work.
*   The RAG pipeline may not always retrieve the most relevant chunks, especially for very broad or ambiguous questions.

## How to Switch Ollama Model in .env

To switch the Ollama model, you can create a `.env` file in the `studybuddy` directory and add the following line:

```
OLLAMA_MODEL=your_model_name
```

Replace `your_model_name` with the name of the model you want to use (e.g., `mistral`, `llama2`).

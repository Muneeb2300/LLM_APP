# Technical Report: Study Buddy RAG Application
## 1. High-Level Overview

### 1.1. Project Goal and Purpose

The Study Buddy application is a command-line tool designed to act as a personal study assistant. Its primary goal is to provide a fast and accurate way for users to ask questions about their own study notes and receive answers that are strictly based on the provided material. The project leverages a Retrieval-Augmented Generation (RAG) pipeline to ensure that the answers are not only relevant but also grounded in the user's own data, preventing the Large Language Model (LLM) from hallucinating or providing information from outside the scope of the notes.

### 1.2. Intended User Flow

The user experience is designed to be as simple and intuitive as possible. The flow is as follows:

1.  **Launch the Application:** The user starts the application by running `python app.py` from the command line.
2.  **Ask a Question:** The user is greeted with a welcome message and a prompt to ask a question about their notes.
3.  **Receive an Answer:** The application processes the question, retrieves relevant information from the study notes, and generates an answer, which is then displayed to the user.
4.  **Continuous Interaction:** The application remains in a loop, allowing the user to ask multiple questions until they decide to exit by typing `exit`.

### 1.3. End-to-End System Workflow

From a technical perspective, the end-to-end workflow of the system is as follows:

1.  **User Input:** The system receives a question from the user via the command-line interface.
2.  **Safety Checks:** The input is first passed through a series of safety checks to detect potential prompt injection attacks and to ensure the question is within a reasonable length.
3.  **Information Retrieval (RAG):** The user's question is converted into a vector embedding. This embedding is then used to perform a cosine similarity search against a pre-computed set of embeddings for the study notes. The most relevant chunks of text from the notes are retrieved.
4.  **Prompt Construction:** The retrieved text chunks are combined with the user's question and a system prompt to create a comprehensive prompt for the LLM.
5.  **LLM Interaction:** The prompt is sent to a local Ollama instance, which generates an answer based on the provided context.
6.  **Telemetry Logging:** The system logs the request details, including the question, the latency of the LLM response, and the number of tokens used.
7.  **Displaying the Answer:** The final answer is displayed to the user in the command-line interface.

## 2. Architecture Explanation

### 2.1. System Architecture Breakdown

The Study Buddy application is built using a modular architecture, where each component has a distinct and well-defined responsibility. This separation of concerns makes the system easier to understand, maintain, and extend. The architecture is designed around a sequential pipeline that processes the user's request at each stage.

### 2.2. Component Descriptions

The application is composed of the following key modules:

*   **`app.py` (CLI):** This is the main entry point of the application. It's responsible for managing the user interface, orchestrating the calls to the other modules, and handling the main application loop.
*   **`safety.py`:** This module acts as a gatekeeper for user input. It contains all the logic for the safety and security checks, such as prompt injection detection and input length validation.
*   **`rag.py`:** This is the core of the RAG pipeline. It's responsible for loading the study notes, chunking them into smaller pieces, generating vector embeddings, and retrieving the most relevant chunks based on the user's question.
*   **`llm.py`:** This module is a wrapper for the Ollama LLM. It's responsible for constructing the prompt, making the API call to the Ollama service, and parsing the response.
*   **`telemetry.py`:** This module handles all the logging for the application. It's responsible for recording the details of each request, including the question, latency, and token count.

### 2.3. Component Interaction and Data Flow

The components interact in a linear sequence, with the output of one component serving as the input for the next. The data flow is as follows:

1.  The `app.py` module receives the user's question as a raw string.
2.  This string is passed to the `safety.py` module, which either returns an error message or allows the request to proceed.
3.  The validated question is then passed to the `rag.py` module, which returns a list of the most relevant text chunks from the study notes.
4.  The question and the retrieved chunks are passed to the `llm.py` module, which returns a dictionary containing the answer, latency, and token count.
5.  The question, latency, and token count are passed to the `telemetry.py` module for logging.
6.  Finally, the answer is returned to the `app.py` module, which displays it to the user.

### 2.4. Architecture Diagram

The following ASCII diagram illustrates the flow of data through the system:

```
      User
        |
        v
+----------------+
|   app.py (CLI) |
+----------------+
        |
        v
+----------------+
|  safety.py     |
+----------------+
        |
        v
+----------------+
|    rag.py      |
+----------------+
        |
        v
+----------------+
|    llm.py      |
+----------------+
        |
        v
+----------------+
| telemetry.py   |
+----------------+
        |
        v
      Answer
```

## 3. Code-Level Explanations

### 3.1. `app.py`

*   **File Responsibility:** This file serves as the main entry point and the central orchestrator of the application. It's responsible for managing the command-line interface (CLI), handling user input, and coordinating the interactions between the other modules.

*   **`main()` function:**
    *   **Logic Flow:**
        1.  The function starts by printing a welcome message and instructions for the user.
        2.  It then enters an infinite `while` loop to continuously accept user input.
        3.  Inside the loop, it prompts the user for a question using the `input()` function.
        4.  It checks if the user's input is "exit" (case-insensitive) and, if so, breaks the loop to terminate the application.
        5.  The function then enters a `try...except` block to gracefully handle any potential errors that may occur during the processing of the user's question.
        6.  It calls the `check_safety()` function from the `safety` module to validate the user's input.
        7.  If the input is deemed unsafe, an error message is printed, and the loop continues to the next iteration.
        8.  It calls the `retrieve_chunks()` function from the `rag` module to get the most relevant text chunks from the study notes.
        9.  It calls the `generate_response()` function from the `llm` module, passing in the user's question and the retrieved chunks.
        10. If the `generate_response()` function returns `None` (indicating an error), a generic error message is printed, and the loop continues.
        11. It extracts the answer, latency, and token count from the response data.
        12. It calls the `log_request()` function from the `telemetry` module to log the details of the request.
        13. Finally, it prints the answer to the console.
    *   **Design Decisions:** The use of a central `main()` function to orchestrate the application's logic promotes a clean and organized code structure. The infinite `while` loop provides a simple and effective way to create a continuous CLI, while the `try...except` block ensures that the application is robust and can handle unexpected errors without crashing.
    *   **Data Flow:** The function takes a raw string from the user and passes it through the various modules, transforming it at each stage until a final answer is generated and displayed.

### 3.2. `safety.py`

*   **File Responsibility:** This module is responsible for implementing the safety and security guardrails of the application. It provides a set of functions to validate user input and protect the system from malicious or an overly long queries.

*   **`is_prompt_injection(prompt)` function:**
    *   **Logic Flow:**
        1.  The function takes a user's prompt as input.
        2.  It checks if the prompt contains any of a predefined list of phrases that are commonly used in prompt injection attacks.
        3.  The check is case-insensitive.
        4.  It returns `True` if a malicious phrase is found and `False` otherwise.
    *   **Inputs and Outputs:** The function takes a string as input and returns a boolean.

*   **`is_too_long(prompt)` function:**
    *   **Logic Flow:**
        1.  The function takes a user's prompt as input.
        2.  It checks if the length of the prompt is greater than 300 characters.
        3.  It returns `True` if the prompt is too long and `False` otherwise.
    *   **Inputs and Outputs:** The function takes a string as input and returns a boolean.

*   **`get_error_message()` function:**
    *   **Logic Flow:** This function simply returns a generic error message.
    *   **Design Decisions:** This function is used to provide a consistent and user-friendly error message in case of any exceptions, preventing technical details from being exposed to the user.

*   **`check_safety(prompt)` function:**
    *   **Logic Flow:**
        1.  This function acts as a facade for the other safety checks in the module.
        2.  It calls `is_prompt_injection()` and `is_too_long()` to validate the prompt.
        3.  If any of the checks fail, it returns an appropriate error message.
        4.  If the prompt passes all the checks, it returns `None`.
    *   **Inputs and Outputs:** The function takes a string as input and returns either a string (in case of an error) or `None`.

### 3.3. `rag.py`

*   **File Responsibility:** This is the heart of the RAG pipeline. It's responsible for all the logic related to information retrieval, including loading the study notes, chunking the text, generating embeddings, and finding the most relevant chunks for a given question.

*   **`load_notes()` function:**
    *   **Logic Flow:**
        1.  The function reads all the `.txt` files from the `seed_data/notes` directory.
        2.  It returns a list of strings, where each string is the content of a note file.

*   **`chunk_text(text, chunk_size)` function:**
    *   **Logic Flow:**
        1.  The function takes a string of text and a chunk size as input.
        2.  It splits the text into a list of words.
        3.  It then groups the words into chunks of the specified size.
        4.  It returns a list of strings, where each string is a chunk of text.
    *   **Design Decisions:** The chunking strategy is simple but effective for the purpose of this application. A more sophisticated approach might involve splitting the text by sentences or using a library like NLTK for more advanced text processing.

*   **`get_embeddings()` function:**
    *   **Logic Flow:**
        1.  This function is responsible for generating and caching the embeddings for the study notes.
        2.  It first checks if the `embeddings.json` file exists and is not empty.
        3.  If the file exists, it loads the embeddings from the file and returns them.
        4.  If the file doesn't exist or is empty, it loads the notes, chunks them, and then uses the `sentence-transformers` library to generate embeddings for each chunk.
        5.  The embeddings are then saved to the `embeddings.json` file for future use.
    *   **Design Decisions:** Caching the embeddings is a crucial optimization that prevents the system from having to re-generate them every time the application starts. This significantly improves the startup time of the application.

*   **`retrieve_chunks(question, top_k)` function:**
    *   **Logic Flow:**
        1.  The function takes a user's question and the number of chunks to retrieve (`top_k`) as input.
        2.  It calls `get_embeddings()` to get the embeddings for the study notes.
        3.  It generates an embedding for the user's question using the same `sentence-transformers` model.
        4.  It then calculates the cosine similarity between the question embedding and the embeddings of all the text chunks.
        5.  It sorts the chunks by their similarity score in descending order and returns the `top_k` most similar chunks.
    *   **RAG Implementation:** This function is the core of the RAG implementation. It uses a vector-based similarity search to find the most relevant context for the user's question, which is then used to augment the prompt for the LLM.

### 3.4. `llm.py`

*   **File Responsibility:** This module is responsible for all interactions with the Ollama LLM. It acts as a wrapper for the Ollama API, handling prompt construction, API calls, and response parsing.

*   **`generate_response(question, retrieved_chunks)` function:**
    *   **Logic Flow:**
        1.  The function takes the user's question and the retrieved text chunks as input.
        2.  It constructs a prompt that includes a system prompt, the retrieved chunks, and the user's question.
        3.  It creates a payload for the Ollama API call, specifying the model to use and the prompt.
        4.  It records the start time of the API call to measure latency.
        5.  It makes a POST request to the Ollama API's `/api/generate` endpoint.
        6.  It records the end time of the API call and calculates the latency.
        7.  It parses the JSON response from the API to extract the answer, and the token count.
        8.  It returns a dictionary containing the answer, latency, and token count.
    *   **Error Handling:** The function uses a `try...except` block to catch any exceptions that may occur during the API call, such as a connection error. If an error occurs, it prints an error message and returns `None`.
    *   **LLM Integration:** This function is the primary point of integration with the LLM. It encapsulates all the details of the API call, making it easy to use from other parts of the application.

### 3.5. `telemetry.py`

*   **File Responsibility:** This module is responsible for logging the details of each request to a telemetry file.

*   **`log_request(question, latency, tokens)` function:**
    *   **Logic Flow:**
        1.  The function takes the user's question, the latency of the LLM response, and the number of tokens used as input.
        2.  It creates a timestamp for the log entry.
        3.  It formats the log entry into a structured string.
        4.  It appends the log entry to the `studybuddy_logs.txt` file.

### 3.6. `run_tests.py`

*   **File Responsibility:** This script is responsible for running the offline evaluation tests for the RAG pipeline.

*   **`run_tests()` function:**
    *   **Logic Flow:**
        1.  The function loads the test cases from the `tests.json` file.
        2.  It iterates through each test case, running the question through the RAG and LLM pipeline.
        3.  It checks if the generated answer contains the expected pattern.
        4.  It keeps track of the number of passed tests.
        5.  After running all the tests, it calculates and prints the pass rate.
    *   **Design Decisions:** The use of an offline evaluation script is a best practice for developing and maintaining LLM-based applications. It provides a way to quantitatively measure the performance of the system and to detect any regressions that may be introduced by changes to the code.

## 4. LLM Integration

### 4.1. Prompt Construction

The quality of the prompt is crucial for getting a good response from the LLM. The prompt in the Study Buddy application is constructed from three main components:

*   **System Prompt:** This is a set of instructions that tells the LLM how to behave. It sets the persona of the "Study Buddy" and defines the rules for generating answers.
*   **Retrieved Chunks:** These are the most relevant text chunks from the study notes, as determined by the RAG pipeline. They provide the context for the LLM to answer the user's question.
*   **User's Question:** This is the original question that the user asked.

These three components are combined into a single prompt that is sent to the LLM.

### 4.2. System Prompt Design

The system prompt is designed to be as clear and concise as possible, while still providing the LLM with all the necessary instructions. The key elements of the system prompt are:

*   **Persona:** "You are StudyBuddy, a strict study assistant." This sets the tone of the interaction and helps the LLM to generate answers that are in line with the application's purpose.
*   **Rule:** "You MUST answer ONLY using the content from the retrieved notes." This is the most important rule in the system prompt. It's designed to prevent the LLM from hallucinating and to ensure that the answers are grounded in the user's own data.
*   **Fallback:** "If the answer is not found in the notes, say: 'I don’t know based on the notes.'" This provides the LLM with a clear instruction on how to handle cases where the answer is not available in the provided context.

### 4.3. Model Calling and Parameters

The application calls the Ollama LLM using a simple HTTP POST request. The key parameters of the API call are:

*   **`model`:** The name of the Ollama model to use. This is specified in the `.env` file and defaults to "llama3".
*   **`prompt`:** The prompt to send to the model.
*   **`stream`:** This is set to `False` to indicate that the application expects a single, non-streaming response from the API.

The application does not currently specify any other parameters, such as `temperature` or `max_tokens`, relying on the default settings of the Ollama model.

### 4.4. Response Parsing and Validation

The response from the Ollama API is a JSON object that contains the generated answer, as well as some metadata about the response. The application parses this JSON object to extract the answer and the token count. No specific validation is performed on the content of the answer itself, as the system prompt is designed to ensure that the answer is always in the desired format.

## 5. Telemetry

### 5.1. Telemetry Implementation

Telemetry in the Study Buddy application is implemented in the `telemetry.py` module. The `log_request()` function is responsible for writing log entries to the `studybuddy_logs.txt` file. The logging is done in a simple and human-readable format, with each log entry being a single line in the file.

### 5.2. Logged Information

Each log entry contains the following information:

*   **`timestamp`:** The date and time of the request.
*   **`pathway`:** The pathway of the request, which is always "RAG" in this application.
*   **`latency`:** The latency of the LLM response in seconds.
*   **`tokens`:** The number of tokens used by the LLM to generate the response.
*   **`q`:** The user's question.

### 5.3. Importance of Latency and Cost Tracking

*   **Latency Tracking:** Tracking the latency of the LLM response is important for understanding the performance of the system. If the latency is too high, it can lead to a poor user experience. By logging the latency of each request, it's possible to identify performance bottlenecks and to track the impact of any changes to the system.
*   **Cost Tracking (Token Usage):** While the Study Buddy application uses a local Ollama instance and therefore does not have any direct costs associated with API calls, logging the token count is still a good practice. In a production environment, where the application might be using a cloud-based LLM, the token count would be directly related to the cost of running the application. By logging the token count, it's possible to monitor the cost of the application and to identify any opportunities for optimization.

## 6. Safety & Robustness

### 6.1. Implemented Guardrails

The Study Buddy application includes several guardrails to protect the system from malicious input and to ensure a robust and reliable user experience. These guardrails are implemented in the `safety.py` module and are designed to be the first line of defense against any potential issues.

### 6.2. Input Length Check

The `is_too_long()` function checks if the length of the user's input is greater than 300 characters. This is a simple but effective way to prevent users from submitting overly long queries, which could potentially be used to abuse the system or to cause performance issues.

### 6.3. Prompt Injection Checks

The `is_prompt_injection()` function checks for the presence of common prompt injection phrases in the user's input. Prompt injection is a type of attack where a user tries to manipulate the LLM's behavior by embedding malicious instructions in their prompt. By checking for these phrases, the application can prevent a wide range of potential attacks.

### 6.4. Importance of Protection Layers

These protection layers are needed to ensure the security and stability of the application. Without them, the application would be vulnerable to a variety of attacks, including:

*   **Denial of Service (DoS):** An attacker could potentially crash the application by submitting an overly long prompt.
*   **Prompt Injection:** An attacker could use prompt injection to bypass the system's instructions and to get the LLM to generate inappropriate or harmful content.
*   **Resource Exhaustion:** An attacker could try to exhaust the system's resources by submitting a large number of long or complex queries.

By implementing these simple but effective guardrails, the Study Buddy application is able to provide a safe and reliable user experience.

## 7. Offline Evaluation

### 7.1. `tests.json` Format

The `tests.json` file contains a list of test cases that are used to evaluate the performance of the RAG pipeline. Each test case is a JSON object with the following fields:

*   **`input`:** The question to ask the system.
*   **`expected_pattern`:** A string that is expected to be present in the generated answer.

### 7.2. Evaluation Script

The `run_tests.py` script is used to run the offline evaluation tests. The script loads the test cases from the `tests.json` file and then iterates through each test case, running the question through the RAG and LLM pipeline.

### 7.3. Pass Rate Calculation

For each test case, the script checks if the generated answer contains the `expected_pattern`. If it does, the test case is considered to have passed. After running all the test cases, the script calculates the pass rate as the percentage of test cases that passed.

## 8. Reproducibility

### 8.1. Purpose of Project Files

The Study Buddy application is designed to be easily reproducible. The following files are included in the project to ensure that anyone can run the application from scratch:

*   **`README.md`:** This file provides a high-level overview of the project, as well as instructions on how to install the dependencies and run the application.
*   **`requirements.txt`:** This file lists all the Python packages that are required to run the application. This allows anyone to create an identical environment using a single command (`pip install -r requirements.txt`).
*   **`.env.example`:** This file serves as a template for the `.env` file, which is used to configure the application. It shows which environment variables are needed to run the application.
*   **`seed_data` folder:** This folder contains the study notes that are used by the RAG pipeline. This allows anyone to run the application with the same data that was used during development.

### 8.2. Running the Project from Scratch

To run the project from scratch, a user would need to follow these steps:

1.  Clone the repository to their local machine.
2.  Install the required Python packages using `pip install -r requirements.txt`.
3.  Create a `.env` file and specify the Ollama model to use.
4.  Run the application using `python app.py`.

## 9. Design & UX Considerations

### 9.1. CLI Design

The Study Buddy application is designed as a command-line interface (CLI) for a few key reasons:

*   **Simplicity:** A CLI is a simple and lightweight interface that is easy to use and does not require any complex setup.
*   **Focus:** A CLI provides a distraction-free environment that allows the user to focus on their study notes.
*   **Portability:** A CLI can be run on any operating system with a Python interpreter, making it highly portable.

### 9.2. User Flow

The user flow is designed to be as simple and intuitive as possible. The application starts with a welcome message and a clear prompt, and the user can ask questions in a continuous loop. The "exit" command provides a clean and obvious way to terminate the application.

### 9.3. UX Touches

*   **Welcome Message:** The application starts with a friendly welcome message that sets the tone for the interaction.
*   **Clear Instructions:** The instructions on how to use the application are clear and concise.
*   **Error Handling:** The application includes robust error handling to ensure that the user never sees a technical error message.

## 10. Known Limitations

### 10.1. Current Limitations

*   **Simple Chunking Strategy:** The current chunking strategy is based on a fixed number of words. This is a simple approach that may not be optimal for all types of content. A more sophisticated approach might involve splitting the text by sentences or using a library like NLTK for more advanced text processing.
*   **Reliance on Local Ollama Instance:** The application requires a local Ollama instance to be running. This may be a barrier to entry for some users.
*   **No Conversation History:** The application does not currently have any concept of conversation history. Each question is treated as a standalone query.

### 10.2. Possible Improvements

*   **Graphical User Interface (GUI):** A GUI could be added to the application to make it more user-friendly.
*   **Support for More File Formats:** The application could be extended to support other file formats, such as PDFs or Word documents.
*   **Integration with Cloud-Based LLMs:** The application could be integrated with cloud-based LLMs, such as GPT-3 or Claude, to provide more powerful and accurate answers.

## 11. Final Summary

### 11.1. Project Functionality and Reliability

The Study Buddy application is a functional and reliable tool that provides a simple and effective way for users to ask questions about their study notes. The modular architecture, robust error handling, and comprehensive test suite all contribute to the reliability of the application.

### 11.2. Value of the LLM

The LLM is the core of the Study Buddy application. It provides the ability to understand and answer natural language questions, which would be very difficult to achieve with traditional programming techniques. The RAG pipeline ensures that the LLM's responses are grounded in the user's own data, making it a powerful and trustworthy study assistant.

### 11.3. How Everything Fits Together

The Study Buddy application is a well-designed and well-engineered system that demonstrates the power of combining LLMs with traditional software engineering practices. The modular architecture, robust safety features, and comprehensive testing all work together to create a high-quality application that is both useful and reliable.

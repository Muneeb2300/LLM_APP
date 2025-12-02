
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

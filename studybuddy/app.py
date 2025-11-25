import rag
import llm
import safety
import telemetry

def main():
    """
    Main function for the Study Buddy CLI.
    """
    print("Welcome to StudyBuddy! Ask a question about your notes.")
    print("Type 'exit' to quit.")

    while True:
        question = input("> ")
        if question.lower() == 'exit':
            break

        try:
            # 1. Safety checks
            safety_error = safety.check_safety(question)
            if safety_error:
                print(safety_error)
                continue

            # 2. RAG pipeline
            retrieved_chunks = rag.retrieve_chunks(question)

            # 3. LLM generation
            response_data = llm.generate_response(question, retrieved_chunks)

            if not response_data:
                print(safety.get_error_message())
                continue

            answer = response_data["answer"]
            latency = response_data["latency"]
            tokens = response_data["tokens"]

            # 4. Telemetry logging
            telemetry.log_request(question, latency, tokens)

            # 5. Print answer
            print(answer)

        except Exception as e:
            print(safety.get_error_message())
            print(f"Error details: {e}")


if __name__ == "__main__":
    main()

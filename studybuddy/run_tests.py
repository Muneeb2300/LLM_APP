import json
import rag
import llm
import safety

TESTS_FILE = "tests.json"

def run_tests():
    """
    Runs the offline evaluation tests.
    """
    with open(TESTS_FILE, "r") as f:
        tests = json.load(f)

    passed_tests = 0
    total_tests = len(tests)

    for i, test in enumerate(tests):
        print(f"Running test {i+1}/{total_tests}...")
        question = test["input"]
        expected_pattern = test["expected_pattern"]

        try:
            retrieved_chunks = rag.retrieve_chunks(question)
            response_data = llm.generate_response(question, retrieved_chunks)

            if not response_data:
                print(f"  FAILED: No response from LLM for question: '{question}'")
                continue

            answer = response_data["answer"]

            if expected_pattern.lower() in answer.lower():
                passed_tests += 1
                print(f"  PASSED: '{question}'")
            else:
                print(f"  FAILED: '{question}'")
                print(f"    Expected pattern: '{expected_pattern}'")
                print(f"    Actual answer: '{answer}'")

        except Exception as e:
            print(f"  ERROR: An exception occurred during test: {e}")

    pass_rate = (passed_tests / total_tests) * 100
    print(f"\nTests passed: {passed_tests}/{total_tests} ({pass_rate:.2f}%)")

if __name__ == "__main__":
    run_tests()

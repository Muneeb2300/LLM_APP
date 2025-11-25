import datetime

def log_request(question, latency, tokens):
    """
    Logs a request to the telemetry file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f'{timestamp} | pathway=RAG | latency={latency:.2f}s | tokens={tokens} | q="{question}"\n'
    with open("studybuddy_logs.txt", "a") as f:
        f.write(log_entry)

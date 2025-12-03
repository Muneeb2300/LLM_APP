# Study Buddy Presentation Script
## 1. Problem (30–45 seconds)

**(Start of script)**

"Hi everyone. Today, I'm going to show you a project called Study Buddy.

So, what’s the problem this app solves? Well, if you’re a student, you know how it feels to have piles of notes, lectures, and readings. Finding a specific piece of information can be really frustrating, especially when you’re studying for an exam.

Existing tools like just searching through PDFs are slow, and generic search engines don’t know anything about your specific course material. This is where an LLM-based solution comes in. An LLM can understand your notes and answer your questions in a natural way, but only if it's focused on the right information. That's why I built Study Buddy—to create a personal, private, and accurate study assistant that only uses *your* notes to answer your questions."

## 2. Demo (1–2 minutes)

"Now, I’ll show you a quick demo of how it works.

**(Scene: Terminal window)**

"Here you can see the app loading my notes. It's a simple command-line interface, so it's super lightweight and fast.

I’ll start by running the app from the terminal.

**(Run `python app.py`)**

"It welcomes me and prompts me for a question. Let's start with something simple. I’ll ask it to explain what recursion is, based on my lecture notes."

**(Type: 'What is recursion?')**

"And here’s the answer. It’s pulled this directly from my notes, defining it as a function that calls itself and mentioning the need for a base case. It’s accurate because it’s only using my material.

Now, let's try something more creative. I'll ask it to generate a few quiz questions to help me study."

**(Type: 'Generate 3 quiz questions about data structures')**

"And here are the quiz questions it generates. This is really useful for active recall and self-testing.

As you can see, the app is able to understand my questions and provide relevant answers by retrieving content from the RAG database, which is built from my personal notes. It’s fast, accurate, and completely private."

## 3. How It Works (RAG/tool/finetune) (1–1.5 minutes)

"So, what’s happening behind the scenes?

"The magic behind Study Buddy is a technique called Retrieval-Augmented Generation, or RAG. Here’s how it works in simple terms.

First, the app looks at the folder containing all my plain-text notes. It reads them and breaks them down into smaller, manageable chunks.

Next, it uses an embedding model—in this case, `nomic-embed-text`—to convert each chunk into a numerical representation, like a coordinate on a map. These embeddings are stored locally.

When I ask a question, my question is also converted into an embedding. The app then uses cosine similarity to find the note chunks with embeddings that are 'closest' to my question’s embedding. These are the most relevant pieces of information.

Finally, the app builds a prompt for the LLM. It takes the most relevant chunks it found, combines them with my original question, and adds a strict system prompt. The model I'm using is `llama3`, running locally with Ollama.

The system prompt has some important safety rules. It tells the model it *must* only use the notes I provide and, if the answer isn't there, it has to say 'I don't know.' This prevents it from making things up.

The app also has a couple of other guardrails. There's a prompt-injection check to block malicious inputs, and an input-length guard to stop overly long questions.

And finally, for every question I ask, the app runs some simple telemetry. It logs the timestamp, the latency of the response, and the pathway used—which, in this case, is always RAG."

## 4. Results & Closing (20–30 seconds)

"So, why does this work so well for studying?

"Because it’s fast, private, and, most importantly, it’s grounded in your own material. This makes it a reliable study partner.

Of course, there are limits. The app is currently CLI-only, and the chunking strategy is pretty simple. In the future, I could add a proper GUI or support for more file types like PDFs.

But for now, this project demonstrates a complete LLM-powered workflow—from RAG to guardrails to evaluation—in a simple app that actually helps with real study tasks.

Thank you."

**(End of script)**

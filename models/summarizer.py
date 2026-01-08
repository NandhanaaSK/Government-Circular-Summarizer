from transformers import pipeline
import re

# Load model once
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def split_text(text, chunk_size=800):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(" ".join(current)) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def to_bullets(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def summarize_text(text, length="medium"):
    if not text or len(text.strip()) < 50:
        return ["Text too short to summarize."]

    # 🔹 UPDATED chunk & length control
    if length == "short":
        max_len, min_len = 60, 25
        max_chunks = 2

    elif length == "medium":
        max_len, min_len = 120, 50
        max_chunks = 4

    elif length == "detailed":
        max_len, min_len = 350, 180
        max_chunks = 8

    else:
        max_len, min_len = 120, 50
        max_chunks = 4

    chunks = split_text(text)
    summaries = []

    for chunk in chunks[:max_chunks]:
        try:
            result = summarizer(
                "summarize: " + chunk,
                max_length=max_len,
                min_length=min_len,
                do_sample=True,
                truncation=True
            )
            summaries.append(result[0]["summary_text"])
        except Exception:
            continue

    full_summary = " ".join(summaries)
    return to_bullets(full_summary)

import json
from pathlib import Path

INPUT_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/chunks")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def load_documents():

    documents = []

    for file in INPUT_DIR.glob("*.txt"):

        text = file.read_text(encoding="utf-8")

        documents.append({

            "source": file.name,

            "text": text

        })

    return documents


def split_text(text):

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def create_chunks(documents):

    all_chunks = []

    chunk_counter = 1

    for document in documents:

        chunks = split_text(document["text"])

        for index, chunk in enumerate(chunks, start=1):

            all_chunks.append({

                "id": chunk_counter,

                "source": document["source"],

                "chunk_number": index,

                "text": chunk.strip()

            })

            chunk_counter += 1

    return all_chunks


def save_chunks(chunks):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents.\n")

    chunks = create_chunks(documents)

    save_chunks(chunks)

    print(f"Created {len(chunks)} chunks.")

    print("Saved to data/chunks/chunks.json")


if __name__ == "__main__":
    main()
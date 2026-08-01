import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INDEX_FILE = Path("data/vector_db/faiss_index.bin")

METADATA_FILE = Path("data/vector_db/metadata.json")

TOP_K = 5


def load_model():

    print("Loading embedding model...")

    return SentenceTransformer(MODEL_NAME)


def load_index():

    return faiss.read_index(str(INDEX_FILE))


def load_metadata():

    with open(METADATA_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


def search(query, model, index, metadata):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        TOP_K
    )

    results = []

    for idx, score in zip(indices[0], scores[0]):

        if idx == -1:
            continue

        chunk = metadata[idx]

        results.append({

            "score": float(score),

            "source": chunk["source"],

            "chunk": chunk["chunk_number"],

            "text": chunk["text"]

        })

    return results

def build_context(results):
    """
    Combine retrieved chunks into a single context string.
    """

    sections = []

    for result in results:

        section = (
            f"Source: {result['source']}\n"
            f"Chunk: {result['chunk']}\n\n"
            f"{result['text']}"
        )

        sections.append(section)

    return "\n\n" + ("-" * 80 + "\n\n").join(sections)


def main():

    model = load_model()

    index = load_index()

    metadata = load_metadata()

    print()

    while True:

        query = input("\nAsk a question (type exit to quit): ")

        if query.lower() == "exit":
            break

        results = search(
            query,
            model,
            index,
            metadata
        )

        context = build_context(results)

        print("\nTop Retrieved Chunks\n")

        for i, result in enumerate(results, start=1):

            print("=" * 60)

            print(f"Result {i}")

            print(f"Source : {result['source']}")

            print(f"Chunk  : {result['chunk']}")

            print(f"Score  : {result['score']:.4f}")

            print()

            print(result["text"])

            print()

        print("\n")

        print("=" * 80)

        print("COMBINED CONTEXT")

        print("=" * 80)

        print(context)

if __name__ == "__main__":
    main()
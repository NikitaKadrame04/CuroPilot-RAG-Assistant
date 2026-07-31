import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


INPUT_FILE = Path("data/chunks/chunks.json")
OUTPUT_DIR = Path("data/embeddings")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_model():

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Model loaded.\n")

    return model


def generate_embeddings(model, chunks):

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


def save_embeddings(chunks, embeddings):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    np.save(
        OUTPUT_DIR / "embeddings.npy",
        embeddings
    )

    with open(
        OUTPUT_DIR / "metadata.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.\n")

    model = load_model()

    embeddings = generate_embeddings(
        model,
        chunks
    )

    save_embeddings(
        chunks,
        embeddings
    )

    print("\nEmbedding generation completed.")

    print(f"Generated {len(embeddings)} embeddings.")

    print("Saved embeddings to data/embeddings/")


if __name__ == "__main__":
    main()
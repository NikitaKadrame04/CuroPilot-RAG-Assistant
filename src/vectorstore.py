import json
from pathlib import Path

import faiss
import numpy as np


EMBEDDINGS_FILE = Path("data/embeddings/embeddings.npy")
METADATA_FILE = Path("data/embeddings/metadata.json")

OUTPUT_DIR = Path("data/vector_db")

INDEX_FILE = OUTPUT_DIR / "faiss_index.bin"
OUTPUT_METADATA = OUTPUT_DIR / "metadata.json"


def load_embeddings():

    embeddings = np.load(EMBEDDINGS_FILE)

    embeddings = embeddings.astype("float32")

    faiss.normalize_L2(embeddings)

    return embeddings


def load_metadata():

    with open(METADATA_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


def build_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def save_index(index, metadata):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_FILE))

    with open(
        OUTPUT_METADATA,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    print("Loading embeddings...")

    embeddings = load_embeddings()

    metadata = load_metadata()

    print(f"Loaded {len(metadata)} vectors.")

    print("Building FAISS index...")

    index = build_index(embeddings)

    print("Saving index...")

    save_index(index, metadata)

    print()

    print("FAISS index created successfully!")

    print(f"Vectors stored: {index.ntotal}")

    print(f"Dimension: {embeddings.shape[1]}")

    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
from pathlib import Path
from collections import Counter
import re

INPUT_DIR = Path("data/extracted")
OUTPUT_DIR = Path("data/processed")

# Remove lines that appear in at least this percentage
# of all documents.
COMMON_LINE_THRESHOLD = 0.8

def load_documents():
    #Load all extracted text documents.
    
    documents = {}

    for file in INPUT_DIR.glob("*.txt"):

        with open(file, "r", encoding="utf-8") as f:

            documents[file.name] = f.read()

    return documents


def find_common_lines(documents):
    #Find lines that appear in many documents.

    counter = Counter()

    total_documents = len(documents)

    for text in documents.values():

        unique_lines = set()

        for line in text.splitlines():

            line = line.strip()

            if line:
                unique_lines.add(line)

        counter.update(unique_lines)

    common_lines = set()

    threshold = total_documents * COMMON_LINE_THRESHOLD

    for line, count in counter.items():

        if count >= threshold:

            common_lines.add(line)

    return common_lines


def clean_document(text, common_lines):

    cleaned_lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line in common_lines:
            continue

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # Collapse multiple spaces
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    # Collapse multiple blank lines
    cleaned_text = re.sub(r"\n{2,}", "\n\n", cleaned_text)

    return cleaned_text.strip()


def save_documents(cleaned_documents):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, text in cleaned_documents.items():

        filepath = OUTPUT_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:

            f.write(text)


def main():

    print("Loading extracted documents...")

    documents = load_documents()

    print(f"{len(documents)} documents loaded.\n")

    common_lines = find_common_lines(documents)

    print(f"Found {len(common_lines)} common lines.\n")

    cleaned_documents = {}

    for filename, text in documents.items():

        cleaned_text = clean_document(text, common_lines)

        cleaned_documents[filename] = cleaned_text

        print(f"Processed: {filename}")

    save_documents(cleaned_documents)

    print("\nCleaning completed successfully!")

    print(f"Clean documents saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
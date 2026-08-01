from retriever import (
    load_model,
    load_index,
    load_metadata,
    search,
    build_context,
)

from llm import generate_answer


def main():

    print("Loading system...\n")

    model = load_model()

    index = load_index()

    metadata = load_metadata()

    print("System Ready!\n")

    while True:

        question = input("Ask a question (exit to quit): ")

        if question.lower() == "exit":
            break

        results = search(
            question,
            model,
            index,
            metadata
        )

        context = build_context(results)

        answer = generate_answer(
            context,
            question
        )

        print("\nAnswer\n")

        print(answer)

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
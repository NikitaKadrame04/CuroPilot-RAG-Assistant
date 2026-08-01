import streamlit as st

from src.retriever import (
    load_model,
    load_index,
    load_metadata,
    search,
    build_context,
)

from src.llm import generate_answer


@st.cache_resource
def initialize():

    model = load_model()

    index = load_index()

    metadata = load_metadata()

    return model, index, metadata


model, index, metadata = initialize()

st.set_page_config(
    page_title="CuroPilot AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CuroPilot Knowledge Assistant")

st.write(
    "Ask questions about CuroPilot using the knowledge collected from the official website."
)

question = st.text_input(
    "Enter your question"
)

if st.button("Ask"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching knowledge base..."):

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

        NOT_FOUND_MESSAGE = (
    "I couldn't find that information in the available CuroPilot knowledge base."
)

        if answer.strip() == NOT_FOUND_MESSAGE:

            st.error(answer)

        else:

            st.success("Answer")

            st.write(answer)

            with st.expander("Retrieved Context"):

                st.text(context)
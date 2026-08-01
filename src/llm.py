import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_NAME = "llama-3.1-8b-instant"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_prompt(context, question):
    """
    Build the prompt for the LLM.
    """

    prompt = f"""
You are a helpful AI assistant for CuroPilot.

Use ONLY the information provided in the context below.

Do NOT use outside knowledge.

If the answer cannot be found in the context, reply exactly:

"I couldn't find that information in the available CuroPilot knowledge base."

----------------------------

Context:

{context}

----------------------------

Question:

{question}

Answer:
"""

    return prompt


def generate_answer(context, question):

    prompt = build_prompt(context, question)

    completion = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0,

        max_tokens=500

    )

    return completion.choices[0].message.content.strip()
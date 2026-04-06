import re
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

MODEL = "gemini-2.5-flash"

chat = client.chats.create(model=MODEL)


def call_genai(prompt_text):

    response = chat.send_message(prompt_text)

    return response.text.strip()


def generate_question(topic, history):

    formatted_history = []

    for item in history:
        formatted_history.append(f"AI: {item['question']}")
        formatted_history.append(f"User: {item['answer']}")

    prompt_text = f"""
            You are a Socratic tutor guiding a user to understand a topic through questioning.

            Topic: {topic}

            Conversation so far:
            {chr(10).join(formatted_history)}

            Ask ONE question that deepens reasoning.

            Return ONLY:

            QUESTION: <question>
            END_SESSION: <YES or NO>
            """

    response = call_genai(prompt_text)

    question_match = re.search(
        r"QUESTION:\s*(.+?)\s*END_SESSION:",
        response,
        re.DOTALL
    )

    end_match = re.search(
        r"END_SESSION:\s*(YES|NO)",
        response
    )

    question = question_match.group(1).strip() if question_match else "Explain further."

    end = end_match.group(1) if end_match else "NO"

    return question, end


def evaluate_conversation(topic, history):

    formatted_history = []

    for item in history:
        formatted_history.append(f"AI: {item['question']}")
        formatted_history.append(f"User: {item['answer']}")

    prompt_text = f"""
        Evaluate the user's reasoning.

        Topic: {topic}

        Conversation:
        {chr(10).join(formatted_history)}

        Return:

        LOGICAL_CORRECTNESS: <number>
        DEPTH_OF_REASONING: <number>
        CONSISTENCY: <number>
        EVIDENCE_USE: <number>
        """

    response = call_genai(prompt_text)

    logic = re.search(r"LOGICAL_CORRECTNESS:\s*(\d+)", response)
    depth = re.search(r"DEPTH_OF_REASONING:\s*(\d+)", response)
    consistency = re.search(r"CONSISTENCY:\s*(\d+)", response)
    evidence = re.search(r"EVIDENCE_USE:\s*(\d+)", response)

    return {
        "Logical Correctness": logic.group(1) + "%" if logic else "0%",
        "Depth of Reasoning": depth.group(1) + "%" if depth else "0%",
        "Consistency": consistency.group(1) + "%" if consistency else "0%",
        "Use of Evidence": evidence.group(1) + "%" if evidence else "0%"
    }

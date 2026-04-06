from ai_engine.agent import generate_question, evaluate_conversation
from ai_engine.memory import Memory

memory = Memory()

topic_store = ""


def start_session(topic):

    global topic_store

    topic_store = topic

    question, end = generate_question(
        topic,
        memory.get_history()
    )

    return question, end


def submit_answer(question, answer):

    memory.add(question, answer)

    question, end = generate_question(
        topic_store,
        memory.get_history()
    )

    return question, end


def evaluate():

    return evaluate_conversation(
        topic_store,
        memory.get_history()
    )

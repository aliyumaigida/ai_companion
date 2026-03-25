from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.tutor_service import start_session, submit_answer, evaluate
from django.shortcuts import render


def home(request):

    return render(request, "index.html")

@api_view(["POST"])
def start(request):

    topic = request.data.get("topic")

    question, end = start_session(topic)

    return Response({
        "question": question,
        "end_session": end
    })


@api_view(["POST"])
def answer(request):

    question = request.data.get("question")

    answer = request.data.get("answer")

    q, end = submit_answer(question, answer)

    return Response({
        "question": q,
        "end_session": end
    })


@api_view(["GET"])
def evaluation(request):

    result = evaluate()

    return Response(result)

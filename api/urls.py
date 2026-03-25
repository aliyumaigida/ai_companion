from django.urls import path
from .views import start, answer, evaluation

urlpatterns = [

    path("start/", start),

    path("answer/", answer),

    path("evaluate/", evaluation)

]
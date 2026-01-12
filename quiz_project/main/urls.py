from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("quiz/create/", views.create_quiz, name="create_quiz"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/question/add/", views.add_question, name="add_question"),
    path("quiz/<int:quiz_id>/publish/", views.quiz_publish, name="quiz_publish"),
    path("my-quizzes/", views.my_quizzes, name="my_quizzes"),
    path("quiz/<int:quiz_id>/edit/", views.quiz_edit, name="quiz_edit"),
    path("quiz/<int:quiz_id>/delete/", views.quiz_delete, name="quiz_delete"),
    path("quiz/<int:quiz_id>/add-image/", views.quiz_add_image, name="quiz_add_image"),

]

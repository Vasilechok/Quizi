from django.urls import path
from . import views
from django.urls import re_path
from . import consumers

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path("quiz/create/", views.create_quiz, name="create_quiz"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/question/add/", views.add_question, name="add_question"),
    path("quiz/<int:quiz_id>/publish/", views.quiz_publish, name="quiz_publish"),
    path("my-quizzes/", views.my_quizzes, name="my_quizzes"),
    path("quiz/<int:quiz_id>/edit/", views.quiz_edit, name="quiz_edit"),
    path("quiz/<int:quiz_id>/delete/", views.quiz_delete, name="quiz_delete"),
    path("quiz/<int:quiz_id>/add-image/", views.quiz_add_image, name="quiz_add_image"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/start/", views.quiz_start, name="quiz_start"),
    path("quiz/<int:quiz_id>/question/", views.quiz_question, name="quiz_question"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path("join/", views.join_by_code, name="join_by_code"),  
    path('session/create/<int:quiz_id>/', views.create_session, name='create_session'),
    path("session/<str:code>/",views.session_lobby,name="session_lobby"),
    path("session/<str:code>/start/", views.start_session, name="start_session"),
    path("session/<str:code>/question/",views.session_question,name="session_question"),
   
]

websocket_urlpatterns = [
    re_path(r"ws/session/(?P<code>\w+)/$", consumers.SessionConsumer.as_asgi()),
]
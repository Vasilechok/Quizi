from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer, SessionPlayer, QuizSession
from .forms import QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
import random
import string
from django.utils import timezone
from datetime import timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
def create_quiz(request):
    quiz = None 
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()

            return redirect("quiz_detail", quiz_id=quiz.id)
            
    else:
        form = QuizForm()

    return render(request, 'main/create_quiz.html', {'form': form, 'quiz': quiz})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    questions = quiz.questions.all()

    return render(request, "main/quiz_detail.html", {
        "quiz": quiz,
        "questions": questions
    })


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            # 1. Створюємо питання
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

           
            correct = request.POST.get("correct")  

            # 3. Створюємо відповіді
            for i in range(1, 5):
                answer_text = request.POST.get(f"answer_{i}")

                if answer_text:  
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=(str(i) == correct)
                    )

            return redirect("home") 

    else:
        form = QuestionForm()

    return render(request, "main/add_question.html", {
        "form": form,
        "quiz": quiz
    })

    
@login_required
def quiz_publish(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if quiz.questions.count() < 2:
        messages.error(request, "У квізі має бути щонайменше 2 питання.")
        return redirect('quiz_detail', quiz_id=quiz.id)

    quiz.is_published = True
    quiz.save()
    return redirect('home')



@login_required
def my_quizzes(request):
    quizzes = Quiz.objects.filter(author=request.user)

    return render(request, "main/my_quizzes.html", {
        "quizzes": quizzes
    })


@login_required
def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Квіз оновлено")
            return redirect("my_quizzes")
    else:
        form = QuizForm(instance=quiz)

    return render(request, "main/quiz_edit.html", {
        "form": form,
        "quiz": quiz
    })


@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if request.method == "POST":
        quiz.delete()
        messages.success(request, "Квіз видалено")
        return redirect("my_quizzes")

    return render(request, "main/quiz_delete.html", {
        "quiz": quiz
    })

@login_required
def quiz_add_image(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if request.method == "POST":
        quiz.image = request.FILES.get("image")
        quiz.save()
        return redirect("quiz_detail", quiz_id=quiz.id)

    return render(request, "main/quiz_add_image.html", {"quiz": quiz})


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.exclude(author=request.user)
    return render(request, "main/quiz_list.html", {"quizzes": quizzes})

@login_required
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    request.session["quiz_id"] = quiz.id
    request.session["question_index"] = 0
    request.session["score"] = 0

    return redirect("quiz_question", quiz_id=quiz.id)



@login_required
def quiz_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())

    index = request.session.get("question_index", 0)

    if index >= len(questions):
        return redirect("quiz_result", quiz_id=quiz.id)

    question = questions[index]

    if request.method == "POST":
        selected = request.POST.get("answer")

        if selected.strip().lower() == question.correct_answer.strip().lower():
            request.session["score"] += 1

        request.session["question_index"] += 1
        return redirect("quiz_question", quiz_id=quiz.id)

    return render(request, "main/quiz_question.html", {
        "quiz": quiz,
        "question": question,
        "index": index + 1,
        "total": len(questions)
    })




@login_required
def quiz_result(request, quiz_id):
    score = request.session.get("score", 0)
    request.session.flush()

    return render(request, "main/quiz_result.html", {"score": score})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # одразу логінимо
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})



def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) 

code = generate_code()

@login_required
def create_session(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    session = QuizSession.objects.create(
        quiz=quiz,
        host=request.user,
        code=generate_code()
    )

    SessionPlayer.objects.create(
        session=session,
        user=request.user
    )

    return redirect("session_lobby", session.code)

@login_required
def join_by_code(request):
    code = request.POST.get("code")
    session = get_object_or_404(QuizSession, code=code)

    SessionPlayer.objects.get_or_create(
        session=session,
        user=request.user
    )

    return redirect("session_lobby", code)\
    
@login_required
def session_lobby(request, code):
    session = get_object_or_404(QuizSession, code=code)

    return render(request, "main/session_lobby.html", {
        "session": session,
    })

from django.utils import timezone

@login_required
def start_session(request, code):
    session = get_object_or_404(QuizSession, code=code)

    if request.user == session.host:
    
        session.started = True
        session.current_question = 0
        session.question_started_at = timezone.now()
        session.save()

       
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"session_{code}",
            {
                "type": "start_game"
            }
        )

    return redirect('session_question', code=code)

QUESTION_TIME = 15  # секунд

@login_required
def session_question(request, code):
    session = get_object_or_404(QuizSession, code=code)

    questions = list(session.quiz.questions.order_by("order"))
    total = len(questions)

    
    if session.current_question >= total:
        return redirect("quiz_result", session.quiz.id)

    question = questions[session.current_question]


    now = timezone.now()
    if session.question_started_at:
        elapsed = (now - session.question_started_at).total_seconds()
        if elapsed >= QUESTION_TIME:
            session.current_question += 1
            session.question_started_at = timezone.now()
            session.save()
            return redirect("session_question", code=code)

    
    if request.method == "POST":
        selected = request.POST.get("answer")

        if selected.strip().lower() == question.correct_answer.strip().lower():
            
            request.session["score"] += 1

        session.current_question += 1
        session.question_started_at = timezone.now()
        session.save()

        return redirect("session_question", code=code)

    remaining = QUESTION_TIME - int(
        (now - session.question_started_at).total_seconds()
    )

    return render(request, "main/session_question.html", {
        "session": session,
        "question": question,
        "remaining": max(0, remaining),
        "index": session.current_question + 1,
        "total": total,
    })


def submit_quiz(request, session_id):
    score = 0

    for question in session.quiz.questions.all():
        key = f"question_{question.id}"
        answer_id = request.POST.get(key)

        print(key, answer_id)  # DEBUG

        if not answer_id:
            continue

        answer = Answer.objects.get(id=answer_id)

        print("-> is_correct:", answer.is_correct)

        if answer.is_correct:
            score += 1

    return render(request, "quiz/result.html", {
        "score": score
    })

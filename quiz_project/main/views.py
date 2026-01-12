from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():

            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

            correct = request.POST.get("correct")


            for i in range(1, 5):
                text = request.POST.get(f"answer_{i}")
                if text:
                    Answer.objects.create(
                        question=question,
                        text=text,
                        is_correct=(str(i) == correct)
                    )

            return redirect("quiz_detail", quiz_id=quiz.id)

    else:
        form = QuestionForm()

    return render(request, "main/add_question.html", {
        "quiz": quiz,
        "form": form
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

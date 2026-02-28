from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="quiz_images/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    correct_answer = models.CharField(
        max_length=255,
        help_text="Правильна відповідь (тимчасово як текст)"
    )

    def __str__(self):
        return self.text



class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='results'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} – {self.quiz}'





class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    current_question = models.PositiveIntegerField(default=0)
    question_started_at = models.DateTimeField(null=True, blank=True)

    started = models.BooleanField(default=False)



class SessionPlayer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name="players")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

from django import forms
from .models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_published']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]


class AnswerForm(forms.Form):
    answer_1 = forms.CharField(label="Відповідь 1")
    answer_2 = forms.CharField(label="Відповідь 2")
    answer_3 = forms.CharField(label="Відповідь 3", required=False)
    answer_4 = forms.CharField(label="Відповідь 4", required=False)

    correct = forms.ChoiceField(
        choices=[
            ("1", "Відповідь 1"),
            ("2", "Відповідь 2"),
            ("3", "Відповідь 3"),
            ("4", "Відповідь 4"),
        ],
        widget=forms.RadioSelect,
        label="Правильна відповідь"
    )
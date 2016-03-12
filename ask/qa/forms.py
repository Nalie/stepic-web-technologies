# -*- coding: utf-8 -*-
from django import forms
from models import Question, Answer


# AskForm - форма добавления вопроса
# title - поле заголовка
# text - поле текста вопроса


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    # def clean(self):

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question


# AnswerForm - форма добавления ответа
# text - поле текста ответа
# question - поле для связи с вопросом
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Ответ')
    question = forms.IntegerField()

    # def clean(self):

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

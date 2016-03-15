# -*- coding: utf-8 -*-
from django import forms
from models import Question, Answer, User


# AskForm - форма добавления вопроса
# title - поле заголовка
# text - поле текста вопроса


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def get_url(self):
        return '/qa/ask/'
    # def clean(self):

    def save(self):
        question = Question(**self.cleaned_data)
        question.author = self._user
        question.save()
        return question


# AnswerForm - форма добавления ответа
# text - поле текста ответа
# question - поле для связи с вопросом
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Ответ')
    question = forms.IntegerField()

    def get_url(self):
        return '/qa/answer/'
    # def clean(self):

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True)
    email = forms.EmailField(label='E-mail')

    def get_url(self):
        return '/qa/signup/'

    def save(self):
        from utils import make_password
        user = User(**self.cleaned_data)
        user.password = make_password(user.password)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True)

    def get_url(self):
        return '/qa/login/'

    def __unicode__(self):
        return self.cleaned_data + "  " + self._user

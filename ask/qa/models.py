# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()

    def __unicode__(self):
        return self.username + self.email + self.password


class Session(models.Model):
    key = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey(User)
    expires = models.DateTimeField()


# Question - вопрос
# title - заголовок вопроса
# text - полный текст вопроса
# added_at - дата добавления вопроса
# rating - рейтинг вопроса (число)
# author - автор вопроса
# likes - список пользователей, поставивших "лайк"
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=False, default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='questions_set')
    likes = models.ManyToManyField(User, related_name='likes_set')

    def __unicode__(self):
        return self.title

    def get_url(self):
        return '/question/%d/' % self.pk

    class Meta:
        # db_table = 'blogposts'
        ordering = ['-added_at']


# Answer - ответ
# text - текст ответа
# added_at - дата добавления ответа
# question - вопрос, к которому относится ответ
# author - автор ответа
class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.text

    def get_url(self):
        return '/question/%d/' % self.question_id

    class Meta:
        # db_table = 'blogposts'
        ordering = ['-added_at']

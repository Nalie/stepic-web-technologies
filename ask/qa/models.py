# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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
    added_at = models.DateTimeField()
    rating = models.IntegerField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='questions_set')
    likes = models.ManyToManyField(User, related_name='likes_set')
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return '/post/%d/' % self.pk
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
    added_at = models.DateTimeField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return self.text
    def get_absolute_url(self):
        return '/post/%d/' % self.pk
    class Meta:
        # db_table = 'blogposts'
        ordering = ['-added_at']

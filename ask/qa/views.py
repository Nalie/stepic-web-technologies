# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator, EmptyPage
from models import Question
from forms import AskForm, AnswerForm, SignupForm, LoginForm
from utils import do_login
from django.db.models import Count


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator


@require_GET
def home(request):
    page, paginator = paginate(request=request, qs=Question.objects.order_by('-pk').all())  # Page
    paginator.baseurl = '/?page='
    return render(request, 'qa/home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


@require_GET
def popular(request):
    page, paginator = paginate(request=request, qs=Question.objects.annotate(likes_count=Count('likes')).order_by(
        '-likes_count').all())  # Page
    paginator.baseurl = '/popular/?page='
    return render(request, 'qa/home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def question(request, pk):
    if request.method is 'POST':
        return answer(request)
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': pk})
    return render(request, 'qa/question.html', {
        'question': question,
        'form': form,
    })


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {
        'form': form,
    })


@require_POST
def answer(request):
    form = AnswerForm(request.POST)
    question = get_object_or_404(Question, pk=form.question_id)
    if form.is_valid():
        form._user = request.user
        answer = form.save()
        url = answer.get_url()
        return HttpResponseRedirect(url)
    return render(request, 'qa/question.html', {
        'question': question,
        'form': form,
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            request.path = "/login/"
            return login(request)
    else:
        form = SignupForm()
    return render(request, 'qa/signup.html', {
        'form': form,
    })


def login(request):
    error = ''
    if request.method == 'POST':
        print request
        form = LoginForm(request)
        print form
        if form.is_valid():
            print 'valid'
            url = request.POST.get('continue', '/')
            print url
            session = do_login(form.cleaned_data['login'], form.cleaned_data['password'])
            if session is not None:
                response = HttpResponseRedirect(url)
                response.set_cookie('sessid', session.key, httponly=True,
                                expires=session.expires,
                                )
                return response
        else:
            error = u'Неверный логин / пароль'
    else:
        form = LoginForm()
    return render(request, 'qa/login.html', {'error': error, 'form': form})

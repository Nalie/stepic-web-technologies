from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator, EmptyPage
from models import Question
from forms import AskForm, AnswerForm
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
        answer = form.save()
        url = answer.get_url()
        return HttpResponseRedirect(url)
    return render(request, 'qa/question.html', {
        'question': question,
        'form': form,
    })

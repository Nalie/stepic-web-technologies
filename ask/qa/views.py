from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from models import Question


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
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator


@require_GET
def home(request):
    page, paginator = paginate(request=request, qs=Question.objects.order_by('-added_at').all())  # Page
    paginator.baseurl = '/?page='
    return render(request, 'qa/home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


@require_GET
def popular(request):
    page, paginator = paginate(request=request, qs=Question.objects.order_by('-likes__count').all())  # Page
    paginator.baseurl = '/popular/?page='
    return render(request, 'qa/home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


@require_GET
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'qa/question.html', {
        'question': question,
    })

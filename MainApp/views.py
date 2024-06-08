from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from MainApp.models import Snippet

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snipppets = Snippet.objects.all()
    context = {
                'pagename': 'Просмотр сниппетов',
                'snippets': snipppets
               }
    return render(request, 'pages/view_snippets.html', context)

def snippet_view(request,snippetid):
    try:
        snipppet = Snippet.objects.get(id=snippetid)
    except Exception:
        return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
    else:
        context = {
                    'pagename': "Просмотр Сниппета",
                    'snippet': snipppet
                }
        return render(request, 'pages/view_snippet.html', context)
    
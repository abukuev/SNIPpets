from django.http import Http404, HttpResponseNotFound ,HttpResponse
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm
from django.core.exceptions import ObjectDoesNotExist

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method=='GET':
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                'form':form,
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method =="POST":
            form = SnippetForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("add_sn")
            return render(request, "pages/add_snippet.html", {'form':form})

# def snippets_create(request):

#     if request.method =="POST":
#             form = SnippetForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect("add_sn")
#             return render(request, "pages/add_snippet.html", {'form':form})
    
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
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
    else:
        context = {
                    'pagename': "Просмотр Сниппета",
                    'snippet': snipppet
                }
        return render(request, 'pages/view_snippet.html', context)
    
def snippets_edit(request,snippetid):
    return HttpResponseNotFound()

def snippets_del(request,snippetid):
    try:
        snipppet = Snippet.objects.get(id=snippetid)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
    else: 
        snipppet.delete()
        return redirect("view_sn")
from django.http import Http404, HttpResponseNotFound ,HttpResponse
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm , UserRegistrationForm , CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        redirect_url = request.POST.get("redirect_url")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
        if redirect_url: return redirect(redirect_url)
        else: return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')

def create_user(request):
    context = {'pagename': 'Регистрация нового пользователя'}
    # Создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    
    # Получаем данные из формы и на их основе создаем новый snippet В БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request, "pages/registration.html", context)

def index_page(request):
    print(request.GET.get('next', ''))
    context = {'pagename': 'PythonBin',
               'redirect_url':request.GET.get('next', '')}
    return render(request, 'pages/index.html', context)

@login_required(login_url='/')
def add_snippet_page(request):
    if request.method=='GET':
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                'form':form,
                'operation':'create',
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method =="POST":
            form = SnippetForm(request.POST)
            if form.is_valid():
                snipped = form.save(commit=False)
                if request.user.is_authenticated:
                    snipped.user= request.user
                    snipped.save()
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
    query = Q(public=True)
    if request.user.is_authenticated:
        query.add(Q(user=request.user), Q.OR)

    snippets = Snippet.objects.filter(query)
    print(snippets)
    context = {
                'pagename': 'Просмотр сниппетов',
                'snippets':snippets,
                'count': snippets.count(),
               }
    return render(request, 'pages/view_snippets.html', context)
@login_required(login_url='/')
def snippets_my(request):

    snippets = Snippet.objects.filter(user_id=request.user)

    context = {
                'pagename': 'Мои сниппеты',
                'snippets':snippets,
                'count':snippets.count(),
               }
    return render(request, 'pages/view_snippets.html', context)

def snippet_view(request,snippetid):
    try:
        snippet = Snippet.objects.get(id=snippetid)
        commentform = CommentForm()
        if snippet.user==request.user: isuser=True
        else: isuser=False
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
    else:
        context = {
                    'pagename': "Просмотр Сниппета",
                    'snippet':snippet,
                    'ismy':isuser,
                    'comment_form':commentform,
                }
        return render(request, 'pages/view_snippet.html', context)
    
@login_required(login_url='/')
def snippets_edit(request,snippetid):
    if request.method=='GET':
        try:
            snippet = Snippet.objects.get(id=snippetid)
            form = SnippetForm(instance=snippet)
            if snippet.user==request.user:
                
                operation = 'edit'
            else:
                
                operation='permission_denied'
            
        except ObjectDoesNotExist:
            return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
        else:
            context = {
                        'pagename': "Редактирование Сниппета",
                        'form': form,
                        'snippetid':snippetid,
                        'operation':operation,
                    }
            
            return render(request, 'pages/add_snippet.html', context)

    if request.method=='POST':
        data  = request.POST
        snippet = Snippet.objects.get(id=snippetid)
        snippet.name = data['name']
        snippet.lang = data['lang']
        snippet.code = data['code']
        
        if 'public' in data.keys():
            if data['public']=='on':
                snippet.public = data.get('public',False)
        else:
            snippet.public = False
        snippet.save()
        return redirect("edit_sn",snippetid)
@login_required(login_url='/')
def snippets_del(request,snippetid):
    try:
        snipppet = Snippet.objects.get(id=snippetid)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snipped ID= {snippetid} not found")
    else: 
        if snipppet.user==request.user:
            snipppet.delete()
        return redirect("view_sn")

@login_required(login_url='/')
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippetid = request.POST.get('snippetid')
        print(snippetid)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippetid)
            comment.save()
            return redirect('get_sn',snippetid=snippetid)
        raise Http404

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
# Create your views here.


def index(request):
    context = {
        "numbers":[1,2,3,4,5],
    }
    return render(request, "index.html", context)

def about(request):
    return render(request, "about.html")

def article(request):
    count = 0
    keyword = request.GET.get('keyword')
    if keyword:
        article = Article.objects.filter(title__contains = keyword)
        return render(request, "article.html",{"article":article})
    article = Article.objects.all()
    for art in article:
        count += 1
    return render(request, "article.html",{"article":article,"count":count})

@login_required(login_url="user:login")
def dashboard(request):
    count = 0
    article = Article.objects.filter(author=request.user)

    for art in article:
        count+=1
    
    context = {
        "article":article,
        "count":count,  
    }
    return render(request, "User/dashboard.html", context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "New Article Successfully added. Thank You "+request.user.username)
        return redirect("article:dashboard")
    return render(request, "User/addarticle.html",{"form":form})

@login_required(login_url="user:login")
def update(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if form.is_valid():
        article.author = request.user
        article.save()
        messages.success(request, "Article Successfully updated. Thank You "+request.user.username)
        return redirect("article:dashboard")
    return render(request, "User/update.html",{"form": form})

@login_required(login_url="user:login")
def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.info(request,"Makale silindi.")
    return redirect("article:dashboard")


def addcomment(request, id):
    article = get_object_or_404(Article, id = id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author= comment_author, comment_content=comment_content)
        newComment.article = article
        newComment.save()
        return redirect(reverse("article:detail", kwargs={"id":id}))
    return redirect(reverse("article:detail", kwargs={"id":id}))

def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()

    return render(request, "User/detail.html", {"article":article,"comments":comments})
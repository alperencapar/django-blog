from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (User, Article, Category)
from .forms import (ArticleForm)
# from django.http import Http404

def home(request):
    articles = Article.objects.active_articles().all()
    categories = Category.objects.all()

    if request.user.id:
        user_is_author = User.objects.get(id = request.user.id).is_author
    else:
        user_is_author = None

    context = {
        "articles": articles,
        "categories": categories,
        "user_is_author": user_is_author,
    }
    return render(request, "blog/home.html", context)

def article_detail(request, slug):
    article = get_object_or_404(Article.objects.active_articles(), slug=slug)

    context = {
        "article": article
    }
    return render(request, "blog/article_detail.html", context)


def category_articles(request, category_name):
    articles = Article.objects.search_category(category_name).all()

    context = {
        "articles": articles
    }
    return render(request, "blog/category_articles.html", context)


@login_required()
def create_article(request):
    article_form = ArticleForm(request.POST or None, request.FILES)

    if request.method == "POST" and article_form.is_valid():
        new_article = article_form.save(commit=False)
        user = request.user
        new_article.author = user
        article_form.save()
        new_article.save()
        return redirect("article_detail", new_article.slug)
    context = {
        "form": article_form,
    }
    return render(request, "blog/article_create.html", context)


@login_required()
def update_article(request, slug):
    article = get_object_or_404(Article.objects.active_articles(), slug=slug)
    form = ArticleForm(request.POST or None, instance=article)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect("article_detail", article.slug)
    
    context = {
        "form": form
    }
    return render(request, "blog/article_create.html", context)
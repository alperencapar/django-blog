from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import (Article, Category)
# from django.http import Http404

def home(request):
    articles = Article.objects.active_articles().all()
    categories = Category.objects.all()

    context = {
        "articles": articles,
        "categories": categories,
        
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
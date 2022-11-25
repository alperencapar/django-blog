from django.urls import path, include
from .views import (
    home,
    article_detail,
    categories_home,
    category_articles,
    create_article,
    update_article,
)

urlpatterns = [
    path('',home, name="blog-home"),
    path('article/<slug:slug>/',article_detail, name="article_detail"),
    path('create-article/',create_article, name="article_create"),
    path('update-article/<slug:slug>',update_article, name="article_update"),
    path('category/',categories_home, name="categories_home"),
    path('category/<slug:category_name>/',category_articles, name="category_detail"),
]

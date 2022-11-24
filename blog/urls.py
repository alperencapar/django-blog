from django.urls import path, include
from .views import (
    home,
    article_detail,
    category_articles
)

urlpatterns = [
    path('',home, name="blog-home"),
    path('article/<slug:slug>/',article_detail, name="article_detail"),
    # path('categories/',article_detail, name="article_detail"),
    path('category/<slug:category_name>/',category_articles, name="article_detail"),
]

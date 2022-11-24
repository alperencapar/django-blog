from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse

from tinymce.models import HTMLField

from .utils import (image_name_path_handler, slugify_title, handle_published_date)


class User(AbstractUser):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    img = models.ImageField(upload_to=image_name_path_handler, null=True, blank=True, verbose_name="User Profile Image")
    is_author = models.BooleanField(default=False)


class AuthorManagerActive(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_author=True)

class Author(User):
    active = AuthorManagerActive()
    class Meta:
        proxy = True


class ModelTrack(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Category(ModelTrack):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to=image_name_path_handler, null=True, blank=True, verbose_name="Category Image")

    def get_absolute_url(self):
        category_name_slug = slugify(self.name)
        return reverse("category_detail", kwargs={"category_name": category_name_slug})

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name[:70]


class Tag(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"


class ArticleQuerySet(models.QuerySet):
    def get_active_articles(self, query=None):
        # Article.objects.all().get_active_articles()
        # Article.objects.all().get_active_articles("101")
        if query is None or query == "":
            return self.filter(is_active=True)
        lookup = Q(is_active=True) & Q(title__icontains=query) | Q(body__icontains=query) | Q(categories__icontains=query)
        return self.filter(lookup)

    def get_category_articles(self, query=None):
        if query is None or query == "":
            return self.none
        category_name = query.replace("-", " ")
        lookup = Q(is_active=True) & Q(categories__name__icontains=category_name)
        return self.filter(lookup)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    
    def active_articles(self, query=None):
        # Article.objects.active_articles()
        # Article.objects.active_articles("searh query")
        return self.get_queryset().get_active_articles(query=query)

    def search_category(self, query=None):
        return self.get_queryset().get_category_articles(query=query)

class Article(ModelTrack):
    title = models.CharField(max_length=500, blank=False, null=False)
    body = HTMLField()
    slug = models.SlugField(max_length=700, unique=True, editable=False, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="author")
    categories = models.ManyToManyField(Category, blank=True, related_name="categories")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    auto_publish_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    img = models.ImageField(upload_to=image_name_path_handler, null=True, blank=True, verbose_name="Article Image")
    objects=ArticleManager()

    class Meta:
        verbose_name = "Makale"
        verbose_name_plural = "Makaleler"
        ordering = ['-created', '-updated']

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

    def get_categories(self):
        return " - ".join([category.name for category in self.categories.all()])

    def __str__(self):
        return self.title[:50]

def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_title(instance, save=False)
    handle_published_date(instance)

def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_title(instance, save=True)

pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)

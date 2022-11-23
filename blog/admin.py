from django.contrib import admin
from .models import (User, Category, Tag, Article)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_author', 'is_staff', 'is_superuser']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']
    exclude = ["password"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_links = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # list_display = ['title', 'author', 'get_categories', 'slug', 'is_active', 'publish_date']
    list_display = ['title', 'author', 'slug', 'is_active', 'publish_date']
    list_filter = ['categories', 'is_active', 'created', 'updated']
    search_fields = ['title']
    ordering = ['-created', '-updated']

    actions = ["make_publish", "make_unpublish"]

    def make_publish(self, request, queryset):
        queryset.update(is_active=True)
    make_publish.short_description = "Yayınla"

    def make_unpublish(self, request, queryset):
        queryset.update(is_active=False)
    make_unpublish.short_description = "Yayından kaldır"



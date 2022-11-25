from django import forms
from .models import (Article)
from tinymce.widgets import TinyMCE


class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Article
        fields = "__all__"
        exclude = ["slug", "author", "published_date", "auto_publish_date"]
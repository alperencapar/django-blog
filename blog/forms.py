from django import forms
from .models import (Article)
from django_ckeditor_5.widgets import CKEditor5Widget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ["slug", "author", "published_date", "auto_publish_date"]
        widgets = {
              "body": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )
          }

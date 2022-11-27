from django import forms
from .models import (Article)
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ["slug", "author", "auto_publish_date"]
        # widgets = {
        #       "body": CKEditorUploadingWidget()
        #   }

from django.shortcuts import render
from django.http.response import HttpResponse

def home(request):
    # return render(request, "")
    return HttpResponse("HomePage")

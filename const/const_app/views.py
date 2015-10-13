from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'const/index.html', context)

def asd(request):
    context = {}
    return render(request, 'const/index2.html', context)

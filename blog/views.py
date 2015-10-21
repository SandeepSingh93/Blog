from django.shortcuts import render
from django.http import HttpResponseRedirect
from blog.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages


def create_user(request):
    if request.method=="POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Signup success!! Now You can login from the login panel.')
            return HttpResponseRedirect('/public')
    else:
        form= UserCreationForm()
    return render(request, 'login.html',{'form':form} )

def login(request):
    if request.method=="POST":
        form=AuthenticationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/home')
    form= AuthenticationForm()
    return  render(request, 'login.html', {'form':form})

@login_required
def create_article(request):
    if request.method=="POST":
        form= article_form(request.POST)
        if form.is_valid():
            article= form.save(commit=False)
            article.owner = request.user
            article.save()
            return HttpResponseRedirect('/home')
    form= article_form()
    return render(request, 'create_article.html', {'form':form})

def public_feed(request):
    feeds= Article.objects.all()
    return render(request, 'public_feed.html',{'feeds':feeds})

@login_required
def home_feed(request):
    user= request.user
    feeds= Article.objects.filter(owner= user)
    if not feeds:
        messages.add_message(request, messages.INFO,"No Articles published by current logged in user! "
                                                    "Create new Article from above panel.")
        return render(request, 'home.html')
    else:
        return render(request, 'home.html', {'feeds':feeds})


def show_article(request, pk):
    article= Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article':article})


def create_comment(request):
    pass
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
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
def create_edit_article(request, id=None):
    if id:
        article = get_object_or_404(Article, pk=id)
        if article.owner != request.user:
            return HttpResponseForbidden()
    else:
        article = Article(owner=request.user)

    if request.method=="POST":
        form= article_form(request.POST,instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home')
    form= article_form(instance=article)
    return render(request, 'create_article.html', {'form':form})


def public_feed(request):
    feeds= Article.objects.all()
    if not feeds:
        messages.add_message(request, messages.INFO,"No Articles published yet! "
                                                    "Create one from above panel.")
        return render(request, 'public_feed.html')
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
    if request.method == "POST":
        form = comment_form(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user= request.user
            article= Article.objects.get(pk=pk)
            article.comment_count+=1
            article.save()
            temp.article= article
            parent = form['parent'].value()

            if parent == '':
                temp.path = []
                temp.save()
                temp.path = [temp.id]
            else:
                node = Comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path
                temp.save()
                temp.path.append(temp.id)

            temp.save()
    form= comment_form()
    article= Article.objects.get(pk=pk)
    comment_tree = Comment.objects.filter(article=pk).order_by('path')
    return render(request, 'article.html', locals())


@login_required
def delete_article(request,id=None):
    if id:
        article = get_object_or_404(Article, pk=id)
        if article.owner != request.user:
            return HttpResponseForbidden()
        else:
            article.delete()
            return HttpResponseRedirect('/home')




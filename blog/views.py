from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from blog.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DeleteView, UpdateView, CreateView


class PublicFeedView(ListView):
    model = Article
    template_name = 'public_feed.html'


class HomeFeedView(ListView):
    model = Article
    template_name = 'home.html'

    def get_queryset(self):
        feeds = Article.objects.filter(owner= self.request.user)
        if not feeds:
            messages.add_message(self.request, messages.INFO,"No Articles published by current logged in user! "
                                                    "Create new Article from above panel.")
        return feeds

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeFeedView, self).dispatch(*args, **kwargs)


class DeleteArticleView(DeleteView):
    success_url = '/home'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        if article.owner != self.request.user:
            return HttpResponseForbidden()
        else:
            return article

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteArticleView, self).dispatch(*args, **kwargs)


class CreateArticleView(CreateView):
    model = Article
    form_class = article_form
    template_name = 'create_article.html'
    success_url = '/home'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner= self.request.user
        return super(CreateArticleView, self).form_valid(form)


class EditArticleView(UpdateView):
    model = Article
    form_class = article_form
    template_name = 'create_article.html'

    def get_success_url(self):
        url= '/article/' + str(self.kwargs['pk'])
        return url

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        if article.owner != self.request.user:
            return HttpResponseForbidden()
        else:
            return article

    def get(self, request, *args, **kwargs):
        self.object= self.get_object()
        form_class= self.get_form_class()
        form= self.get_form(form_class)
        context= self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditArticleView, self).dispatch(*args, **kwargs)


class CreateUserView(CreateView):
    template_name = 'login.html'
    success_url = '/'
    model = User
    form_class = UserCreationForm


# def create_user(request):
#     if request.method=="POST":
#         form= UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, 'Signup success!! Now You can login from the login panel.')
#             return HttpResponseRedirect('/public')
#     else:
#         form= UserCreationForm()
#     return render(request, 'login.html',{'form':form} )


# def login(request):
#     if request.method=="POST":
#         form=AuthenticationForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/home')
#     form= AuthenticationForm()
#     return  render(request, 'login.html', {'form':form})


# @login_required
# def create_edit_article(request, id=None):
#     if id:
#         article = get_object_or_404(Article, pk=id)
#         if article.owner != request.user:
#             return HttpResponseForbidden()
#     else:
#         article = Article(owner=request.user)
#
#     if request.method=="POST":
#         form= article_form(request.POST,instance=article)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/home')
#     form= article_form(instance=article)
#     return render(request, 'create_article.html', {'form':form})
#

# def public_feed(request):
#     feeds= Article.objects.all()
#     if not feeds:
#         messages.add_message(request, messages.INFO,"No Articles published yet! "
#                                                     "Create one from above panel.")
#         return render(request, 'public_feed.html')
#     return render(request, 'public_feed.html',{'feeds':feeds})
#
#
# @login_required
# def home_feed(request):
#     user= request.user
#     feeds= Article.objects.filter(owner= user)
#     if not feeds:
#         messages.add_message(request, messages.INFO,"No Articles published by current logged in user! "
#                                                     "Create new Article from above panel.")
#         return render(request, 'home.html')
#     else:
#         return render(request, 'home.html', {'feeds':feeds})


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


# @login_required
# def delete_article(request,id=None):
#     if id:
#         article = get_object_or_404(Article, pk=id)
#         if article.owner != request.user:
#             return HttpResponseForbidden()
#         else:
#             article.delete()
#             return HttpResponseRedirect('/home')




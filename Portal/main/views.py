from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
#from Portal.account import models
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required


def base (request):
    return render(request, 'main/main.html')


def about (request):
    return render(request, 'main/about.html')


def index (request):
    return render(request, 'main/index.html')


def contacts (request):
    return render(request, 'main/contacts.html')


def mynews (request):
    return render(request, 'main/mynews.html')


def news (request):
    return render(request, 'main/news.html')


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/details.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = Comment()
        return context


class BaseCommentView:
    model = Comment

    def get_success_url(self):
        post = models.PostModel.objects.get(pk=self.object.post.pk)
        return reverse(
            "blog:post_page",
            kwargs={"category_slug": post.category.slug, "slug": post.slug},
        )

class AddCommentView(BaseCommentView, CreateView):
    form_class = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = models.PostModel.objects.get(pk=self.kwargs.get("pk"))
        return super().form_valid(form)

class EditCommentView(BaseCommentView, UpdateView):
    form_class = Comment
    template_name = "blog/comment_edit.html"


class DeleteCommentView(BaseCommentView, DeleteView):
    template_name = "blog/comment_delete.html"

class PostCreate( PermissionRequiredMixin, CreateView ):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'edit_news.html'



class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post')
    form_class = PostForm
    model = Post
    template_name = 'edit_news.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post')
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('post_list')


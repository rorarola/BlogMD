from django.shortcuts import render
from .models import Category, Post
from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import PostForm

# Create your views here.
def index(request):
    context = {
        'categories': Category.objects.all(),
        # 'posts': Post.objects.all(),
    }
    return render(request, 'index.html', context=context)

def postDetail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'categories': Category.objects.all(),
        'post': post,
    }
    return render(request, 'post_detail.html', context=context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = str(request.user)
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')

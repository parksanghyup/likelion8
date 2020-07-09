from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html', {'posts':posts})


def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'post/detail.html', {'post':post})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('detail', id=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/edit_form.html', {'form':form})

def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid(): 
            post = form.save(commit = False)
            post.save()
            return redirect('detail', id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/edit_form.html', {'form':form})    

def post_delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('index')
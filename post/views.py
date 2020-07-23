from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

def index(request):
    categories = Category.objects.all()
    
    cate = request.GET.get('category','')

    if cate == '':
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(category=cate)

    return render(request, 'post/index.html', {'posts':posts,'categories':categories})


def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    commentForm = CommentForm()
    return render(request, 'post/detail.html', {'post':post,'commentForm':commentForm})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('detail', id=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {'form':form})

def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): 
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.category = form.cleaned_data['category']
            post.save()
            return redirect('detail', id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/edit_form.html', {'form':form, 'post':post})

def post_delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('index')


def comment_new(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=post_id)
            comment.save()
            return redirect('detail', id=post_id)
    else:
        return redirect('index')
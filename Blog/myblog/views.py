from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm, CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    query = request.GET.get('q')
    author = request.GET.get('author')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    posts = Post.objects.all().order_by('-created_date')
    users = User.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
    if author:
        posts = posts.filter(author__username=author)
    if start_date:
        posts = posts.filter(published_date__gte=parse_date(start_date))
    if end_date:
        posts = posts.filter(published_date__lte=parse_date(end_date))

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myblog/index.html', {
        'page': page,
        'users': users
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myblog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myblog/post_edit.html', {'form': form, 'post': None})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myblog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'myblog/post_confirm_delete.html', {'post': post})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myblog/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'myblog/login.html'
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request, 'myblog/my_posts.html', {'posts': posts})

@login_required
def profile(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request, 'myblog/profile.html', {'form': form, 'posts': posts})

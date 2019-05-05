from django.db.models import Count,Q
# from next_prev import next_in_order, prev_in_order

from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post,Category,Author
from marketing.models import Signup
from .forms import CommentForm,PostForm
from django.urls import reverse


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None




def search(request):
    queryset= Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset
    }
    return render(request,'search_results.html',context)

def get_cat_count():
    queryset = Category.objects.all()
    return queryset



def index(request):
    queryset = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST.get('email')
        new_signup = Signup()
        new_signup.email = email 
        new_signup.save()

    context = {
        'posts': queryset,
        'latest':latest
    }
    return render(request,'index.html', context)

def blog(request):
    category_count = get_cat_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    queryset = Post.objects.all()
    paginator = Paginator(queryset, 3) # Show 25 contacts per page
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {
        'post_list':paged_posts,
        'most_recent':most_recent,
        'category_count':category_count
    }
    return render(request,'blog.html',context)

def post(request,slug):
    category_count = get_cat_count()

    post = get_object_or_404(Post,slug=slug)

    next_post = (Post.objects 
    .filter(id__gt=post.id) 
    .exclude(id=post.id) 
    .order_by('id')
    .first()) 

    prev_post = (Post.objects
    .filter(id__lt=post.id)
    .exclude(id=post.id)
    .order_by('-id')
    .first())  
    most_recent = Post.objects.order_by('-timestamp')[:3]
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            redirect(reverse('post-detail',kwargs={
                'slug':post.slug
            }))
    context = {
        'post':post,
        'next_post':next_post,
        'prev_post':prev_post,
        'most_recent':most_recent,
        'category_count':category_count,
        'form':form
      
    }
    return render(request,'post.html',context)
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None,request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail',kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title':title,
        'form':form
    }
    return render(request,'post_create.html',context)

def post_update(request,id):
    title = 'Update'
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail',kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title': title,
        'form':form
    }
    return render(request,'post_create.html',context)
def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect(reverse('post-list'))

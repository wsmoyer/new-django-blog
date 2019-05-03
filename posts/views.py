from django.db.models import Count,Q

from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post,Category
from marketing.models import Signup



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
    queryset = Post \
    .objects \
    .values('category__title') \
    .annotate(Count('category__title'))
    return queryset



def index(request):
    queryset = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST['email']
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
    paginator = Paginator(queryset, 1) # Show 25 contacts per page
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {
        'post_list':paged_posts,
        'most_recent':most_recent,
        'category_count':category_count
    }
    return render(request,'blog.html',context)

def post(request,slug):
    post = get_object_or_404(Post,slug=slug)
    context = {
        'post':post
    }
    return render(request,'post.html',context)
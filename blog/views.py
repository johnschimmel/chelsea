# Create your views here.
# from django.core.cache import cache
from blog.models import Blog, Category
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('blog.logger')

def show404(request):
    return render_to_response('404.html')

def index(request):
    
    blog_posts = Blog.objects.filter(status='published').order_by('-display_date')

    paginator = Paginator(blog_posts, 10) # Show 10 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    template_data = {
        'categories': Category.objects.all(),
        'posts': posts,
        'recentPosts' : Blog.objects.filter(status='published').order_by('-display_date')[:3],
        'baseContainerClasses' : ['blog_page']
    }

    return render_to_response('index.html',template_data)

def view_post(request, slug, year, month,):   
    
    post = get_object_or_404(Blog, slug=slug)

    try:
        nextPost = post.get_next_by_display_date()
    except:
        nextPost = None

    try:
        previousPost = post.get_previous_by_display_date()
    except:
        previousPost = None

    template_data = {
        'post': post,
        'nextPost' : nextPost,
        'previousPost' : previousPost,
        'recentPosts' : Blog.objects.filter(status='published').order_by('-display_date')[:3],
        'baseContainerClasses' : ['blog_page','blog_item']
    }
    return render_to_response('blog_entry.html', template_data)

def view_category(request, categorySlug):
    # Get specified category
    try:
        posts = Blog.objects.filter(status='published').order_by('-display_date')
    except Blog.DoesNotExist:
        raise Http404

    category_posts = []
    for post in posts:
        if post.categories.filter(slug=categorySlug):
            category_posts.append(post)

    # Add pagination
    paginator = Paginator(category_posts, 10)

    # Get the category
    try:
        category = Category.objects.filter(slug=categorySlug)[0]
    except:
        raise Http404


    # Get the specified page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    # Display all the posts
    return render_to_response('index.html', {
        'posts': posts,
        'category': category,
        'recentPosts' : Blog.objects.filter(status='published').order_by('-display_date')[:3],
        'baseContainerClasses' : ['blog_page','blog_category']
    })

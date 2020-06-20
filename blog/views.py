from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from comment.models import Comment
from comment.forms import CommentForm

from .models import Blog, BlogType, ReadNum
# from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_data
# from user.forms import LoginForm

from datetime import datetime


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每10篇进行分页
    page_num = request.GET.get("page", 1) # 获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页码
    # 获取当前页码各两页的页码的范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 加上首页和尾页页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    # 获取博客分类的对应博客数量
    # method 1
    # BlogType.objects.annotate(blog_count = Count("blog"))
    # method 2
    """
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type = blog_type).count()
        blog_types_list.append(blog_type)
    """

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates("created_time", "month", order = "DESC").annotate(blog_count = Count("created_time"))
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year, 
                                         created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    
    context = {}
    context["blogs"] = page_of_blogs.object_list
    context["page_of_blogs"] = page_of_blogs
    context["page_range"] = page_range
    context["blog_types"] = BlogType.objects.annotate(blog_count = Count("blog"))
    context["blog_dates"] = blog_dates_dict # Blog.objects.dates("created_time", "month", order = "DESC")

    return context


# Create your views here.
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)

    return render(request, "blog/blog_list.html", context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk = blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context["blog_type"] = blog_type
    
    return render(request, "blog/blogs_with_type.html", context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year = year, created_time__month = month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context["blogs_with_date"] = "%s年%s月" % (year, month)
    
    return render(request, "blog/blogs_with_date.html", context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk = blog_pk)
    if not request.COOKIES.get("blog_%s_readed" % blog_pk):
        if ReadNum.objects.filter(blog = blog).count():
            # 存在记录
            readnum = ReadNum.objects.get(blog = blog)
        else:
            # 不存在对应的记录
            readnum = ReadNum(blog = blog)
        
        # 计数加1
        readnum.read_num += 1
        readnum.save()

    context = {}
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type = blog_content_type, object_id = blog.pk)
    context["blog"] = blog
    context["previous_blog"] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context["next_blog"] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context["user"] = request.user
    context["comments"] = comments
    context["comment_form"] = CommentForm(initial = {"content_type": blog_content_type.model, "object_id": blog_pk})

    response = render(request, "blog/blog_detail.html", context)
    response.set_cookie(
        "blog_%s_readed" % blog_pk, 
        "true", 
        # max_age = 60, 
        # expires = datetime
    )
    
    return response
from django.urls import path
from . import views


"""
http://localhost:8000/blog/1
http://localhost:8000
"""


# start with blog
urlpatterns = [
    # http://localhost:8000/blog/
    path("", views.blog_list, name = "blog_list"),
    # http://localhost:8000/blog/1
    path("<int:blog_pk>", views.blog_detail, name = "blog_detail"),
    # http://localhost:8000/blog/type/1
    path("type/<int:blog_type_pk>", views.blogs_with_type, name = "blogs_with_type"),
    # http://localhost:8000/blog/date/2020/5
    path("date/<int:year>/<int:month>", views.blogs_with_date, name = "blogs_with_date"),
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Main site pages
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('book/', views.book, name='book'),

    # Blog URLs
    path('blog/', views.BlogListView.as_view(), name='post_list'),  # Changed back to post_list
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.BlogDetailView.as_view(), name='post_detail'),
    path('blog/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('blog/review/<int:post_id>/', views.add_review, name='add_review'),
    path('blog/like/<int:post_id>/', views.like_post, name='like_post'),
]
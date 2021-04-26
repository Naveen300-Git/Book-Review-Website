from django.urls import path
from .views import (
    post_review_create_list_view,
    like_unlike_post_view,
    create_post_view,
    create_review_view,
    like_unlike_review_view,
    delete_post_view,
    delete_review_view,
    search_book_list_view,
    show_book_view,
    )

app_name = 'posts'

urlpatterns = [
    path('',post_review_create_list_view,name='main-post-view'),
    path('add_post/',create_post_view,name='create-post-view'),
    path('post_liked/',like_unlike_post_view,name='like-post-view'),
    path('delete_post/',delete_post_view,name='delete-post-view'),
    path('add_review/',create_review_view,name='create-review-view'),
    path('review_liked/',like_unlike_review_view,name='like-review-view'),
    path('delete_review/',delete_review_view,name='delete-review-view'),
    path('search_book/',search_book_list_view,name='search-book'),
    path('book/<str:id>/',show_book_view,name='show-book'),
    #path('show_profile/',show_profile_from_post,name='show-profile-from-post')
]

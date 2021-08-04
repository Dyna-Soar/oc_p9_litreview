from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create-review", views.create_review, name="create-review"),
    path("create-review-ticket/<int:id>", views.create_review_ticket, name="create-review-ticket"),
    path("feed", views.feed, name="feed"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("update-review/<int:review_id>", views.update_review, name="update-review"),
    path("update-ticket/<int:ticket_id>", views.update_ticket, name="update-ticket"),
    path("view-posts", views.view_posts, name="view-posts"),
    path("create-ticket", views.create_ticket, name="create-ticket"),

    # Sub path actions
    path("subscribe/add_user_follow", views.add_user_follow, name="add_user_follow"),
    path("subscribe/remove_user_follow", views.remove_user_follow, name="remove_user_follow"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

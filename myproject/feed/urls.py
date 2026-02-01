from django.urls import path
from .views import create_post, delete_comment, feed, like_post, like_comment, leaderboard, add_comment, login_view, signup_view, delete_post, unlike_post, unlike_comment

urlpatterns = [
    path("feed/", feed),
    path("like/post/<int:post_id>/", like_post),
    path("like/comment/<int:comment_id>/", like_comment),
    path("unlike/post/<int:post_id>/", unlike_post),
    path("unlike/comment/<int:comment_id>/", unlike_comment),
    path("comment/<int:post_id>/", add_comment),
    path("post/<int:post_id>/", delete_post),
    path("leaderboard/", leaderboard),
    path("login/", login_view),
    path("signup/", signup_view),
    path("post/", create_post),
    path("comment/delete/<int:comment_id>/", delete_comment),

]

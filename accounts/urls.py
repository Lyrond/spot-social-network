from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CreateNewPostView, lit_hub, LikePostView, comment_post, hub_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.title, name='title'),
    path('main.html', views.main, name='home'),
    path('cars.html', views.cars, name='cars'),
    path('crypto.html', views.crypto, name='crypto'),
    path('games.html', views.games, name='games'),
    path('health.html', views.health, name='health'),
    path('index.html', views.index, name='index'),
    path('mental.html', views.mental, name='mental'),
    path('create_post.html', views.post, name='post'),
    path('sports.html', views.sports, name='sports'),
    path('loggedmain.html', views.loggedmain, name='loggedmain'),
    path('profile.html', views.profile, name='profile'),
    # path('create_post.html', views.create_post, name='create_post'),
    path('metamask.html', views.metamask, name='metamask'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lit.html', views.lit_hub, name='lit_hub'),
    path('create_new_post/', CreateNewPostView.as_view(), name='create_new_post'),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('comment_post/<int:post_id>/', comment_post, name='comment_post'),
    path('<str:hub_name>/', hub_view, name='hub_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


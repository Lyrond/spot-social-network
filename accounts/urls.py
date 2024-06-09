from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CreateNewPostView, CreateNewEventView, lit_hub, LikePostView, comment_post, hub_view, join_event, event_detail
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
    path('sports.html', views.sports, name='sports'),
    path('loggedmain.html', views.loggedmain, name='loggedmain'),
    path('profile.html', views.profile, name='profile'),
    path('metamask.html', views.metamask, name='metamask'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_new_post/', CreateNewPostView.as_view(), name='create_new_post'),
    path('create_event/', CreateNewEventView.as_view(), name='create_event'),  # Ensure this is correct
    path('lit.html', views.lit_hub, name='lit_hub'),
    path('like_post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('comment_post/<int:post_id>/', comment_post, name='comment_post'),
    path('join_event/<int:event_id>/', join_event, name='join_event'),
    path('<str:hub_name>/', hub_view, name='hub_view'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

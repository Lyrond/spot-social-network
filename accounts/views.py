from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import Hub, Post, Like, Comment
from .models import CustomUser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.urls import reverse



def main(request):
    if request.user.is_authenticated:
        context = {
            'is_logged_in': True,
            'username': request.user.username,
        }
    else:
        context = {
            'is_logged_in': False,
        }
    return render(request, 'teamo2/main.html', context)


def cars(request):
    return render(request, 'teamo2/cars.html')


def crypto(request):
    return render(request, 'teamo2/crypto.html')


def games(request):
    posts = Post.objects.filter(hub__name='games')
    return render(request, 'teamo2/games.html', {'posts': posts})
def health(request):
    return render(request, 'teamo2/health.html')

def mental(request):
    return render(request, 'teamo2/mental.html')


def post(request):
    return render(request, 'teamo2/create_post.html')

def sports(request):
    return render(request, 'teamo2/sports.html')

def loggedmain(request):
    return render(request, 'teamo2/loggedmain.html')

def profile(request):
    return render(request, 'teamo2/profile.html')
def title(request):
    return render(request, 'teamo2/title.html')



User = get_user_model()

def index(request):
    if request.method == 'POST':
        if 'email2' in request.POST:
            email = request.POST['email2']
            password = request.POST['password3']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('index')

        elif 'email' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists!")
                    return redirect('index')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exists!")
                    return redirect('index')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    new_profile = Profile.objects.create(username=user, name="", last_name="", age=0)
                    new_profile.save()
                    messages.success(request, "Account created successfully!")
                    return redirect('index')
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('index')

    return render(request, "teamo2/index.html")


@method_decorator(login_required, name='dispatch')
class CreateNewPostView(View):
    def post(self, request, *args, **kwargs):
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Get the content
        paragraph_name = data.get('paragraph_name', '')
        image_url = data.get('image_url', '')
        text_content = data.get('text_content', '')
        hub_name = data.get('hub', '')

        # Validate the content (e.g., check for empty content)
        if not paragraph_name.strip() or not text_content.strip():
            return JsonResponse({'success': False, 'message': 'Content cannot be empty'}, status=400)

        # Handle other hub names
        if hub_name == 'other':
            hub_name = data.get('new_hub', '')

        # Ensure hub name is handled case-insensitively and strip whitespace
        hub_name = hub_name.strip().lower()
        hub, created = Hub.objects.get_or_create(name=hub_name)

        # Create the new post
        new_post = Post(
            hub=hub,
            user=request.user,
            paragraph_name=paragraph_name,
            image_url=image_url,
            text_content=text_content
        )
        new_post.save()

        return JsonResponse({'success': True, 'message': 'Post created successfully'}, status=201)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@method_decorator(login_required, name='dispatch')
class LikePostView(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=403)

        post = get_object_or_404(Post, id=post_id)

        user_has_liked = request.user in post.liked_by.all()

        if user_has_liked:
            post.liked_by.remove(request.user)
            message = 'Post unliked successfully'
        else:
            post.liked_by.add(request.user)
            message = 'Post liked successfully'

        likes_count = post.liked_by.count()

        return JsonResponse({'success': True, 'message': message, 'likes_count': likes_count, 'user_has_liked': not user_has_liked})

@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text', '')
        if text.strip():
            Comment.objects.create(user=request.user, post=post, text=text)
        return redirect('lit_hub')

def lit_hub(request):
    posts = Post.objects.all()
    return render(request, 'teamo2/lit.html', {'posts': posts})





def metamask(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        wallet_address = request.POST.get('wallet_address')
        username = request.POST.get('username')

        if action == 'signup':
            if wallet_address and username:
                if CustomUser.objects.filter(wallet_address=wallet_address).exists():
                    messages.error(request, 'Wallet address already registered.')
                else:
                    user = CustomUser.objects.create(username=username, wallet_address=wallet_address)
                    messages.success(request, 'Signup successful! Please login.')
                    return redirect('metamask')
            else:
                messages.error(request, 'Username and wallet address are required.')
        elif action == 'login':
            if wallet_address:
                user = CustomUser.objects.filter(wallet_address=wallet_address).first()
                if user:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('loggedmain')
                else:
                    messages.error(request, 'Wallet address not found. Please sign up.')
                    return redirect('metamask_auth')
            else:
                messages.error(request, 'Wallet address is required.')

    return render(request, 'teamo2/metamask.html')




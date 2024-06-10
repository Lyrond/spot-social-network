from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import Hub, Post, Like, Comment, Event
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
    posts = Post.objects.filter(hub__name='cars')
    return render(request, 'teamo2/cars.html', {'posts': posts})


def crypto(request):
    posts = Post.objects.filter(hub__name='crypto')
    return render(request, 'teamo2/crypto.html', {'posts': posts})


def games(request):
    posts = Post.objects.filter(hub__name='games')
    return render(request, 'teamo2/games.html', {'posts': posts})
def health(request):
    posts = Post.objects.filter(hub__name='health')
    return render(request, 'teamo2/health.html', {'posts': posts})

def mental(request):
    posts = Post.objects.filter(hub__name='mental')
    return render(request, 'teamo2/mental.html', {'posts': posts})




def event(request):
    return render(request, 'teamo2/create_event.html')

def sports(request):
    posts = Post.objects.filter(hub__name='sports')
    return render(request, 'teamo2/sports.html', {'posts': posts})

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
        hub_name = request.POST.get('hub')
        paragraph_name = request.POST.get('paragraph_name')
        text_content = request.POST.get('text_content')
        image = request.FILES.get('image')

        if not paragraph_name.strip() or not text_content.strip():
            return JsonResponse({'success': False, 'message': 'Content cannot be empty'}, status=400)

        if hub_name == 'other':
            hub_name = request.POST.get('new_hub')

        hub_name = hub_name.strip().lower()
        hub, created = Hub.objects.get_or_create(name=hub_name)

        new_post = Post(
            hub=hub,
            user=request.user,
            paragraph_name=paragraph_name,
            image=image,
            text_content=text_content
        )
        new_post.save()

        return redirect('lit_hub')

    def get(self, request, *args, **kwargs):
        return render(request, 'teamo2/create_post.html')

@method_decorator(login_required, name='dispatch')
class CreateNewEventView(View):
    def post(self, request, *args, **kwargs):
        hub_name = request.POST.get('hub')
        event_name = request.POST.get('event_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        event_date = request.POST.get('event_date')

        if not event_name.strip() or not description.strip() or not event_date.strip():
            return JsonResponse({'success': False, 'message': 'Content cannot be empty'}, status=400)

        if hub_name == 'other':
            hub_name = request.POST.get('new_hub')

        hub_name = hub_name.strip().lower()
        hub, created = Hub.objects.get_or_create(name=hub_name)

        new_event = Event(
            hub=hub,
            user=request.user,
            event_name=event_name,
            description=description,
            image=image,
            event_date=event_date
        )
        new_event.save()

        return redirect('lit_hub')

    def get(self, request, *args, **kwargs):
        return render(request, 'teamo2/create_event.html')

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

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.participants.all():
        event.participants.remove(user)
        joined = False
    else:
        event.participants.add(user)
        joined = True

    participants_count = event.participants.count()
    return JsonResponse({'success': True, 'joined': joined, 'participants_count': participants_count})

@login_required
def join_event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.participants.all():
        event.participants.remove(user)
        joined = False
    else:
        event.participants.add(user)
        joined = True

    participants = [{'username': participant.username} for participant in event.participants.all()]

    return JsonResponse({
        'success': True,
        'joined': joined,
        'participants_count': event.participants.count(),
        'participants': participants
    })

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'teamo2/event.html', {'event': event})

def lit_hub(request):
    posts = Post.objects.all()
    events = Event.objects.all()  # Fetch all events
    context = {
        'posts': posts,
        'events': events,
    }
    return render(request, 'teamo2/lit.html', context)

def hub_view(request, hub_name):
    hub = get_object_or_404(Hub, name=hub_name)
    posts = Post.objects.filter(hub=hub)
    return render(request, f'teamo2/{hub_name}.html', {'posts': posts})





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




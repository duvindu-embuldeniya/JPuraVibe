from django.shortcuts import render, redirect
from . models import Rooms, Topic, Message, Profile
from . forms import RoomForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views 


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Rooms.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)
    )
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    rooms_messages = Message.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'rooms_messages': rooms_messages}    
    return render(request, 'home/index.html', context)


def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # new_user = form.save(commit=False)
            # new_user.username = new_user.username.lower()
            new_user = form.save()
            auth.login(request, new_user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'home/register.html', {'form': form})


class CustomLoginView(auth_views.LoginView):
    template_name = 'home/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # messages.info(request, "You are already logged in!")
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # messages.success(self.request, "You have logged in successfully!")
        return super().get_success_url()
    

def logoutUser(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You are not logged-in!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect('home')


def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.rooms_set.all()
    # rooms_messages = user.message_set.all()
    rooms_messages = Message.objects.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'rooms_messages' : rooms_messages, 'topics': topics}
    return render(request, 'home/profile.html', context)


@login_required
def updateUser(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile', pk = user.pk)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm()
    return render(request, 'home/update_user.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def room(request, pk):
    room = Rooms.objects.get(pk=pk)
    room_messages = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        message.save()
        room.participants.add(request.user)

        return redirect('room', pk = room.pk)
    participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'home/room.html', context)


@login_required
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
            topic_name = request.POST.get('topic')
            topic,created = Topic.objects.get_or_create(name = topic_name)
            
            room = Rooms.objects.create(
                host = request.user,
                topic = topic,
                name = request.POST.get('name'),
                description = request.POST.get('description'),
            )
            return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'home/room_form.html', context)


@login_required
def updateRoom(request, pk):
    room = Rooms.objects.get(pk=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    current_topic = room.topic
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        rooms_count = current_topic.rooms_set.all().count()
        if rooms_count == 0:
            current_topic.delete()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'room':room}
    return render(request, 'home/room_form.html', context)


@login_required
def deleteRoom(request, pk):
    room = Rooms.objects.get(pk=pk)
    r_topic = room.topic
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    if request.method == 'POST':
        room.delete()

        count = r_topic.rooms_set.all().count()
        if count == 0:
            r_topic.delete()
        return redirect('home')
    return render(request, 'home/delete.html', {'obj': room})


@login_required
def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)
    room = message.room
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    if request.method == 'POST':
        message.delete()

        remaining_messages = Message.objects.filter(room=room, user=request.user).count()

        if remaining_messages == 0:
            room.participants.remove(request.user)

        return redirect('room', pk = room.pk)
    return render(request, 'home/delete.html', {'obj': message})

@login_required
def deleteProfile(request, pk):
    usr = User.objects.get(pk=pk)
    if request.user != usr:
        return HttpResponse("You are not allowed here!")
    if request.method == 'POST':
        usr.delete()
        return redirect('home')
    return render(request, 'home/user_delete.html', {'usr': usr})



def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains = q)
    )
    context = {'topics': topics}
    return render(request, 'home/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'home/activity.html', context)


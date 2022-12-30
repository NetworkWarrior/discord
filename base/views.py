from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Group, Topic, Message, User
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import GroupForm, UserForm, MyUserCreationForm

# Create your views here.

# groups = [
# {'id':1, 'name':'Dive into Machine-Learning with Python'},
#  {'id':2, 'name':'Create Android apps with Java'},
#   {'id':3, 'name':'Build realistic games with C++'}
# ]


def handle_not_found(request, exception):
    return render(request, 'base/Not-Found.html')


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not match')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return messages.error(request, 'An error occurred during registration')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    page_size = request.GET.get('page_size', 3)
    paginator = Paginator(groups, page_size)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    room_count = groups.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]
    context = {'page_obj':page_obj, 'topics': topics, "room_count": room_count, 'room_messages':room_messages}
    return render(request, "base/home.html", context)


def group(request, id):
    group = Group.objects.get(id=id)
    participants = group.participants.all()
    group_messages = group.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = group,
            body = request.POST.get('body')
        )
        group.participants.add(request.user)
        return redirect('group', id=group.id)
    context = {"group": group, 'group_messages':group_messages, 'participants':participants}
    return render(request, "base/group.html", context)


def user_profile(request, id):
    user = User.objects.get(id=id)
    rooms = user.group_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    page_size = request.GET.get('page_size', 3)
    paginator = Paginator(rooms, page_size)
    paginator2 = Paginator(room_messages, page_size)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    page_object = paginator2.get_page(page_num)
    context = {'user':user, 'page_obj':page_obj, 'topics':topics, 'page_object':page_object}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = GroupForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Group.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, id):
    room = Group.objects.get(id=id)
    form = GroupForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("Oops , looks like you have no authorized ownership!!!")
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {"form": form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete(request, id):
    room = Group.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("Oops , looks like you have no authorized ownership!!!")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse("Oops , looks like you have no authorized ownership!!!")
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=user.id)
    context = {'form':form}
    return render(request, 'base/update-user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})







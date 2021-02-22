import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView

from .forms import UserChangeForm, UserStandardCreationForm, PostForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Friend, Post, Profile
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect


@login_required(login_url='login')
def Home(request):
    postdata = Post.objects.all()[::-1]
    context = {'postdata': postdata}
    return render(request, 'account/home.html', context)


@csrf_protect
def RegisterPageView(request):
    form = UserStandardCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserStandardCreationForm(request.POST)

        if form.is_valid():

            print('form', form)
            form.save()
            return redirect('login')
        else:
            messages.warning(request, 'Fill all the data fields')
            return redirect('register')
    else:
        return render(request, 'account/registerpage.html', context)


def LoginPageView(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        print(phone_number)
        print(password)
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.warning(request, 'username or password wrong')
    return render(request, 'account/loginpage.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def ProfileView(request):
    current_user = request.user.id
    user = User.objects.get(id=current_user)
    context = {'user': user}
    return render(request, 'account/userprofile.html', context)


def profileEditView(request):
    form = EditProfileForm()
    user = User.objects.filter(id=request.user.id)
    context = {'form': form}
    if request.method == 'POST' and request.FILES:
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            item_form_obj = form.save(commit=False)
            item_form_obj.user = user[0]

            item_form_obj.save()
            return HttpResponseRedirect(reverse('profile'))

        else:
            return HttpResponseRedirect(reverse('homepage'))

    else:
        return render(request, 'account/userprofileedit.html', context)


def FindFriendsView(request):
    users = User.objects.all()

    return render(request, 'account/findfriendspage.html', {users: 'users'})


def ResultsView(request):  # multiple search
    user = request.user

    if request.method == 'GET':
        search = request.GET.get('user')
        user = request.user
        friend_filter = Friend.objects.filter(
            Q(user1=user) | Q(user2=user))

        if search:
            users = User.objects.filter(
                (Q(full_name__icontains=search) | Q(email__icontains=search) | Q(
                    phone_number__contains=search))).exclude(phone_number=user)

            if users:
                return render(request, 'account/findfriendspage.html', {'users': users, 'friend_filter': friend_filter})
            else:
                # messages.error(request,"No similar results for")
                messages.error(request, search)
        else:

            return render(request, 'account/findfriendspage.html')
    return render(request, 'account/findfriendspage.html')


def PostDataView(request):
    form = PostForm()
    user = User.objects.filter(id=request.user.id)
    context = {'form': form}
    if request.method == 'POST' and request.FILES:
        form = PostForm(request.POST, request.FILES)
        print('form', form)
        if form.is_valid():
            item_form_obj = form.save(commit=False)
            item_form_obj.user = user[0]
            print('ssssssssssss', item_form_obj.user)
            item_form_obj.save()
            return HttpResponseRedirect(reverse('homepage'))
        else:
            redirect('register')
    else:
        return render(request, 'account/postpage.html', context)


def AllPostView(request):
    return render(request, 'account/allpostpage.html')


def AddFriendView(request, id):
    user1 = User.objects.filter(id=request.user.id)
    user2 = User.objects.filter(id=id)
    Friend.objects.create(user1=user1[0], user2=user2[0])
    print(user2)

    return redirect('homepage')


def FriendListView(request):
    user = request.user

    friend_filter = Friend.objects.filter(
        Q(user1=user) | Q(user2=user))

    return render(request, 'account/friendListpage.html', {'friend_filter': friend_filter})


@login_required(login_url='login')
def autocomplete(request):
    if 'term' in request.GET:
        qs = User.objects.filter(phone_number__contains=request.GET.get('term'))
        titles = list()
        for search in qs:
            titles.append(search.phone_number)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request, 'account/findfriendspage.html')

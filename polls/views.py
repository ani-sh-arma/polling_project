from django.shortcuts import render, redirect, HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# from django.views.generic import ListView,DetailView
from .models import Poll,Choice
# from .models import Vote
from .forms import addPoll

user = User.objects.all()

@login_required(login_url="login")
def index(request):
    poll = Poll.objects.all()
    # vote = Vote.objects.all()
    choice = Choice.objects.all()
    if request.user.is_anonymous:
        return redirect("/login")

    if request.GET.get('search'):
        poll = poll.filter(question__icontains = request.GET.get('search') )


    if request.user.is_superuser:
        return render(request, "adminHome.html",{"polls":poll,"choices":choice})
    
    return render(request, "index.html",{"polls":poll,"choices":choice,"vote":vote })




# Home view by class , We can use ListView and DetailView by doing this
# class Home(ListView):
#     model = Poll
#     template_name = "index.html"



def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:

            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = fname
            new_user.last_name = lname

            new_user.save()
            return redirect("login")
            # Redirect or perform other actions for successful registration
        except IntegrityError:
            # Handle the case when a user with the same username already exists
            error_message = (
                "Username or Email already exists. Please choose a different username."
            )
            return render(
                request,
                "register.html",
                {"error_message": error_message},
            )

    else:
        return render(
            request, "register.html"
        )  # Render the registration form for GET requests

def mypolls(request):
    poll = Poll.objects.all()
    # vote = Vote.objects.all()
    choice = Choice.objects.all()

    if request.GET.get('search'):
        poll = poll.filter(question__icontains = request.GET.get('search') )
    if request.user.is_anonymous:
        return redirect("/login")
    
    if poll.exists():
        return render(request, "mypolls.html",{"polls":poll,"choice":choice,"vote":vote,"user":request.user})
    else:
        return HttpResponse("You haven't yet created any poll.")

    # return HttpResponse(poll.creator)

def about(request):
    return render(request,'about.html')


def addpoll(request):
    if request.method == "POST":
        form = addPoll(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.creator = request.user
            poll.save()

            options_str = form.cleaned_data['options']
            options_list = [option.strip() for option in options_str.split(",")]

            for option_text in options_list:
                Choice.objects.create(question=poll, option_text=option_text)

            return redirect("home")
    else:
        form = addPoll()

    return render(request, "addpoll.html", {"form": form})


def delete(request,id):

    queryset = Poll.objects.get(id = id)
    queryset.delete()

    return redirect("mypolls")




def update(request,id):

    queryset = Poll.objects.get(id = id)

    if request.method == "POST":
        form = addPoll(request.POST)
        if form.is_valid():

            # form.question = request.POST.get("question")
            poll = form.save(commit=False)
            poll.creator = request.user
            poll.save()
            return redirect("mypolls")
    else:
        form = addPoll()

    return render(request,"updatepoll.html",{"form":form })



def vote(request,id):
    queryset = Choice.objects.get(id = id)

    if request.method == "GET":
        queryset.votes += 1
        queryset.save()
        return redirect("/")

    return redirect("/")
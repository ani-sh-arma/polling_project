from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import logout
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError

from .models import Poll, Choice, Voted
from .forms import addPoll

user = User.objects.all()


def index(request):
    polls = Poll.objects.all().order_by("-pub_date")

    # Handle search
    if request.GET.get("search"):
        polls = polls.filter(question__icontains=request.GET.get("search"))

    # Calculate statistics for hero section
    total_votes = Choice.objects.aggregate(total=Sum("votes"))["total"] or 0
    total_users = User.objects.count()

    # Get user's voted choices if authenticated
    user_voted_choices = []
    if request.user.is_authenticated:
        user_voted_choices = list(
            Voted.objects.filter(user=request.user).values_list("choice_id", flat=True)
        )

    context = {
        "polls": polls,
        "total_votes": total_votes,
        "total_users": total_users,
        "user_voted_choices": user_voted_choices,
    }

    # Check if user is authenticated for conditional rendering
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, "adminHome.html", context)
        return render(request, "index.html", context)
    else:
        return render(request, "index.html", context)


def custom_logout(request):

    logout(request)
    return redirect("login")


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


@login_required(login_url="login")
def mypolls(request):
    # Get user's polls
    user_polls = Poll.objects.filter(creator=request.user).order_by("-pub_date")

    # Handle search
    if request.GET.get("search"):
        user_polls = user_polls.filter(question__icontains=request.GET.get("search"))

    # Calculate statistics for the user
    user_polls_count = user_polls.count()

    # Calculate total votes for user's polls
    total_votes = 0
    for poll in user_polls:
        poll_votes = poll.choice_set.aggregate(total=Sum("votes"))["total"] or 0
        total_votes += poll_votes

    # Calculate recent polls (this week)
    week_ago = timezone.now() - timedelta(days=7)
    recent_polls = user_polls.filter(pub_date__gte=week_ago).count()

    context = {
        "polls": user_polls,
        "user_polls_count": user_polls_count,
        "total_votes": total_votes,
        "recent_polls": recent_polls,
        "user": request.user,
    }

    return render(request, "mypolls.html", context)


def about(request):
    # Calculate statistics for about page
    total_polls = Poll.objects.count()
    total_votes = Choice.objects.aggregate(total=Sum("votes"))["total"] or 0
    total_users = User.objects.count()

    context = {
        "total_polls": total_polls,
        "total_votes": total_votes,
        "total_users": total_users,
    }

    return render(request, "about.html", context)


@login_required(login_url="login")
def addpoll(request):
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        options = request.POST.get("options", "").strip()

        if not question:
            return render(
                request,
                "addpoll.html",
                {"error_message": "Please provide a question for your poll."},
            )

        if not options:
            return render(
                request,
                "addpoll.html",
                {"error_message": "Please provide at least 2 options for your poll."},
            )

        # Create the poll
        poll = Poll.objects.create(question=question, creator=request.user)

        # Parse and create options
        options_list = [
            option.strip() for option in options.split(",") if option.strip()
        ]

        if len(options_list) < 2:
            poll.delete()  # Clean up the poll if options are invalid
            return render(
                request,
                "addpoll.html",
                {"error_message": "Please provide at least 2 options for your poll."},
            )

        # Create choices
        for option_text in options_list:
            if option_text:  # Only create non-empty options
                Choice.objects.create(question=poll, option_text=option_text)

        return redirect("home")

    return render(request, "addpoll.html")


def delete(request, id):

    queryset = Poll.objects.get(id=id)
    queryset.delete()

    return redirect("mypolls")


@login_required(login_url="login")
def update(request, id):
    poll = get_object_or_404(Poll, id=id)

    # Check if the user is the creator of the poll
    if poll.creator != request.user:
        return redirect("mypolls")

    # Get existing choices
    existing_choices = poll.choice_set.all()
    existing_options = ", ".join([choice.option_text for choice in existing_choices])

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        options = request.POST.get("options", "").strip()

        if not question:
            return render(
                request,
                "updatepoll.html",
                {
                    "poll": poll,
                    "existing_options": existing_options,
                    "error_message": "Please provide a question for your poll.",
                },
            )

        if not options:
            return render(
                request,
                "updatepoll.html",
                {
                    "poll": poll,
                    "existing_options": existing_options,
                    "error_message": "Please provide at least 2 options for your poll.",
                },
            )

        # Parse and validate options
        options_list = [
            option.strip() for option in options.split(",") if option.strip()
        ]

        if len(options_list) < 2:
            return render(
                request,
                "updatepoll.html",
                {
                    "poll": poll,
                    "existing_options": existing_options,
                    "error_message": "Please provide at least 2 options for your poll.",
                },
            )

        # Update the poll question
        poll.question = question
        poll.save()

        # Delete existing choices and create new ones
        poll.choice_set.all().delete()
        for option_text in options_list:
            if option_text:  # Only create non-empty options
                Choice.objects.create(question=poll, option_text=option_text)

        return redirect("mypolls")

    context = {
        "poll": poll,
        "existing_options": existing_options,
    }

    return render(request, "updatepoll.html", context)


@require_POST
@login_required
def vote(request, id):

    try:

        choice = get_object_or_404(Choice, id=id)
        poll = choice.question  # Get the associated poll

        # Check if the user has already voted for this poll
        if Voted.objects.filter(user=request.user, poll=poll).exists():
            # User has already voted for this poll
            return JsonResponse({"error": "You have already voted for this poll."})

        # Record the user's vote in the Voted table
        Voted.objects.create(user=request.user, poll=poll, choice=choice, voted=True)

        # Update the votes count for the chosen option
        choice.votes = int(choice.votes) + 1
        choice.save()

        updated_votes = choice.votes

        return JsonResponse(
            {"success": "Vote recorded successfully.", "votes": updated_votes}
        )

    except Exception as e:
        return JsonResponse({"error": str(e)})

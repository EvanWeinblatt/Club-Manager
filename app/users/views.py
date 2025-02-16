"""
HTML views.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http import HttpRequest
from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.core.exceptions import BadRequest, ValidationError
from django.urls import reverse
from rest_framework import status

from clubs.models import Club, Event, ClubMembership
from clubs.services import ClubService
from users.forms import LoginForm, RegisterForm
from users.services import UserService
from utils.models import get_or_none


def register_user_view(request: HttpRequest):
    """Add new user to the system."""
    context = {}
    initial_data = {}

    if request.POST:
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            form_data = {
                "first_name": data.get("first_name", None),
                "last_name": data.get("last_name", None),
                "email": data.get("email", None),
                "password": data.get("password", None),
            }

            confirmed_password = data.get("confirm_password", None)

            if confirmed_password != form_data["password"]:
                raise ValidationError("Passwords do not match.")

            user = UserService.register_user(**form_data)
            UserService.login_user(request, user)

            club: Club = data.get("club", None)
            event: Event = data.get("event", None)

            if club:
                club_svc = ClubService(club)
                club_svc.add_member(user)

            if event:
                club_svc = ClubService(event.club)
                club_svc.add_member(user)
                club_svc.record_member_attendance(user, event)

            return redirect("clubs:available")

        else:
            context["form"] = form
            return render(
                request,
                "users/register-user.html",
                context,
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "GET":
        club_id = request.GET.get("club", None)
        event_id = request.GET.get("event", None)

        if club_id:
            initial_data["club"] = get_or_none(Club, id=club_id)

        if event_id:
            initial_data["event"] = get_or_none(Event, id=event_id)

        form = RegisterForm(initial=initial_data)

    else:
        raise BadRequest("Method must be GET or POST.")

    context["form"] = form
    return render(request, "users/register-user.html", context)


def login_user_view(request: HttpRequest):
    """Authenticate user's credentials, create user session."""
    form = LoginForm()
    context = {}

    if request.POST:
        form = LoginForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get("username", None)
            password = data.get("password", None)

            user = UserService.authenticate_user(
                request, username_or_email=username, password=password
            )
            UserService.login_user(request, user)

            return redirect("users:profile")

    context["form"] = form
    return render(request, "users/login-user.html", context)


@login_required()
def logout_user_view(request: HttpRequest):
    """Clear session of current user."""
    return logout_then_login(request, reverse("users:login"))


@login_required()
def user_profile_view(request: HttpRequest):
    """Display user's profile."""
    user = request.user
    profile = user.profile

    club_memberships = ClubMembership.objects.filter(user=user).select_related("club")
    
    context = {
        "user": user,
        "profile": profile,
        "clubs": club_memberships,
    }

    return render(request, "users/profile.html", context=context)


@login_required()
def user_points_view(request: HttpRequest):
    """Summary showing the user's points."""
    return render(request, "users/points.html", context={})

"""
Club views for API and rendering html pages.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from clubs.models import Club, Event
from clubs.services import ClubService


@login_required()
def join_club_view(request: HttpRequest, club_id: int):
    """Registers a new or existing user to a club."""
    club = get_object_or_404(Club, id=club_id)

    club_svc = ClubService(club)
    club_svc.add_member(request.user)

    url = reverse("clubs:home", kwargs={"club_id": club.id})
    return redirect(url)


def club_home_view(request: HttpRequest, club_id: int):
    """Base page for a club."""
    club = get_object_or_404(Club, id=club_id)

    return render(request, "clubs/club-home.html", context={"club": club})


@login_required()
def record_attendance_view(request: HttpRequest, club_id: int, event_id: int):
    """Records a club member attended an event."""
    event = get_object_or_404(Event, id=event_id)
    ClubService(event.club).record_event_attendance(request.user, event)

    return redirect("clubs:join-event-done", club_id=club_id, event_id=event_id)


@login_required()
def available_clubs_view(request: HttpRequest):
    """Display list of clubs to user for them to join."""

    return render(request, "clubs/available-clubs.html")

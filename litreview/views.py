from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from .forms import UploadTicketForm, UploadReviewForm

from .models import User, Ticket, UserFollows, Review


def index(request):
    """Index page"""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))
    elif request.user.is_authenticated:
        return redirect("feed")
    else:
        return render(request, "index.html")


def register(request):
    """Register new user"""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def logout_view(request):
    """Logout"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def subscribe(request):
    """Show user's following posts"""
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "subscribe.html", {"following": following, "followers": followers})


@login_required
def update_review(request, review_id):
    """Let user update a review"""
    if request.method == "POST":
        review_update = Review.objects.get(id=review_id)
        review_update.headline = request.POST["headline"]
        review_update.body = request.POST["body"]
        review_update.rating = request.POST["rating"]
        review_update.save()
        return HttpResponseRedirect(reverse("view-posts"))
    else:
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form_review = UploadReviewForm(initial={"user": request.user,
                                                "ticket": review.ticket,
                                                "headline": review.headline,
                                                "body": review.body,
                                                "rating": review.rating,
                                                })
        return render(request, "update-review.html", {"review": review, "form_review": form_review, "ticket": ticket})


@login_required
def update_ticket(request, ticket_id):
    """Let user update a ticket"""
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket_update = Ticket.objects.get(id=ticket_id)
        form_ticket = UploadTicketForm(request.POST, request.FILES, instance=ticket_update)
        if form_ticket.is_valid():
            form_ticket.save()
            return HttpResponseRedirect(reverse("view-posts"))
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user,
                                                "title": ticket.title,
                                                "description": ticket.description,
                                                "image": ticket.image,
                                                })
        return render(request, "update-ticket.html", {"ticket": ticket, "form_ticket": form_ticket})


@login_required
def add_user_follow(request):
    """Save user to follow"""
    data_follow = request.POST
    username_search = data_follow["username_search"]
    username_search = User.objects.get(username=username_search)
    user_follow = UserFollows.objects.create(
        user=request.user,
        followed_user=username_search
    )
    user_follow.save()
    return HttpResponseRedirect(reverse("subscribe"))


@login_required
def remove_user_follow(request):
    """Remove user from following"""
    followed_user = request.POST["followed_user"]
    user_defollow = UserFollows.objects.filter(followed_user=followed_user).filter(user=request.user)
    user_defollow.delete()
    return HttpResponseRedirect(reverse("subscribe"))


@login_required
def create_ticket(request):
    """Create ticket"""
    # Method POST
    if request.method == "POST":
        form_ticket = UploadTicketForm(request.POST, request.FILES)
        if form_ticket.is_valid():
            form_ticket.save()
    # Method GET
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user})
        return render(request, "create-ticket.html", {'form_ticket': form_ticket})


@login_required
def create_review(request):
    """V2 Create review without answering a ticket"""
    if request.method == "POST":
        form_ticket = UploadTicketForm(request.POST, request.FILES)
        form_review = UploadReviewForm(request.POST)
        # Form Ticket Saving
        if form_ticket.is_valid():
            form_ticket.save()
        # Form Review Saving
        # Manually adding the data
        ticket = Ticket.objects.filter(user=request.user).latest("time_created")
        headline = request.POST["headline"]
        body = request.POST["body"]
        user = request.user
        rating = request.POST["rating"]
        ticket = ticket
        review = Review.objects.create(
            headline=request.POST["headline"],
            body=request.POST["body"],
            user=request.user,
            rating=request.POST["rating"],
            ticket=ticket
        )
        return HttpResponseRedirect(reverse("view-posts"))
        #return render(request, "test.html", {"data": request.POST, "data_review": review, "data_ticket": ticket})
    else:
        form_ticket = UploadTicketForm(initial={"user": request.user})
        form_review = UploadReviewForm(initial={"user": request.user})
        return render(request, "create-review.html", {"form_ticket": form_ticket, "form_review": form_review})


@login_required
def create_review_ticket(request, id):
    """Create review in response to a ticket"""
    if request.method == "POST":
        ticket = Ticket.objects.get(id=id)
        review = Review.objects.create(
            headline=request.POST["headline"],
            body=request.POST["body"],
            user=request.user,
            rating=request.POST["rating"],
            ticket=ticket
        )
        review.save()
        return HttpResponseRedirect(reverse("view-posts"))
    else:
        ticket = Ticket.objects.get(id=id)
        return render(request, "create-review-ticket.html", {"ticket": ticket})


@login_required
def feed(request):
    """Show user's feed"""
    tickets = Ticket.objects.all
    reviews = Review.objects.all
    return render(request, "feed.html", {"tickets": tickets, "reviews": reviews})


@login_required
def view_posts(request):
    """Show user's posts"""
    reviews = Review.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, "view-posts.html", {"reviews": reviews, "tickets": tickets})


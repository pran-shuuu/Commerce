from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True).order_by("-created_at")
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": highest_bid,
    })

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        content = request.POST.get("content")
        listing = get_object_or_404(Listing, pk=listing_id)

        Comment.objects.create(
            author = request.user,
            content=content,
            listing=listing
        )
        return redirect("listing", listing_id=listing_id)

@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        if request.user in listing.watchers.all():
            listing.watchers.remove(request.user)
        else:
            listing.watchers.add(request.user)
        return redirect("listing", listing_id=listing_id)

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(is_active=True, watchers=request.user).order_by("-created_at")
    })

@login_required
def close(request):
    return render(request, "auctions/closed_listing.html", {
        "listings": Listing.objects.filter(is_active=False).order_by("-created_at")
    })

@login_required
def bid(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        try:
            amount = float(request.POST.get("bid"))
            highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
            current_price = highest_bid.amount if highest_bid else listing.starting_bid
            if amount > current_price:
                Bid.objects.create(
                    amount=amount,
                    user=request.user,
                    listing=listing
                )
                messages.success(request, "Bid placed successfully!")
            else:
                messages.error(request, "Value must be greater than current price.")
        except (ValueError, TypeError):
            messages.error(request, "Enter appropriate value")
        
    return redirect("listing", listing_id=listing_id)

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    listing = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listing,
        "category_name": category_name
    })

def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.creator == request.user:
        listing.is_active = False
        highest_bid = listing.bids.order_by("-amount").first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.save()
        messages.success(request, "Auction closed successfully!")
    return redirect("listing", listing_id=listing_id)
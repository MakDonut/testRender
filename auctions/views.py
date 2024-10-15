from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ListForm, BidForm, CommentForm 

def index(request):
    listings = List.objects.filter(is_active=True)
    return render(request, 'auctions/index.html', {
        "listings": listings
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
def create_listing(request):

    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            # Nuevo Listado (el guardado esta en espera).
            newListing = form.save(commit=False)
            # Asignar el usuario actual al listado.
            newListing.user = request.user
            # Guardar el listado con el usuario.
            newListing.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ListForm()

    return render(request, "auctions/create.html", {
        "form": form
    })

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def category_listings_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = List.objects.filter(category=category_id, is_active=True)
    return render(request, 'auctions/category_listings.html', {
        "category": category,
        "listings": listings
    })

def list_detail(request, list_id):
    listing = get_object_or_404(List, id=list_id)
    max_bid = listing.starting_bid

    if listing.bid_list.exists():
        max_bid = listing.bid_list.order_by('-amount').first().amount
        current_winner = listing.bid_list.order_by('-amount').first().user
    else:
        current_winner = None

    comments = Commentary.objects.filter(listing=listing).order_by('-created_at')

    is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists() if request.user.is_authenticated else False
    
    bid_count = listing.bid_list.count()

    if request.method == "POST":

        if 'end_auction' in request.POST and request.user == listing.user:
            listing.close_auction()
            messages.success(request, "Auction has been successfully closed :).")
            return redirect('list_detail', list_id=list_id)

        # Si se envía una oferta
        if 'bid' in request.POST:

            if not listing.is_active:
                messages.error(request, "The auction is closed; Good luck next time." )
                return redirect('list_detail', list_id=list_id)
            
            try:
                amount = float(request.POST['bid'])
                if amount <= max_bid:
                    messages.warning(request, f'Your bid must be higher than {max_bid}.')
                else:
                    new_bid = Bid(listing=listing, amount=amount, user=request.user)
                    new_bid.save()
                    messages.success(request, "Bid was made successfully!")
                    return redirect('list_detail', list_id=list_id)
            except ValueError:
                messages.error(request, "Please enter a valid bid amount.")

        # Si se envía un comentario
        elif 'comment' in request.POST:
            comment_text = request.POST['comment']
            headline_text = request.POST.get('headline')  
            if comment_text and headline_text: 
                new_comment = Commentary(
                    listing=listing,
                    author=request.user,
                    comment=comment_text,
                    headline=headline_text 
                )
                new_comment.save()
                messages.success(request, "Comment added successfully!")
                return redirect('list_detail', list_id=list_id)

    return render(request, 'auctions/list_detail.html', {
        "listing": listing,
        "max_bid": max_bid,
        "comments": comments,
        "is_in_watchlist": is_in_watchlist,
        "bid_count": bid_count,
        'current_winner': current_winner
    })

@login_required
def toggle_watchlist(request, list_id):
    listing = get_object_or_404(List, id=list_id)

    if request.user.is_authenticated:

        if Watchlist.objects.filter(user=request.user, listing=listing).exists():
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            messages.success(request, f'{listing.title} removed from your Watchlist.')
        else:
            Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, f'{listing.title} added to your Watchlist!')
    
    return redirect('list_detail', list_id=list_id)

@login_required
def watchlist(request):

    if request.user.is_authenticated:

        user_watch = request.user.watchlist.all()

        price = []
        for item in user_watch:
            max_bid = item.listing.starting_bid

            if item.listing.bid_list.exists():
                 max_bid = item.listing.bid_list.order_by('-amount').first().amount
            price.append({
                'item': item,
                'current_price': max_bid
            })

        return render(request, 'auctions/watchlist.html', {
            "watchlist": price
        })
    else:
        messages.error(request, "You have to be logged to view your Watchlist.")
        return redirect('login')

@login_required
def user_listings(request):
    user = request.user  # Obtiene el usuario actual
    user_listings = List.objects.filter(user=user)  # Filtra las subastas del usuario
    
    context = {
        'user_listings': user_listings,
    }
    return render(request, 'auctions/user_listings.html', context)
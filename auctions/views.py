from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, ListingForm, Bids, BidForm, Comments, CommentForm

    


def index(request):
    return HttpResponseRedirect(reverse("active_listings"))

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
        
def create_listing(request):
    return render(request, 'auctions/createListing.html', {
        "listingform" : ListingForm()
       })

# 'Active Listings' page
def show_listings(request):
    if request.method == "POST":
        listingForm = ListingForm(request.POST,request.FILES)
        if listingForm.is_valid():
            
            cur_listing = Listing(title=listingForm.cleaned_data["title"], 
            description =listingForm.cleaned_data["description"],
            start_bid =listingForm.cleaned_data["start_bid"],
            category =listingForm.cleaned_data["category"],
            image = listingForm.cleaned_data["image"],
            created_by=request.user,
            auction_open=True)
                     
            cur_listing.save()
           
            return HttpResponseRedirect(reverse("active_listings"))
        else:
            return HttpResponse(listingForm.errors)
    else:        
        print(get_highest_bid_for_listing())
        bids_for_listing = get_highest_bid_for_listing()
        return render(request, 'auctions/activeListings.html',{
            "listings" : bids_for_listing
    })

# Show exactly one listing
def show_one_listing(request, **listing):
    pathList = request.path.split("/")  
    cur_listing = Listing.objects.get(id=pathList[len(pathList) - 1])
    cur_biddings = cur_listing.bids.all().order_by("amount") # Get all biddings from the auction
    isCreator = is_current_user_creator(request, cur_listing.created_by)
    
    # simply gets homepage
    if request.method == "GET":     
        comments = cur_listing.comments.all()
        print(comments)
        return render(request, 'auctions/listing.html', {
            "biddings": cur_biddings,
            "listing": cur_listing, 
            "bidform" : BidForm(),
            "commentform" : CommentForm(),
            "isCreator": isCreator,
            "winner" : get_winner(cur_biddings)==request.user,
            "comments" : comments
        })
        
    # closes current auction by setting boolean-field in listing-instance to 'false'
    elif request.method == "POST" and "closing" in request.POST: 
        cur_listing.auction_open = False
        cur_listing.save()
        return HttpResponseRedirect(reverse("listing", args=(pathList[len(pathList) - 1],)))
        
    # Saves comment for listing
    elif request.method == "POST" and "commenting" in request.POST: 
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            cur_comment = Comments(comment = commentForm.cleaned_data["comment"], auction_item = cur_listing, posted_by = request.user)
            cur_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(pathList[len(pathList) - 1],)))
    
    # posts listing and saves it to DB
    elif request.method == "POST":
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            bid = Bids(amount=bidform.cleaned_data["amount"], created_by=request.user, auction_item=cur_listing)
            if len(cur_biddings) == 0 and bid.amount > cur_listing.start_bid:
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=(pathList[len(pathList) - 1],)))
            elif len(cur_biddings) > 0 and cur_biddings[len(cur_biddings) - 1].amount < bid.amount:
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=(pathList[len(pathList) - 1],)))
            else:
                return HttpResponse("Bid too small!")
                
# Checks if current user created listing, by comparing it with field in database                
def is_current_user_creator(request, creator):
    if request.user == creator:
        return True
    else:
        return False
        
def watchlist(request):
    user_list = User.objects.all()
    
    if request.method == "GET":
        return HttpResponse("Under Construction")
        
    
    

# Gets the winner of an auction if it is closed
def get_winner(biddings):
    winner = ""
    offer = 0
    for bid in biddings:
        if bid.amount > offer:
            winner = bid.created_by
            offer = bid.amount

    return winner;
 
 
# goes through all biddings for an item, and get the highest one - used in procedure below    
def get_highest_offer(biddings):

    winner = ""
    offer = 0
    for bid in biddings:
        if bid.amount > offer:
            winner = bid.created_by
            offer = bid.amount

    current_highest_offer = {   
            "bidder": winner, 
            "amount":offer,
            "listing": None
            }
    print(current_highest_offer)
    return current_highest_offer

# gets a dictionary for all listings and its associated highest bidding and bidder.
def get_highest_bid_for_listing():

    all_listings = Listing.objects.all()
    listing_bid_bidder = []
    
    for listing in all_listings:
        bid_data = get_highest_offer(listing.bids.all().order_by("amount"))
        bid_data["listing"] = listing
        listing_bid_bidder.append(bid_data)
    
    return listing_bid_bidder
        
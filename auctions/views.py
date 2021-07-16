from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import UserCreationForm, ListingForm
from .util_datetime import current_datetime
from .models import ListingModel

UserModel = get_user_model()


def index(request):
    """List all active listings."""
    # Query all users saved in database (class.Manager.QuerySet)
    users = UserModel.objects.all()
    listings = []
    for user in users:
        cur_datetime = current_datetime()
        # Query all active listings (instance.RelatedManager.QuerySet)
        listings.extend(user.listings.filter(end_datetime__gt=cur_datetime))

    context = {'listings': listings}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Attempt to sign user in
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "auctions/login.html")

    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # Get fields or throw an error
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Create form & validate all user fields (.clean, .clear_field, validators)
        user_form = UserCreationForm(
            data={'username': username, 'email': email, 'phone': phone, 'password': password, 'password1': password, 'password2': confirmation})

        # Check form errors
        if user_form.is_valid():
            try:
                # Create new user via UserManager (password hashing, etc.) (doesn't validate passed user fields)
                user = UserModel.objects.create_user(
                    username, email, password, phone=phone)
                # TODO: user.full_clean()
                # Save created user in the database
                # or: save form model instance (data)
                user.save()
            except IntegrityError:
                messages.error(request, "Username already taken.")
                return render(request, "auctions/register.html")

            # Login into newly created user account
            login(request, user)
            messages.info(request, "Successfuly registred new account!")
            return HttpResponseRedirect(reverse("index"))
        else:
            # Render errors from all validated form fields
            for field_error, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, str(
                        field_error) + ': ' + str(error))
            return render(request, "auctions/register.html")
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    """Render full listing webpage (render listing model)."""
    # Get specific listing by primary key (listing id)
    listing = ListingModel.objects.get(pk=listing_id)

    return render(request, 'auctions/listings/listing.html', context={'listing': listing})


@login_required(login_url='/login/')
def add_listing(request):
    """Render form to create new listing."""
    if request.method == 'POST':
        # Fill form with data
        form = ListingForm(data=request.POST or None)
        # Validate form data
        if form.is_valid():
            # Loged in AUTH_USER_MODEL user instance
            user = request.user
            # Cleaned listing model instance (ModelForm specific)
            listing = form.save(commit=False)
            # Modify listing object
            listing.seller = user
            # Save listing object to database
            listing.save()
            # Redirect to home page
            return redirect(reverse('index'))
        else:
            # Custom (message-based) form errors rendering
            for field, errors in form.errors.items():
                # Iterate field and non-field (model) errors
                for err in errors:
                    messages.error(request, f'{field}: {err}')
            # Clear all errors to avoid dublicate rendering
            form.errors.clear()
            # Return populated form back to the client
            context = {'form': form}
            return render(request, 'auctions/listings/add.html', context)

    # Empty unbound form
    form = ListingForm()
    context = {'form': form}
    return render(request, "auctions/listings/add.html", context, content_type='text/html', status=200)


def owner_required(func):
    """Check weather user is the owner of requesting listing."""
    def inner(request, listing_id):
        l = ListingModel.objects.get(pk=listing_id)
        if l:
            if l.seller == request.user:
                return func(request, listing_id)
        raise Http404()
    return inner


@owner_required
def delete_listing(request, listing_id):
    """Delete listing with id=listing_id."""
    ListingModel.objects.get(pk=listing_id).delete()
    return redirect(reverse('index'))


@owner_required
def update_listing(request, listing_id):
    """Return form to edit created listing."""
    # Requesting listing
    l = ListingModel.objects.get(pk=listing_id)

    if request.method == 'POST':
        # Modify instance with new request data
        form = ListingForm(data=request.POST, instance=l)

        # Validate new data
        form.full_clean()
        if form.is_valid():
            # Commit changes to the instance
            form.save(commit=True)
            return redirect(reverse('index'))
        else:
            # Send errounius form with populated data
            return render(request, 'auctions/listings/update.html',
                          context={'listing': l, 'form': form})

    # Make bound (instance) form
    form = ListingForm(instance=l)
    return render(request, 'auctions/listings/update.html',
                  context={'listing': l, 'form': form})


@login_required
def my_listings(request):
    """Return listings of the requesting user."""
    # Get user listings
    listings = ListingModel.objects.filter(seller=request.user)

    context = {'listings': listings}
    return render(request, 'auctions/listings/listings.html', context)

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import UserCreationForm

UserModel = get_user_model()


def index(request):
    return render(request, "auctions/index.html")


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
            data={'username': username, 'email': email, 'phone': phone, 'password1': password, 'password2': confirmation})

        # Check form errors
        if user_form.is_valid():
            try:
                # Create new user via UserManager (password hashing, etc.) (doesn't validate passed user fields)
                user = UserModel.objects.create_user(
                    username, email, password, phone=phone)
                # Save created user in the database
                # or: save form model instance (data)
                user.save()
            except IntegrityError:
                messages.error(request, "Username already taken.")
                return render(request, "auctions/register.html")

            # Login into newly created user account
            login(request, user)
            messages.info(request, "Successfuly registred an account!")
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

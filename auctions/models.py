from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Models = database schema
# blank | null | default | unique


class User(AbstractUser):
    """
    Extends AbstractUser (username, password, email, First/Last name)
    with custom database schema (fields) and user creation/authentication form.
    """
    phone = PhoneNumberField(null=True, unique=True)


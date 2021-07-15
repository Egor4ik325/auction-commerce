from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .util_datetime import current_datetime

# Models = database schema
# blank | null | default | unique | primary_key
# verbose_name | help_text | editable


class User(AbstractUser):
    """
    Extends AbstractUser (username, password, email, First/Last name)
    with custom database schema (fields) and user creation/authentication form.
    """
    phone = PhoneNumberField(null=True, unique=True)


class ListingModel(models.Model):
    """
    Listing about 1 item at the auction.
    Belong to one user and can be bid by other users.
    """
    listing_id = models.AutoField(primary_key=True)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_("Item seller"),
        help_text=_("Enter creator of the listing"),
    )
    title = models.CharField(max_length=50)
    description = models.TextField(
        verbose_name=_("Listing description"), blank=True,
        help_text=_("Description of the selling item")
    )

    class Condition(models.TextChoices):
        NEW = 'NEW', 'New'
        RENTAL = 'RENTAL', 'Rental'
        USED = 'USED', 'Used'
        USED_GOOD = 'USED_GOOD', 'Used - Good'
        USED_VERYGOOD = 'USED_VERYGOOD', 'Used - Very Good'

    condition = models.CharField(
        verbose_name=_("Item condition"), max_length=50,
        choices=Condition.choices
    )
    starting_price = models.FloatField(_("Listing startign price (in $)"))
    start_datetime = models.DateTimeField(
        verbose_name=_("Listing start time"),
        help_text=_("Time when listing starts at the auction (>now)"),
        validators=[MinValueValidator(current_datetime())]
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Listing start time"),
        help_text=_("Time when listing ends at the auction (>now)"),
        validators=[MinValueValidator(current_datetime())]
    )

    def clean(self):
        """Custom model validation. clean() = pass in BaseModel."""
        if self.start_datetime > self.end_datetime:
            raise ValidationError({
                'start_datetime': _("Listing start time is greater than listing end time!")
            })

    def __str__(self):
        return f'{self.title}, {int(self.starting_price)}$'

    def is_started(self):
        """Determine weather listing is started or not."""
        cur_datetime = current_datetime()
        return cur_datetime > self.start_datetime

    def price():
        pass

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _  # ugettext_lazy not working
from phonenumber_field.modelfields import PhoneNumberField

from .util_datetime import current_datetime

# Models = database schema
# blank | null | default | unique | primary_key
# verbose_name | help_text | editable
# cascade | protect | set null


class User(AbstractUser):
    """
    Extends AbstractUser (username, password, email, First/Last name)
    with custom database schema (fields) and user creation/authentication form.
    """
    phone = PhoneNumberField(null=True, unique=True)

    # User-Listing watchlisted listings (M:M)
    # ManyToManyField = RelatedManager = QuerySet of ListingModel
    watchlist = models.ManyToManyField("auctions.ListingModel", verbose_name=_(
        "Watchlisted listings"), related_name="watchers")


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

    # Django enumeration type
    class Condition(models.TextChoices):
        # CONSTANT = (value, label)
        NEW = 'NEW', _('New')
        USED = 'USED', _('Used')
        RENTAL = 'RENTAL', _('Rental')
        USED_GOOD = 'USED_GOOD', _('Used - Good')
        USED_VERYGOOD = 'USED_VERYGOOD', _('Used - Very Good')

    # Retrieve human-readable name: instance.get_condition_display()
    condition = models.CharField(
        verbose_name=_("Item condition"), max_length=50,
        choices=Condition.choices
    )
    starting_price = models.FloatField(_("Listing startign price (in $)"))
    start_datetime = models.DateTimeField(
        verbose_name=_("Listing start time"),
        help_text=_("Time when listing starts at the auction (>now)"),
        # TODO: dynamic validator (current_datetime is constant): move to clean()
        validators=[MinValueValidator(current_datetime())]
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Listing star time"),
        help_text=_("Time when listing ends at the auction (>now)"),
        validators=[MinValueValidator(current_datetime())]
    )

    # User-defined listing active status
    closed = models.BooleanField(
        _("Listing before endtime closed"), default=False)

    photo_url = models.URLField(
        _("Internet photo URL for listing"), max_length=200, default="https://www.freeiconspng.com/uploads/no-image-icon-32.png")

    # Integer enum functional API
    Category = models.IntegerChoices("Category", [_("Antiques"), _("Art"), _("Baby"), _("Books"), _("Business & Industrial"), _("Cameras & Photo"), _("Cell Phones & Accessories"), _("Clothing, Shoes & Accessories"), _("Coins & Paper Money"), _("Collectibles"), _("Computers/Tablets & Networking"), _("Consumer Electronics"), _("Crafts"), _("Dolls & Bears"), _("DVDs & Movies"), _("Entertainment Memorabilia"), _(
        "Everything Else"), _("Gift Cards & Coupons"), _("Health & Beauty"), _("Home & Garden"), _("Jewelry & Watches"), _("Music"), _("Musical Instruments & Gear"), _("Pet Supplies"), _("Pottery & Glass"), _("Real Estate"), _("Specialty Services"), _("Sporting Goods"), _("Sports Mem, Cards & Fan Shop"), _("Stamps"), _("Tickets & Experiences"), _("Toys & Hobbies"), _("Travel"), _("Video Games & Consoles"), ])

    category = models.IntegerField(
        _("Listing category"), choices=Category.choices, null=True)

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

    # Listing statuses:
    # - starts (cur time before start)
    # - active (cur time between start/end)
    # - over (cur time after end)
    # - closed (_active = False)

    @property
    def active(self):
        """Return wether listing is still active."""
        cur_datetime = current_datetime()
        now = self.start_datetime < cur_datetime < self.end_datetime
        not_closed = not self.closed
        return now and not_closed

    @property
    def current_bid(self):
        """Return PRICE value of max listing bid - current bid."""
        bids = self.bids.all()
        if bids.exists():
            max_bid = max(bids, key=lambda b: b.bid)
            return max_bid.bid
        else:
            return self.starting_price

    @property
    def bid(self):
        """Same as self.current_bid but retuns actual BidModel instance."""
        bids = self.bids.all()
        if bids.exists():
            return max(bids, key=lambda b: b.bid)
        else:
            return None

    @property
    def bid_count(self):
        """Return number of bids accosiated with this listing."""
        return self.bids.count()


class BidModel(models.Model):
    """
    Bid - suggested listing/item price tag.
    Bid should be higher than previous bid.
    """
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE,
                                related_name='bids', verbose_name=_('Bidding listing'))
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='bids', verbose_name=_('Listing bidder'))
    bid = models.FloatField(_('Placed bid/price tag (in $)'),
                            help_text=_('Make sure that bid is greater than current bid.'))

    def __str__(self):
        return f'${self.bid}'

    def clean(self):
        """Custom bid model-wide validation."""
        # Skip validation if fields aren't available at form._post_clean -> model.clean()
        if hasattr(self, 'bidder') and hasattr(self, 'listing'):
            if self.bidder == self.listing.seller:
                raise ValidationError(
                    _("Listing owner can not be it's bidder."))


class CommentModel(models.Model):
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE,
                                related_name='comments',
                                verbose_name=_("Listing commented"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name=_("User commented"))
    comment = models.TextField(_("Comment text"))

    post_datetime = models.DateTimeField(
        _("Comment post date"), auto_now=False, auto_now_add=True)

    last_modified_datetime = models.DateTimeField(
        _("Date and time of last modification to the comment"), auto_now=True, auto_now_add=False)

    def __str__(self):
        """Render comment in template."""
        return self.comment

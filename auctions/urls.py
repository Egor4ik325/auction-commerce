from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Auth urls
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    # Listing CRUD urls
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/add/",
         views.add_listing, name="add_listing"),
    path("listings/delete/<int:listing_id>/",
         views.delete_listing, name="delete_listing"),
    path("listings/update/<int:listing_id>/",
         views.update_listing, name="update_listing"),
    path("listings/close/<int:listing_id>/",
         views.close_listing, name="close_listing"),
    path("listings/", views.my_listings, name="my_listings"),
    # Bid listing
    path('bid/<int:listing_id>/', views.bid, name="bid"),
    # Comment listing
    path('comment/<int:listing_id>/', views.comment, name="comment"),
    # Watch listing
    path('watch/<int:listing_id>/', views.watch, name="watch"),
    # Watchlist of listings
    path('watchlist/', views.watchlist, name='watchlist')
]

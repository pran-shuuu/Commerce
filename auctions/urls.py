from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/watchlist", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("categories", views.categories, name="category"),
    path("categories/<str:category_name>", views.category_view, name="category_view"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("closed_listings", views.close, name="closed")
]

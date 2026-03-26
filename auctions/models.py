from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
      name = models.CharField(max_length=64)
      def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing",)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="listing", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    @property
    def current_price(self):
        
        highest_bid = self.bids.order_by("-amount").first()
        if highest_bid:
            return highest_bid.amount
        return self.starting_bid

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    class Meta:
        ordering = ["-created_at"]

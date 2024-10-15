from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class User(AbstractUser):

    biografy = models.TextField(default='')
    # Talvez agregarle un icono al Usuario.

    def __str__(self):
          return f'User: {self.username}'

class Category(models.Model):
      name = models.CharField(max_length=50)
      image_url = models.URLField(blank=True, null=True)

      def __str__(self):
            return f'{self.name}'

class List(models.Model):
        
        title = models.CharField(max_length=100)
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='listings')
        starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
        description = models.TextField()
        winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won")
        is_active = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)
        image_url = models.URLField(blank=True, null=True)
        category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
        
      
        def __str__(self):
            return f'Title: {self.title}'
        
        def close_auction(self):
              hg_bid = self.bid_list.order_by('-amount').first()
              if hg_bid:
                  self.winner = hg_bid.user
              self.is_active = False
              self.save()                    

class Bid(models.Model):
      
      listing = models.ForeignKey(List, on_delete=models.CASCADE, related_name='bid_list') 
      amount = models.DecimalField(max_digits=9, decimal_places=2)
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_user')

      def clean(self):
            if self.amount < self.listing.starting_bid:
                  raise ValidationError(f'La oferta minima es {self.listing.starting_bid}.')
            
class Commentary(models.Model):

      author = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, related_name="author")
      listing = models.ForeignKey(List, on_delete=models.CASCADE, blank= True, null= True, related_name="comment_list")
      headline = models.CharField(max_length=255)
      comment = models.TextField()
      created_at = models.DateTimeField(default=timezone.now)

      def __str__(self):
            return f'{self.author} comment on {self.listing}'
      
class Watchlist(models.Model):

      user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="watchlist")
      listing = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True, related_name="watchlist_by")

      class Meta:
            unique_together = ('user', 'listing')
      
      def __str__(self):
            return f"{self.user.username} - {self.listing.title}"
        
    


        
      


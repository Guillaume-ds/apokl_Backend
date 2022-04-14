from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
  
class NFT(models.Model):    
  class SaleType(models.TextChoices):
    AUCTION = 'Auction'
    FIXED = 'Fixed price'
      
  class Blockchain(models.TextChoices):
    Ethereum = 'Ethereum'
    Polygon = 'Polygon'
    Other = 'Other'

  creator = models.CharField(max_length=500,default='Artiste Anonyme')
  slug = models.CharField(max_length=200, unique=True)
  title = models.CharField(max_length=150)   
  description = models.TextField(blank=True)
  sale_type = models.CharField(max_length=50, choices=SaleType.choices, default=SaleType.FIXED)
  blockchain = models.CharField(max_length=50, choices=Blockchain.choices, default=Blockchain.Polygon)
  price = models.IntegerField(default=1)
  rarity = models.IntegerField(default=1)    
  is_published = models.BooleanField(default=True)
  create_at = models.DateTimeField(default=now, blank=True)

  def __str__(self):
    return self.title
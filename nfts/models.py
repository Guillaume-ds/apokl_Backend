from django.db import models
from creators.models import Creator
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
  
class NFT(models.Model):    
  class SaleType(models.TextChoices):
    AUCTION = 'Auction'
    FIXED = 'Fixed price'
      
  class Blockchain(models.TextChoices):
    Ethereum = 'Ethereum'
    Polygon = 'Polygon'
    Other = 'Other'

  creator = models.ForeignKey(Creator, related_name="nfts", on_delete=models.CASCADE)
  title = models.CharField(max_length=150)   
  description = models.TextField(blank=True)
  tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
  sale_type = models.CharField(max_length=50, choices=SaleType.choices, default=SaleType.FIXED)
  blockchain = models.CharField(max_length=50, choices=Blockchain.choices, default=Blockchain.Polygon)
  price = models.IntegerField(default=1)
  rarity = models.IntegerField(default=1)  
  royalties = models.IntegerField(default=0)  
  tokenId = models.IntegerField(unique=True)   
  is_published = models.BooleanField(default=True)
  create_at = models.DateTimeField(default=now, blank=True)

  def __str__(self):
    return self.title
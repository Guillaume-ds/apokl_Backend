from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from profiles.models import Profile

def collection_directory_path(instance, filename):
    name = hash(instance.creator.name)
    return f'photos/collection/{name}/{filename}'.format(filename=filename)  

class Collection(models.Model):
    creator = models.ForeignKey(Profile, related_name="collections", on_delete=models.CASCADE,null=True, blank=True)
    slug = models.CharField(max_length=200, unique=True,default='Atest')
    name = models.CharField(max_length=200,default='')
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    nfts_array = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    picture = models.ImageField(upload_to=collection_directory_path, default='', max_length=1000, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']

class CollectionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

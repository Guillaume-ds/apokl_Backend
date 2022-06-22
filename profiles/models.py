from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField

def user_directory_path(instance, filename):
    name = hash(instance.name)
    return f'photos/profile/{name}/{filename}'.format(filename=filename)

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE,null=True, blank=True,unique=True)
    name = models.CharField(max_length=500,default='', blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=user_directory_path, default='', max_length=1000) 
    instagramUrl = models.CharField(max_length=500,default='', blank=True)
    twitterUrl = models.CharField(max_length=500,default='', blank=True)
    youtubeUrl = models.CharField(max_length=500,default='', blank=True)
    discordUrl = models.CharField(max_length=500,default='', blank=True)
    
    def __str__(self):
        return self.name
    
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


     

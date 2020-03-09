from django.db import models
from django.contrib.auth.models import User
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = CloudinaryField('image')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return str('f{self.user.username} Profile')

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


    def create_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
class Caption(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,default="user", related_name='posts')
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    # def get_absolute_url(self):
    #     return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.name} Caption'

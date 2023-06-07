from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


class SubscribedUsers(models.Model):
    """Newsletter subscribed users"""
    email = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)


class Profile(models.Model):
    """Add links and profile picture for users"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True,
                                    upload_to="images/profile_pic")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        """get absolute url for user new profile"""
        return reverse('home')


def create_user_profile_page(instance, created, **kwargs):
    """When a new users register he will be able to edit his profile"""
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile_page, sender=User)


class Category(models.Model):
    """We use this category to assign each user
    an id and allow them to access their edit profiles"""
    title = models.CharField(max_length=30)

    class Meta:
        """Category in Categories"""
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

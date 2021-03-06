from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio",max_length=300)
    email = models.EmailField(max_length=200,blank=True)
    country = models.CharField(max_length=200,blank=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars/')
    #install pillow
    #createmedia_root
    #find avatar.png
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    you_follow = models.ManyToManyField(User, blank=True, related_name='you_follow')
    slug = models.SlugField(unique=True,blank=True)
    exp = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_followers(self):
        return self.followers.all()

    def get_followers_no(self):
        return self.followers.all().count()

    def get_you_follow(self):
        return self.you_follow.all()

    def get_you_follow_no(self):
        return self.you_follow.all().count()

    def get_posts_num(self):
        return self.posts.all().count()

    def get_likes_num(self):
        likes = self.post_like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked+=1
        return total_liked

    def get_likes_received_post_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def get_likes_received_review_no(self):
        reviews = self.reviews.all()
        total_liked = 0
        for item in reviews:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name :
            to_slug = slugify(str(self.first_name)+str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else :
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('send', 'follow'),
    ('send', 'unfollow')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

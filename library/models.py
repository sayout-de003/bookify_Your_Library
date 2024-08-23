# library/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
# Customizing Genre display with GenreAdmin

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    extra_images = models.ImageField(upload_to='extra_images/', blank=True, null=True)
    description = models.TextField()
    published_date = models.DateField()
    genre = models.ManyToManyField('Genre')
    available = models.BooleanField(default=True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=True,
        null=True
    )
    epub_file = models.FileField(upload_to='epub/', blank=True, null=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'



#class Subscription(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    subscribed = models.BooleanField(default=False)
#    subscription_date = models.DateField(auto_now_add=True)



class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=14))
    returned_on = models.DateTimeField(null=True, blank=True)


# library/models.py


# library/models.py

# library/models.py

class CreativeWork(models.Model):
    CATEGORY_CHOICES = [
        ('painting', 'Painting'),
        ('dancing', 'Dancing'),
        ('article', 'Article'),
        ('research', 'Research Paper'),
    ]
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='article')
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    
    content = models.FileField(upload_to='creative_works/', default='creative_works/placeholder.jpg')

    def __str__(self):
        return self.title



# Model for comments on creative works
class Comment(models.Model):
    work = models.ForeignKey(CreativeWork, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.work}'

# Model for likes on creative works
class Like(models.Model):
    work = models.ForeignKey(CreativeWork, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('work', 'user')

    def __str__(self):
        return f'Like by {self.user} on {self.work}'


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=timezone.now() + timedelta(days=30))  # Setting the default
    active = models.BooleanField(default=True)

    def days_remaining(self):
        return (self.end_date - timezone.now().date()).days

    def __str__(self):
        return f"{self.user.username}'s Subscription"
    
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"    
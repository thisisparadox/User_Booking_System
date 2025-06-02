from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('POOL', 'Pools'),
        ('CABANA', 'Cabanas'),
        ('HUT', 'Beach Huts'),
        ('GUEST', 'Guest House'),
        ('CONF', 'Conference'),
        ('EXCL', 'Exclusive'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.CharField(max_length=6, choices=SERVICE_CATEGORIES)
    description = models.TextField()
    adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    child_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    senior_pwd_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    main_image = models.ImageField(upload_to='services/')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        db_table = "service"  # Custom table name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        db_table = "service_image"  # Custom table name

    def __str__(self):
        return f"Image for {self.service.name}"
    
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    featured_image = models.ImageField(upload_to='blog/featured/')
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    
    class Meta:
        ordering = ('-publish_date',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish_date.year, 
                                               self.publish_date.month, 
                                               self.publish_date.day, 
                                               self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.post.title}"

class BlogReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    post = models.ForeignKey(BlogPost, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    stay_date = models.DateField()
    booking_id = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_date',)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.post.title}"

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created_date',)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class ReviewImage(models.Model):
    review = models.ForeignKey(BlogReview, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/reviews/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for review by {self.review.user.username}"

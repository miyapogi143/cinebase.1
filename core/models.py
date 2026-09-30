from django.db import models
from django.utils.text import slugify
class Genre(models.Model):
    name=models.CharField(max_length=80); slug=models.SlugField(unique=True)
    def __str__(self): return self.name
class Movie(models.Model):
    title=models.CharField(max_length=180); slug=models.SlugField(unique=True,blank=True); year=models.PositiveIntegerField(); runtime_minutes=models.PositiveIntegerField(); synopsis=models.TextField(); poster=models.ImageField(upload_to='posters/',blank=True); trailer_url=models.URLField(blank=True); genres=models.ManyToManyField(Genre,blank=True); is_published=models.BooleanField(default=True); date_created=models.DateTimeField(auto_now_add=True)
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.title)
        super().save(*a,**kw)
    @property
    def avg_rating(self):
        vals=list(self.reviews.values_list('rating',flat=True)); return round(sum(vals)/len(vals),1) if vals else 0
    def __str__(self): return self.title
class CastMember(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='cast'); name=models.CharField(max_length=120); character=models.CharField(max_length=120); order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order','name']
class Review(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='reviews'); author_name=models.CharField(max_length=100); rating=models.PositiveIntegerField(); body=models.TextField(max_length=500); has_spoilers=models.BooleanField(default=False); date_created=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-date_created']
class WatchlistItem(models.Model):
    STATUS=(('want','Want to Watch'),('watched','Watched'))
    session_key=models.CharField(max_length=64); movie=models.ForeignKey(Movie,on_delete=models.CASCADE); status=models.CharField(max_length=10,choices=STATUS,default='want'); date_added=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=[('session_key','movie')]

from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[]
 operations=[
  migrations.CreateModel(name='Genre',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=80)),('slug',models.SlugField(unique=True))]),
  migrations.CreateModel(name='Movie',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=180)),('slug',models.SlugField(blank=True,unique=True)),('year',models.PositiveIntegerField()),('runtime_minutes',models.PositiveIntegerField()),('synopsis',models.TextField()),('poster',models.ImageField(blank=True,upload_to='posters/')),('trailer_url',models.URLField(blank=True)),('is_published',models.BooleanField(default=True)),('date_created',models.DateTimeField(auto_now_add=True)),('genres',models.ManyToManyField(blank=True,to='core.genre'))]),
  migrations.CreateModel(name='CastMember',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=120)),('character',models.CharField(max_length=120)),('order',models.PositiveIntegerField(default=0)),('movie',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='cast',to='core.movie'))]),
  migrations.CreateModel(name='Review',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('author_name',models.CharField(max_length=100)),('rating',models.PositiveIntegerField()),('body',models.TextField(max_length=500)),('has_spoilers',models.BooleanField(default=False)),('date_created',models.DateTimeField(auto_now_add=True)),('movie',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='reviews',to='core.movie'))]),
  migrations.CreateModel(name='WatchlistItem',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('session_key',models.CharField(max_length=64)),('status',models.CharField(choices=[('want','Want to Watch'),('watched','Watched')],default='want',max_length=10)),('date_added',models.DateTimeField(auto_now_add=True)),('movie',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='core.movie'))]),
  migrations.AlterUniqueTogether(name='watchlistitem',unique_together={('session_key','movie')}),
 ]

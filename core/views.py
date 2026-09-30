from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from .models import Movie,Genre,Review,WatchlistItem,CastMember

def sk(request):
    if not request.session.session_key: request.session.create()
    return request.session.session_key

def movie_list(request):
    qs=Movie.objects.filter(is_published=True).prefetch_related('genres','reviews').order_by('-date_created')
    q=request.GET.get('q','').strip(); genres=request.GET.getlist('genre'); min_year=request.GET.get('min_year'); max_year=request.GET.get('max_year'); min_rating=request.GET.get('min_rating')
    if q: qs=qs.filter(title__icontains=q)
    if genres: qs=qs.filter(genres__slug__in=genres).distinct()
    if min_year: qs=qs.filter(year__gte=min_year)
    if max_year: qs=qs.filter(year__lte=max_year)
    if min_rating:
        ids=[m.id for m in qs if m.avg_rating>=float(min_rating)]; qs=qs.filter(id__in=ids)
    context={'movies':qs,'genres':list(Genre.objects.values('id','name','slug')),'selected_genres':genres,'q':q,'min_year':int(min_year or 1990),'max_year':int(max_year or 2026),'min_rating':float(min_rating or 0),'watch_count':WatchlistItem.objects.filter(session_key=sk(request)).count()}
    if request.headers.get('HX-Request'):
        return render(request,'partials/movie_grid.html',context)
    return render(request,'movies/movie_list.html',context)

def movie_detail(request,slug):
    movie=get_object_or_404(Movie.objects.prefetch_related('genres','cast','reviews'),slug=slug,is_published=True)
    in_watch=WatchlistItem.objects.filter(session_key=sk(request),movie=movie).exists()
    return render(request,'movies/movie_detail.html',{'movie':movie,'in_watch':in_watch,'watch_count':WatchlistItem.objects.filter(session_key=sk(request)).count()})

def watchlist(request):
    items=list(WatchlistItem.objects.filter(session_key=sk(request)).select_related('movie').prefetch_related('movie__genres','movie__reviews'))
    data=[{'id':i.id,'title':i.movie.title,'year':i.movie.year,'rating':i.movie.avg_rating,'runtime':i.movie.runtime_minutes,'status':i.status,'slug':i.movie.slug} for i in items]
    return render(request,'movies/watchlist.html',{'items':items,'watch_json':data,'watch_count':len(items)})
@require_POST
def toggle_watchlist(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id); session=sk(request); item,created=WatchlistItem.objects.get_or_create(session_key=session,movie=movie)
    if not created: item.delete()
    count=WatchlistItem.objects.filter(session_key=session).count()
    resp=HttpResponse(''); resp['HX-Trigger']=f'{{"watchlist-changed":{{"count":{count},"added":{str(created).lower()}}}}}'; return resp
@require_POST
def remove_watchlist(request,item_id):
    WatchlistItem.objects.filter(id=item_id,session_key=sk(request)).delete(); return HttpResponse('')
@require_POST
def add_review(request,slug):
    movie=get_object_or_404(Movie,slug=slug); rating=int(request.POST.get('rating',0)); body=request.POST.get('body','').strip(); name=request.POST.get('author_name','Anonymous').strip() or 'Anonymous'; spoiler=request.POST.get('has_spoilers')=='on'
    if not 1<=rating<=10 or len(body)<10:
        return render(request,'partials/review_form.html',{'movie':movie,'error':'Choose 1–10 and write at least 10 characters.'})
    Review.objects.create(movie=movie,author_name=name,rating=rating,body=body,has_spoilers=spoiler)
    resp=render(request,'partials/reviews.html',{'movie':movie}); resp['HX-Trigger']='review-saved'; return resp

def movie_create(request):
    genres=list(Genre.objects.values('id','name','slug'))
    if request.method=='POST':
        title=request.POST.get('title','').strip(); synopsis=request.POST.get('synopsis','').strip(); year=request.POST.get('year') or 2026; runtime=request.POST.get('runtime') or 120
        if title and synopsis:
            from django.utils.text import slugify
            m=Movie.objects.create(title=title,slug=slugify(title),year=year,runtime_minutes=runtime,synopsis=synopsis,is_published=True)
            m.genres.set(request.POST.getlist('genres')); return redirect('movie_detail',slug=m.slug)
    return render(request,'movies/movie_form.html',{'genres':genres})

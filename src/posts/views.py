from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post,Post_Like,Review,Review_Like
from profiles.models import Profile
from .ML import predict as pr
from django.http import *
from django.core.files.storage import FileSystemStorage

# Create your views here.
def post_review_create_list_view(request):
    user = request.user
    posts = Post.objects.all()
    reviews = Review.objects.all()
    profile = Profile.objects.get(user=request.user)

    context ={
        'profile':profile,
        'posts':posts,
        'reviews':reviews,
    }

    return render(request,'posts/main.html',context)


def like_unlike_post_view(request):
    user = request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id1')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else :
            post_obj.liked.add(profile)

        like, created = Post_Like.objects.get_or_create(user=profile,post=post_obj)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else :
                like.value = 'Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()
        a = str(request.META.get('HTTP_REFERER'))
        a = a[22:]
        if 'posts/book/' in a:
            return HttpResponseRedirect(reverse('posts:show-book',kwargs={'id':post_obj.id}))
    return redirect('posts:main-post-view')

def create_post_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method=='POST':
        book_image = request.FILES['bookimage']
        fs = FileSystemStorage()
        fs.save(book_image.name, book_image)
        book_name = request.POST.get('p_name')
        book_author = request.POST.get('p_author')
        caption = request.POST.get('p_caption')

        post, created = Post.objects.get_or_create(author=profile,book_image=book_image.name,book_name=book_name,book_author=book_author,caption=caption)
        post.save()

    return redirect('posts:main-post-view')



def create_review_view(request):
    user = request.user

    if request.method=='POST':
        profile = Profile.objects.get(user=user)
        post_id = request.POST.get('post_id2')
        post_obj = Post.objects.get(id=post_id)
        review_body = request.POST.get('review_body')
        expertivity= pr.calc_expertivity(profile.get_followers_no(),profile.get_likes_received_review_no())
        review, created = Review.objects.get_or_create(user=profile,body=review_body,post_id=post_id,expertivity=expertivity)
        review.save()
        profile.exp += 2
        profile.save()

        a = str(request.META.get('HTTP_REFERER'))
        a = a[22:]
        if 'posts/book/' in a:
            return HttpResponseRedirect(reverse('posts:show-book',kwargs={'id':post_obj.id}))

    return redirect('posts:main-post-view')

def like_unlike_review_view(request):
    user = request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id3')
        review_id = request.POST.get('review_id')
        post_obj = Post.objects.get(id=post_id)
        review_obj = Review.objects.get(id=review_id)
        profile = Profile.objects.get(user=user)
        review_author = Profile.objects.get(id=review_obj.user.id)

        if profile in review_obj.liked.all():
            review_obj.liked.remove(profile)
        else :
            review_obj.liked.add(profile)

        like, created = Review_Like.objects.get_or_create(user=profile,review=review_obj)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
                review_author.exp -= 1
            else:
                like.value='Like'
                review_author.exp += 1
        else:
            like.value='Like'
            review_author.exp += 1

        like.save()
        review_obj.save()
        review_author.save()
        review_obj.expertivity = pr.calc_expertivity(review_author.get_followers_no(),review_author.get_likes_received_review_no())
        review_obj.save()
        a = str(request.META.get('HTTP_REFERER'))
        a = a[22:]

        if 'posts/book/' in a:
            return HttpResponseRedirect(reverse('posts:show-book',kwargs={'id':post_obj.id}))
    return redirect('posts:main-post-view')

def delete_post_view(request):
    user = request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id4')
        posts = Post.objects.all()
        if not post_id:
            return redirect('posts:main-post-view')
        post_obj = Post.objects.get(id=post_id)

        if post_obj in posts:
            Post.objects.filter(id=post_id).delete()

    return redirect('posts:main-post-view')

def delete_review_view(request):
    user = request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id')
        review_id = request.POST.get('review_id')
        reviews = Review.objects.all()


        if not post_id:
            return redirect('posts:main-post-view')
        elif not review_id:
            return redirect('post:main-post-view')

        review_obj = Review.objects.get(id=review_id)
        re_auth = Profile.objects.get(id=review_obj.user.id)

        if review_obj in reviews:
            re_auth.exp = re_auth.exp -2
            Review.objects.filter(id=review_id).delete()

    return redirect('posts:main-post-view')

def show_book_view(request, id):
    book = Post.objects.get(id=id)
    reviews = Review.objects.all()
    profile = Profile.objects.get(user=request.user)
    context ={
        'profile':profile,
        'posts':book,
        'reviews':reviews,
    }
    return render(request,'posts/search_book.html',context)

def search_book_list_view(request):
    user = request.user
    if request.method=='POST':
        flag=0
        book_name = request.POST.get('book_name')
        all_books = Post.objects.all()
        for book in all_books:
            if book_name in book.book_name.lower():
                book_found = book
                flag=1
        reviews = Review.objects.all()
        profile = Profile.objects.get(user=request.user)

        if flag:
            context ={
                'profile':profile,
                'posts':book_found,
                'reviews':reviews,
            }

            return HttpResponseRedirect(reverse('posts:show-book',kwargs={'id':book_found.id}))
            #return render(request,'posts/search_book.html',context)
        else :
            message = "book "+ book_name +" not found"
            context ={
                'message':message,
            }
            return render(request,'notfound.html',context)

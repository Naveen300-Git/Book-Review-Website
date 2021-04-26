from django.shortcuts import render,redirect
from .models import Profile,Relationship
from posts.models import Review
from posts.ML import predict as pr
from .forms import ProfileModelForm
from django.contrib.auth.models import User

# Create your views here.
def my_profile_view(request):
    obj = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,request.FILES or None,instance=obj)
    confirm = False
    if request.method =='POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'obj': obj,
        'form':form,
        'confirm':confirm
    }
    return render(request,'profiles/myprofile.html',context)

def my_followers_list_view(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    followers = profile.get_followers()
    content = {
        'obj':followers,
        'profile':profile,
    }
    return render(request,'profiles/followers.html',content)

def you_follow_list_view(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    you_follow = profile.get_you_follow()
    content = {
        'obj':you_follow,
        'profile':profile,
    }
    return render(request,'profiles/you_follow.html',content)

def all_users_list_view(request):
    user=  request.user
    notfound = True
    searched = False
    all_users = Profile.objects.all()
    if request.method=='POST':
        searched = True
        user_name = request.POST.get('user')
        for profile in all_users:
            if user_name in str(profile.user).lower():
                notfound = False
            elif user_name in profile.slug.lower():
                notfound = False
            if not notfound:
                user_content = {
                    'obj':profile,
                    'profile':Profile.objects.get(user=request.user),
                }
                return render(request,'profiles/profile_view.html',user_content)

    content = {
        'profiles':all_users,
        'user_found':notfound,
        'searched':searched,
    }
    return render(request, 'profiles/users_list.html',content)

def view_profile_view(request):
    user = request.user
    if request.method=='POST':
        id = request.POST.get('profile_id')
        profile = Profile.objects.get(user=User.objects.get(username=id))
        content = {
            'obj':profile,
            'profile':Profile.objects.get(user=request.user),
        }
        return render(request,'profiles/profile_view.html',content)
    else:
        return render(request,'profiles/profile_view.html')

def specific_profile_view(request):
    user = request.user
    if request.method=='POST':
        id = request.POST.get('profile_id')
        profile = Profile.objects.get(slug=id)
        content = {
            'obj':profile,
            'profile':Profile.objects.get(user=request.user),
        }
        return render(request,'profiles/profile_view.html',content)

def register(request):
    args={
        'uname':'',
        'u_already_exists':False,
    }
    if request.method=='POST':
        existing = True
        username = request.POST.get('username')
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            existing = False

        args={
            'uname':username,
            'u_already_exists':existing,
        }
        if password1!=password2:
            return render(request,'accounts/main_signup.html',args)

        if existing:
            return render(request, 'accounts/main_signup.html',args)

        User.objects.create_user(username=username,password=password1)
            #return render(request,'accounts/signup.html',args)
        return redirect('profiles:login')
    else :
        return render(request,'accounts/main_signup.html',args)

def follow_unfollow_view(request):
    user = request.user
    if request.method=='POST':
        p_id = request.POST.get('profile_id')
        from_profile = Profile.objects.get(user=user)
        to_profile = Profile.objects.get(id=p_id)
        if to_profile in from_profile.get_you_follow():
            status='unfollow'
        else:
            status='follow'

        relation, created = Relationship.objects.get_or_create(sender=from_profile,receiver=to_profile,status=status)
        if not created:
            from_profile.you_follow.remove(to_profile.user)
            to_profile.followers.remove(from_profile.user)
            Relationship.objects.filter(sender=from_profile,receiver=to_profile).delete()
            from_profile.save()
            to_profile.save()
        else:
            relation.save()

        reviews = Review.objects.all()
        for re in reviews:
            if to_profile.user==re.user.user:
                re.expertivity = pr.calc_expertivity(to_profile.get_followers_no(),to_profile.get_likes_received_review_no())
                re.save()

        return redirect('profiles:my-profile-view')

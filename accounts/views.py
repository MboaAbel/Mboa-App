from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserAddressForm
from django.shortcuts import render, redirect
from .models import Post, LikePost, FollowersCount,UserAddress
from itertools import chain
import random
User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f"You've  Made a Great Choice, Thanks For Joining MboaEx We Generating Your Mboa-ID . "
                    f'Your Super Mboa-ID  is {user.account.account_no}.   '
                    f'Stay Belong and Enjoy the Experience'
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'
    
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


@login_required(login_url='/accounts/login')
def Sure_kuleft(request):
    if request.user.is_anonymous:
        return redirect('user_login.html')
    return render(request, 'accounts/user_logout.html')


@login_required(login_url='/accounts/login')
def index(request):
    
    user_profile = UserAddress.objects.get(user=request.user)
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=id)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    
    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(user=user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = UserAddress.objects.filter(user=request.user)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    
    username_profile = []
    username_profile_list = []
    
    for users in final_suggestions_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = UserAddress.objects.filter(user=request.user)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))
    
    return render(request, 'blog/index.html', {'user_profile': user_profile, 'posts': feed_list,
                                               'suggestions_username_profile_list': suggestions_username_profile_list[
                                                                                    :4]})


@login_required(login_url='/accounts/login')
def upload(request):
    if request.method == 'POST':
        user = UserAddress.Name
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(username=user, image=image, caption=caption)
        new_post.save()
        
        return render(request, 'blog/profile.html')
    else:
        return render(request, 'blog/blog.html')


@login_required(login_url='/accounts/login')
def search(request):
    user_profile = UserAddress.objects.get(user=request.user)
    
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        
        username_profile = []
        username_profile_list = []
        
        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = UserAddress.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'blog/search.html',
                  {'user_profile': user_profile})


@login_required(login_url='/accounts/login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='/accounts/login')
def profile(request, pk):
    user_object = User.objects.get(slug=pk)
    user_profile = UserAddress.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'blog/profile.html', context)


@login_required(login_url='/accounts/login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')


@login_required(login_url='/accounts/login')
def settings(request):
    user_profile = UserAddress.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return render(request, 'fx/setting.html')
    return render(request, 'fx/ex_setting.html', {'user_profile': user_profile})


from django.shortcuts import render,redirect

from web.forms import SignUpForm,LoginForm,PostForm,ProfileForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Userprofile,Posts,Comments
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# Create your views here.


def signin_requird(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

dec = [signin_requird,never_cache]



class SignupView(View):

    def get(self,request,*args,**kwargs):
        form = SignUpForm()
        return render(request,'signup.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup')
        else:
            return render(request,'signup.html',{'form':form})


class SigninView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    def post (self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            # print(uname,pwd)
            usr = authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect('index')
            else:
                return render(request,'login.html',{'form':form})


@method_decorator(dec,name='dispatch')
class Indexview(CreateView,ListView):
    model = Posts
    form_class = PostForm
    template_name = 'index.html'
    success_url = reverse_lazy('index')
    context_object_name = 'posts'

    def form_valid(self, form): 
        form.instance.user=self.request.user
        return super().form_valid(form)  #super means parent class


    def get_queryset(self):
        return Posts.objects.all().order_by('-created_date')


@method_decorator(dec,name='dispatch')
class ProfileCreateView(CreateView):
    form_class = ProfileForm
    model = Userprofile
    template_name = 'profile-create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     form = ProfileForm()
    #     return render(request,'profile-create.html',{'form':form})

    # def post(self,request,*args,**kwargs):
    #     form = ProfileForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         usr=User.objects.get(username=request.user.username)
    #         form.instance.user=usr
    #         form.save()
    #         return redirect('profile-view')
    #     else:
    #         return render(request,'index.html',{'form':form})


@method_decorator(dec,name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Userprofile
    form_class=ProfileForm
    template_name = 'profile-edit.html'
    success_url= reverse_lazy('index')

    pk_url_kwarg='id'  #in updateview id is expected as pk so we override pk to id


@method_decorator(dec,name='dispatch')
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Posts.objects.get(id=id).delete()
        return redirect('index')

@method_decorator(dec,name='dispatch')
class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        aid=kwargs.get('id')
        post = Posts.objects.get(id=aid)
        com = request.POST.get('comment')
        usr = request.user
        Comments.objects.create(user=usr,posts=post,comment=com)
        return redirect('index')

@method_decorator(dec,name='dispatch')
class LikeView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        com = Comments.objects.get(id=id)
        com.likes.add(request.user)
        com.save()
        return redirect('index')

@method_decorator(dec,name='dispatch')
class LikeRemoveView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        com = Comments.objects.get(id=id)
        com.likes.remove(request.user)
        com.save()
        return redirect('index')




class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')



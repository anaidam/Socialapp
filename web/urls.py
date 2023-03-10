from django.urls import path
from web import views



urlpatterns = [
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('login/',views.SigninView.as_view(),name='signin'),
    path('home/',views.Indexview.as_view(),name='index'),
    path('profile-add/',views.ProfileCreateView.as_view(),name='profile-add'),
    path('profile/<int:id>/change',views.ProfileUpdateView.as_view(),name='profile-edit'),
    path('posts/<int:pk>/remove',views.PostDeleteView.as_view(),name='post-delete'),
    path('posts/<int:id>/comments/add',views.AddCommentView.as_view(),name='add-comment'),
    path('comments/<int:id>/like/add',views.LikeView.as_view(),name='like'),
    path('comments/<int:id>/like/remove',views.LikeRemoveView.as_view(),name='like-remove'),
    path('signout',views.SignoutView.as_view(),name='signout')
    

]
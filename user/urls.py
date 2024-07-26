from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views
router=DefaultRouter()
router.register(r'list',views.UserViewSet)
router.register(r'profile',views.UserProfileViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('register/', views.UserRegistrationsApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('deposit/', views.DepositAPIView.as_view(), name='deposit'),  
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),        
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
]
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
router=DefaultRouter()
router.register(r'list',views.UserViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('register/', views.UserRegistrationsApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('deposit/', views.DepositAPIView.as_view(), name='deposit'), 
    path('UserProfileList/',views.UserProfileList.as_view(),name='UserProfileList'),
    path('UserProfileDetail/<int:user_id>/',views.UserProfileDetail.as_view(),name='UserProfileDetail'), 
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),        
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('petlist', views.PetViewSet, basename='petlist')
router.register('list', views.PetViewSetwithoutPagination, basename='list')
router.register('sex', views.SexViewSet, basename='sex')
router.register('species', views.SpeciesViewSet, basename='species')
router.register('color', views.ColorViewSet, basename='color')
router.register('breed', views.BreedViewSet, basename='breed')
router.register('size', views.SizeViewSet, basename='size')
router.register('status', views.StatusViewSet, basename='status')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('adopt/', views.AdoptAPIView.as_view(), name='adopt-pet'),
    path('<int:pet_id>/reviews/', views.ReviewCreateView.as_view(), name='create-review'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
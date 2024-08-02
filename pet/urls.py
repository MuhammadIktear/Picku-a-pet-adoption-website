from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('petlist', views.PetViewSet, basename='petlist')
router.register('sex', views.SexViewSet, basename='sex')
router.register('species', views.SpeciesViewSet, basename='species')
router.register('color', views.ColorViewSet, basename='color')
router.register('breed', views.BreedViewSet, basename='breed')
router.register('size', views.SizeViewSet, basename='size')
router.register('status', views.StatusViewSet, basename='status')

urlpatterns = [
    path('', include(router.urls)),
    path('adopt/<int:pet_id>/', views.AdoptPetAPIView.as_view(), name='adopt'),
    path('PetReviewList/',views.PetReviewList.as_view(),name='PetReviewList'),
]
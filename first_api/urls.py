from django.urls import path, include
from rest_framework.routers import DefaultRouter

from first_api import views


router = DefaultRouter() ## router use with viewset 
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')

## do not need to define basename due to use query set in UserProfileViewSet
## queryset all ready provide a basename
router.register(r'profile',views.UserProfileViewSet)
router.register(r'feed',views.UserProfileFeedViewSet)
router.register(r'company',views.CompanyViewSet)
router.register(r'all_village',views.VillageViewSet)

# Home Secure main routers


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
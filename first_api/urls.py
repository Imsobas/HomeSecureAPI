from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from first_api import views


router = DefaultRouter() ## router use with viewset 
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')

## do not need to define basename due to use query set in UserProfileViewSet
## queryset all ready provide a basename
router.register(r'profiles',views.UserProfileViewSet)
router.register(r'feeds',views.UserProfileFeedViewSet)
router.register(r'companys',views.CompanyViewSet)
router.register(r'villages',views.VillageViewSet)
router.register(r'homes',views.HomeViewSet)




## Binding URL

## village 
villages_pk_zones = views.VillageViewSet.as_view({
    'get': 'villages_pk_zones'
})
villages_pk_zones_pk = views.VillageViewSet.as_view({
    'get': 'villages_pk_zones_pk'
})

# Home Secure main routers
urlpatterns = [
    ##village
    path('villages/<int:pk>/zones/', villages_pk_zones ,name='villages_pk_zones'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/', villages_pk_zones_pk ,name='villages_pk_zones_pk'),

    path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
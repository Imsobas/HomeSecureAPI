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


get_villages_pk_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones'
})
get_villages_pk_zones_pk = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones_pk'
})
get_villages_zones_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_zones_homes'
})

# Home Secure main routers
urlpatterns = [
    ##zone function
    path('villages/<int:pk>/zones/', get_villages_pk_zones ,name='villages_pk_zones'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/', get_villages_pk_zones_pk ,name='villages_pk_zones_pk'),

    ##home function 
    path('villages/zones/homes/', get_villages_zones_homes, name='get_villages_zones_homes'),

    path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
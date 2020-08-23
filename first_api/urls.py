from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from first_api import views


router = DefaultRouter() ## router use with viewset 
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')

## do not need to define basename due to use query set in UserProfileViewSet
## queryset all ready provide a basename
router.register(r'profiles',views.UserProfileViewSet)
# router.register(r'feeds',views.UserProfileFeedViewSet)
router.register(r'companys',views.CompanyViewSet)
router.register(r'villages',views.VillageViewSet)
router.register(r'homes',views.HomeViewSet)
router.register(r'zones',views.ZoneViewSet)
router.register(r'general_users',views.GeneralUserViewSet)


## Binding URL

## village
get_villages_active = views.VillageViewSet.as_view({
    'get': 'get_villages_active'
})

get_villages_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_zones'
})

## zone
get_villages_pk_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones'
})
get_villages_pk_zones_pk = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones_pk'
})


## home
get_villages_zones_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_zones_homes'
})

get_villages_pk_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_pk_homes'
})

get_villages_pk_zones_pk_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_homes'
})

get_homes_active = views.HomeViewSet.as_view({
    'get': 'get_homes_active'
})

##general users

get_general_users_active = views.GeneralUserViewSet.as_view({
    'get': 'get_general_users_active'
})

get_villages_pk_zones_pk_general_users = views.GeneralUserViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_general_users'
})


# Home Secure main routers
urlpatterns = [

    ##Note: if most end point unless viewset default especially list function will return if is_active = true, 

    ## village end point 
    path('villages_active/',get_villages_active,name='get_villages_active'),

    ##zone end point
    path('villages/zones/', get_villages_zones ,name='villages_zones'),
    path('villages/<int:pk>/zones/', get_villages_pk_zones ,name='villages_pk_zones'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/', get_villages_pk_zones_pk ,name='villages_pk_zones_pk'),
    
    ##home end point
    path('homes_active/', get_homes_active, name='get_homes_active'),
    path('villages/<int:village_pk>/homes/',get_villages_pk_homes, name='get_villages_pk_homes'),
    path('villages/zones/homes/', get_villages_zones_homes, name='get_villages_zones_homes'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/homes/', get_villages_pk_zones_pk_homes, name='get_villages_pk_zones_pk_homes'),

    ##general user end point 
    path('general_users_active/', get_general_users_active, name='get_general_users_active'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/general_users/', get_villages_pk_zones_pk_general_users, name='get_villages_pk_zones_pk_general_users'),
    
    

    # path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
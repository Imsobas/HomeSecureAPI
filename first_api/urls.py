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
router.register(r'checkpoints',views.CheckpointViewSet)
router.register(r'works',views.WorkViewSet)
router.register(r'secure_guards',views.SecureGuardViewSet)
router.register(r'qrcodes',views.QrCodeViewSet)
router.register(r'settings',views.SettingViewSet)
# router.register(r'point_inspections',views.PointInspectionViewSet)
router.register(r'point_observation',views.PointObservationViewSet)
router.register(r'point_observation_point_list',views.PointObservationPointListViewSet)
router.register(r'point_observation_record',views.PointObservationRecordViewSet)
router.register(r'maintenance_fee_period',views.MaintenanceFeePeriodViewSet)
router.register(r'maintenance_fee',views.MaintenanceFeeViewSet)

## Binding URL

## village
get_villages_active = views.VillageViewSet.as_view({
    'get': 'get_villages_active'
})

get_villages_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_zones'
})

get_companys_pk_villages = views.VillageViewSet.as_view({
    'get': 'get_companys_pk_villages'
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

get_villages_pk_general_users = views.GeneralUserViewSet.as_view({
    'get': 'get_villages_pk_general_users'
})

## user

get_profiles_check  = views.UserProfileViewSet.as_view({
    'get': 'get_profiles_check'
})

## checkpoint 

get_villages_pk_checkpoints = views.CheckpointViewSet.as_view({
    'get': 'get_villages_pk_checkpoints'
})

get_villages_pk_zones_pk_checkpoints = views.CheckpointViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_checkpoints'
})

## work 

get_villages_pk_works = views.WorkViewSet.as_view({
    'get': 'get_villages_pk_works'
})

## qrcodes 

get_qrcodes_homedetails = views.QrCodeViewSet.as_view({
    'get': 'get_qrcodes_homedetails'
})

get_villages_location_pk = views.VillageViewSet.as_view({
    'get': 'get_villages_location_pk'
})

## qr_inside_screen services
get_villages_pk_qrcodes = views.QrCodeViewSet.as_view({
    'get': 'get_villages_pk_qrcodes'
})

## qr_user_screen services
get_villages_pk_homes_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_villages_pk_homes_pk_qrcodes'
})

## qr_exit_screen services
get_villages_pk_contents_content_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_villages_pk_contents_content_qrcodes'
})

## qr_history_screen services (filter by village, zone, date) 
get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes'
})
## qr_history_screen services (filter by village, zone)
get_historyservice_list_villages_pk_zones_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_zones_pk_qrcodes'
})

## qr_history_screen services (filter by village, date) 
get_historyservice_list_villages_pk_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_dates_year_month_day_qrcodes'
})

## qr_history_screen services (filter by village) 
get_historyservice_list_villages_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_qrcodes'
})

## Test 
testObservation = views.PointObservationViewSet.as_view({
    'post': 'testObservation' 
})

## use for retrieve checked status in point observation screen
pointobservation_fetch_record_checked_pk = views.PointObservationViewSet.as_view({
    'get': 'pointobservation_fetch_record_checked_pk'
})

pointobservation_fetch_record = views.PointObservationViewSet.as_view({
    'get': 'pointobservation_fetch_record'
})

fetch_pointobservation = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation'
})

fetch_pointobservation_null_work = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_null_work'
})

fetch_pointobservation_null_zone = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_null_zone'
})

fetch_pointobservation_null_zone_null_work = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_null_zone_null_work'
})

fetch_pointobservationrecord_percent = views.PointObservationRecordViewSet.as_view({
    'get': 'fetch_pointobservationrecord_percent'
})

fetch_pointobservationrecord_timeslots_percent = views.PointObservationRecordViewSet.as_view({
    'get': 'fetch_pointobservationrecord_timeslots_percent'
})

fetch_pointobservationrecord_pointlist = views.PointObservationPointListViewSet.as_view({
    'get': 'fetch_pointobservationrecord_pointlist'
})

fetch_pointobservation_update_work = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_update_work'
})

fetch_pointobservation_update_zone = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_update_zone'
})

## MaintenanceFeePeriod

get_villages_pk_maintenance_fee_period = views.MaintenanceFeePeriodViewSet.as_view({
    'get': 'get_villages_pk_maintenance_fee_period'
})

# Home Secure main routers
urlpatterns = [

    ##Note: if most end point unless viewset default especially list function will return if is_active = true, 

    ## village end point 
    path('villages_active/',get_villages_active,name='get_villages_active'),
    path('companys/<int:pk>/villages/',  get_companys_pk_villages, name='  get_companys_pk_villages'), ## conpany adapted
    path('villages/location/<int:villagePk>', get_villages_location_pk, name='get_villages_location_pk'),

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
    path('villages/<int:village_pk>/general_users/', get_villages_pk_general_users, name='get_villages_pk_general_users'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/general_users/', get_villages_pk_zones_pk_general_users, name='get_villages_pk_zones_pk_general_users'),
    
    ##user
    path('profiles_check/<str:new_username>/', get_profiles_check, name='get_profiles_check'),
    
    ##checkpoint 
    path('villages/<int:village_pk>/checkpoints/', get_villages_pk_checkpoints, name='get_villages_pk_checkpoints'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/checkpoints/', get_villages_pk_zones_pk_checkpoints, name='get_villages_pk_zones_pk_checkpoints'),

    ##work 
    path('villages/<int:pk>/works/', get_villages_pk_works ,name='get_villages_pk_works'),

    ##qr
    path('qrcodes/homedetails/<int:number>', get_qrcodes_homedetails ,name='get_qrcodes_homedetails'),
    path('villages/<int:village_pk>/qrcodes/', get_villages_pk_qrcodes, name = 'get_villages_pk_qrcodes'),
    path('villages/<int:village_pk>/homes/<int:home_pk>/qrcodes/', get_villages_pk_homes_pk_qrcodes, name = 'get_villages_pk_homes_pk_qrcodes'),
    path('villages/<int:village_pk>/contents/<str:content>/qrcodes/', get_villages_pk_contents_content_qrcodes, name = 'get_villages_pk_contents_content_qrcodes'),
    path('historyservice/list/villages/<int:village_pk>/zones/<int:zone_pk>/dates/<int:year>/<int:month>/<int:day>/qrcodes/', get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes, name = 'get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes'),
    path('historyservice/list/villages/<int:village_pk>/zones/<int:zone_pk>/qrcodes/', get_historyservice_list_villages_pk_zones_pk_qrcodes, name = 'get_historyservice_list_villages_pk_zones_pk_qrcodes'),
    path('historyservice/list/villages/<int:village_pk>/dates/<int:year>/<int:month>/<int:day>/qrcodes/', get_historyservice_list_villages_pk_dates_year_month_day_qrcodes, name = 'get_historyservice_list_villages_pk_dates_year_month_day_qrcodes'),
    path('historyservice/list/villages/<int:village_pk>/qrcodes/', get_historyservice_list_villages_pk_qrcodes, name = 'get_historyservice_list_villages_pk_qrcodes'),


    #test 
    path('pointobservation_create_service/', testObservation ,name='testObservation'),
    path('pointobservation_fetch_record_checked_pk/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/timeslots/<int:timeslot>/', pointobservation_fetch_record_checked_pk ,name='pointobservation_fetch_record_checked_pk'),
    path('pointobservation_fetch_record/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/timeslots/<int:timeslot>/', pointobservation_fetch_record ,name='pointobservation_fetch_record'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/dates/<str:date>/', fetch_pointobservation ,name='fetch_pointobservation'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/<int:zone_pk>/works/null/dates/<str:date>/', fetch_pointobservation_null_work ,name='fetch_pointobservation_null_work'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/null/works/<int:work_pk>/dates/<str:date>/', fetch_pointobservation_null_zone ,name='fetch_pointobservation_null_zone'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/null/works/null/dates/<str:date>/', fetch_pointobservation_null_zone_null_work ,name='fetch_pointobservation_null_zone_null_work'),
    path('fetch_pointobservationrecord/pointobservation/<int:pointobservation_pk>/timeslots/<int:timeslot>/percent/',fetch_pointobservationrecord_percent,name='fetch_pointobservationrecord_percent'),
    path('fetch_pointobservationrecord/pointobservation/<int:pointobservation_pk>/timeslots/percent/', fetch_pointobservationrecord_timeslots_percent,name='fetch_pointobservationrecord_timeslots_percent'),
    path('fetch_pointobservationrecord_pointlist/pointobservation/<int:pointobservation_pk>/timeslots/<int:timeslot>/checkpoint_status/', fetch_pointobservationrecord_pointlist,name='fetch_pointobservationrecord_pointlist'),
    path('fetch_pointobservationrecord_updatework/works/<int:work_pk>/', fetch_pointobservation_update_work,name='fetch_pointobservation_update_work'),
    path('fetch_pointobservationrecord_updatework/zones/<int:zone_pk>/', fetch_pointobservation_update_zone,name='fetch_pointobservation_update_zone'),

    ## maintenancefeeperiod
    path('villages/<int:village_pk>/maintenance_fee_period/', get_villages_pk_maintenance_fee_period,name='get_villages_pk_maintenance_fee_period'),
    
    

    
    # path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
from django.urls import path,re_path,include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from first_api import views
from django.conf.urls import include, url
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet, FCMDeviceViewSet

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
router.register(r'maintenance_fee_record',views.MaintenanceFeeRecordViewSet)
router.register(r'votetopic',views.VoteTopicViewSet)
router.register(r'votechoice',views.VoteChoiceViewSet)
router.register(r'voterecord',views.VoteRecordViewSet)
router.register(r'problem',views.ProblemViewSet)
router.register(r'secure_location',views.SecureLocationViewSet)
router.register(r'secure_work',views.SecureWorkViewSet)
router.register(r'checkin_checkpoints',views.CheckinCheckpointViewSet)
router.register(r'working_records',views.WorkingRecordViewSet)
router.register(r'notification',views.NotificationViewSet)
router.register(r'devices', views.CustomFCMDeviceViewSet)
router.register(r'managers', views.ManagerViewSet)
router.register(r'votecount', views.VoteCountViewSet)

## Binding URL

## profile 
get_profiles_detail = views.UserProfileViewSet.as_view({
    'get': 'get_profiles_detail'
})

create_username_with_usertype = views.UserProfileViewSet.as_view({
    'post' : 'create_username_with_usertype'
})

change_p = views.UserProfileViewSet.as_view({
    'post' : 'change_p'
})


##fcm 

test_fcm = views.CustomFCMDeviceViewSet.as_view({
    'get': 'test_fcm'
})

update_device = views.CustomFCMDeviceViewSet.as_view({
    'post': 'update_device',
    'get': 'update_device'
})

delete_device = views.CustomFCMDeviceViewSet.as_view({
    'post': 'delete_device'
})



## village
 
temporary_delete_village = views.VillageViewSet.as_view({
    'patch':'temporary_delete_village'
})

get_villages_active = views.VillageViewSet.as_view({
    'get': 'get_villages_active'
})

get_villages_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_zones'
})

get_companys_pk_villages_zones = views.ZoneViewSet.as_view({
    'get': 'get_companys_pk_villages_zones'
})

get_villages_pk_villages_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_villages_zones'
})

get_companys_pk_villages = views.VillageViewSet.as_view({
    'get': 'get_companys_pk_villages'
})

create_village_with_setting = views.VillageViewSet.as_view({
    'post': 'create_village_with_setting'
})

## setting 

get_village_pk_setting = views.SettingViewSet.as_view({
    'get': 'get_village_pk_setting',
    'patch': 'patch_village_pk_setting'
})

## zone

temporary_delete_zone = views.ZoneViewSet.as_view({
    'patch': 'temporary_delete_zone'
})

get_villages_pk_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones'
})

get_villages_pk_zones_pk = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zones_pk'
})

get_villages_pk_zone_pk_single_villages_single_zones = views.ZoneViewSet.as_view({
    'get': 'get_villages_pk_zone_pk_single_villages_single_zones'
})


## home

temporary_delete_home = views.HomeViewSet.as_view({
    'patch': 'temporary_delete_home'
})

create_home_and_check_duplicate = views.HomeViewSet.as_view({
    'post': 'create_home_and_check_duplicate'
})

get_villages_zones_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_zones_homes'
})

get_villages_pk_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_pk_homes'
})

get_villages_pk_zones_null_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_pk_zones_null_homes'
})

get_villages_pk_zones_pk_homes = views.HomeViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_homes'
})

get_homes_active = views.HomeViewSet.as_view({
    'get': 'get_homes_active'
})

get_homespk_number = views.HomeViewSet.as_view({
    'get': 'get_homespk_number'
})

get_homes_pk_homenumber = views.HomeViewSet.as_view({
    'get': 'get_homes_pk_homenumber'
})

## manager

get_companies_manager = views.ManagerViewSet.as_view({
    'get': 'get_companies_manager'
})

get_villages_manager = views.ManagerViewSet.as_view({
    'get': 'get_villages_manager'
})

permanent_delete_manager_with_delete_username = views.ManagerViewSet.as_view({
    'delete': 'permanent_delete_manager_with_delete_username'
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

patch_temporary_delete_generaluser_with_delete_username = views.GeneralUserViewSet.as_view({
    'patch': 'patch_temporary_delete_generaluser_with_delete_username'
})

##secure guard 

get_villages_pk_secureguards = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_secureguards'
})

get_villages_pk_zones_pk_secureguards = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_secureguards'
})

get_villages_pk_secureguards_for_location = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_secureguards_for_location'
})

get_villages_pk_zones_pk_secureguards_for_location = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_secureguards_for_location'
})

get_villages_pk_secureguards_for_mainfetching = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_secureguards_for_mainfetching'
})

get_villages_pk_zones_pk_secureguards_for_mainfetching = views.SecureGuardViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_secureguards_for_mainfetching'
})

patch_temporary_delete_secureguard_with_delete_username = views.SecureGuardViewSet.as_view({
    'patch': 'patch_temporary_delete_secureguard_with_delete_username'
})

##secure location 

get_secureguards_pk_securelocation = views.SecureLocationViewSet.as_view({
    'get':'get_secureguards_pk_securelocation'
})

## user

get_profiles_check  = views.UserProfileViewSet.as_view({
    'post': 'get_profiles_check'
})


## checkpoint 

get_villages_pk_checkpoints = views.CheckpointViewSet.as_view({
    'get': 'get_villages_pk_checkpoints'
})

get_villages_pk_zones_pk_checkpoints = views.CheckpointViewSet.as_view({
    'get': 'get_villages_pk_zones_pk_checkpoints'
})

##checkincheckpoint

get_villages_pk_checkincheckpoints = views.CheckinCheckpointViewSet.as_view({
    'get': 'get_villages_pk_checkincheckpoints'
})

## work 

get_villages_pk_works = views.WorkViewSet.as_view({
    'get': 'get_villages_pk_works',
    
})

patch_work = views.WorkViewSet.as_view({
    'patch': 'patch_work',
})

temporary_delete_work = views.WorkViewSet.as_view({
    'patch': 'temporary_delete_work',
})

## qrcodes 

get_villages_pk_qrcodes_non_exit = views.QrCodeViewSet.as_view({
    'get': 'get_villages_pk_qrcodes_non_exit'
})

temporary_delete_qrcode = views.QrCodeViewSet.as_view({
    'patch': 'temporary_delete_qrcode'
})

patch_qrcodes_userscan = views.QrCodeViewSet.as_view({
    'patch': 'patch_qrcodes_userscan'
})

patch_qrcodes_exitscan = views.QrCodeViewSet.as_view({
    'patch': 'patch_qrcodes_exitscan'
})

patch_qrcodes_insidescan = views.QrCodeViewSet.as_view({
    'patch': 'patch_qrcodes_insidescan'
})

get_qrcodes_history_additionaldetail = views.QrCodeViewSet.as_view({
    'get': 'get_qrcodes_history_additionaldetail'
})

get_qrcodes_village_pk_home_number_homedetails = views.QrCodeViewSet.as_view({
    'post': 'get_qrcodes_village_pk_home_number_homedetails'
})

get_villages_location_pk = views.VillageViewSet.as_view({
    'get': 'get_villages_location_pk'
})

## qr_inside_screen services
get_villages_pk_qrcodes = views.QrCodeViewSet.as_view({
    'get': 'get_villages_pk_qrcodes'
})

get_villages_pk_zone_pk_qrcodes = views.QrCodeViewSet.as_view({
    'get': 'get_villages_pk_zone_pk_qrcodes'
})

## qr_user_screen services
get_villages_pk_homes_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_villages_pk_homes_pk_qrcodes'
})

## qr_exit_screen services
get_villages_pk_contents_content_qrcodes = views.QrCodeViewSet.as_view({
     'post': 'get_villages_pk_contents_content_qrcodes'
})

## qr_history_screen services (for null village) ## using
get_historyservice_list_villages_null_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_null_dates_year_month_day_qrcodes'
})

## qr_history_screen services (filter by village, zone, date) ## using
get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes'
})
## qr_history_screen services (filter by village, zone)
get_historyservice_list_villages_pk_zones_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_zones_pk_qrcodes'
})

## qr_history_screen services (filter by village, date)  ## using
get_historyservice_list_villages_pk_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_dates_year_month_day_qrcodes'
})

## qr_history_screen services (filter by village) 
get_historyservice_list_villages_pk_qrcodes = views.QrCodeViewSet.as_view({
     'get': 'get_historyservice_list_villages_pk_qrcodes'
})

get_historyservice_list_home_pk_dates_year_month_day_qrcodes = views.QrCodeViewSet.as_view({
    'get': 'get_historyservice_list_home_pk_dates_year_month_day_qrcodes'
})


## create code with no coupon condition
create_qrcodes_home_pk_nocopon = views.QrCodeViewSet.as_view({
     'post': 'create_qrcodes_home_pk_nocopon'
})

## Test '
testDateCreation = views.PointObservationViewSet.as_view({
    'post': 'testDateCreation' 
})

testObservation = views.PointObservationViewSet.as_view({
    # 'post': 'testObservation'  ## old method for createObservation
    'post': 'createObservation'  ## new method for createObservation
    
})

pointobservation_fetch_record_with_checkpoint_by_start_end_time = views.PointObservationViewSet.as_view({
    'get': 'pointobservation_fetch_record_with_checkpoint_by_start_end_time'
})

pointobservation_fetch_record_with_checkpoint =  views.PointObservationViewSet.as_view({
    'get': 'pointobservation_fetch_record_with_checkpoint'
})
## use for retrieve checked status in point observation screen

get_current_time = views.PointObservationViewSet.as_view({
    'get': 'get_current_time'
})

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

fetch_pointobservation_null_village_null_zone_null_work = views.PointObservationViewSet.as_view({
    'get': 'fetch_pointobservation_null_village_null_zone_null_work'
})

fetch_pointobservationrecord_percent = views.PointObservationRecordViewSet.as_view({
    'get': 'fetch_pointobservationrecord_percent'
})

fetch_pointobservationrecord_timeslots_percent = views.PointObservationRecordViewSet.as_view({
    'get': 'fetch_pointobservationrecord_percent_by_set_of_starttime_endtime'
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

get_maintenance_fee_period_filterby_villagePk_year = views.MaintenanceFeePeriodViewSet.as_view({
    'get': 'get_maintenance_fee_period_filterby_villagePk_year'
})

get_villages_pk_maintenance_fee_period_pk = views.MaintenanceFeePeriodViewSet.as_view({
    'get': 'get_villages_pk_maintenance_fee_period_pk'
})

create_maintenance_fee_period = views.MaintenanceFeePeriodViewSet.as_view({
    'post': 'create_maintenance_fee_period'
})


get_maintenance_fee_period_total_amount_number_paid_home = views.MaintenanceFeePeriodViewSet.as_view({
    'get': 'get_maintenance_fee_period_total_amount_number_paid_home'
})

## VoteTopic 
get_votetopics_filterby_villagepk_month_year = views.VoteTopicViewSet.as_view({
    'get': 'get_votetopics_filterby_villagepk_month_year'
})

get_votetopics_filterby_villagepk_homepk_month_year = views.VoteTopicViewSet.as_view({
    'get': 'get_votetopics_filterby_villagepk_homepk_month_year'
})

get_votetopics_pk_result_user_home_pk = views.VoteTopicViewSet.as_view({
    'get': 'get_votetopics_pk_result_user_home_pk'
})

get_votetopics_pk_result_admin = views.VoteTopicViewSet.as_view({
    'get': 'get_votetopics_pk_result_admin'
})

patch_votetopics_result = views.VoteTopicViewSet.as_view({
    'patch': 'patch_votetopics_result'
})

checkvoteable_village_pk_home_pk = views.VoteTopicViewSet.as_view({
    'get': 'checkvoteable_village_pk_home_pk'
})




## VoteChoice
get_votetopics_pk_votechoices = views.VoteChoiceViewSet.as_view({
    'get': 'get_votetopics_pk_votechoices'
})

## VoteRecord 

post_add_multiple_voterecord  = views.VoteRecordViewSet.as_view({
    'post': 'post_add_multiple_voterecord'
})


## MaintenanceFeeRecord

get_maintenance_fee_record_filterby_home_pk_year = views.MaintenanceFeeRecordViewSet.as_view({
    'get': 'get_maintenance_fee_record_filterby_home_pk_year'
})

get_maintenance_fee_period_pk_maintenance_fee_record = views.MaintenanceFeeRecordViewSet.as_view({
    'get': 'get_maintenance_fee_period_pk_maintenance_fee_record'
})

mtr_check_isexist_and_isduplicate_home = views.MaintenanceFeeRecordViewSet.as_view({
    'post': 'mtr_check_isexist_and_isduplicate_home'
})

## Problem 

get_homes_pk_problems = views.ProblemViewSet.as_view({
    'get': 'get_homes_pk_problems'
})

get_problems_filterby_homepk_month_year = views.ProblemViewSet.as_view({
    'get': 'get_problems_filterby_homepk_month_year'
})

get_problems_with_home_number  = views.ProblemViewSet.as_view({
    'get': 'get_problems_with_home_number'
})

get_problems_with_home_number_filterby_month_year = views.ProblemViewSet.as_view({
    'get': 'get_problems_with_home_number_filterby_month_year'
})

## Secure Work 

get_secureguards_pk_works = views.SecureWorkViewSet.as_view({
    'get': 'get_secureguards_pk_works'
})

delete_secureguards_pk_works_pk = views.SecureWorkViewSet.as_view({
    'get': 'delete_secureguards_pk_works_pk'
})

## WorkingRecord

create_workingrecord_with_secure_checkout = views.WorkingRecordViewSet.as_view({
    'post': 'create_workingrecord_with_secure_checkout'
})

create_workingrecord_with_secure_checkin = views.WorkingRecordViewSet.as_view({
    'post': 'create_workingrecord_with_secure_checkin'
})

get_secure_pk_workingrecord_lasted = views.WorkingRecordViewSet.as_view({
    'get': 'get_secure_pk_workingrecord_lasted'
})

fetch_workingrecord  = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_workingrecord'
})

fetch_workingrecord_null_work = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_workingrecord_null_work'
})

fetch_workingrecord_null_zone = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_workingrecord_null_zone'
})

fetch_workingrecord_null_zone_null_work = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_workingrecord_null_zone_null_work'
})

fetch_workingrecord_null_village_null_zone_null_work = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_workingrecord_null_village_null_zone_null_work'
})

fetch_detailed_workingrecord = views.WorkingRecordViewSet.as_view({
    'get': 'fetch_detailed_workingrecord'
})

## notification 

create_enter_qrcode_and_notificaton = views.NotificationViewSet.as_view({
    'post': 'create_enter_qrcode_and_notificaton'
})

get_notification_generaluser_pk = views.NotificationViewSet.as_view({
    'get': 'get_notification_generaluser_pk'
})

get_notification_generaluser_pk_month_year = views.NotificationViewSet.as_view({
    'get': 'get_notification_generaluser_pk_month_year'
})

get_unread_notification_count = views.NotificationViewSet.as_view({
    'get': 'get_unread_notification_count'
})

test_path = views.VoteCountViewSet.as_view({
    'get': 'test_path'
})

# Home Secure main routers
urlpatterns = [

    ##Note: if most end point unless viewset default especially list function will return if is_active = true, 

    ## username 
    path('profiles/change_p/',change_p,name='change_p'),
    path('profiles/detail/',get_profiles_detail,name='get_profiles_detail'),
    path('profiles/create_username/with_type/',create_username_with_usertype,name='create_username_with_usertype'),
    

    ## fcm 
    path('test_fcm/',test_fcm,name='test_fcm'),
    path('device/update_device/', update_device,name='update_device'),
    path('device/delete_device/', delete_device,name='delete_device'),

    

    ## village end point 
    path('villages/<int:village_pk>/temporary_delete/',temporary_delete_village,name="temporary_delete_village"),
    path('villages_active/',get_villages_active,name='get_villages_active'),
    path('companys/<int:pk>/villages/',  get_companys_pk_villages, name='  get_companys_pk_villages'), ## conpany adapted
    path('villages/location/<int:villagePk>', get_villages_location_pk, name='get_villages_location_pk'),
    path('create_villages_with_setting/', create_village_with_setting, name='create_village_with_setting'),


    ##zone end point
    path('zones/<int:zone_pk>/temporary_delete/',temporary_delete_zone,name="temporary_delete_zone"),
    path('companys/<int:company_pk>/villages/zones/', get_companys_pk_villages_zones ,name='get_companys_pk_villages_zones'),
    path('companys/<int:company_pk>/villages/zones/', get_companys_pk_villages_zones ,name='get_companys_pk_villages_zones'),
    path('villages/<int:village_pk>/villages/zones/', get_villages_pk_villages_zones ,name='get_villages_pk_villages_zones'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/villages/zones/', get_villages_pk_zone_pk_single_villages_single_zones ,name='get_villages_pk_zone_pk_single_villages_single_zones'),
    

    path('villages/zones/', get_villages_zones ,name='villages_zones'),
    path('villages/<int:pk>/zones/', get_villages_pk_zones ,name='villages_pk_zones'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/', get_villages_pk_zones_pk ,name='villages_pk_zones_pk'),
    
    
    ##home end point
    path('home/<int:home_pk>/temporary_delete/',temporary_delete_home, name='temporary_delete_home'),
    path('homes/create_home_and_check_duplicate', create_home_and_check_duplicate, name='create_home_and_check_duplicate'),
    path('homes_active/', get_homes_active, name='get_homes_active'),
    path('villages/<int:village_pk>/homes/',get_villages_pk_homes, name='get_villages_pk_homes'),
    # path('villages/zones/homes/', get_villages_zones_homes, name='get_villages_zones_homes'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/homes/', get_villages_pk_zones_pk_homes, name='get_villages_pk_zones_pk_homes'),
    path('villages/<int:village_pk>/zones/null/homes/', get_villages_pk_zones_null_homes, name='get_villages_pk_zones_null_homes'),
    path('homes/<str:home_number>/check_home_exist/', get_homespk_number, name='get_homespk_number'),
    path('homes/<int:home_pk>/home_number/', get_homes_pk_homenumber, name='get_homes_pk_homenumber'),
    

    ## manager 
    path('companies/<int:company_pk>/manager/',get_companies_manager, name='get_companies_manager'),
    path('manager/<int:user_pk>/delete_with_username/',permanent_delete_manager_with_delete_username, name='permanent_delete_manager_with_delete_username'),
    path('villages/<int:village_pk>/manager/', get_villages_manager, name='get_villages_manager'),

    
    ##general user end point 
    path('general_users_active/', get_general_users_active, name='get_general_users_active'),
    path('villages/<int:village_pk>/general_users/', get_villages_pk_general_users, name='get_villages_pk_general_users'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/general_users/', get_villages_pk_zones_pk_general_users, name='get_villages_pk_zones_pk_general_users'),
    path('general_users/<int:genuser_pk>/temporary_delete/username_delete/',  patch_temporary_delete_generaluser_with_delete_username, name='patch_temporary_delete_generaluser_with_delete_username'),
    
    
    ##user
    path('profiles_check/', get_profiles_check, name='get_profiles_check'),

    ##secure guard 
    path('villages/<int:village_pk>/secure_guards/', get_villages_pk_secureguards, name='get_villages_pk_secureguards'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/secure_guards/', get_villages_pk_zones_pk_secureguards, name='get_villages_pk_zones_pk_secureguards'),
    path('villages/<int:village_pk>/secure_guards/for_location/',  get_villages_pk_secureguards_for_location, name='get_villages_pk_secureguards_for_location'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/secure_guards/for_location/', get_villages_pk_zones_pk_secureguards_for_location, name='get_villages_pk_zones_pk_secureguards_for_location'),
    path('villages/<int:village_pk>/secure_guards/for_mainfetching/',  get_villages_pk_secureguards_for_mainfetching, name='get_villages_pk_secureguards_for_mainfetching'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/secure_guards/for_mainfetching/',get_villages_pk_zones_pk_secureguards_for_mainfetching, name='get_villages_pk_zones_pk_secureguards_for_mainfetching'),
    path('secure_guards/<int:secure_pk>/temporary_delete/username_delete/',  patch_temporary_delete_secureguard_with_delete_username, name='patch_temporary_delete_secureguard_with_delete_username'),
  

    ##secure location 
    path('secure_guards/<int:secure_guard_pk>/securelocations/', get_secureguards_pk_securelocation, name='get_secureguards_pk_securelocation'),
    
   
    
    ##checkpoint 
    path('villages/<int:village_pk>/checkpoints/', get_villages_pk_checkpoints, name='get_villages_pk_checkpoints'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/checkpoints/', get_villages_pk_zones_pk_checkpoints, name='get_villages_pk_zones_pk_checkpoints'),
    
    
    ##checkincheckpoint 
    path('villages/<int:village_pk>/checkin_checkpoints/', get_villages_pk_checkincheckpoints, name='get_villages_pk_checkincheckpoints'),
    

    ##work 
    path('villages/<str:pk>/works/', get_villages_pk_works ,name='get_villages_pk_works'),
    path('works/update_work/<int:pk>/', patch_work ,name='patch_work'),
    path('work/<int:work_pk>/temporary_delete/',temporary_delete_work,name="temporary_delete_work"),
    

    ##qr
    path('qrcodes/temporary_delete_qrcode/<int:pk>/',temporary_delete_qrcode,name="temporary_delete_qrcode"),
    path('qrcodes/<int:pk>/insidescan/', patch_qrcodes_insidescan ,name='patch_qrcodes_insidescan'),
    path('qrcodes/<int:pk>/exitscan/', patch_qrcodes_exitscan ,name='patch_qrcodes_exitscan'),
    path('qrcodes/<int:pk>/userscan/', patch_qrcodes_userscan ,name='patch_qrcodes_userscan'),
    
    path('qrcodes/village/<int:village_pk>/homedetail/', get_qrcodes_village_pk_home_number_homedetails ,name='get_qrcodes_village_pk_home_number_homedetails'),
    path('villages/<int:village_pk>/qrcodes/', get_villages_pk_qrcodes, name = 'get_villages_pk_qrcodes'),
    path('villages/<int:village_pk>/zones/<int:zone_pk>/qrcodes/', get_villages_pk_zone_pk_qrcodes, name = 'get_villages_pk_zone_pk_qrcodes'),
    path('villages/<int:village_pk>/qrcodes/non_exit/', get_villages_pk_qrcodes_non_exit, name = 'get_villages_pk_qrcodes_non_exit'),
    path('historyservice/qrcodes/<int:qrcode_pk>/additional_detail/', get_qrcodes_history_additionaldetail, name = 'get_qrcodes_history_additionaldetail'),
    


    path('villages/<int:village_pk>/homes/<int:home_pk>/qrcodes/', get_villages_pk_homes_pk_qrcodes, name = 'get_villages_pk_homes_pk_qrcodes'),
    path('villages/<int:village_pk>/qrcodes_contents/', get_villages_pk_contents_content_qrcodes, name = 'get_villages_pk_contents_content_qrcodes'),
    ## currently use this
    path('historyservice/list/villages/<int:village_pk>/zones/<int:zone_pk>/dates/<int:year>/<int:month>/<int:day>/qrcodes/', get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes, name = 'get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes'),
    ## currently use this
    path('historyservice/list/villages/<int:village_pk>/dates/<int:year>/<int:month>/<int:day>/qrcodes/', get_historyservice_list_villages_pk_dates_year_month_day_qrcodes, name = 'get_historyservice_list_villages_pk_dates_year_month_day_qrcodes'),
    ## currently use this
    path('historyservice/list/villages/null/dates/<int:year>/<int:month>/<int:day>/qrcodes/',get_historyservice_list_villages_null_dates_year_month_day_qrcodes,name='get_historyservice_list_villages_null_dates_year_month_day_qrcodes'),
    path('qrcodes/create_qrcodes_nocoupon/', create_qrcodes_home_pk_nocopon, name = 'create_qrcodes_home_pk_nocopon'),
    path('historyservice/list/homes/<int:home_pk>/dates/<int:year>/<int:month>/<int:day>/qrcodes/',  get_historyservice_list_home_pk_dates_year_month_day_qrcodes, name = ' get_historyservice_list_home_pk_dates_year_month_day_qrcodes'),
   


    #point observation
    path('testDateCreation/',testDateCreation, name='testDateCreation'),
    path('get_current_time/', get_current_time, name="get_current_time"),
    path('pointobservation_create_service/', testObservation ,name='testObservation'),
    path('pointobservation_fetch_record_checked_pk/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/timeslots/<int:timeslot>/', pointobservation_fetch_record_checked_pk ,name='pointobservation_fetch_record_checked_pk'),
    path('pointobservation_fetch_record/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/timeslots/<int:timeslot>/', pointobservation_fetch_record ,name='pointobservation_fetch_record'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/dates/<str:date>/', fetch_pointobservation ,name='fetch_pointobservation'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/<int:zone_pk>/works/null/dates/<str:date>/', fetch_pointobservation_null_work ,name='fetch_pointobservation_null_work'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/null/works/<int:work_pk>/dates/<str:date>/', fetch_pointobservation_null_zone ,name='fetch_pointobservation_null_zone'),
    path('fetch_pointobservation/villages/<int:village_pk>/zones/null/works/null/dates/<str:date>/', fetch_pointobservation_null_zone_null_work ,name='fetch_pointobservation_null_zone_null_work'),
    path('fetch_pointobservation/villages/null/zones/null/works/null/dates/<str:date>/',     fetch_pointobservation_null_village_null_zone_null_work ,name='    fetch_pointobservation_null_village_null_zone_null_work'),
    path('fetch_pointobservationrecord/pointobservation/<int:pointobservation_pk>/timeslots/<int:timeslot>/percent/',fetch_pointobservationrecord_percent,name='fetch_pointobservationrecord_percent'),
    path('fetch_pointobservationrecord/pointobservation/<int:pointobservation_pk>/timeslots/percent/', fetch_pointobservationrecord_timeslots_percent,name='fetch_pointobservationrecord_timeslots_percent'),
    path('fetch_pointobservationrecord_pointlist/pointobservation/<int:pointobservation_pk>/start_time/<str:start_time>/end_time/<str:end_time>/', fetch_pointobservationrecord_pointlist,name='fetch_pointobservationrecord_pointlist'),
    path('fetch_pointobservationrecord_updatework/works/<int:work_pk>/', fetch_pointobservation_update_work,name='fetch_pointobservation_update_work'),
    path('fetch_pointobservationrecord_updatework/zones/<int:zone_pk>/', fetch_pointobservation_update_zone,name='fetch_pointobservation_update_zone'),
    ##new endpoint for fetchnig pointobservation along with check point in point_observation_screen
    path('fetch_pointobservationrecord/checkpoint_with_timesliot/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/timeslots/<int:timeslot>/', pointobservation_fetch_record_with_checkpoint ,name='pointobservation_fetch_record_with_checkpoint'),
    path('fetch_pointobservationrecord/checkpoint_with_timesliot/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/secures/<int:secure_pk>/dates/<str:date>/startTime/<str:start_time>/endTime/<str:end_time>/', pointobservation_fetch_record_with_checkpoint_by_start_end_time ,name='pointobservation_fetch_record_with_checkpoint_by_start_end_time'),
    

    ## maintenancefeeperiod
    path('maintenance_fee_period/homes/<int:home_pk>/year/<int:year>/',get_maintenance_fee_record_filterby_home_pk_year,name="get_maintenance_fee_record_filterby_home_pk_year"),
    path('maintenance_fee_period/villages/<int:village_pk>/year/<int:year>/', get_maintenance_fee_period_filterby_villagePk_year,name='get_maintenance_fee_period_filterby_villagePk_year'),
    path('villages/<int:village_pk>/maintenance_fee_period/<int:mfpPk>/', get_villages_pk_maintenance_fee_period_pk,name='get_villages_pk_maintenance_fee_period_pk'),
    path('maintenance_fee_period/create/maintenance_fee_record/', create_maintenance_fee_period,name='create_maintenance_fee_period'),
    path('maintenance_fee_period/<int:pk>/total_amount_and_paid_home_num/', get_maintenance_fee_period_total_amount_number_paid_home,name='get_maintenance_fee_period_total_amount_number_paid_home'),


    ## maintenancefeerecord
    path('maintenance_fee_period/<int:pk>/maintenance_fee_record/', get_maintenance_fee_period_pk_maintenance_fee_record, name='get_maintenance_fee_period_pk_maintenance_fee_record'),
    path('maintenance_fee_record/checkisexist/checkduplicate/maintenance_fee_period/<int:mfp_pk>/', mtr_check_isexist_and_isduplicate_home, name='mtr_check_isexist_and_isduplicate_home'),
    
    ## votetopic
    path('votetopics/villages/<int:village_pk>/month/<int:month>/year/<int:year>/', get_votetopics_filterby_villagepk_month_year,name='get_votetopics_filterby_villagepk_month_year'),
    path('votetopics/villages/<int:village_pk>/homes/<int:home_pk>/month/<int:month>/year/<int:year>/', get_votetopics_filterby_villagepk_homepk_month_year,name='get_votetopics_filterby_villagepk_homepk_month_year'),
    path('votetopics/<int:votetopic_pk>/result/homes/<int:home_pk>/', get_votetopics_pk_result_user_home_pk,name='get_votetopics_pk_result_user_home_pk'),
    path('votetopics/<int:votetopic_pk>/result/admin/', get_votetopics_pk_result_admin,name='get_votetopics_pk_result_admin'),
    path('votetopics/<int:pk>/confirmresult/', patch_votetopics_result,name='patch_votetopics_result'),
    path('villages/<int:village_pk>/homes/<int:home_pk>/checkvoteable/', checkvoteable_village_pk_home_pk,name='checkvoteable_village_pk_home_pk'),
    

    ## votechoice
    path('votetopics/<int:votetopic_pk>/votechoices/', get_votetopics_pk_votechoices,name='get_votetopics_pk_votechoices'),
    
    ## voterecord
    path('voterecord/add_multiple/', post_add_multiple_voterecord, name='post_add_multiple_voterecord'),

    ## problem 
    path('homes/<int:home_pk>/problems/',  get_homes_pk_problems,name='get_homes_pk_problems'),
    path('problems/home/<int:home_pk>/month/<int:month>/year/<int:year>/',get_problems_filterby_homepk_month_year, name='get_problems_filterby_homepk_month_year'),
    path('problems/<int:village_pk>/',  get_problems_with_home_number,name='get_problems_with_home_number'),
    path('problems/village/<int:village_pk>/month/<int:month>/year/<int:year>/',  get_problems_with_home_number_filterby_month_year,name=' get_problems_with_home_number_filterby_month_year'),

   
    
    ## securework 
    path('secure_guards/<int:secureguard_pk>/works/',  get_secureguards_pk_works,name='get_secureguards_pk_works'),
    path('secure_guards/<int:secureguard_pk>/works/<int:work_pk>/delete/',  delete_secureguards_pk_works_pk,name='delete_secureguards_pk_works_pk'),
    
    ## workingrecord
   
    path('secure_guards/checkout/',create_workingrecord_with_secure_checkout,name="create_workingrecord_with_secure_checkout"),
    path('secure_guards/checkin/',create_workingrecord_with_secure_checkin,name="create_workingrecord_with_secure_checkin"),
    path('secure_guards/<int:secureguard_pk>/lasted_checkin/',  get_secure_pk_workingrecord_lasted,name='get_secure_pk_workingrecord_lasted'),
    path('fetch_workingrecord/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/dates/<str:date_str>/', fetch_workingrecord ,name='fetch_workingrecord'),
    path('fetch_workingrecord/villages/<int:village_pk>/zones/null/works/<int:work_pk>/dates/<str:date_str>/', fetch_workingrecord_null_zone, name='fetch_workingrecord_null_zone'),
    path('fetch_workingrecord/villages/<int:village_pk>/zones/<int:zone_pk>/works/null/dates/<str:date_str>/', fetch_workingrecord_null_work, name='fetch_workingrecord_null_work'),
    path('fetch_workingrecord/villages/<int:village_pk>/zones/null/works/null/dates/<str:date_str>/', fetch_workingrecord_null_zone_null_work, name='fetch_workingrecord_null_zone_null_work'),
    path('fetch_workingrecord/villages/null/zones/null/works/null/dates/<str:date_str>/', fetch_workingrecord_null_village_null_zone_null_work, name='fetch_workingrecord_null_village_null_zone_null_work'),
    path('detailed_fetch_workingrecord/villages/<int:village_pk>/zones/<int:zone_pk>/works/<int:work_pk>/dates/<str:date_str>/secure_guard/<int:secure_pk>/', fetch_detailed_workingrecord, name='fetch_detailed_workingrecord'),

    ##notification 

    
    path('qrcodes/create_enter_and_notification/',  create_enter_qrcode_and_notificaton,name='create_enter_qrcode_and_notificaton'),
    path('general_users/<int:user_pk>/notification/',  get_notification_generaluser_pk,name='get_notification_generaluser_pk'),
    path('general_users/<int:user_pk>/month/<int:month>/year/<int:year>/notification/',get_notification_generaluser_pk_month_year,name='get_notification_generaluser_pk_month_year'),
    path('general_users/<int:user_pk>/unread_notification/count/',  get_unread_notification_count,name='get_unread_notification_count'),


    
    ## setting
    path('villages/<int:village_pk>/setting/',  get_village_pk_setting,name='get_village_pk_setting'),
   
    ## test path
    

    # re_path(r'^stores/\w+/',test_path,name='test_path'),
    # re_path(r'homes/check_home_exist/<str:home_number>/', get_homespk_number, name='get_homespk_number'),
    
    
    
    ##fcm 
    # url(r'fcm/', include('fcm.urls')),


    # path('hello-view/', views.HelloApiView.as_view()), 
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
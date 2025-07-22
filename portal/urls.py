from django.urls import path
from .views import *
from django.contrib import admin 
from django.contrib.auth.views import LogoutView
import json
app_name = 'mapApp'
from portal.admin import *
urlpatterns = [

  path('admin/', admin.site.urls),

#   path('', loginView, name='employeelist'),

  path('', dashboardview, name='dashboard'),
  path('report/', reportview, name='dashboard'),

  path('oppsdashboard/', oppsdashboardview, name='dashboard'),
   

  path('map/', mapview, name='dashboard'),

  #  path('community/', communityview, name='community'),
  path('community/', communityview, name='community_view'),
  path('community_data/', get_community_data, name='community_data'),
  path('add_community/', add_community, name='add_community'),
  path('get_community/<int:community_id>/', get_community, name='get_community'),
  path('update_community/<int:community_id>/', update_community, name='update_community'),
  path('delete_community/<int:community_id>/', delete_community, name='delete_community'),


  #healthfacilities
  path('healthfacilities/', healthfacilitiesview, name='healthfacilities'),
  path('health_facilities/', health_facilities, name='health_facilities'),
  path('health_facilities/data/', health_facilities_data, name='health_facilities_data'),
  path('add_health_facility/', add_health_facility, name='add_health_facility'),
  path('get_health_facility/<int:id>/', get_health_facility, name='get_health_facility'),
  path('edit_health_facility/', edit_health_facility, name='edit_health_facility'),
  path('delete_health_facility/', delete_health_facility, name='delete_health_facility'),

  #Health Workers
  path('healthworker/', healthworkerview, name='healthworker'),
  path('health_workers/', health_workers, name='health_workers'),
  path('health_workers/data/', health_workers_data, name='health_workers_data'),
  path('add_health_worker/', add_health_worker, name='add_health_worker'),
  path('get_health_worker/<int:id>/', get_health_worker, name='get_health_worker'),
  path('edit_health_worker/', edit_health_worker, name='edit_health_worker'),
  path('delete_health_worker/', delete_health_worker, name='delete_health_worker'),


  #cwcschedule
  path('cwcschedule/', cwcscheduleview, name='healthworker'),
  path('cwc_schedule/', cwcscheduleview, name='cwc_schedule'),
  path('cwc_schedule/data/', cwc_schedule_data, name='cwc_schedule_data'),
  path('add_cwc_schedule/', add_cwc_schedule, name='add_cwc_schedule'),
  path('get_cwc_schedule/<int:id>/', get_cwc_schedule, name='get_cwc_schedule'),
  path('edit_cwc_schedule/', edit_cwc_schedule, name='edit_cwc_schedule'),
  path('delete_cwc_schedule/', delete_cwc_schedule, name='delete_cwc_schedule'),


  path('assets/', assets_view, name='assets'),
  path('assets/data/', assets_data, name='assets_data'),
  path('add_asset/', add_asset, name='add_asset'),
  path('add_asset_type/', add_asset_type, name='add_asset_type'),
  path('get_asset/<int:asset_id>/', get_asset, name='get_asset'),
  path('edit_asset/', edit_asset, name='edit_asset'),
  path('delete_asset/', delete_asset, name='delete_asset'),

  path('pc_reports/', pc_reports_view, name='pc_reports'),
  path('pc_reports/data/', pc_reports_data, name='pc_reports_data'),
  path('get_pc_report/<int:report_id>/', get_pc_report, name='get_pc_report'),
  path('add_pc_report/', add_pc_report, name='add_pc_report'),
  path('edit_pc_report/', edit_pc_report, name='edit_pc_report'),
  path('delete_pc_report/', delete_pc_report, name='delete_pc_report'),


  path('map/district/', DistrictBoundarylayerView.as_view()),

  path('map/region/', RegionBoundarylayerView.as_view()),

  path('test/', testview, name='healthworker'),
  


path('map/healthfacilities/', healthFacilitiestblView.as_view(), name='healthworker'),

path('map/pcreport/', pcreportTblView.as_view(), name='healthworker'),


path('autocomplete/', AutocompleteView , name='autocompleteview'),

 path('hfextent/<int:code>/<slug:ftype>/', hfextentView, name=''),


  path('fetchpc/', fetchdataView, name=''),

  path('map/heatmap/', heatmapview, name=''),

   path('pcreport/', pcreportview, name=''),
  
]
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

   path('community/', communityview, name='community'),

   path('healthfacilities/', healthfacilitiesview, name='healthfacilities'),

   path('healthworker/', healthworkerview, name='healthworker'),

  path('cwcschedule/', cwcscheduleview, name='healthworker'),


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
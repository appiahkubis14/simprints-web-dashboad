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

   path('map/', mapview, name='dashboard'),

   path('community/', communityview, name='community'),

   path('healthfacilities/', healthfacilitiesview, name='healthfacilities'),

   path('healthworker/', healthworkerview, name='healthworker'),

  path('cwcschedule/', cwcscheduleview, name='healthworker'),


  path('map/district/', DistrictBoundarylayerView.as_view()),

  path('map/region/', RegionBoundarylayerView.as_view()),

  path('test/', testview, name='healthworker')
  
]
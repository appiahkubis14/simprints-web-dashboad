from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login as Login,logout as Logout
from django.contrib.auth.decorators import login_required
import ast,json
from django.db.models import Q
from djgeojson.views import GeoJSONLayerView
from django.contrib.gis.db.models import Extent
from .models import *

@ login_required(login_url='/accounts/login')
def dashboardview(request):
   
    return render(request, 'portal/index.html', locals())



@ login_required(login_url='/accounts/login')
def reportview(request):
   
    return render(request, 'portal/report.html', locals())


@ login_required(login_url='/accounts/login')
def communityview(request):
    comm =communityTbl.objects.all()
    return render(request, 'portal/community.html', locals())


@ login_required(login_url='/accounts/login')
def healthfacilitiesview(request):
    hf =healthFacilitiesTbl.objects.all()
    return render(request, 'portal/healthfacilities.html', locals())



@ login_required(login_url='/accounts/login')
def healthworkerview(request):
    hf =healthWorkersTbl.objects.all()
    return render(request, 'portal/healthworkers.html', locals())

@ login_required(login_url='/accounts/login')
def cwcscheduleview(request):
    cwc =cwcScheduleTbl.objects.all()
    return render(request, 'portal/cwcschedule.html', locals())


@ login_required(login_url='/accounts/login')
def mapview(request):
   
    return render(request, 'portal/map.html', locals())




class DistrictBoundarylayerView(GeoJSONLayerView):
  model = Districts
  precision = 4   
  simplify = 0.0001
  properties = ('district_2',"id","pilot")




class RegionBoundarylayerView(GeoJSONLayerView):
  model = Region
  precision = 4   
  simplify = 0.0001
  properties = ('reg_name', 'reg_code', 'pilot')
  
def testview(request):
    for aa in Districts.objects.all():
        name= aa.district.replace('DISTRICT','').replace('MUNICIPAL','').replace('METROPOLITAN','')
        Districts.objects.filter(id=aa.id).update(district_2=name)
    return render(request, 'portal/cwcschedule.html', locals())

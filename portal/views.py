from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login as Login,logout as Logout
from django.contrib.auth.decorators import login_required

from django.db.models import Sum

import ast,json
from django.db.models import Q
from djgeojson.views import GeoJSONLayerView
from django.contrib.gis.db.models import Extent
from .models import *

@ login_required(login_url='/accounts/login')
def dashboardview(request):
    hf = healthFacilitiesTbl.objects.all().count()
    community = healthFacilitiesTbl.objects.all().aggregate(Sum('no_of_commuities'))['no_of_commuities__sum']
    print("asd",community)
    hw = healthWorkersTbl.objects.all().count()
    # community=communityTbl.objects.all().count()
    district = Districts.objects.filter(pilot=True)
    dist = district.count()
    alldist = my_list = [item.district for item in district] 
    # district.values_list('district',flat=True)

    hfcount=[]
    hwcount=[]
    comarr=[]
    for aa in district :
        chf= healthFacilitiesTbl.objects.filter(district=aa.id).count()
        chw = healthWorkersTbl.objects.filter(healthFacilitiesTbl_foreignkey__district=aa.id).count()
        comm= healthFacilitiesTbl.objects.filter(district=aa.id).aggregate(Sum('no_of_commuities'))['no_of_commuities__sum']
        hfcount.append(chf)
        hwcount.append(chw)
        comarr.append(comm)
    print(comarr)
   
    return render(request, 'portal/index.html', locals())


def oppsdashboardview(request):
    hf = healthFacilitiesTbl.objects.all().count()
    hw = healthWorkersTbl.objects.all().count()
    district = Districts.objects.filter(pilot=True)
    dist = district.count()
    alldist = my_list = [item.district for item in district] 
    # district.values_list('district',flat=True)
    hfcount=[]
    hwcount=[]
    for aa in district :
        chf= healthFacilitiesTbl.objects.filter(district=aa.id).count()
        chw = healthWorkersTbl.objects.filter(healthFacilitiesTbl_foreignkey__district=aa.id).count()
        hfcount.append(chf)
        hwcount.append(chw)

    print(hwcount)
   
    return render(request, 'portal/operationsdashboard.html', locals())



@ login_required(login_url='/accounts/login')
def reportview(request):
   
    return render(request, 'portal/report.html', locals())



#######################################################################################

@ login_required(login_url='/accounts/login')
def communityview(request):
    comm =communityTbl.objects.all()
    healthfacility = healthFacilitiesTbl.objects.all()

    context = {
        'comm':comm,
        'healthfacility':healthfacility,
    }

    return render(request, 'portal/community.html', context)



from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from portal.models import communityTbl, healthFacilitiesTbl
from django.shortcuts import get_object_or_404

@require_http_methods(["GET"])
def get_community_data(request):
    # This view should return JSON data for DataTables
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    
    # Get total count
    total = communityTbl.objects.count()
    
    # Get filtered count (if there's a search)
    search_value = request.GET.get('search[value]', '')
    if search_value:
        communities = communityTbl.objects.filter(
            Q(community__icontains=search_value) |
            Q(community_leader_name__icontains=search_value) |
            Q(community_leader_contact__icontains=search_value) |
            Q(healthFacilitiesTbl_foreignkey__facility_name__icontains=search_value)
        )
        filtered_count = communities.count()
    else:
        communities = communityTbl.objects.all()
        filtered_count = total
    
    # Apply pagination
    communities = communities.order_by('-id')[start:start + length]
    
    # Prepare data
    data = []
    for community in communities:
        data.append({
            'id': community.id,
            'community': community.community,
            'health_facility': {
                'id': community.healthFacilitiesTbl_foreignkey.id,
                'facility_name': community.healthFacilitiesTbl_foreignkey.facility_name,
                'facility_type': community.healthFacilitiesTbl_foreignkey.facility_type,
            } if community.healthFacilitiesTbl_foreignkey else None,
            'population': community.population,
            'community_leader_name': community.community_leader_name,
            'community_leader_contact': community.community_leader_contact,
        })
    
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': filtered_count,
        'data': data,
    })

@csrf_exempt
@require_http_methods(["POST"])
def add_community(request):
    try:
        health_facility_id = request.POST.get('health_facility')
        community_name = request.POST.get('community')
        population = request.POST.get('population')
        leader_name = request.POST.get('leader_name', '')
        leader_contact = request.POST.get('leader_contact', '')
        
        if not all([health_facility_id, community_name, population]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        health_facility = get_object_or_404(healthFacilitiesTbl, id=health_facility_id)
        
        community = communityTbl(
            healthFacilitiesTbl_foreignkey=health_facility,
            community=community_name,
            population=population,
            community_leader_name=leader_name,
            community_leader_contact=leader_contact
        )
        community.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_community(request, community_id):
    try:
        community = get_object_or_404(communityTbl, id=community_id)
        
        return JsonResponse({
            'success': True,
            'community': {
                'id': community.id,
                'community': community.community,
                'population': community.population,
                'community_leader_name': community.community_leader_name,
                'community_leader_contact': community.community_leader_contact,
                'healthFacilitiesTbl_foreignkey': {
                    'id': community.healthFacilitiesTbl_foreignkey.id,
                    'facility_name': community.healthFacilitiesTbl_foreignkey.facility_name,
                } if community.healthFacilitiesTbl_foreignkey else None,
            }
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def update_community(request, community_id):
    try:
        community = get_object_or_404(communityTbl, id=community_id)
        
        health_facility_id = request.POST.get('health_facility')
        community_name = request.POST.get('community')
        population = request.POST.get('population')
        leader_name = request.POST.get('leader_name', '')
        leader_contact = request.POST.get('leader_contact', '')
        
        if not all([health_facility_id, community_name, population]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        health_facility = get_object_or_404(healthFacilitiesTbl, id=health_facility_id)
        
        community.healthFacilitiesTbl_foreignkey = health_facility
        community.community = community_name
        community.population = population
        community.community_leader_name = leader_name
        community.community_leader_contact = leader_contact
        community.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def delete_community(request, community_id):
    try:
        community = get_object_or_404(communityTbl, id=community_id)
        community.delete()
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



######################################################################################################


@ login_required(login_url='/accounts/login')
def healthfacilitiesview(request):
    hf =healthFacilitiesTbl.objects.all()
    district = Districts.objects.all()

    context = {
        'hf': hf,
        'districts': district
    }
    return render(request, 'portal/healthfacilities.html', context)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# from .models import HealthFacilitiesTbl, District
from django.core.paginator import Paginator
import json

def health_facilities(request):
    districts = Districts.objects.all()
    return render(request, 'portal/health_facilities.html', {'districts': districts})

@csrf_exempt
def health_facilities_data(request):
    if request.method == 'GET':
        # Get Datatables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Base query
        query = healthFacilitiesTbl.objects.all().order_by('-id')
        
        # Apply search filter
        if search_value:
            query = query.filter(
                Q(facility_name__icontains=search_value) |
                Q(district__name__icontains=search_value) |
                Q(incharge_name__icontains=search_value) |
                Q(incharge_contact__icontains=search_value)
            )
        
        # Total records before filtering
        total_records = healthFacilitiesTbl.objects.count()
        
        # Total records after filtering
        filtered_records = query.count()
        
        # Pagination
        paginator = Paginator(query, length)
        page = (start // length) + 1
        page_obj = paginator.get_page(page)
        
        # Prepare data
        data = []
        for facility in page_obj:
            data.append({
                'id': facility.id,
                'district': facility.district.district if facility.district else '',
                'district_id': facility.district.id if facility.district else None,
                'facility_name': facility.facility_name,
                'no_of_communities': facility.no_of_commuities,
                'incharge_name': facility.name_of_incharge,
                'incharge_contact': facility.contact_of_incharge,
                'longitude': facility.longitude,
                'latitude': facility.latitude,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)

@csrf_exempt
def add_health_facility(request):
    if request.method == 'POST':
        try:
            district_id = request.POST.get('district')
            facility_name = request.POST.get('facility_name')
            no_of_communities = request.POST.get('no_of_communities')
            incharge_name = request.POST.get('incharge_name')
            incharge_contact = request.POST.get('incharge_contact')
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            
            # Validate required fields
            if not all([district_id, facility_name, no_of_communities, incharge_name, incharge_contact]):
                return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
            
            # Create new facility
            district = Districts.objects.get(id=district_id)
            facility = healthFacilitiesTbl(
                district=district,
                facility_name=facility_name,
                no_of_communities=no_of_communities,
                incharge_name=incharge_name,
                incharge_contact=incharge_contact,
                longitude=longitude,
                latitude=latitude
            )
            facility.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_health_facility(request, id):
    if request.method == 'GET':
        try:
            facility = healthFacilitiesTbl.objects.get(id=id)
            data = {
                'id': facility.id,
                'district': facility.district.district if facility.district else '',
                'district_id': facility.district.id if facility.district else None,
                'facility_name': facility.facility_name,
                'no_of_communities': facility.no_of_commuities,
                'incharge_name': facility.name_of_incharge,
                'incharge_contact': facility.contact_of_incharge,
                'longitude': facility.longitude,
                'latitude': facility.latitude,
            }
            
            return JsonResponse(data)
        except healthFacilitiesTbl.DoesNotExist:
            return JsonResponse({'error': 'Facility not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.contrib.gis.geos import Point
@csrf_exempt
def edit_health_facility(request):
    if request.method == 'POST':
        print("hello")
        try:
            facility_id = request.POST.get('id')
            district_id = request.POST.get('district')
            facility_name = request.POST.get('facility_name')
            no_of_communities = request.POST.get('no_of_communities')
            incharge_name = request.POST.get('incharge_name')
            incharge_contact = request.POST.get('incharge_contact')
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            print(facility_id, district_id, facility_name, no_of_communities, incharge_name, incharge_contact, longitude, latitude)
            
            # Validate required fields
            if not all([facility_id, district_id, facility_name, no_of_communities, incharge_name, incharge_contact]):
                return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
            
            # Convert longitude and latitude to float and create Point
            point = None
            if longitude and latitude:
                try:
                    point = Point(float(longitude), float(latitude))
                except (ValueError, TypeError):
                    return JsonResponse({'success': False, 'error': 'Invalid longitude/latitude values'})
            
            # Update facility
            facility = healthFacilitiesTbl.objects.get(id=facility_id)
            district = Districts.objects.get(id=district_id)
            
            facility.district = district
            facility.facility_name = facility_name
            facility.no_of_commuities = no_of_communities
            facility.name_of_incharge = incharge_name
            facility.contact_of_incharge = incharge_contact
            
            # if point:
            #     facility.location = point  # or whatever your PointField is named
            # # OR if you have separate longitude/latitude fields:
            # facility.longitude = longitude
            # facility.latitude = latitude
            
            facility.save()
            
            return JsonResponse({'success': True})
        
        except healthFacilitiesTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Facility not found'})
        except Districts.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'District not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})




@csrf_exempt
def delete_health_facility(request):
    if request.method == 'POST':
        try:
            facility_id = request.POST.get('id')
            
            if not facility_id:
                return JsonResponse({'success': False, 'error': 'Facility ID is required'})
            
            facility = healthFacilitiesTbl.objects.get(id=facility_id)
            facility.delete()
            
            return JsonResponse({'success': True})
        
        except healthFacilitiesTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Facility not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


########################################################################################################





@ login_required(login_url='/accounts/login')
def healthworkerview(request):
    hf =healthWorkersTbl.objects.all()
    health_facilities = healthFacilitiesTbl.objects.all()

    context = {
        'health_facilities':health_facilities
    }
    return render(request, 'portal/healthworkers.html', context)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
# from .models import HealthWorkersTbl, HealthFacilitiesTbl
from django.core.paginator import Paginator
import json

def health_workers(request):
    facilities = healthWorkersTbl.objects.all()
    return render(request, 'portal/health_workers.html', {'facilities': facilities})

@csrf_exempt
def health_workers_data(request):
    if request.method == 'GET':
        # Get Datatables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Base query
        query = healthWorkersTbl.objects.select_related('healthFacilitiesTbl_foreignkey').all().order_by('-id')
        
        # Apply search filter
        if search_value:
            query = query.filter(
                Q(hw_name__icontains=search_value) |
                Q(designation__icontains=search_value) |
                Q(hw_contact__icontains=search_value) |
                Q(healthFacilitiesTbl_foreignkey__facility_name__icontains=search_value)
            )
        
        # Total records before filtering
        total_records = healthWorkersTbl.objects.count()
        
        # Total records after filtering
        filtered_records = query.count()
        
        # Pagination
        paginator = Paginator(query, length)
        page = (start // length) + 1
        page_obj = paginator.get_page(page)
        
        # Prepare data
        data = []
        for worker in page_obj:
            data.append({
                'id': worker.id,
                'facility_id': worker.healthFacilitiesTbl_foreignkey.id if worker.healthFacilitiesTbl_foreignkey else None,
                'facility_name': worker.healthFacilitiesTbl_foreignkey.facility_name if worker.healthFacilitiesTbl_foreignkey else '',
                'hw_name': worker.hw_name,
                'designation': worker.designation,
                'hw_contact': worker.hw_contact,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)

@csrf_exempt
def add_health_worker(request):
    if request.method == 'POST':
        try:
            facility_id = request.POST.get('facility')
            hw_name = request.POST.get('hw_name')
            designation = request.POST.get('designation')
            hw_contact = request.POST.get('hw_contact')
            
            # Validate required fields
            if not all([facility_id, hw_name, designation, hw_contact]):
                return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
            
            # Create new worker
            facility = healthWorkersTbl.objects.get(id=facility_id)
            worker = healthWorkersTbl(
                healthFacilitiesTbl_foreignkey=facility,
                hw_name=hw_name,
                designation=designation,
                hw_contact=hw_contact
            )
            worker.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_health_worker(request, id):
    if request.method == 'GET':
        try:
            worker = healthWorkersTbl.objects.get(id=id)
            data = {
                'id': worker.id,
                'facility_id': worker.healthFacilitiesTbl_foreignkey.id if worker.healthFacilitiesTbl_foreignkey else None,
                'hw_name': worker.hw_name,
                'designation': worker.designation,
                'hw_contact': worker.hw_contact,
            }
            return JsonResponse(data)
        except healthWorkersTbl.DoesNotExist:
            return JsonResponse({'error': 'Worker not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_health_worker(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            worker_id = request.POST.get('id')
            facility_id = request.POST.get('facility')
            hw_name = request.POST.get('hw_name')
            designation = request.POST.get('designation')
            hw_contact = request.POST.get('hw_contact')

            print(worker_id)
            print(facility_id)
            print(hw_name)
            print(designation)
            print(hw_contact)
            
            # Validate required fields
            if not all([worker_id, facility_id, hw_name, designation, hw_contact]):
                return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
            
            # Update worker
            worker = healthWorkersTbl.objects.get(id=worker_id)
            facility = healthFacilitiesTbl.objects.get(id=facility_id)
            
            worker.healthFacilitiesTbl_foreignkey = facility
            worker.hw_name = hw_name
            worker.designation = designation
            worker.hw_contact = hw_contact
            worker.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_health_worker(request):
    if request.method == 'POST':
        try:
            worker_id = request.POST.get('id')
          
            
            if not worker_id:
                return JsonResponse({'success': False, 'error': 'Worker ID is required'})
            
            worker = healthWorkersTbl.objects.get(id=worker_id)
            worker.delete()
            
            return JsonResponse({'success': True})
        
        except healthWorkersTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Worker not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# @csrf_exempt
# def delete_health_facility(request):
#     if request.method == 'POST':
#         try:
#             facility_id = request.POST.get('id')
            
#             if not facility_id:
#                 return JsonResponse({'success': False, 'error': 'Facility ID is required'})
            
#             facility = healthFacilitiesTbl.objects.get(id=facility_id)
#             facility.delete()
            
#             return JsonResponse({'success': True})
        
#         except healthFacilitiesTbl.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Facility not found'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})



#####################################################################################################





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import json

@login_required(login_url='/accounts/login')
def cwcscheduleview(request):
    cwc_types = cwcScheduleTbl.CATEGORY_CHOICES
    cwc_categories = cwcScheduleTbl.CHOICES

    health_facilities = healthFacilitiesTbl.objects.all()
    
    context = {
        'cwc_types': cwc_types,
        'cwc_categories': cwc_categories,
        'health_facilities': health_facilities
    }
    return render(request, 'portal/cwcschedule.html', context)

@csrf_exempt
def cwc_schedule_data(request):
    if request.method == 'GET':
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Get filter parameters
        facility_id = request.GET.get('facility')
        cwc_type = request.GET.get('cwc_type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Base query
        query = cwcScheduleTbl.objects.select_related('healthFacilitiesTbl_foreignkey').all()
        
        # Apply filters
        if facility_id:
            query = query.filter(healthFacilitiesTbl_foreignkey_id=facility_id)
        
        if cwc_type:
            query = query.filter(cwc_type=cwc_type)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(date__range=[start_date, end_date])
            except ValueError:
                pass
        
        # Apply search filter
        if search_value:
            query = query.filter(
                Q(cwc_type__icontains=search_value) |
                Q(cwc_category__icontains=search_value) |
                Q(healthFacilitiesTbl_foreignkey__facility_name__icontains=search_value)
            )
        
        # Total records before filtering
        total_records = cwcScheduleTbl.objects.count()
        
        # Total records after filtering
        filtered_records = query.count()
        
        # Pagination
        paginator = Paginator(query, length)
        page = (start // length) + 1
        page_obj = paginator.get_page(page)
        
        # Prepare data
        data = []
        for schedule in page_obj:
            data.append({
                'id': schedule.id,
                'facility_id': schedule.healthFacilitiesTbl_foreignkey.id,
                'facility_name': schedule.healthFacilitiesTbl_foreignkey.facility_name,
                'cwc_type': schedule.get_cwc_type_display(),
                'cwc_category': schedule.get_cwc_category_display(),
                'date': schedule.date.isoformat(),
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)

@csrf_exempt
def add_cwc_schedule(request):
    if request.method == 'POST':
        try:
            data = request.POST
            facility_id = data.get('facility')
            cwc_type = data.get('cwc_type')
            cwc_category = data.get('cwc_category')
            date = data.get('date')
            
            # Validate required fields
            if not all([facility_id, cwc_type, cwc_category, date]):
                return JsonResponse({'success': False, 'error': 'All fields are required'})
            
            # Create new schedule
            schedule = cwcScheduleTbl(
                healthFacilitiesTbl_foreignkey_id=facility_id,
                cwc_type=cwc_type,
                cwc_category=cwc_category,
                date=date
            )
            schedule.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_cwc_schedule(request, id):
    if request.method == 'GET':
        try:
            schedule = cwcScheduleTbl.objects.get(id=id)
            data = {
                'id': schedule.id,
                'facility_id': schedule.healthFacilitiesTbl_foreignkey.id,
                'cwc_type': schedule.cwc_type,
                'cwc_category': schedule.cwc_category,
                'date': schedule.date.isoformat(),
            }
            return JsonResponse(data)
        except cwcScheduleTbl.DoesNotExist:
            return JsonResponse({'error': 'Schedule not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_cwc_schedule(request):
    if request.method == 'POST':
        try:
            data = request.POST
            schedule_id = data.get('id')
            facility_id = data.get('facility')
            cwc_type = data.get('cwc_type')
            cwc_category = data.get('cwc_category')
            date = data.get('date')
            
            # Validate required fields
            if not all([schedule_id, facility_id, cwc_type, cwc_category, date]):
                return JsonResponse({'success': False, 'error': 'All fields are required'})
            
            # Update schedule
            schedule = cwcScheduleTbl.objects.get(id=schedule_id)
            schedule.healthFacilitiesTbl_foreignkey_id = facility_id
            schedule.cwc_type = cwc_type
            schedule.cwc_category = cwc_category
            schedule.date = date
            schedule.save()
            
            return JsonResponse({'success': True})
        
        except cwcScheduleTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Schedule not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_cwc_schedule(request):
    if request.method == 'POST':
        try:
            schedule_id = request.POST.get('id')
            
            if not schedule_id:
                return JsonResponse({'success': False, 'error': 'Schedule ID is required'})
            
            schedule = cwcScheduleTbl.objects.get(id=schedule_id)
            schedule.delete()
            
            return JsonResponse({'success': True})
        
        except cwcScheduleTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Schedule not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})







#Assets
######################################################################################################


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import assetType, asset
from datetime import datetime

def assets_view(request):
    asset_types = assetType.objects.all()
    return render(request, 'portal/assets.html', {
        'asset_types': asset_types
    })

@require_http_methods(["GET"])
def assets_data(request):
    # Get query parameters
    asset_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    # Start with all assets
    assets = asset.objects.select_related('asset_type_foreignkey').all()
    
    # Apply filters
    if asset_type:
        assets = assets.filter(asset_type_foreignkey_id=asset_type)
    
    if status.lower() == 'true':
        assets = assets.filter(status=True)
    elif status.lower() == 'false':
        assets = assets.filter(status=False)
    
    if search:
        assets = assets.filter(
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(serial_number__icontains=search)
        )
    
    # Prepare data for DataTables
    data = []
    for a in assets:
        data.append({
            'id': a.id,
            'asset_type': a.asset_type_foreignkey.asset_type,
            'brand': a.brand,
            'model': a.model,
            'serial_number': a.serial_number,
            'purchase_date': a.purchase_date.isoformat(),
            'warranty_expiration': a.warranty_expiration.isoformat(),
            'status': a.status
        })
    
    return JsonResponse({
        'data': data,
        'draw': request.GET.get('draw', 1),
        'recordsTotal': asset.objects.count(),
        'recordsFiltered': assets.count()
    }, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_asset(request):
    try:
        asset_type_id = request.POST.get('asset_type')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        serial_number = request.POST.get('serial_number')
        purchase_date = request.POST.get('purchase_date')
        warranty_expiration = request.POST.get('warranty_expiration')
        status = request.POST.get('status', 'false') == 'on'
        
        # Validate required fields
        if not all([asset_type_id, brand, model, serial_number, purchase_date, warranty_expiration]):
            return JsonResponse({'success': False, 'error': 'All fields are required'}, status=400)
        
        # Check if serial number already exists
        if asset.objects.filter(serial_number=serial_number).exists():
            return JsonResponse({'success': False, 'error': 'Serial number already exists'}, status=400)
        
        # Create new asset
        new_asset = asset(
            asset_type_foreignkey_id=asset_type_id,
            brand=brand,
            model=model,
            serial_number=serial_number,
            purchase_date=purchase_date,
            warranty_expiration=warranty_expiration,
            status=status
        )
        new_asset.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def add_asset_type(request):
    try:
        asset_type_name = request.POST.get('asset_type')
        
        if not asset_type_name:
            return JsonResponse({'success': False, 'error': 'Asset type name is required'}, status=400)
        
        if assetType.objects.filter(asset_type=asset_type_name).exists():
            return JsonResponse({'success': False, 'error': 'Asset type already exists'}, status=400)
        
        new_type = assetType(asset_type=asset_type_name)
        new_type.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_asset(request, asset_id):
    try:
        a = get_object_or_404(asset, pk=asset_id)
        return JsonResponse({
            'id': a.id,
            'asset_type_foreignkey': a.asset_type_foreignkey_id,
            'brand': a.brand,
            'model': a.model,
            'serial_number': a.serial_number,
            'purchase_date': a.purchase_date.isoformat(),
            'warranty_expiration': a.warranty_expiration.isoformat(),
            'status': a.status
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def edit_asset(request):
    try:
        asset_id = request.POST.get('id')
        asset_type_id = request.POST.get('asset_type')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        serial_number = request.POST.get('serial_number')
        purchase_date = request.POST.get('purchase_date')
        warranty_expiration = request.POST.get('warranty_expiration')
        status = request.POST.get('status', 'false') == 'on'
        
        # Validate required fields
        if not all([asset_id, asset_type_id, brand, model, serial_number, purchase_date, warranty_expiration]):
            return JsonResponse({'success': False, 'error': 'All fields are required'}, status=400)
        
        # Get the asset to edit
        a = get_object_or_404(asset, pk=asset_id)
        
        # Check if serial number is being changed to one that already exists
        if a.serial_number != serial_number and asset.objects.filter(serial_number=serial_number).exists():
            return JsonResponse({'success': False, 'error': 'Serial number already exists'}, status=400)
        
        # Update the asset
        a.asset_type_foreignkey_id = asset_type_id
        a.brand = brand
        a.model = model
        a.serial_number = serial_number
        a.purchase_date = purchase_date
        a.warranty_expiration = warranty_expiration
        a.status = status
        a.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_asset(request):
    try:
        asset_id = request.POST.get('id')
        if not asset_id:
            return JsonResponse({'success': False, 'error': 'Asset ID is required'}, status=400)
        
        a = get_object_or_404(asset, pk=asset_id)
        a.delete()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
###############################################################################################

#PC DAILY REPORT


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import pcreportTbl
import json
from datetime import datetime


from django.shortcuts import render

def pc_reports_view(request):
    """Render the PC Reports page"""
    return render(request, 'portal/pcreport.html', {
        'page_title': 'PC Daily Reports',
        'active_tab': 'reports'
    })

@csrf_exempt
def pc_reports_data(request):
    if request.method == 'GET':
        # Get filter parameters from request
        pc_name = request.GET.get('pc_name', '')
        district = request.GET.get('district', '')
        facility = request.GET.get('facility', '')
        date = request.GET.get('date', '')
        
        # Start with all reports
        reports = pcreportTbl.objects.all()
        
        # Apply filters
        if pc_name:
            reports = reports.filter(name_of_pc__icontains=pc_name)
        if district:
            reports = reports.filter(district__icontains=district)
        if facility:
            reports = reports.filter(hf_name__icontains=facility)
        if date:
            reports = reports.filter(reporting_date=date)
        
        # Prepare data for DataTables
        data = []
        for report in reports:
            data.append({
                'id': report.id,
                'name_of_pc': report.name_of_pc,
                'reporting_date': report.reporting_date.isoformat(),
                'district': report.district,
                'hf_name': report.hf_name,
                'new_registrants': report.new_registrants,
            })
        
        return JsonResponse({
            'data': data,
            'draw': request.GET.get('draw', 1),
            'recordsTotal': pcreportTbl.objects.count(),
            'recordsFiltered': reports.count(),
        })

@csrf_exempt
def get_pc_report(request, report_id):
    if request.method == 'GET':
        try:
            report = pcreportTbl.objects.get(id=report_id)
            data = {
                'id': report.id,
                'name_of_pc': report.name_of_pc,
                'reporting_date': report.reporting_date.isoformat(),
                'district': report.district,
                'hf_name': report.hf_name,
                'hf_coodinates_lat': report.hf_coodinates_lat,
                'hf_coodinates_lng': report.hf_coodinates_lng,
                'new_registrants': report.new_registrants,
                'tablets_functional': report.tablets_functional,
                'scanners_functional': report.scanners_functional,
                'hw_concern_about_etracker': report.hw_concern_about_etracker,
                'hw_concern_about_biometrics': report.hw_concern_about_biometrics,
                'clients_have_issues': report.clients_have_issues,
                'positive_feedback': report.positive_feedback,
                'hw_positive_feedback': report.hw_positive_feedback,
                'feedback_comment': report.feedback_comment,
                'recommendation': report.recommendation,
                'success': True
            }
            return JsonResponse(data)
        except pcreportTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'}, status=404)

@csrf_exempt
def add_pc_report(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            
            # Create new report
            report = pcreportTbl(
                name_of_pc=data.get('name_of_pc'),
                reporting_date=data.get('reporting_date'),
                district=data.get('district'),
                hf_name=data.get('hf_name'),
                hf_coodinates_lat=float(data.get('hf_coodinates_lat', 0)),
                hf_coodinates_lng=float(data.get('hf_coodinates_lng', 0)),
                new_registrants=data.get('new_registrants'),
                tablets_functional=data.get('tablets_functional'),
                scanners_functional=data.get('scanners_functional'),
                hw_concern_about_etracker=data.get('hw_concern_about_etracker'),
                hw_concern_about_biometrics=data.get('hw_concern_about_biometrics'),
                clients_have_issues=data.get('clients_have_issues'),
                positive_feedback=data.get('positive_feedback'),
                hw_positive_feedback=data.get('hw_positive_feedback'),
                feedback_comment=data.get('feedback_comment'),
                recommendation=data.get('recommendation'),
                SubmissionDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                uid=request.user.id if request.user.is_authenticated else 'anonymous'
            )
            report.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def edit_pc_report(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            report_id = data.get('id')
            
            # Get existing report
            report = pcreportTbl.objects.get(id=report_id)
            
            # Update fields
            report.name_of_pc = data.get('name_of_pc')
            report.reporting_date = data.get('reporting_date')
            report.district = data.get('district')
            report.hf_name = data.get('hf_name')
            report.hf_coodinates_lat = float(data.get('hf_coodinates_lat', 0))
            report.hf_coodinates_lng = float(data.get('hf_coodinates_lng', 0))
            report.new_registrants = data.get('new_registrants')
            report.tablets_functional = data.get('tablets_functional')
            report.scanners_functional = data.get('scanners_functional')
            report.hw_concern_about_etracker = data.get('hw_concern_about_etracker')
            report.hw_concern_about_biometrics = data.get('hw_concern_about_biometrics')
            report.clients_have_issues = data.get('clients_have_issues')
            report.positive_feedback = data.get('positive_feedback')
            report.hw_positive_feedback = data.get('hw_positive_feedback')
            report.feedback_comment = data.get('feedback_comment')
            report.recommendation = data.get('recommendation')
            
            report.save()
            
            return JsonResponse({'success': True})
        except pcreportTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def delete_pc_report(request):
    if request.method == 'POST':
        try:
            report_id = request.POST.get('id')
            report = pcreportTbl.objects.get(id=report_id)
            report.delete()
            return JsonResponse({'success': True})
        except pcreportTbl.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)



###################################################################################################


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



class healthFacilitiestblView(GeoJSONLayerView):
  model = healthFacilitiesTbl

  precision = 4   
  simplify = 0.0001
  properties = ("district__district",'facility_name','facility_type','ownership','no_of_commuities','name_of_incharge','contact_of_incharge','longitude','latitude')
  


class pcreportTblView(GeoJSONLayerView):
    model = pcreportTbl

    precision = 4   
    simplify = 0.0001
    properties = ("name_of_pc",'reporting_date','district','hf_name','hf_coodinates_lat','hf_coodinates_lng','new_registrants','tablets_functional','latitude','positive_feedback','hw_positive_feedback','feedback_comment','SubmissionDate')

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_query = self.build_filter_query()
        return queryset.filter(**filter_query)

    def build_filter_query(self):
        filter_query = {}
        
        name_of_pc = self.request.GET.get('pc')
        if name_of_pc:
            filter_query['name_of_pc'] = name_of_pc
            queryset = self.filter_by_user(queryset, name_of_pc)

        startdate = self.request.GET.get('startDate')
        enddate = self.request.GET.get('endDate')

        if startdate and enddate:
            print("hellooo")
            filter_query['reporting_date__range'] = (startdate, enddate)
        elif startdate:
            filter_query['reporting_date__date__gte'] = startdate
        elif enddate:
            filter_query['reporting_date__date__lte'] = enddate

        return filter_query

    

def testview(request):
    for aa in Districts.objects.all():
        name= aa.district.replace('DISTRICT','').replace('MUNICIPAL','').replace('METROPOLITAN','')
        Districts.objects.filter(id=aa.id).update(district_2=name)
    return render(request, 'portal/cwcschedule.html', locals())



def AutocompleteView(request):
	# data = Farms.objects.filter(farmerTbl_foreignkey__first_name__icontains = request.GET['phrase'])[:10]
	data1 = []
	n = 0
  

	data =  healthFacilitiesTbl.objects.filter(facility_name__icontains = request.GET['phrase'])[:10]
	for s in data:
		sname = str(s.facility_name)
		data1.append({'code':str(s.id),'name':sname , 'type' : 'facility'})

	
	return JsonResponse(data1, safe=False)


def hfextentView(request,code,ftype):
    tojson = ""
    if ftype == "facility":
        tojson=healthFacilitiesTbl.objects.filter(id=code).aggregate(Extent('geom')).get('geom__extent')
    
    return JsonResponse(tojson,safe = False)


# def fetchdataView(request):
#     import pysurveycto ,json,csv,datetime
#     server_name = "simprints"
#     username="ghanaconnector@simprints-apis.com"
#     password="kwarteng19"
#     scto = pysurveycto.SurveyCTOObject(server_name, username, password)

#     date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
#     datas = scto.get_form_data('PC_monitoring_form',format='json', oldest_completion_date=date_input)
#     # dataz = json.load(datas)
#     for data in datas:
#         print(data)
       
#         CompletionDate = data['CompletionDate']
#         SubmissionDate= data['SubmissionDate']
#         name_of_pc= data['name_of_pc']
#         reporting_date= data['reporting_date']
#         district= data['district']
#         hf_name= data['hf_name']
#         hf_coodinates= data['hf_coodinates']
#         new_registrants= data['new_registrants']
#         tablets_functional= data['tablets_functional']
#         tabissues=[]
#         if tablets_functional == "no":
#             if data['issue_with_tablet_Battery_'] == '1':
#                 tabissues.append("issue_with_tablet_Battery_")
#             if data['issue_with_tablet_Cracked_Screen'] == '1':
#                 tabissues.append("issue_with_tablet_Cracked_Screen")

#             if data['issue_with_tablet_Freezing'] =='1':
#                 tabissues.append("issue_with_tablet_Freezing")

#             if data['issue_with_tablet_Chargingport_Malfunctioning']== '1':
#                 tabissues.append("issue_with_tablet_Chargingport_Malfunctioning")

#             if data['issue_with_tablet_Faulty_Charger']== '1':
#                 tabissues.append("issue_with_tablet_Faulty_Charger")

#             if data['issue_with_tablet_Black_Screen']== '1':
#                 tabissues.append("issue_with_tablet_Black_Screen")
#             if data['issue_with_tablet_Constant_Restarting']== '1':
#                 tabissues.append("issue_with_tablet_Constant_Restarting")

#             if data['issue_with_tablet_Over_Heating']== '1':
#                 tabissues.append("issue_with_tablet_Over_Heating")

#             if data['issue_with_tablet_Other']== '1':
#                 tabissues.append("issue_with_tablet_Other")

#         print(tabissues)
            

#     return JsonResponse("tojson",safe = False)
# def fetchdataView(request):
#     import pysurveycto
#     import json
#     import datetime
#     from django.http import JsonResponse

#     server_name = "simprints"
#     username = "ghanaconnector@simprints-apis.com"
#     password = "kwarteng19"
#     scto = pysurveycto.SurveyCTOObject(server_name, username, password)

#     date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
#     datas = scto.get_form_data('PC_monitoring_form', format='json', oldest_completion_date=date_input)

#     all_data = []
    
#     for data in datas:
#         tabissues = []
#         scanissues =[]
#         concern_about=[]
#         CompletionDate = data.get('CompletionDate')
#         SubmissionDate = data.get('SubmissionDate')
#         name_of_pc = data.get('name_of_pc')
#         reporting_date = data.get('reporting_date')
#         district = data.get('district')
#         hf_name = data.get('hf_name')
#         hf_coordinates = data.get('hf_coodinates')
#         coordinates = hf_coordinates.split()
#         latitude = float(coordinates[0])
#         longitude = float(coordinates[1])
#         new_registrants = data.get('new_registrants')
#         tablets_functional = data.get('tablets_functional')
#         scanners_functional =  data.get('scanners_functional')
#         hw_concern_about_etracker =  data.get('hw_concern_about_etracker')
#         hw_concern_about_biometrics=data.get('hw_concern_about_biometrics')
#         clients_have_issues=data.get('clients_have_issues')
#         positive_feedback=data.get('positive_feedback')
#         hw_positive_feedback=data.get('hw_positive_feedback')
#         feedback_comment=data.get('feedback_comment')
#         recommendation=data.get('recommendation')
#         instanceID=data.get('instanceID')

#         print(instanceID)
        
#         if tablets_functional == "no":
#             issues = [
#                 'issue_with_tablet_Battery_',
#                 'issue_with_tablet_Cracked_Screen',
#                 'issue_with_tablet_Freezing',
#                 'issue_with_tablet_Chargingport_Malfunctioning',
#                 'issue_with_tablet_Faulty_Charger',
#                 'issue_with_tablet_Black_Screen',
#                 'issue_with_tablet_Constant_Restarting',
#                 'issue_with_tablet_Over_Heating',
#                 'issue_with_tablet_Other'
#             ]
#             for issue in issues:
#                 if data.get(issue) == '1':  # Use .get() to avoid KeyError
#                     print(issue)  # For debugging
#                     tabissues.append(issue)


#             if scanners_functional == "no":
#                 sissues = [
#                     'issue_with_scanner_Update_Failure',
#                     'issue_with_scanner_Bluetooth_Not_Connecting',
#                     'issue_with_scanner_Cracked__Lens',
#                     'issue_with_scanner_Faulty_Power'
#                     'issue_with_scanner_Scanning_Button'
#                     'issue_with_scanner_Other'
#                 ]
#                 for issue in sissues:
#                     if data.get(issue) == '1':  # Use .get() to avoid KeyError
#                         scanissues.append(issue)

#             if hw_concern_about_etracker == "yes":
#                 hw_concern_about_etracker_com = [

#                     'hw_concern_Synncing_Failure_'
#                     'hw_concern_Permission_Errors_With_Program_Enrolments'
#                     'hw_concern_Constant_Crushing'
#                     'hw_concern_Difficulty_Finding_Enrolled_Clients_With_Demographic_Search_'
#                     'hw_concern_Other'
#                 ]
#                 for com in hw_concern_about_etracker_com:
#                     if data.get(com) == '1':  # Use .get() to avoid KeyError
#                         concern_about.append(com)


#             if hw_concern_about_biometrics == "yes":
#                 hw_concern_about_biometrics_con = [

#                     'hw_concern_biometric_Configuraton_Error',
#                     'hw_concern_biometric_Verification_Failure',
#                     'hw_concern_biometric_Person_Not_Found_Error_Screen',
#                     'hw_concern_biometric_Failed_Identifcation',
#                     'hw_concern_biometric_Failed_Syncing_In_Sid'

#                 ]
#                 for con in hw_concern_about_biometrics_con:
#                     if data.get(com) == '1':  # Use .get() to avoid KeyError
#                         concern_about.append(com)



#             if clients_have_issues == "yes":
#                 clients_have_issues_con = [

#                     'client_issue_Religious_Reasons',
#                     'client_issue_Personal_Reasons',
#                     'client_issue_Political_Reasons',
#                     'client_issue_Lack_Of_Education',

#                 ]
#                 for con in clients_have_issues_con:
#                     if data.get(com) == '1':  # Use .get() to avoid KeyError
#                         concern_about.append(com)


#             if positive_feedback == 'yes':
#                 hw_positive_feedback=hw_positive_feedback
#             else:
#                 hw_positive_feedback = ""


#         # Add processed data to the list
#         all_data.append({
#             'CompletionDate': CompletionDate,
#             'SubmissionDate': SubmissionDate,
#             'name_of_pc': name_of_pc,
#             'reporting_date': reporting_date,
#             'district': district,
#             'hf_name': hf_name,
#             'hf_coordinates': hf_coordinates,
#             'latitude':latitude,
#             'longitude':longitude,
#             'new_registrants': new_registrants,
#             'tablets_functional': tablets_functional,
#             'tabissues': tabissues,
#             'scanners_functional':scanners_functional,
#             'scanissues' : scanissues,
#             'clients_have_issues':clients_have_issues,
#             'hw_concern_about_etracker' :concern_about,
            
#             'hw_concern_about_biometrics':hw_concern_about_biometrics,
#             'positive_feedback':positive_feedback,
#             "hw_positive_feedback":hw_positive_feedback,
#             'feedback_comment' : feedback_comment,
#             'recommendation':recommendation,
#             'instanceID':instanceID
#         })

#         # print(all_data)


#         for dat in all_data:
#             obj,creat = pcreportTbl.objects.get_or_create(
#             uid =  dat.instanceID,
#             defaults=dict(
#             name_of_pc=dat.name_of_pc,
#             reporting_date=dat.reporting_date,
#             district=dat.district,
#             hf_name=dat.hf_name,
#             hf_coodinates_lat=dat.latitude,
#             hf_coodinates_lng=dat.longitude,
#             new_registrants=dat.new_registrants,
#             tablets_functional=dat.tablets_functional,
#             scanners_functional=dat.scanners_functional,
#             hw_concern_about_etracker=dat.hw_concern_about_etracker,
#             hw_concern_about_biometrics=dat.hw_concern_about_biometrics,
#             clients_have_issues=dat.clients_have_issues,
#             positive_feedback=dat.positive_feedback,
#             hw_positive_feedback=dat.hw_positive_feedback,
#             feedback_comment=dat.feedback_comment,
#             recommendation=dat.recommendation,
#             SubmissionDate=dat.SubmissionDate,
#             uid=dat.instanceID
#             )

#             )

#             if obj :
#                 if tablets_functional == 'no':
#                     for tab in tabissues:
#                         obj,creat = tabletissueTbl.objects.get_or_create(
#                             pcreportTbl_foreignkey=obj,
#                             tablet_issue=tab
#                         )
                
#                 if scanners_functional == 'no':
#                     for scan in scanissues:
#                         obj,creat = issuewithscannerTbl.objects.get_or_create(
#                             pcreportTbl_foreignkey=obj,
#                             tablet_issue=scan
#                         )

#                 if hw_concern_about_etracker == 'yes':
#                     for hwconcern in hw_concern_about_etracker:
#                         obj,creat = hw_concernTbl.objects.get_or_create(
#                             pcreportTbl_foreignkey=obj,
#                             tablet_issue=hwconcern
#                         )

#                 if hw_concern_about_biometrics == 'yes':
#                     for biom in hw_concern_about_biometrics:
#                         obj,creat = hw_concern_biometricTbl.objects.get_or_create(
#                             pcreportTbl_foreignkey=obj,
#                             tablet_issue=biom
#                         )

#                 if clients_have_issues == 'yes':
#                     for client_issue in clients_have_issues:
#                         obj,creat = client_issueTbl.objects.get_or_create(
#                             pcreportTbl_foreignkey=obj,
#                             tablet_issue=client_issue
#                         )
                
#     return JsonResponse(all_data, safe=False)



def fetchdataView(request):
    import pysurveycto
    import json
    import datetime
    from django.http import JsonResponse

    server_name = "simprints"
    username = "ghanaconnector@simprints-apis.com"
    password = "kwarteng19"
    scto = pysurveycto.SurveyCTOObject(server_name, username, password)

    date_input = datetime.datetime(2020, 1, 12, 13, 42, 42)
    datas = scto.get_form_data('PC_monitoring_form', format='json', oldest_completion_date=date_input)

    all_data = []

    tablet_issues = [
        'issue_with_tablet_Battery_',
        'issue_with_tablet_Cracked_Screen',
        'issue_with_tablet_Freezing',
        'issue_with_tablet_Chargingport_Malfunctioning',
        'issue_with_tablet_Faulty_Charger',
        'issue_with_tablet_Black_Screen',
        'issue_with_tablet_Constant_Restarting',
        'issue_with_tablet_Over_Heating',
        'issue_with_tablet_Other'
    ]

    scanner_issues = [
        'issue_with_scanner_Update_Failure',
        'issue_with_scanner_Bluetooth_Not_Connecting',
        'issue_with_scanner_Cracked__Lens',
        'issue_with_scanner_Faulty_Power',
        'issue_with_scanner_Scanning_Button',
        'issue_with_scanner_Other'
    ]

    hw_concern_etracker = [
        'hw_concern_Synncing_Failure_',
        'hw_concern_Permission_Errors_With_Program_Enrolments',
        'hw_concern_Constant_Crushing',
        'hw_concern_Difficulty_Finding_Enrolled_Clients_With_Demographic_Search_',
        'hw_concern_Other'
    ]

    hw_concern_biometrics = [
        'hw_concern_biometric_Configuraton_Error',
        'hw_concern_biometric_Verification_Failure',
        'hw_concern_biometric_Person_Not_Found_Error_Screen',
        'hw_concern_biometric_Failed_Identifcation',
        'hw_concern_biometric_Failed_Syncing_In_Sid'
    ]

    client_issues = [
        'client_issue_Religious_Reasons',
        'client_issue_Personal_Reasons',
        'client_issue_Political_Reasons',
        'client_issue_Lack_Of_Education',
    ]

    from datetime import datetime
    for data in datas:
        # Extract data
        CompletionDate = data.get('CompletionDate')
        SubmissionDate = data.get('SubmissionDate')
        name_of_pc = data.get('name_of_pc')
        reporting_date = data.get('reporting_date')
        reporting_date = datetime.strptime(reporting_date, "%b %d, %Y").date()
        district = data.get('district')
        hf_name = data.get('hf_name')
        hf_coordinates = data.get('hf_coodinates').split()
        latitude = float(hf_coordinates[0])
        longitude = float(hf_coordinates[1])
        new_registrants = data.get('new_registrants')
        tablets_functional = data.get('tablets_functional')
        scanners_functional = data.get('scanners_functional')
        hw_concern_about_etracker = data.get('hw_concern_about_etracker')
        hw_concern_about_biometrics = data.get('hw_concern_about_biometrics')
        clients_have_issues = data.get('clients_have_issues')
        positive_feedback = data.get('positive_feedback')
        hw_positive_feedback = data.get('hw_positive_feedback')
        feedback_comment = data.get('feedback_comment')
        recommendation = data.get('recommendation')
        instanceID = data.get('instanceID')

        tabissues = get_issues(data, tablet_issues) if tablets_functional == "no" else []
        scanissues = get_issues(data, scanner_issues) if scanners_functional == "no" else []
        concern_about = []
        biometric = []
        client_iss = []
        if hw_concern_about_etracker == "yes":
            concern_about.extend(get_issues(data, hw_concern_etracker))
        if hw_concern_about_biometrics == "yes":
            biometric.extend(get_issues(data, hw_concern_biometrics))
        if clients_have_issues == "yes":
            client_iss.extend(get_issues(data, client_issues))

        all_data.append({
            'CompletionDate': CompletionDate,
            'SubmissionDate': SubmissionDate,
            'name_of_pc': name_of_pc,
            'reporting_date': reporting_date,
            'district': district,
            'hf_name': hf_name,
            'hf_coordinates': ' '.join(hf_coordinates),
            'latitude': latitude,
            'longitude': longitude,
            'new_registrants': new_registrants,
            'tablets_functional': tablets_functional,
            'tabissues': tabissues,
            'scanners_functional': scanners_functional,
            'scanissues': scanissues,
            'biometric':biometric,
            'client_iss':client_iss,
            'clients_have_issues': clients_have_issues,
            'hw_concern_about_etracker': hw_concern_about_etracker,
            'hw_concern_about_biometrics': hw_concern_about_biometrics,
            'positive_feedback': positive_feedback,
            'hw_positive_feedback': hw_positive_feedback if positive_feedback == 'yes' else "",
            'feedback_comment': feedback_comment,
            'recommendation': recommendation,
            'instanceID': instanceID
        })

        # Save to the database
        save_to_database(all_data,concern_about)

    return JsonResponse(all_data, safe=False)


def get_issues(data, issues):
    """ Helper function to get issues from the data. """
    return [issue for issue in issues if data.get(issue) == '1']


def save_to_database(all_data,concern_about):
    """ Helper function to save all data to the database. """
    for dat in all_data:
        obj, created = pcreportTbl.objects.get_or_create(
            uid=dat['instanceID'],
            defaults=dict(
                name_of_pc=dat['name_of_pc'],
                reporting_date=dat['reporting_date'],
                district=dat['district'],
                hf_name=dat['hf_name'],
                hf_coodinates_lat=dat['latitude'],
                hf_coodinates_lng=dat['longitude'],
                new_registrants=dat['new_registrants'],
                tablets_functional=dat['tablets_functional'],
                scanners_functional=dat['scanners_functional'],
                hw_concern_about_etracker=dat['hw_concern_about_etracker'],
                hw_concern_about_biometrics=dat['hw_concern_about_biometrics'],
                clients_have_issues=dat['clients_have_issues'],
                positive_feedback=dat['positive_feedback'],
                hw_positive_feedback=dat['hw_positive_feedback'],
                feedback_comment=dat['feedback_comment'],
                recommendation=dat['recommendation'],
                SubmissionDate=dat['SubmissionDate'],
            )
        )

        if obj:
            if dat['tablets_functional'] == 'no':
                for tab in dat['tabissues']:
                    pc_tabletissueTbl.objects.get_or_create(
                        pcreportTbl_foreignkey=obj,
                        tablet_issue=tab
                    )

            if dat['scanners_functional'] == 'no':
                for scan in dat['scanissues']:
                    pc_issuewithscannerTbl.objects.get_or_create(
                        pcreportTbl_foreignkey=obj,
                        issue_with_scanner=scan
                    )

            if dat['hw_concern_about_etracker'] == 'yes':
                for hwconcern in concern_about:
                    pc_hw_concernTbl.objects.get_or_create(
                        pcreportTbl_foreignkey=obj,
                        hw_concern=hwconcern
                    )

            if dat['hw_concern_about_biometrics'] == 'yes':
                for biom in dat['biometric']:
                    pc_hw_concern_biometricTbl.objects.get_or_create(
                        pcreportTbl_foreignkey=obj,
                        hw_concern_biometric=biom
                    )

            if dat['clients_have_issues'] == 'yes':
                for client_issue in dat['clients_have_issues']:
                    pc_client_issueTbl.objects.get_or_create(
                        pcreportTbl_foreignkey=obj,
                        client_issue=client_issue
                    )




def heatmapview(request):
    all = pcreportTbl.objects.all().count()
    pcr = pcreportTbl.objects.all().distinct("hf_name")
    for aa in pcr :
        print(aa)
        val =  pcreportTbl.objects.filter(hf_name = aa.hf_name).count() 
        # /all
        res = []
        for aa in pcr:
            res.append([aa.hf_coodinates_lat,aa.hf_coodinates_lng,0.5])


        # print(hwcount)
    
        return JsonResponse(res , safe=False)
    

@ login_required(login_url='/accounts/login')
def pcreportview(request):
   
    return render(request, 'portal/pcreport.html', locals())



def pcreportvResultsview(request):
   
    return render(request, 'portal/pcreport.html', locals())





















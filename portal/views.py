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

    for data in datas:
        # Extract data
        CompletionDate = data.get('CompletionDate')
        SubmissionDate = data.get('SubmissionDate')
        name_of_pc = data.get('name_of_pc')
        reporting_date = data.get('reporting_date')
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
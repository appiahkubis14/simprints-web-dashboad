from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

class staffTblResource(resources.ModelResource):
    class Meta:
        model = staffTbl
        fields =('id','user','first_name','last_name','gender','contact','designation','email_address')
class staffTblAdmin(ImportExportModelAdmin):
    resource_class = staffTblResource
    list_display = ('id','user','first_name','last_name','gender','contact','designation','email_address')
    search_fields = ['first_name','last_name','contact','designation']
admin.site.register(staffTbl, staffTblAdmin)



class districtStaffTblResource(resources.ModelResource):
    class Meta:
        model = districtStaffTbl
        fields =('id','staffTbl_foreignkey','district_foreignkey')
class districtStaffTblAdmin(ImportExportModelAdmin):
    resource_class = districtStaffTblResource
    list_display = ('id','staffTbl_foreignkey','district_foreignkey')
    search_fields = ['staffTbl_foreignkey__first_name','staffTbl_foreignkey__last_name','staffTbl_foreignkey__contact']
    raw_id_fields =('staffTbl_foreignkey','district_foreignkey')
    
admin.site.register(districtStaffTbl, districtStaffTblAdmin)


class regionStaffTblResource(resources.ModelResource):
    class Meta:
        model = regionStaffTbl
        fields =('id','staffTbl_foreignkey','region_foreignkey')
class regionStaffTblAdmin(ImportExportModelAdmin):
    resource_class = regionStaffTblResource
    list_display = ('id','staffTbl_foreignkey','region_foreignkey')
    search_fields = ['staffTbl_foreignkey__first_name','staffTbl_foreignkey__last_name','staffTbl_foreignkey__contact']
    raw_id_fields =('staffTbl_foreignkey','region_foreignkey')
admin.site.register(regionStaffTbl, regionStaffTblAdmin)



class healthFacilitiesTblResource(resources.ModelResource):
    class Meta:
        model = healthFacilitiesTbl
        fields =('id','district','facility_name','no_of_commuities','name_of_incharge','contact_of_incharge','longitude','latitude','point')
class healthFacilitiesTblAdmin(ImportExportModelAdmin):
    resource_class = healthFacilitiesTblResource
    list_display = ('district','facility_name','no_of_commuities','name_of_incharge','contact_of_incharge','longitude','latitude',)
    search_fields = ['facility_name','name_of_incharge','contact_of_incharge','district__district']
    # raw_id_fields =['district',]
admin.site.register(healthFacilitiesTbl, healthFacilitiesTblAdmin)

class healthWorkersTblResource(resources.ModelResource):
    class Meta:
        model = healthWorkersTbl
        fields =('id','healthFacilitiesTbl_foreignkey','hw_name','designation','hw_contact')
class healthWorkersTblAdmin(ImportExportModelAdmin):
    resource_class = healthWorkersTblResource
    list_display = ('id','healthFacilitiesTbl_foreignkey','hw_name','designation','hw_contact')
    search_fields = ['healthFacilitiesTbl_foreignkey__facility_name','hw_name','hw_contact','designation']
    raw_id_fields =('healthFacilitiesTbl_foreignkey',)
admin.site.register(healthWorkersTbl, healthWorkersTblAdmin)


# class healthWorkersTblResource(resources.ModelResource):
#     class Meta:
#         model = healthWorkersTbl
#         fields =('id','healthFacilitiesTbl_foreignkey','hw_name','designation','hw_contact')

# class healthWorkersTblAdmin(ImportExportModelAdmin):
#     resource_class = healthWorkersTblResource
#     list_display = ('id','healthFacilitiesTbl_foreignkey','hw_name','designation','hw_contact')
#     search_fields = ['healthFacilitiesTbl_foreignkey__facility_name','hw_name','hw_contact','designation']
# admin.site.register(healthWorkersTbl, healthWorkersTblAdmin)


class cwcScheduleTblResource(resources.ModelResource):
    class Meta:
        model = cwcScheduleTbl
        fields =('id','healthFacilitiesTbl_foreignkey','cwc_category','cwc_type','date')
class cwcScheduleTblAdmin(ImportExportModelAdmin):
    resource_class = cwcScheduleTblResource
    list_display = ('id','healthFacilitiesTbl_foreignkey','cwc_category','cwc_type','date')
    search_fields = ['healthFacilitiesTbl_foreignkey__facility_name','cwc_category','cwc_type']
admin.site.register(cwcScheduleTbl, cwcScheduleTblAdmin)



class communityTblResource(resources.ModelResource):
    class Meta:
        model = communityTbl
        fields =('id','healthFacilitiesTbl_foreignkey','community','population')
class communityTblAdmin(ImportExportModelAdmin):
    resource_class = communityTblResource
    list_display = ('id','healthFacilitiesTbl_foreignkey','community','population')
    search_fields = ['healthFacilitiesTbl_foreignkey__facility_name','community']
    raw_id_fields =('healthFacilitiesTbl_foreignkey',)

    def response_add(self, request, obj, post_url_continue=None):
        messages.success(request, f'"{obj}" was added successfully.')
        return HttpResponseRedirect('/community/')  # Redirect after adding

    def response_change(self, request, obj):
        messages.success(request, f'"{obj}" was updated successfully.')
        return HttpResponseRedirect('/community/')  # Redirect after updating
    def response_delete(self, request, obj_display, context):
        messages.success(request, f'"{obj_display}" was deleted successfully.')
        return HttpResponseRedirect('/community/')  # Redirect after deleting

    

admin.site.register(communityTbl, communityTblAdmin)

class assetTypeResource(resources.ModelResource):
    class Meta:
        model = assetType
        fields =('id','asset_type',)
class assetTypeAdmin(ImportExportModelAdmin):
    resource_class = assetTypeResource
    list_display =('asset_type',)
    search_fields = ['asset_type',]
admin.site.register(assetType, assetTypeAdmin)


class assetResource(resources.ModelResource):
    class Meta:
        model = asset
        fields =('id','asset_type_foreignkey','brand','model','serial_number','purchase_date','warranty_expiration','status',)
class assetAdmin(ImportExportModelAdmin):
    resource_class = assetResource
    list_display = ('id','asset_type_foreignkey','brand','model','serial_number','purchase_date','warranty_expiration','status',)
    search_fields = ['asset_type_foreignkey','serial_number','model','brand','status']
    raw_id_fields =('asset_type_foreignkey',)
admin.site.register(asset,assetAdmin)



class assetSaffassignementTblResource(resources.ModelResource):
    class Meta:
        model = assetSaffassignementTbl
        fields =('id','staffTbl_foreignkey','assetTbl_foreignkey')
class assetSaffassignementTblAdmin(ImportExportModelAdmin):
    resource_class = assetSaffassignementTblResource
    list_display = ('id','staffTbl_foreignkey','assetTbl_foreignkey')
    search_fields = ['staffTbl_foreignkey','assetTbl_foreignkey__serial_number','assetTbl_foreignkey__asset_type']
    raw_id_fields =('staffTbl_foreignkey','assetTbl_foreignkey')
admin.site.register(assetSaffassignementTbl, assetSaffassignementTblAdmin)


class aassetFacilityassignementTblResource(resources.ModelResource):
    class Meta:
        model = assetFacilityassignementTbl
        fields =('id','staffTbl_foreignkey','assetTbl_foreignkey')
class assetFacilityassignementTblAdmin(ImportExportModelAdmin):
    resource_class = aassetFacilityassignementTblResource
    list_display = ('id','healthFacilitiesTbl_foreignkey','assetTbl_foreignkey')
    search_fields = ['healthFacilitiesTbl_foreignkey__facility_name','assetTbl_foreignkey__serial_number','assetTbl_foreignkey__asset_type_asset_type']
    raw_id_fields =('healthFacilitiesTbl_foreignkey','assetTbl_foreignkey')
admin.site.register(assetFacilityassignementTbl, assetFacilityassignementTblAdmin)



class DistrictsResource(resources.ModelResource):
    class Meta:
        model = Districts
        fields =('id','region','district','district_code','reg_code','pilot')
class DistrictsAdmin(ImportExportModelAdmin):
    resource_class = DistrictsResource
    list_display = ('id','region','district','district_code','reg_code','pilot')
    search_fields = ['region','district','district_code','reg_code__region','pilot']
    # raw_id_fields =('district',)
    ordering = ['district']
admin.site.register(Districts, DistrictsAdmin)


# admin.site.register(Region,)
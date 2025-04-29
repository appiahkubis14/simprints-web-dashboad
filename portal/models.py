from django.db import models
# from django.contrib.gis.db import models
from django.contrib.gis.db import models 
from django.contrib.auth.models import User ,Group
from django.contrib.gis.geos import Point
# Create your models here.
class protectedValueError(Exception):
    def __init__(self, msg):
        super(protectedValueError, self).__init__(msg)
    
class timeStampManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(timeStampManager, self).__init__(*args, **kwargs)
    
    def get_queryset(self):
        if self.alive_only:
            return timeStampQuerySet(self.model).filter(delete_field="no")
        return timeStampQuerySet(self.model)	
    
    def hard_delete(self):
        return self.get_queryset().hard_delete()

class timeStampQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            item.delete()
        return super(timeStampQuerySet, self)

    def hard_delete(self):
        return super(timeStampQuerySet, self).delete()
    
    def alive(self):
        return self.filter(delete_field="no")
    
    def dead(self):
        return self.filter(delete_field="yes")

class timeStamp(models.Model):
    """
    Description: This models is an abstract class that defines the columns that should be present in every table.
    """
    created_date = models.DateTimeField(auto_now=True)
    delete_field = models.CharField(max_length=10, default="no")
    objects = timeStampManager()
    default_objects = models.Manager()
    class Meta:
        abstract = True


class Region(models.Model):

    geom = models.MultiPolygonField(blank=True, null=True)
    reg_name = models.CharField(max_length=50, blank=True, null=True)
    reg_code = models.CharField(primary_key=True)
    pilot = models.BooleanField()

    def __str__(self):
        return str(f'{self.reg_code}')
    class Meta:
        managed = True
        db_table = 'region'
        


class Districts(models.Model):
    geom = models.GeometryField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    district_2 = models.CharField(max_length=50, blank=True, null=True)
    district_code = models.CharField(max_length=254, blank=True, null=True)
    reg_code =  models.ForeignKey(Region, on_delete=models.CASCADE)
    pilot = models.BooleanField()
    
    def __str__(self):
        return str(f'{self.district}')

    class Meta:
        managed = True
        db_table = 'district'



class staffTbl(timeStamp):
    """
    Description: Contains details for Staff, Facilitators and other key personnel
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    designation = models.ForeignKey(Group, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=250, blank=True)
    uid= models.CharField(max_length=22000,blank=True, null=True)
    district = models.CharField(max_length=250, blank=True, null=True)
    staffid = models.CharField(max_length=250, blank=True, null=True)
    mpassword = models.CharField(max_length=250,default="P@ssw0rd2000")

    def __str__(self):
        return str(f'{self.first_name} {self.last_name}')
    class Meta:
        verbose_name_plural = "Staff Details"


class districtStaffTbl(timeStamp):
    staffTbl_foreignkey = models.ForeignKey(staffTbl, on_delete=models.CASCADE)
    district_foreignkey = models.ForeignKey(Districts, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Staff District Assignments"
        
class regionStaffTbl(timeStamp):
    staffTbl_foreignkey = models.ForeignKey(staffTbl, on_delete=models.CASCADE)
    region_foreignkey = models.ForeignKey(Region, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Staff Region Assignments"


class healthFacilitiesTbl(timeStamp):
    FACILITY_CHOICES = [
        ('Health Centre', 'Health Centre'),
        ('CHPS Compound', 'CHPS Compound'),
        ('Polyclinic', 'Polyclinic'),
        ('Maternity Home', 'Maternity Home'),
        ('Hospital', 'Hospital'),
        ('Clinic', 'Clinic'),
    ]


    # ownership_CHOICES = [

    #     ('government', 'Government'),
    #     ('private_facility', 'Private Facility'),
    #     ('chag', 'CHAG'),
    # ]

    district = models.ForeignKey(Districts,on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=20000,)
    facility_type = models.CharField(max_length=20000, choices=FACILITY_CHOICES)
    ownership = models.CharField(max_length=20000)
    no_of_commuities = models.IntegerField(blank=True, null=True)
    name_of_incharge = models.CharField(blank=True, null=True)
    contact_of_incharge = models.CharField(blank=True, null=True)
    longitude = models.FloatField(max_length=10,blank=True, null=True)
    latitude = models.FloatField(max_length=10,blank=True, null=True)
    geom = models.PointField(blank=True,null=True)  # For point geometry
    def save(self, *args, **kwargs):
        # Create a Point using longitude and latitude
        if self.longitude and self.latitude:
            self.geom = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.facility_name


class healthWorkersTbl(timeStamp):
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    hw_name = models.CharField(max_length=20000,)
    designation = models.CharField(max_length=54,)
    hw_contact = models.CharField(max_length=10,)
    etracker_trained = models.CharField(max_length=10,)
   

class cwcScheduleTbl(timeStamp):
    CATEGORY_CHOICES = [
        ('Static', 'Static'),
        ('Outreach', 'Outreach'),
    ]

    CHOICES = [
        ('Heavy', 'Heavy'),
        ('Normal', 'Normal'),
    ]
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    cwc_type = models.CharField(max_length=2000,choices=CATEGORY_CHOICES)
    cwc_category = models.CharField(max_length=2000,choices=CHOICES,default="Normal")
    date = models.DateField(max_length=2000,)

class communityTbl(timeStamp):
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    community = models.CharField(max_length=2000,)
    community_leader_name= models.CharField(max_length=2000,blank=True)
    community_leader_contact= models.CharField(max_length=2000,blank=True,default="Not available")
    population = models.IntegerField()
 


class assetType(timeStamp):
    asset_type = models.CharField(max_length=30)
    def __str__(self):
        return self.asset_type
    

class asset(timeStamp):
 
    asset_type_foreignkey = models.ForeignKey(assetType,on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    warranty_expiration = models.DateField()
    status = models.BooleanField(default=True)  # True for active, False for inactive

    def __str__(self):
        return f"{self.brand} "
    

class assetSaffassignementTbl(timeStamp):
    staffTbl_foreignkey = models.ForeignKey(staffTbl,on_delete=models.CASCADE)
    assetTbl_foreignkey = models.ForeignKey(asset,on_delete=models.CASCADE)


class assetFacilityassignementTbl(timeStamp):
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    assetTbl_foreignkey = models.ForeignKey(asset,on_delete=models.CASCADE)

  

# add category to the cwc tbl
#   movement_plan tbl 
class pcreportTbl(timeStamp):
    name_of_pc= models.CharField(max_length=2000,blank=True)
    reporting_date= models.DateField(max_length=2000,blank=True)
    district= models.CharField(max_length=2000,blank=True)
    hf_name= models.CharField(max_length=2000,blank=True)
    hf_coodinates_lat= models.FloatField(max_length=2000,blank=True)
    hf_coodinates_lng = models.FloatField(max_length=2000,blank=True)
    geom = models.GeometryField(null=True,blank=True)
    new_registrants= models.CharField(max_length=2000,blank=True)
    tablets_functional= models.CharField(max_length=2000,blank=True)
    # issue_with_tablet= models.CharField(max_length=2000,blank=True)
    scanners_functional= models.CharField(max_length=2000,blank=True)
    # issue_with_scanner= models.CharField(max_length=2000,blank=True)
    hw_concern_about_etracker= models.CharField(max_length=2000,blank=True)
    # hw_concern= models.CharField(max_length=2000,blank=True)
    hw_concern_about_biometrics= models.CharField(max_length=2000,blank=True)
    # hw_concern_biometric= models.CharField(max_length=2000,blank=True)
    clients_have_issues= models.CharField(max_length=2000,blank=True)
    # client_issue= models.CharField(max_length=2000,blank=True)
    positive_feedback= models.CharField(max_length=2000,blank=True)
    hw_positive_feedback= models.CharField(max_length=2000,blank=True)
    feedback_comment= models.CharField(max_length=2000,blank=True,null=True)
    recommendation= models.CharField(max_length=2000,blank=True,null=True)
    SubmissionDate= models.CharField(max_length=2000,blank=True)
    uid= models.CharField(max_length=2000,blank=True)

    def save(self, *args, **kwargs):
        # Create a Point using longitude and latitude
        if self.hf_coodinates_lat and self.hf_coodinates_lng:
            self.geom = Point(self.hf_coodinates_lng, self.hf_coodinates_lat)
        super().save(*args, **kwargs)  # Call the original save method



class pc_tabletissueTbl(timeStamp):
    pcreportTbl_foreignkey = models.ForeignKey(pcreportTbl, on_delete=models.CASCADE)
    tablet_issue= models.CharField(max_length=2000,blank=True)

class pc_issuewithscannerTbl(timeStamp):
    pcreportTbl_foreignkey = models.ForeignKey(pcreportTbl, on_delete=models.CASCADE)
    issue_with_scanner= models.CharField(max_length=2000,blank=True)

class pc_hw_concernTbl(timeStamp):
    pcreportTbl_foreignkey = models.ForeignKey(pcreportTbl, on_delete=models.CASCADE)
    hw_concern = models.CharField(max_length=2000,blank=True)

class pc_hw_concern_biometricTbl(timeStamp):
    pcreportTbl_foreignkey = models.ForeignKey(pcreportTbl, on_delete=models.CASCADE)
    hw_concern_biometric = models.CharField(max_length=2000,blank=True)


class pc_client_issueTbl(timeStamp):
    pcreportTbl_foreignkey = models.ForeignKey(pcreportTbl, on_delete=models.CASCADE)
    client_issue = models.CharField(max_length=2000,blank=True)
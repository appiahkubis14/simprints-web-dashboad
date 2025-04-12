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
    uid= models.CharField(max_length=2500,blank=True, null=True)
    district = models.CharField(max_length=250, blank=True, null=True)
    staffid = models.CharField(max_length=250, blank=True, null=True)
    mpassword = models.CharField(max_length=250,default="P@ssw0rd24")

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
    ]


    ownership_CHOICES = [

        ('government', 'Government'),
        ('private_facility', 'Private Facility'),
        ('chag', 'CHAG'),
    ]

    district = models.ForeignKey(Districts,on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=24, default="na")
    facility_type = models.CharField(max_length=24,  default="na" , choices=FACILITY_CHOICES)
    ownership = models.CharField(max_length=24,choices=ownership_CHOICES)
    no_of_commuities = models.IntegerField()
    name_of_incharge = models.CharField()
    contact_of_incharge = models.CharField()
    longitude = models.FloatField(max_length=10,)
    latitude = models.FloatField(max_length=10,)
    geom = models.PointField(blank=True,null=True)  # For point geometry
    def save(self, *args, **kwargs):
        # Create a Point using longitude and latitude
        self.point = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.facility_name


class healthWorkersTbl(timeStamp):
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    hw_name = models.CharField(max_length=240,)
    designation = models.CharField(max_length=54,)
    hw_contact = models.CharField(max_length=10,)
   

class cwcScheduleTbl(timeStamp):
    CATEGORY_CHOICES = [
        ('Static', 'Static'),
        ('Outright', 'Outright'),
    ]

    CHOICES = [
        ('Heavy', 'Heavy'),
        ('Normal', 'Normal'),
    ]
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    cwc_type = models.CharField(max_length=24,choices=CATEGORY_CHOICES)
    cwc_category = models.CharField(max_length=24,choices=CHOICES,default="Normal")
    date = models.DateField(max_length=24,)

class communityTbl(timeStamp):
    healthFacilitiesTbl_foreignkey = models.ForeignKey(healthFacilitiesTbl,on_delete=models.CASCADE)
    community = models.CharField(max_length=24,)
    community_leader_name= models.CharField(max_length=24,blank=True)
    community_leader_contact= models.CharField(max_length=24,blank=True,default="Not available")
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
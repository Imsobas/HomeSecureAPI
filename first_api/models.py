from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from first_api.user_role import user_role_list
from datetime import timedelta

## User model

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username, user_role, password=None): ## overide old method 
        """Create a new user profile"""
        if not username:
            raise ValueError('Users must have an email address')

        ## should add some username normalized
        user = self.model(username=username,user_role=user_role)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password): ## overide old method 
        """Create and save a new superuser with given details"""
        user = self.create_user(username, 'Admin' ,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""


    USER_ROLE_CHOICE = (
        ('Admin','Admin'),
        ('Manager','Manager'),
        ('SecureBoss','SecureBoss'),
        ('SecureGuard','SecureGuard'),
        ('GeneralUser','GeneralUser')
    )


    username = models.CharField(max_length=20,unique=True)
    user_role = models.CharField(max_length=20,choices=USER_ROLE_CHOICE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.username

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.username

    def __str__(self):
        """Return string representation of user"""
        return self.username

# Home Secure main models 

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    company_phone = models.CharField(max_length=100, null=True, blank=True)
    ## to delete with out remove data
    is_active = models.BooleanField(default=True)

    def __str__(self):
         """Return the model as a string"""
         return self.company_name

class Village(models.Model):
    village_name = models.CharField(max_length=100)
    village_address = models.CharField(max_length=200, null=True, blank=True)
    ## fk company
    village_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING) 
    ##old lat lon is 11,7
    village_lat = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    village_lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return self.village_name

class Zone(models.Model):
    zone_name = models.CharField(max_length=100)
    zone_number = models.IntegerField(default=0)
    ## fk village
    zone_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING) 
    zone_village = models.ForeignKey(Village,null=True, blank=True, on_delete=models.DO_NOTHING) 
    zone_lat = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    zone_lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    zone_last_update = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    ## not have is_active due to you need to delete every home incase want to delete zone

    def __str__(self):
        """Return the model as a string"""
        return self.zone_name

class Home(models.Model):
    
    
    home_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    home_address = models.CharField(max_length=200, null=True, blank=True)
    home_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING) 
    home_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    ## fk zone
    home_zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.DO_NOTHING) 
    home_lat = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    home_lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return str(self.home_number)

class GeneralUser(models.Model):
    ## keep firs, last name in this cause 1.easier when list all user 
    ## 2. one user can be both general and secure

    GENERAL_USER_ROLE_CHOICE = (
        ('Villager','Villager'),
        ('Manager','Manager'),
        ('Caretaker','Caretaker')
    )

    gen_user_firstname = models.CharField(max_length=100)
    gen_user_lastname = models.CharField(max_length=100)
    gen_user_username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING) 
    gen_user_type = models.CharField(max_length=100,choices=GENERAL_USER_ROLE_CHOICE)
    gen_user_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING) 
    gen_user_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    gen_user_zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.DO_NOTHING)
    gen_user_home  = models.ForeignKey(Home, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        """Return the model as a string"""
        # return str(self.gen_user_firstname)+" "+str(self.gen_user_lastname)
        if self.gen_user_firstname==None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return str(self.gen_user_firstname)+" "+str(self.gen_user_lastname)
        


class Work(models.Model):
    work_name = models.CharField(max_length=100, unique=True)
    work_start_time = models.TimeField(null=True, blank=True)
    work_end_time = models.TimeField(null=True, blank=True)
    work_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return self.work_name

class SecureGuard(models.Model):

    SECURITY_POSITION_CHOICE = (
        ('SecureBoss','SecureBoss'),
        ('Enter','Enter'),
        ('Exit','Exit'),
        ('Inside','Inside')
    )

    secure_firstname = models.CharField(max_length=100)
    secure_lastname = models.CharField(max_length=100)
    secure_username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    secure_type = models.CharField(max_length=100,choices=SECURITY_POSITION_CHOICE)
    secure_zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.DO_NOTHING)
    secure_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    secure_company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    secure_join_date = models.DateTimeField(null=True, blank=True)
    secure_left_date = models.DateTimeField(null=True, blank=True)
    secure_work_start_time = models.DateTimeField(null=True, blank=True)
    secure_work_end_time = models.DateTimeField(null=True, blank=True)
    secure_work_shift = models.ForeignKey(Work, null=True, blank=True,on_delete=models.DO_NOTHING)
    secure_current_location = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    secure_current_location_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        """Return the model as a string"""
        return str(self.secure_firstname)+" "+str(self.secure_lastname)




class Qrcode(models.Model):
    qr_content = models.CharField(max_length=200)
    qr_type = models.CharField(max_length=20)
    # qr_format = models.CharField(max_length=20)
    # qr_format_detail = models.CharField(max_length=100)
    qr_car_number = models.CharField(max_length=10)
    qr_home_number = models.CharField(max_length=20)
    qr_car_color = models.CharField(max_length=20)
    qr_car_brand = models.CharField(max_length=20)
    qr_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING)
    qr_village = models.ForeignKey(Village,null=True, blank=True, on_delete=models.DO_NOTHING)
    qr_zone = models.ForeignKey(Zone,null=True, blank=True, on_delete=models.DO_NOTHING)
    qr_home = models.ForeignKey(Home,null=True, blank=True, on_delete=models.DO_NOTHING)
    qr_user = models.ForeignKey(GeneralUser,null=True, blank=True, on_delete=models.DO_NOTHING)
    ## security who check this in village
    qr_enter_secure = models.ForeignKey(SecureGuard,null=True, blank=True, on_delete=models.DO_NOTHING, related_name='qr_enter_secure') 
    qr_inside_secure = models.ForeignKey(SecureGuard,null=True, blank=True, on_delete=models.DO_NOTHING, related_name='qr_inside_secure') 
    qr_exit_secure = models.ForeignKey(SecureGuard,null=True, blank=True, on_delete=models.DO_NOTHING, related_name='qr_exit_secure') 
    qr_enter_time = models.DateTimeField(null=True, blank=True)
    qr_inside_time = models.DateTimeField(null=True, blank=True)
    qr_home_time = models.DateTimeField(null=True, blank=True) ## changed name
    qr_exit_time = models.DateTimeField(null=True, blank=True)
    qr_enter_status = models.BooleanField(default=False)
    qr_inside_status = models.BooleanField(default=False)
    qr_home_status = models.BooleanField(default=False) ## changed name
    qr_exit_status = models.BooleanField(default=False)
    qr_enter_lat = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_enter_lon = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_inside_lat = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_inside_lon = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_home_lat = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_home_lon = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_exit_lat = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_exit_lon = models.DecimalField(max_digits=11, decimal_places=8,  null=True, blank=True)
    qr_detail = models.CharField(null=True,blank=True,max_length=200,default=None)
    qr_livehome_status = models.BooleanField(null=True,blank=True,default=None)  
    qr_complete_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return str(self.qr_content)
        
    




    

class Checkpoint(models.Model):
    point_name = models.CharField(max_length=100)
    ## point_active is status to active point in app 
    point_active = models.BooleanField(default=True)
    point_zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.DO_NOTHING)
    point_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    point_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.DO_NOTHING) 
    point_lat = models.DecimalField(max_digits=11, decimal_places=8, default=0.000000)
    point_lon = models.DecimalField(max_digits=11, decimal_places=8, default=0.000000)
    is_active = models.BooleanField(default=True)


class Setting(models.Model):
    setting_village = models.ForeignKey(Village,null=True, blank=True, on_delete=models.DO_NOTHING)
    inside_scan_duration = models.DurationField(default=timedelta(minutes=6))

    def __str__(self):
        """Return the model as a string"""
        return str(self.pk)

class PointInspection(models.Model):
    inspect_checkin_time = models.DateTimeField(null=True, blank=True)
    inspect_checkout_time = models.DateTimeField(null=True, blank=True)
    inspect_checkpoint = models.ForeignKey(Checkpoint, null=True, blank=True, on_delete=models.DO_NOTHING)
    inspect_village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.DO_NOTHING)
    inspect_zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.DO_NOTHING)
    inspect_secure = models.ForeignKey(SecureGuard, null=True, blank=True, on_delete=models.DO_NOTHING)
    insepect_work = models.ForeignKey(Work, null=True, blank=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        """Return the model as a string"""
        return str(self.pk)







    


## Old model

# class Article(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self): ## to tell what we gonna do when convert model instance into a string. 
#         return self.title
 
# class ProfileFeedItem(models.Model):
#     """Profile Status Update"""
#     user_profile = models.ForeignKey(
#         settings.AUTH_USER_MODEL, ## associated with user which is user auth model.
#         on_delete=models.CASCADE
#     )
#     status_text = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         """Return the model as a string"""
#         return self.status_text




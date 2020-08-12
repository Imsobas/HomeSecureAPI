from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from first_api.user_role import user_role_list

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
    village_company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.SET_NULL) 
    village_lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    village_lon = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return self.village_name

class Zone(models.Model):
    zone_name = models.CharField(max_length=100)
    zone_number = models.IntegerField(default=0)
    ## fk village
    zone_village = models.ForeignKey(Village,null=True, blank=True, on_delete=models.SET_NULL) 
    zone_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    zone_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.00000)
    zone_last_update = models.DateTimeField(null=True, blank=True)
    ## not have is_active due to you need to delete every home incase want to delete zone

    def __str__(self):
        """Return the model as a string"""
        return self.zone_name

class QRcode(models.Model):
    qr_content = 
    qr_type = 
    qr_format = 

    qr_car = 
    qr_car_color =
    qr_car_digit = 

    qr_home = models.
    ## can add multiple user
    qr_user = models.ManyToManyField(null=True, blank=True)

    ## security who check this in village

    # qr_enter_check_guard = models.ForeignKey(Village,null=True, blank=True, on_delete=models.SET_NULL) 
    # qr_inside_check_guard = models.ForeignKey(Village,null=True, blank=True, on_delete=models.SET_NULL) 
    # qr_exit_check_guard = models.ForeignKey(Village,null=True, blank=True, on_delete=models.SET_NULL) 

    qr_enter_check_time = models.DateTimeField(null=True, blank=True)
    qr_inside_check_time = models.DateTimeField(null=True, blank=True)
    qr_user_check_time = models.DateTimeField(null=True, blank=True)
    qr_exit_check_time = models.DateTimeField(null=True, blank=True)

    qr_enter_check_status = models.BooleanField(default=False)
    qr_inside_check_status = models.BooleanField(default=False)
    qr_user_check_status = models.BooleanField(default=False)
    qr_exit_check_status = models.BooleanField(default=False)

    qr_enter_check_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    qr_enter_check_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    
    qr_inside_check_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    qr_inside_check_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)

    qr_user_check_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    qr_user_check_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)

    qr_exit_check_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    qr_exit_check_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)

    qr_complete_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)




class Home(models.Model):
    home_number = models.CharField(max_length=100)
    home_address = models.CharField(max_length=200, null=True, blank=True)
    ## fk zone
    home_zone = models.ForeignKey(Zone, null=True, blank=True) 
    home_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
    home_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.00000)
    ## 
    # user_model = 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the model as a string"""
        return self.home_number

# class Checkpoint(models.Model):
#     point_name = models.CharField(max_length=100)
#     ## point_active is status to active point in app 
#     point_active = BooleanField(default=True)
#     ## fk zone
#     point_zone = models.ForeignKey(Zone, null=True, blank=True) 
#     point_lat = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
#     point_lon = models.DecimalField(max_digits=11, decimal_places=7, default=0.000000)
#     is_active = models.BooleanField(default=True)

# class GeneralUser(models.Model):
#     general_first_name = models.CharField(max_length=100)
#     general_last_name = models.CharField(max_length=100)
#     general_username = models.ForeignKey(settings.AUTH_USER_MODEL) 


# class SecureGuard(models.Model):

    
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
        user = self.create_user(username, password)

        user.is_superuser = True
        user.is_staff = True
        user.user_role = user_role_list[0] ## Admin 
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    username = models.CharField(max_length=20,unique=True)
    user_role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.username

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.username

    def __str__(self):
        """Return string representation of user"""
        return self.username

## Old model

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): ## to tell what we gonna do when convert model instance into a string. 
        return self.title
 
class ProfileFeedItem(models.Model):
    """Profile Status Update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, ## associated with user which is user auth model.
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text




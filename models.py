from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import generate_id, get_current_epoch
from .managers import UserLoginManager
import re

primary_key_length = 255

SALUTATIONS = [
    ("MR", "Mr"),
    ("MRS", "Mrs"),
]

GENDERS = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHERS", "Others"),
]

MARITAL_STATUSES = [
    ("SINGLE", "Single"),
    ("MARRIED", "Married"),
    ("DIVORCED", "Divorced"),
]

BLOOD_GROUPS = (
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)


class CountryMaster(models.Model):
    country_id = models.CharField(primary_key=True, max_length=primary_key_length, default=generate_id,editable=False )
    country_name = models.CharField( max_length=200, null=False, blank=False, unique=True )
    country_shortcode = models.CharField(max_length=200, null=True, blank=False)
    country_numeric_code = models.CharField(max_length=200, null=True, blank=False)
    country_phonecode = models.CharField(max_length=200, null=True, blank=False)
    country_currency = models.CharField(max_length=200, null=True, blank=False)
    country_currencyname = models.CharField(max_length=200, null=True, blank=False)
    country_latitude = models.CharField(max_length=200, null=True, blank=False)
    country_longitude = models.CharField(max_length=200, null=True, blank=False)
    last_updated_at = models.FloatField(default=get_current_epoch, editable=False )
    created_at = models.FloatField(default=get_current_epoch, editable=False )

    def __str__(self):
        return self.country_name

    class Meta:
        managed = True
        db_table = "country_master"
        ordering = ["country_name"]
        verbose_name_plural = "CountryMaster"


class StateMaster(models.Model):
    state_id = models.CharField( primary_key=True, max_length=primary_key_length,default=generate_id,editable=False)
    state_name = models.CharField(max_length=200, null=False, blank=False)
    state_shortcode = models.CharField(max_length=200, null=True, blank=False)
    state_latitude = models.CharField(max_length=200, null=True, blank=False)
    state_longitude = models.CharField(max_length=200, null=True, blank=False)
    country = models.ForeignKey( CountryMaster, on_delete=models.CASCADE, related_name="country")
    last_updated_at = models.FloatField(default=get_current_epoch, editable=False )
    created_at = models.FloatField(default=get_current_epoch, editable=False )

    def __str__(self):
        return f"{self.state_name}"

    class Meta:
        managed = True
        db_table = "state_master"
        ordering = ["state_name"]
        verbose_name_plural = "StateMaster"


class CityMaster(models.Model):
    city_id = models.CharField( primary_key=True, max_length=primary_key_length, default=generate_id, editable=False, )
    city_name = models.CharField(max_length=200, null=False, blank=False)
    city_latitude = models.CharField(max_length=200, null=True, blank=False)
    city_longitude = models.CharField(max_length=200, null=True, blank=False)
    state = models.ForeignKey( StateMaster, on_delete=models.CASCADE, related_name="state")
    last_updated_at = models.FloatField(default=get_current_epoch, editable=False )
    created_at = models.FloatField(default=get_current_epoch, editable=False )


    def __str__(self):
        return f"{self.city_name}"

    class Meta:
        managed = True
        db_table = "city_master"
        ordering = ["city_name"]
        verbose_name_plural = "CityMaster"




class UserMaster(models.Model):
    user_id = models.CharField( primary_key=True, max_length=primary_key_length, default=generate_id ,editable=False )
    initials = models.CharField(null=True, blank=True, max_length=10)
    salutation = models.CharField(max_length=10, null=True, blank=True, choices=SALUTATIONS)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=True )
    user_bio = models.TextField(null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDERS)
    marital_status = models.CharField(max_length=20,null=True,blank=True,choices=MARITAL_STATUSES)
    marrige_date = models.DateField(null=True, blank=True,)
    user_profile_pic = models.CharField(null=True, max_length=255, blank=True,)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_no = models.CharField(max_length=12, null=True, blank=True)
    blood_group = models.CharField(choices=BLOOD_GROUPS, null=True, blank=True)
    nationality = models.CharField(null=True, blank=True)
    last_updated_at = models.FloatField(default=get_current_epoch, editable=False )
    created_at      = models.FloatField(default=get_current_epoch, editable=False )

    
    def __str__(self):
        return self.getFullName()
    

    def getFullName(self):
        name_parts = []
        if self.first_name != None:
            name_parts.append(self.first_name)

        if self.last_name != None:
            name_parts.append(self.last_name)

        return re.sub(r"\s+", " ", str(" ".join(name_parts)))
    

    def getEmail(self):
        return self.cm_user.first().email


    def getPhoneNumber(self):
        return self.cm_user.first().phone_no


    class Meta:
        managed = True
        db_table = "user_master"
        ordering = ["-last_updated_at"]
        verbose_name_plural = "UserMaster"



class UserLogin(AbstractUser):
    user_login_id       = models.CharField( primary_key=True, max_length=primary_key_length, default=generate_id ,editable=False)
    ul_user             = models.ForeignKey( UserMaster, on_delete=models.CASCADE, related_name="ul_user",null=True )
    password            = models.CharField(max_length=255, null=False, blank=False)
    first_name          = None
    last_name           = None
    username            = None
    email               = None
    last_updated_at     = models.FloatField( default=get_current_epoch, editable=False )
    created_at          = models.FloatField( default=get_current_epoch, editable=False )

    
    USERNAME_FIELD      = "user_login_id"
    REQUIRED_FIELDS     = ["password"]
    objects             = UserLoginManager()


    def __str__(self):
        return f"{self.user_login_id} ({self.ul_user})"


    def create_user_master(self):
        user_id = generate_id()
        UserMaster( user_id=user_id, first_name=self.user_login_id).save()
        return user_id


    class Meta:
        managed = True
        db_table = "user_login"
        ordering = ["-last_updated_at"]
        verbose_name_plural = "UserLogin"



class BankDetails(models.Model):
    bank_id         = models.CharField( primary_key=True, max_length=primary_key_length, default=generate_id ,editable=False)
    bd_bank_user    = models.ForeignKey( UserMaster, on_delete=models.CASCADE, related_name="bd_bank_user" )
    bank_name       = models.CharField( max_length=50,  null=True, blank=True )
    bank_account_no = models.CharField( max_length=20,  null=True, blank=True )
    bank_ifsc_code  = models.CharField( max_length=20,  null=True, blank=True )
    bank_passbook   = models.CharField( max_length=255, null=True, blank=True )
    bank_statement  = models.CharField( max_length=255, null=True, blank=True )
    last_updated_at = models.FloatField( default=get_current_epoch, editable=False )
    created_at      = models.FloatField( default=get_current_epoch, editable=False )

    def __str__(self):
        return f"{self.bank_id} ({self.bd_bank_user})"

    class Meta:
        managed = True
        db_table = "bank_details"
        ordering = ["-last_updated_at"]
        verbose_name_plural = "BankDetails"


class ContactMaster(models.Model):
    contact_master_id   = models.CharField( primary_key=True, max_length=primary_key_length, default=generate_id ,editable=False)
    cm_user             = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="cm_user")

    # Phone Number
    phone_no    = models.CharField(max_length=15, null=True, blank=True, db_index=True, unique=True)
    whatsapp_no = models.CharField(max_length=15, null=True, blank=True, db_index=True, unique=True)
    
    # Email
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True, unique=True)

    # Address
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    cm_country = models.ForeignKey( CountryMaster, on_delete=models.CASCADE, related_name="cm_country", null=True,blank=True)
    cm_state = models.ForeignKey( StateMaster, on_delete=models.CASCADE, related_name="cm_state", null=True, blank=True)
    cm_city = models.ForeignKey( CityMaster, on_delete=models.CASCADE, related_name="cm_city", null=True, blank=True )
    pincode = models.CharField(max_length=20, null=True, blank=True)

    last_updated_at = models.FloatField(default=get_current_epoch, editable=False )
    created_at = models.FloatField( default=get_current_epoch, editable=False )

    def __str__(self):
        return f"{self.contact_master_id} | {self.cm_user.getFullName()}"

    def getFormattedAddress(self):
        address = " ,".join(
            [
                self.address_line1,
                self.address_line2,
                self.getCityName(),
                self.getStateName(),
                self.getCountryName(),
            ]
        )

        address = f"{address} - {self.pincode}" if self.pincode else address
        return address

    def getCityName(self):
        return self.cm_city.city_name

    def getStateName(self):
        return self.cm_state.state_name

    def getCountryName(self):
        return self.cm_country.country_name


    class Meta:
        managed = True
        db_table = "contact_master"
        ordering = ["-last_updated_at"]
        verbose_name_plural = "ContactMaster"





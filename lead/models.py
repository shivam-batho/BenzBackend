from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    employee = models.CharField(max_length=255,unique=True,default='EMP-001',db_column='employee_id',null=True)
    name=models.CharField(max_length=255,db_column='employee_name')
    email =models.CharField(max_length=255,db_column='employee_email',unique=True)
    password=models.CharField(max_length=255)
    country_code = models.CharField(max_length=3,blank=True,null=True)
    mobile_no = models.CharField(max_length=13, blank=True,null=True)
    deleted = models.BooleanField(default=False,db_column='is_deleted')
    profile_pic = models.CharField(max_length=255 , blank=True , null =True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        managed = True
        db_table='tbl_users'

    def __str__(self):
        return self.name


class UserInfoDetails(models.Model):
    employee_type = (
        (1,'super_admin'),
        (2 , 'admin'),
        (3, 'manager'),
        (4 , 'report_handler'),
        (5 , 'sales_manager'),
        (6, 'user'),
    )
    user = models.OneToOneField(User , related_name='userInfo',on_delete=models.DO_NOTHING)
    designation = models.CharField(max_length=255,blank=True,null=True)
    address = models.TextField(blank=True , null=True)
    user_role=models.IntegerField(choices = employee_type , default=6)
    gender = models.CharField(max_length = 10 , null=True)
    dob = models.DateField()
    doj = models.DateField()
    experience = models.FloatField(db_column='yers_exper' , default='Fresher')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        managed = True
        db_table = 'tbl_user_details'


    def __str__(self):        
        return self.address
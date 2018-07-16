from django.db import models

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel
from django.urls import reverse

#####################
### 사용자 정보 관리

class LightSaltUserManager(BaseUserManager):
    def create_user(self, member_id, name, email, password=None):
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)

        user = self.model(
            member_id = member_id,
            name = name,
            email = LightSaltUserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, member_id, name, email, password):
        user = self.create_user(member_id, name, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class LightSaltUser(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    member_id = models.CharField(max_length=30, 
        blank=False,
        null=False,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(max_length=255, unique=True)
    member_type_code = models.CharField(max_length=2, blank=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'member_id'
    REQUIRED_FIELDS = ['email', 'name']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = LightSaltUserManager()

    class Meta:
        db_table="LSMB001M"

    def get_absolute_url(self): 
        return reverse('main') 

#####################
### 목사 정보 관리

class LightSaltPastorManager(models.Manager):
    use_in_migrations = True

# 목사 테이블
class LightSaltPastor(TimeStampedModel):
    church_no = models.AutoField(primary_key=True)
    pastor_id = models.CharField(max_length=30, 
        blank=False,
        null=False,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    church_name = models.CharField(max_length=100)

    graduation_proof = models.ImageField(null=True)     #대학원 졸업증(이미지)   
    church_satification = models.ImageField(null=True)  #안수증(이미지)  

    church_type_code = models.CharField(max_length=10)
    church_post = models.CharField(max_length=10)
    church_address = models.CharField(max_length=300)
    authentication_yn = models.BooleanField(default=False)

    objects = LightSaltPastorManager()

    class Meta:
        db_table="LSMB002M"

    def get_absolute_url(self): 
        return reverse('pastor_detail', kwargs={"church": self.church_no}) 
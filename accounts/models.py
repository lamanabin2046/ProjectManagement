from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile number must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(mobile, password, **extra_fields)
class CustomUser(AbstractUser):
    USER_CHOICES = (
        (1, 'ADMIN'),
        (2, 'CAO'),
        (3, 'PLANNING OFFICER'),
        (4, 'ENGINEER'),
        (5, 'WARD STAFF'),
        (6, 'WARD SACHIB'),
        (7, 'WARD ENGINEER'),
        (8, 'PALIKA ENGINEER'),
        (9, 'WARD CHAIRPERSON'),

    )
    username = None
    mobile = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(choices=USER_CHOICES, max_length=50, default=1)

    USERNAME_FIELD = 'mobile'  
    REQUIRED_FIELDS = []      
    objects = CustomUserManager() 
    def __str__(self):
        return self.mobile
  
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Cao(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)
    
    def __str__(self):
        return self.name
    
 
class PlanningOfficer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)
    def __str__(self):
        return self.name
       
class Engineer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)
    def __str__(self):
        return self.name
    
class Ward(models.Model):
    name = models.CharField(max_length=250)
    chairperson = models.CharField(max_length=250, null = True)
    def __str__(self):
        return self.name
    



    
class WadaStaff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    wards = models.ManyToManyField(Ward)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)
    def __str__(self):
        return self.name


class WardSachib(models.Model):
    """वडा सचिव — secretary of a single ward. Logs in to issue the
    सिफारिस (recommendation) letter required before a उपभोक्ता समिति
    project agreement (सम्झौता) can be printed for that ward."""
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="ward_sachibs")
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)

    def __str__(self):
        return f"{self.name} – {self.ward.name}"


class WardEngineer(models.Model):
    """वडा इन्जिनियर — engineer assigned to a single ward. Logs in to see
    that ward's योजनाहरू only, and enters लागत अनुमान (cost estimate)
    details for those projects."""
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="ward_engineers")
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)

    def __str__(self):
        return f"{self.name} – {self.ward.name}"


class PalikaEngineer(models.Model):
    """पालिका इन्जिनियर — municipality-wide engineer, not tied to any one
    वडा. Unlike WardEngineer (scoped to a single ward), a Palika Engineer
    sees every project across all wards and can add or edit the लागत
    अनुमान (cost estimate) for any of them."""
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)

    def __str__(self):
        return self.name


class WardChairperson(models.Model):
    """वडा अध्यक्ष — approves (स्वीकृत) उपभोक्ता समिति agreements for their own ward when the
    palika has delegated the process to the ward (वडा प्रत्यायोजित)."""
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="ward_chairpersons")
    name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)
    status = models.CharField(default="Active", null=True, max_length=200)

    def __str__(self):
        return f"{self.name} – {self.ward.name}"


# ================= भूमिका र अनुमति (accounts/permissions.py हेर्नुहोस्) =================
class RolePermission(models.Model):
    """Admin ले "भूमिका र अनुमति" पेजबाट बदलेको अनुमति (नभए default लागू)।"""
    role = models.CharField(max_length=5)
    perm = models.CharField(max_length=50)
    allowed = models.BooleanField(default=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("role", "perm")

    def __str__(self):
        return f"{self.role}:{self.perm}={'✓' if self.allowed else '✗'}"


class UserPermission(models.Model):
    """कुनै व्यक्तिलाई दिइएको थप अनुमति (जस्तै CAO ले स्वीकृत अधिकार प्रत्यायोजन)।"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="extra_perms")
    perm = models.CharField(max_length=50)
    granted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "perm")

    def __str__(self):
        return f"{self.user_id}:{self.perm}"

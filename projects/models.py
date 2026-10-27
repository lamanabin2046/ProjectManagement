from django.db import models

from accounts.models import Ward


class FiscalYear(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


 
class Project_Type(models.Model):
    type = models.CharField(max_length=100)
    def __str__(self):
        return self.type

class Budget_Type(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name     
    
    
class Procurement_Type(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    
    

    
class Project(models.Model):
    STATUS_CHOICES = [
        (0, 'Open for Bids'),
        (1, 'In Progress'),
        (2, 'Completed'),
    ]
    fiscalyear = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True)
    procurement_type = models.ForeignKey(Procurement_Type, on_delete=models.CASCADE, null=True)
    budget_type = models.ForeignKey(Budget_Type, on_delete=models.CASCADE, null=True)
    project_type = models.ForeignKey(Project_Type,on_delete=models.CASCADE,null=True)
    address = models.TextField()
    budget = models.FloatField()
    # '' = use the palika's default (Palika.uc_mode)
    EXECUTION_MODES = (
        ("", "पालिकाको नियम अनुसार"),
        ("municipal", "पालिका केन्द्रित"),
        ("ward", "वडा प्रत्यायोजित"),
    )
    execution_mode = models.CharField("कार्यान्वयन तह", max_length=20, choices=EXECUTION_MODES, blank=True, default="")
    status = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.name} ({self.fiscalyear.name})"
    
    
    


from django.db import models
from django.conf import settings
from .models import Project

class ProjectTimeline(models.Model):
    # काम सुरु हुनु अघि / भइरहेको बेला / सम्पन्न भएपछि — the three checkpoints
    # a Ward Engineer must photograph for every project. Left nullable so
    # older, free-form timeline entries (uploaded before this field existed)
    # keep working unchanged.
    STAGE_BEFORE = 1
    STAGE_DURING = 2
    STAGE_AFTER = 3
    STAGE_CHOICES = (
        (STAGE_BEFORE, "काम सुरु हुनु अघि"),
        (STAGE_DURING, "काम भइरहेको बेला"),
        (STAGE_AFTER, "काम सम्पन्न भएपछि"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="timelines"
    )

    stage = models.IntegerField(choices=STAGE_CHOICES, null=True, blank=True)

    image = models.ImageField(
        upload_to="project_timelines/"
    )

    description = models.TextField()

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]   # 🔥 auto timeline

    def __str__(self):
        return f"{self.project.name} - {self.created_at}"


def project_uc_mode(project):
    """'municipal' or 'ward' for a उपभोक्ता समिति project (project override, else the palika default)."""
    if getattr(project, "execution_mode", ""):
        return project.execution_mode
    from django.db import connection

    return getattr(getattr(connection, "tenant", None), "uc_mode", None) or "municipal"

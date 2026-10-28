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
    # कामको प्रकार (सडक, भवन …) — भौतिक उपलब्धि (ProjectOutput) भर्दा छानिन्छ
    work_category = models.ForeignKey("WorkCategory", on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="projects", verbose_name="कामको प्रकार")


    def __str__(self):
        return f"{self.name} ({self.fiscalyear.name})"
    
    
    


from django.db import models
from django.conf import settings
from .models import Project

# ================= भौतिक उपलब्धि (कति कि.मि. बाटो, कति भवन …) =================
class WorkCategory(models.Model):
    """कामको प्रकार: सडक/बाटो, भवन, खानेपानी … (पालिकाले थप्न/बदल्न मिल्ने)."""
    name = models.CharField("कामको प्रकार", max_length=150)
    sort = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("सक्रिय", default=True)

    class Meta:
        ordering = ["sort", "id"]

    def __str__(self):
        return self.name


class OutputIndicator(models.Model):
    """उपलब्धि सूचक: जस्तै "नयाँ ट्रयाक (कच्ची बाटो)" — कि.मि.; "नयाँ भवन" — वटा."""
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name="indicators")
    name = models.CharField("उपलब्धि", max_length=200)
    unit = models.CharField("एकाइ", max_length=40)
    sort = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("सक्रिय", default=True)

    class Meta:
        ordering = ["category__sort", "category_id", "sort", "id"]

    def __str__(self):
        return f"{self.name} ({self.unit})"


class ProjectOutput(models.Model):
    """एउटा योजनाको एउटा सूचकको परिमाण — प्रतिवेदनमा जोडिन्छ।"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="outputs")
    indicator = models.ForeignKey(OutputIndicator, on_delete=models.PROTECT, related_name="values")
    quantity = models.DecimalField("परिमाण", max_digits=14, decimal_places=3)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "indicator")
        ordering = ["indicator__category__sort", "indicator__sort", "indicator_id"]

    def __str__(self):
        return f"{self.project_id}: {self.indicator} = {self.quantity}"


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

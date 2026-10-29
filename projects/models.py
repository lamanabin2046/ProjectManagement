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
    # क्षेत्र / उपक्षेत्र (स्थानीय तहको बजेट वर्गीकरण — पालिकाले सेटिङबाट मिलाउन मिल्ने)
    sector = models.ForeignKey("Sector", on_delete=models.SET_NULL, null=True, blank=True, related_name="projects",
                               verbose_name="क्षेत्र")
    subsector = models.ForeignKey("SubSector", on_delete=models.SET_NULL, null=True, blank=True, related_name="projects",
                                  verbose_name="उपक्षेत्र")
    # बजेट उपशीर्षक / कार्यक्रम (बजेट नियन्त्रण) — विनियोजित रकम यही शीर्षकको सीमाभित्र
    budget_head = models.ForeignKey("BudgetHead", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="projects", verbose_name="बजेट शीर्षक")


    def __str__(self):
        return f"{self.name} ({self.fiscalyear.name})"
    
    
    


from django.db import models
from django.conf import settings
from .models import Project

# ================= क्षेत्र / उपक्षेत्र =================
class Sector(models.Model):
    """क्षेत्र: आर्थिक विकास, सामाजिक विकास, पूर्वाधार विकास …"""
    name = models.CharField("क्षेत्र", max_length=150)
    sort = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("सक्रिय", default=True)

    class Meta:
        ordering = ["sort", "id"]

    def __str__(self):
        return self.name


class SubSector(models.Model):
    """उपक्षेत्र: शिक्षा, स्वास्थ्य, सडक तथा पुल … (एउटा क्षेत्रभित्र)."""
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="subsectors")
    name = models.CharField("उपक्षेत्र", max_length=150)
    sort = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("सक्रिय", default=True)

    class Meta:
        ordering = ["sector__sort", "sector_id", "sort", "id"]

    def __str__(self):
        return self.name


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



# ================= धरौटी फिर्ता (उपभोक्ता समिति / बोलपत्र / दरभाउपत्र) =================
class RetentionRelease(models.Model):
    """एउटा योजनाको धरौटी फिर्ता: इन्जिनियर/वडाको सिफारिस (अपलोड) → टिप्पणी → फिर्ता दर्ता."""
    REC_BY = (("engineer", "इन्जिनियर (प्राविधिक)"), ("ward", "वडा कार्यालय"))
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="retention_release")
    held_amount = models.DecimalField("रोक्का धरौटी", max_digits=14, decimal_places=2, default=0)
    # सिफारिस
    rec_by = models.CharField("सिफारिस गर्ने", max_length=20, choices=REC_BY, default="engineer")
    rec_number = models.CharField("पत्र संख्या / च.नं.", max_length=100, blank=True)
    rec_date = models.DateField("सिफारिस मिति")
    rec_document = models.FileField("सिफारिस पत्र", upload_to="retention/")
    rec_remarks = models.TextField("कैफियत", blank=True)
    rec_uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="+")
    rec_uploaded_at = models.DateTimeField(auto_now_add=True)
    # टिप्पणी
    tippani_printed_at = models.DateTimeField(null=True, blank=True)
    # फिर्ता
    released_on = models.DateField("फिर्ता मिति", null=True, blank=True)
    released_amount = models.DecimalField("फिर्ता रकम", max_digits=14, decimal_places=2, null=True, blank=True)
    voucher_number = models.CharField("भौचर / चेक नं.", max_length=100, blank=True)
    approved_document = models.FileField("सदर भएको टिप्पणी (स्क्यान)", upload_to="retention/", null=True, blank=True)
    early_reason = models.TextField("म्यादअघि फिर्ताको कारण", blank=True)
    released_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="+")

    def __str__(self):
        return f"धरौटी फिर्ता – {self.project.name}"



# ================= बजेट नियन्त्रण =================
class BudgetHead(models.Model):
    """बजेट उपशीर्षक / कार्यक्रम — आ.व.अनुसार स्वीकृत (विनियोजित) रकम.
    यस शीर्षकमा राखिएका योजनाको विनियोजित रकमको जोड यो रकमभन्दा बढी हुन पाउँदैन।"""
    fiscalyear = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, related_name="budget_heads",
                                   verbose_name="आर्थिक वर्ष")
    code = models.CharField("बजेट उपशीर्षक नं.", max_length=50, blank=True)
    name = models.CharField("शीर्षक / कार्यक्रम", max_length=250)
    budget_type = models.ForeignKey(Budget_Type, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="स्रोत / बजेट प्रकार")
    allocated = models.DecimalField("स्वीकृत रकम", max_digits=16, decimal_places=2, default=0)
    is_active = models.BooleanField("सक्रिय", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fiscalyear_id", "code", "id"]

    def __str__(self):
        return f"{self.code} {self.name}".strip()


class BudgetAmendment(models.Model):
    """विनियोजित रकमको संशोधन: थप (थप बजेट), कटौती / समर्पण, वा योजनाबीच रकमान्तर.
    दर्ता हुनेबित्तिकै योजनाको विनियोजित रकम (Project.budget) बदलिन्छ; पहिले/पछिको रकम यहीँ रहन्छ।"""
    KINDS = (("increase", "थप"), ("decrease", "कटौती / समर्पण"), ("transfer", "रकमान्तर"))
    kind = models.CharField("प्रकार", max_length=20, choices=KINDS)
    from_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="budget_out", verbose_name="घटाउने योजना")
    to_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="budget_in", verbose_name="थप्ने योजना")
    amount = models.DecimalField("रकम", max_digits=16, decimal_places=2)
    from_before = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    from_after = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    to_before = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    to_after = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    decision_by = models.CharField("निर्णय गर्ने", max_length=150, blank=True)
    decision_no = models.CharField("निर्णय नं.", max_length=100, blank=True)
    decision_date = models.DateField("निर्णय मिति")
    reason = models.TextField("कारण")
    document = models.FileField("निर्णयको प्रतिलिपि", upload_to="budget/", null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-decision_date", "-id"]

    def __str__(self):
        return f"{self.get_kind_display()} रु. {self.amount}"

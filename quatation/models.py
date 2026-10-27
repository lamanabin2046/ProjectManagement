from django.db import models
from projects.models import Project
from django.core.exceptions import ValidationError

# Create your models here.
class Suchikrit(models.Model):
    firm_name = models.CharField(max_length=250)
    firm_owner = models.CharField(max_length=250)
    firm_address = models.CharField(max_length=250)
    firm_pan = models.CharField(max_length=250)
    firm_contact = models.CharField(max_length=250)
    suchikrit_date =  models.DateField(null=True)
    
    
    def __str__(self):
        return self.firm_name 
    
    
class Quation(models.Model):
    suchikrit = models.ManyToManyField(Suchikrit, related_name='quations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cost_estimate = models.DecimalField(max_digits=12, decimal_places=2)
    contingency = models.FloatField(null=True)
    is_selected = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    bidded_prices = models.JSONField(null=True, blank=True)  # Field to store all bidded prices
    agreement_date = models.DateField(null=True)
    expire_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.project.name} - {', '.join([firm.firm_name for firm in self.suchikrit.all()])}"

    def clean(self):
        # Custom validation to enforce uniqueness between suchikrit and project
        if self.suchikrit.count() > 0:
            for firm in self.suchikrit.all():
                if Quation.objects.filter(suchikrit=firm, project=self.project).exists():
                    raise ValidationError(f"Firm {firm.firm_name} is already associated with this project.")
                
            
                
class QuationFinal(models.Model):
    quation = models.ForeignKey(Quation, on_delete=models.CASCADE)
    application_date =models.DateField(null=True)
    totalValuation = models.FloatField(null=True)
    retension = models.FloatField(null=True)
    taxdeduction = models.FloatField(null=True)
    finalpayment = models.FloatField(null=True)
    
    def __str__(self):
        return f"{self.quation.project.name} - {self.finalpayment}"


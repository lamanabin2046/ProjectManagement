"""पत्रको पाठ सम्पादन.

LetterTemplate — पालिकाको ढाँचा: एक प्रकारका सबै पत्रमा लागू, {{project.name}} जस्ता placeholder सहित।
LetterOverride — एउटा पत्र मात्र (एउटा योजना/कागजात) को सम्पादित अन्तिम पाठ।
key  = पत्रको प्रकार (जस्तै "uc.bank_letter"), ref = त्यो पत्रको पेज (URL path)।
"""
from django.conf import settings
from django.db import models


class LetterTemplate(models.Model):
    key = models.CharField(max_length=80, unique=True)
    title = models.CharField(max_length=200, blank=True)
    html = models.TextField()
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "key"]

    def __str__(self):
        return self.title or self.key


class LetterOverride(models.Model):
    key = models.CharField(max_length=80)
    ref = models.CharField(max_length=300)
    title = models.CharField(max_length=200, blank=True)
    html = models.TextField()
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("key", "ref")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.key} @ {self.ref}"

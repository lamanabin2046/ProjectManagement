from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.
class SealedBid(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="biddings")

    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    bidding_number = models.CharField(max_length=100)

    bid_published_date = models.DateField(null=True, blank=True)
    bid_opening_date = models.DateField(null=True, blank=True)
    bid_evaluation_date = models.DateField(null=True, blank=True)

    total_cost_estimate = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cost_estimate_vat = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    contingency_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    ps_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    bidder_name_nepali = models.CharField(max_length=250, null=True, blank=True)
    bidder_name_english = models.CharField(max_length=250, null=True, blank=True)
    bidder_address_nepali = models.CharField(max_length=250, null=True, blank=True)
    bidder_owner_nepali = models.CharField(max_length=250, null=True, blank=True)

    bidding_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    STATUS_CHOICES = (
        (0, "Published"),
        (1, "Evaluated"),
        (2, "Approved"),
        (3, "Contract Signed"),
        (4, "Completed"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} – {self.bidding_number}"

class Contract(models.Model):
    sealed_bid = models.OneToOneField(
        SealedBid,
        on_delete=models.CASCADE,
        related_name="contract"
    )

    contract_date = models.DateField(null=True, blank=True)

    # 🔹 ORIGINAL expiry (never overwrite)
    contract_expire_date = models.DateField(
        null=True,
        blank=True,
        help_text="Original contract expiry date"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract – {self.sealed_bid.project.name}"

    # ✅ Always get latest expiry
    @property
    def current_expiry_date(self):
        last_extension = self.extensions.order_by("-extended_expiry_date").first()
        return last_extension.extended_expiry_date if last_extension else self.contract_expire_date
    
    
    @property
    def total_running_paid(self):
        return self.running_evaluations.aggregate(
            total=models.Sum("net_payable")
        )["total"] or Decimal("0")

class ContractExtension(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="extensions"
    )

    previous_expiry_date = models.DateField()
    extended_expiry_date = models.DateField()

    remarks = models.TextField(blank=True, null=True)

    extended_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract Extended – {self.contract.sealed_bid.project.name}"

class PerformanceBondRequirement(models.Model):
    sealed_bid = models.OneToOneField(
        SealedBid,
        on_delete=models.CASCADE,
        related_name="bond_requirement",
        null=True,      # 👈 TEMPORARY
        blank=True      # 👈 TEMPORARY
    )

    bid_approved_date = models.DateField(null=True, blank=True)
    required_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    required_expiry_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"PG Required – {self.sealed_bid.project.name}"

    
    
from django.db import models
from datetime import date




class PerformanceBondIssued(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name="bond_issued"
    )

    bond_number = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250)

    issued_amount = models.DecimalField(max_digits=14, decimal_places=2)
    issue_date = models.DateField()

    # ✅ ORIGINAL EXPIRY DATE (same name as you want)
    expiry_date = models.DateField()

    document = models.FileField(
        upload_to="performance_bonds/",
        null=True,
        blank=True
    )

    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------
    # CURRENT EXPIRY (AUTO)
    # ----------------------------
    @property
    def current_expiry_date(self):
        last_extension = self.extensions.order_by("-extended_expiry_date").first()
        return last_extension.extended_expiry_date if last_extension else self.expiry_date

    @property
    def days_left(self):
        return (self.current_expiry_date - date.today()).days

    @property
    def days_left_abs(self):
        return abs(self.days_left)

    @property
    def is_expiring_soon(self):
        return 0 <= self.days_left <= 30

    def __str__(self):
        return f"PG – {self.contract.sealed_bid.project.name}"


class PerformanceBondExtension(models.Model):
    bond = models.ForeignKey(
        PerformanceBondIssued,
        on_delete=models.CASCADE,
        related_name="extensions"
    )

    previous_expiry_date = models.DateField()
    extended_expiry_date = models.DateField()

    extended_on = models.DateField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"PG Extension – {self.bond.bond_number}"





from django.db import models
from decimal import Decimal

class AdvancePayment(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="advance_payments"  # plural
    )

    approved_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    approval_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Advance Payment – {self.contract.sealed_bid.project.name} "
            f"({self.approved_amount})"
        )
        
        
        
        
        

from datetime import date
class AdvanceBankGuarantee(models.Model):
    advance_payment = models.OneToOneField(
        AdvancePayment,
        on_delete=models.CASCADE,
        related_name="bank_guarantee"
    )

    guarantee_number = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250)

    guaranteed_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Must be >= advance approved amount"
    )

    issue_date = models.DateField()
    expiry_date = models.DateField()

    document = models.FileField(
        upload_to="advance_guarantees/",
        null=True,
        blank=True
    )

    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days_left(self):
        return (self.expiry_date - date.today()).days

    @property
    def is_expired(self):
        return self.days_left <= 0

    def clean(self):
        if self.guaranteed_amount < self.advance_payment.approved_amount:
            raise ValueError(
                "Advance Bank Guarantee amount cannot be less than approved advance payment."
            )

    def __str__(self):
        return f"Advance BG – {self.advance_payment.contract.sealed_bid.project.name}"
    
    
    
    
    
    
    from django.db import models
from decimal import Decimal

class FinalPayment(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name="final_payment"
    )

    bidding_amount = models.DecimalField(max_digits=14, decimal_places=2)

    total_advance_payment = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    # 🔹 Basis used to compute final_amount:
    # if running bills were taken -> total_evaluation_amount - total_running_bill_amount
    # else                        -> total_evaluation_amount - total_advance_payment
    total_evaluation_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        help_text="कुल मूल्याङ्कन रकम used as the basis for this final payment"
    )
    total_running_bill_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        help_text="Total running bill (net_payable) already paid on this contract, if any"
    )

    agrim_tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    vat_deduction = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    dharauti_deduction = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bahal_tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    final_amount = models.DecimalField(max_digits=14, decimal_places=2)

    payment_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)





from django.db import models
from decimal import Decimal

from django.db import models
from decimal import Decimal

class RunningEvaluation(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="running_evaluations"
    )

    evaluation_date = models.DateField()

    # 🔹 Total evaluated work value up to this date (cumulative)
    total_evaluated_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Cumulative evaluated amount till this running bill"
    )

    # 🔹 Amount payable in THIS running (incremental)
    payable_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    # 🔹 Advance adjusted in this running
    advance_adjusted = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    # 🔹 Deductions
    agrim_tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    vat_deduction = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    dharauti_deduction = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bahal_tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    # 🔹 Net payable for this running
    net_payable = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["evaluation_date"]

    def save(self, *args, **kwargs):
        deductions = (
            self.advance_adjusted +
            self.agrim_tax +
            self.vat_deduction +
            self.dharauti_deduction +
            self.bahal_tax
        )
        self.net_payable = self.payable_amount - deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Running Evaluation – {self.contract.sealed_bid.project.name} "
            f"({self.evaluation_date})"
        )
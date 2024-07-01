from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.

PRECENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

YES = 'Y'
NO = 'N'
NULL = 'NA'
CHOICES_YN = (
    (NULL, 'NA'),
    (YES, 'Y'),
    (NO, 'N'),
)
# level
A = 'A'
B = 'B'
C = 'C'
CHOICES_LEVEL = (
    (NULL, 'NA'),
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
)

# scga class
INCOMPLETE_TESTS = "incomplete Tests"
REQUIREMENTS_CODE_MISMATCH = "requirements-code mismatch"
DEACTIVATED_CODE = "deactivated code"
DEFENSIVE_CODE = "defensive code"
TEST_ENVIRONMENT_LIMITATIONS = "test environment limitations"
PREVIOUSLY_ANALYZED_SOFTWARE = "previously analyzed software"
OTHER = "other"
CHOICES_CLASS = (
    (NULL, 'NA'),
    (INCOMPLETE_TESTS, "Incomplete Tests"),
    (REQUIREMENTS_CODE_MISMATCH, "Requirements-Code Mismatch"),
    (DEACTIVATED_CODE, "Deactivated Code"),
    (DEFENSIVE_CODE, "Defensive Code"),
    (TEST_ENVIRONMENT_LIMITATIONS, "Test Environment Limitations"),
    (PREVIOUSLY_ANALYZED_SOFTWARE, "Previously Analyzed Software"),
    (OTHER, "Other"),
)


class Scga(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    baseline = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name


class Level(models.Model):
    level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL)
    scga_file = models.ForeignKey(Scga, to_field="id", related_name="levels",
                                  null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.level


class TestPlan(models.Model):
    # main table scga file
    # related_name is the field name that should be defined in serializer
    # scga_file = models.ForeignKey(Scga, to_field="file_name", related_name="test_plans",
    #   null=True, blank=True, on_delete=models.CASCADE)
    sheet_name = models.CharField(max_length=255)
    level = models.OneToOneField(Level, to_field="id", related_name="test_plan",
                                 null=True, blank=True, on_delete=models.CASCADE)
    # level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL)

    def __str__(self):
        self.sheet_name


class TestException(models.Model):
    # main table scga file
    # related_name is the field name that should be defined in serializer
    # scga_file = models.ForeignKey(Scga, to_field="file_name", related_name="test_exceptions",
    #   null=True, blank=True, on_delete=models.CASCADE)
    sheet_name = models.CharField(max_length=255)
    level = models.OneToOneField(Level, to_field="id", related_name="test_exception",
                                 null=True, blank=True, on_delete=models.CASCADE)
    # level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL)

    def __str__(self):
        self.sheet_name


class LvTotalCoverage(models.Model):
    percent_coverage_MCDC = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    percent_coverage_Analysis = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    total_coverage = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    # main table function
    test_plan = models.OneToOneField(TestPlan, to_field="id", related_name="lv_total_coverage",
                                     null=True, blank=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # 将值四舍五入到两位小数
        self.percent_coverage_MCDC = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.percent_coverage_Analysis = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.total_coverage = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)


class SCGAModule(models.Model):
    module_name = models.CharField(max_length=255)
    process = models.CharField(max_length=255)
    # main table test plan
    test_plan = models.ForeignKey(TestPlan, to_field="id", related_name="modules",
                                  null=True, blank=True, on_delete=models.CASCADE)
    # main table test exception
    test_exception = models.ForeignKey(TestException, to_field="id", related_name="modules",
                                       null=True, blank=True, on_delete=models.CASCADE)


class SCGAFunction(models.Model):
    # main table module
    module = models.ForeignKey(SCGAModule, to_field="id", related_name="functions",
                               null=True, blank=True, on_delete=models.CASCADE)
    # common info
    function_name = models.CharField(max_length=255)
    analyst = models.CharField(max_length=255)
    # in test plan
    site = models.CharField(max_length=255)
    start_date = models.DateField()
    # coverage = models.OneToOneField(to="Coverage", to_field="id", null=False, blank=False)
    # covered = models.OneToOneField(to="moduleStrucData", to_field="id")
    # total = models.OneToOneField(to="moduleStrucData", to_field="id")
    # defect_classification = models.OneToOneField(to="defectClassification", to_field="id")
    oversight = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, null=True)

    # in test exception
    note = models.CharField(max_length=255, null=True)
    uncoverage_count = models.IntegerField()


class Coverage(models.Model):
    percent_coverage_MCDC = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    percent_coverage_Analysis = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    total_coverage = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    # main table function
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="coverage",
                                    null=True, blank=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # 将值四舍五入到两位小数
        self.percent_coverage_MCDC = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.percent_coverage_Analysis = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.total_coverage = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)



class Covered(models.Model):
    branches = models.IntegerField()
    pairs = models.IntegerField()
    statement = models.IntegerField()
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="covered",
                                    null=True, blank=True, on_delete=models.CASCADE)


class total(models.Model):
    branches = models.IntegerField()
    pairs = models.IntegerField()
    statement = models.IntegerField()
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="total",
                                    null=True, blank=True, on_delete=models.CASCADE)



class DefectClassification(models.Model):
    tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, null=True)
    non_tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, null=True)
    process = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, null=True)
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="defect_classification",
                                    null=True, blank=True, on_delete=models.CASCADE)


class Uncoverage(models.Model):
    function = models.ForeignKey(SCGAFunction, to_field="id", related_name="uncoverages",
                                 null=True, blank=True, on_delete=models.CASCADE)
    uncovered_sw_line = models.IntegerField()
    uncovered_instrument_sw_line = models.TextField(default='')
    requirement_id = models.CharField(max_length=255)
    _class = models.CharField(max_length=255, choices=CHOICES_CLASS, default=NULL)
    analysis_summary = models.CharField(max_length=255, default='')
    correction_summary = models.CharField(max_length=255, default='')
    issue = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)
    # applicable
    PAR_SCR = models.CharField(max_length=255, default='N/A')
    comment = models.CharField(max_length=255, default='')
    

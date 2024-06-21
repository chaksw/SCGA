from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# Create your models here.

PRECENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

YES = 'Yes'
NO = 'No'
NULL = ''
CHOICES_YN = (
    (YES, 'Y'),
    (NO, 'N'),
    (NULL, 'Null'),
)
# level
A = 'A'
B = 'B'
C = 'C'
UNKOWN = 'Unknown'
CHOICES_LEVEL = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
    (UNKOWN, 'Unknown'),
)

# scga class
INCOMPLETE_TESTS = "Incomplete Tests"
REQUIREMENTS_CODE_MISMATCH = "Requirements-Code Mismatch"
DEACTIVATED_CODE = "Deactivated Code"
DEFENSIVE_CODE = "Defensive Code"
TEST_ENVIRONMENT_LIMITATIONS = "Test Environment Limitations"
PREVIOUSLY_ANALYZED_SOFTWARE = "Previously Analyzed Software"
OTHER = "Other"
CHOICES_CLASS = (
    (INCOMPLETE_TESTS, "Incomplete Tests"),
    (REQUIREMENTS_CODE_MISMATCH, "Requirements-Code Mismatch"),
    (DEACTIVATED_CODE, "Deactivated Code"),
    (DEFENSIVE_CODE, "Defensive Code"),
    (TEST_ENVIRONMENT_LIMITATIONS, "Test Environment Limitations"),
    (PREVIOUSLY_ANALYZED_SOFTWARE, "Previously Analyzed Software"),
    (OTHER, "Other"),
)


class Scga(models.Model):
    file_name = models.CharField(max_length=200)
    baseline = models.CharField(max_length=200)

    def __str__(self):
        return self.file_name


class testPlan(models.Model):
    sheet_name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=UNKOWN)
    # main table scga file
    scga_file = models.ForeignKey(to="Scga", to_field="id", related_name="testPlans",
                                  null=True, blank=True, on_delete=models.CASCADE)


class testException(models.Model):
    sheet_name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=UNKOWN)
    scga_file = models.ForeignKey(to="Scga", to_field="id", related_name="testExceptions",
                                  null=True, blank=True, on_delete=models.CASCADE)


class SCGAModule(models.Model):
    module_name = models.CharField(max_length=200)
    process = models.CharField(max_length=200)
    # main table test plan
    test_plan = models.ForeignKey(to="testPlan", to_field="id", related_name="modules",
                                  null=True, blank=True, on_delete=models.CASCADE)
    # main table test exception
    test_exception = models.ForeignKey(to="testException", to_field="id", related_name="modules",
                                       null=True, blank=True, on_delete=models.CASCADE)


class SCGAFunction(models.Model):
    # main table module
    module = models.ForeignKey(to="SCGAModule", to_field="id", related_name="functions",
                                  null=True, blank=True, on_delete=models.CASCADE)
    # common info
    function_name = models.CharField(max_length=200)
    analyst = models.CharField(max_length=200)
    # in test plan
    site = models.CharField(max_length=200)
    start_date = models.DateField()
    # coverage = models.OneToOneField(to="Coverage", to_field="id", null=False, blank=False)
    # covered = models.OneToOneField(to="moduleStrucData", to_field="id")
    # total = models.OneToOneField(to="moduleStrucData", to_field="id")
    # defect_classification = models.OneToOneField(to="defectClassification", to_field="id")
    oversight = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)

    # in test exception
    note = models.CharField(max_length=200)
    uncoverage_count = models.IntegerField()


class Coverage(models.Model):
    percent_coverage_MCDC = models.DecimalField(
        max_digits=5, max_length=3, decimal_places=0, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    percent_coverage_Analysis = models.DecimalField(
        max_digits=5, max_length=3, decimal_places=0, default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    total_coverage = models.DecimalField(max_digits=5, max_length=3, decimal_places=0,
                                         default=Decimal(0), validators=PRECENTAGE_VALIDATOR)
    # main table function
    function = models.OneToOneField(to="SCGAFunction", to_field="id", null=True, blank=True, on_delete=models.CASCADE)


class covered(models.Model):
    branches = models.IntegerField()
    pairs = models.IntegerField()
    statement = models.IntegerField()
    function = models.OneToOneField(to="SCGAFunction", to_field="id", null=True, blank=True, on_delete=models.CASCADE)


class total(models.Model):
    branches = models.IntegerField()
    pairs = models.IntegerField()
    statement = models.IntegerField()
    function = models.OneToOneField(to="SCGAFunction", to_field="id", null=True, blank=True, on_delete=models.CASCADE)

#


class defectClassification(models.Model):
    tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)
    non_tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)
    process = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)
    unction = models.OneToOneField(to="SCGAFunction", to_field="id", null=True, blank=True, on_delete=models.CASCADE)


class uncoverage(models.Model):
    uncovered_sw_line = models.IntegerField()
    uncovered_instrument_sw_line = models.TextField(default='')
    requirement_id = models.CharField(max_length=200)
    _class = models.CharField(max_length=200, choices=CHOICES_CLASS, default='')
    analysis_summary = models.CharField(max_length=200, default='')
    correction_summary = models.CharField(max_length=200, default='')
    issue = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL)
    # applicable
    PAR_SCR = models.CharField(max_length=200, default='N/A')
    comment = models.CharField(max_length=200, default='')
    function = models.ForeignKey(to="SCGAFunction", to_field="id", related_name="uncoverage",
                                 null=True, blank=True, on_delete=models.CASCADE)

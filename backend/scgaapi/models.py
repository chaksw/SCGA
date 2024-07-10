from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.

PRECENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

NULL = ''
YES = 'Y'
NO = 'N'
CHOICES_YN = (
    (NULL, ''),
    (YES, 'Y'),
    (NO, 'N'),
)
# level
A = 'A'
B = 'B'
C = 'C'
CHOICES_LEVEL = (
    (NULL, ''),
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
)

# scga class
INCOMPLETE_TESTS = 'INCOMPLETE_TESTS'
REQUIREMENTS_CODE_MISMATCH = 'REQUIREMENTS_CODE_MISMATCH'
DEACTIVATED_CODE = 'DEACTIVATED_CODE'
DEFENSIVE_CODE = 'DEFENSIVE_CODE'
TEST_ENVIRONMENT_LIMITATIONS = 'TEST_ENVIRONMENT_LIMITATIONS'
PREVIOUSLY_ANALYZED_SOFTWARE = 'PREVIOUSLY_ANALYZED_SOFTWARE'
OTHER = 'OTHER'
CHOICES_CLASS = (
    (NULL, ''),
    (INCOMPLETE_TESTS, "Incomplete Tests"),
    (REQUIREMENTS_CODE_MISMATCH, "Requirements-Code Mismatch"),
    (DEACTIVATED_CODE, "Deactivated Code"),
    (DEFENSIVE_CODE, "Defensive Code"),
    (TEST_ENVIRONMENT_LIMITATIONS, "Test Environment Limitations"),
    (PREVIOUSLY_ANALYZED_SOFTWARE, "Previously Analyzed Software"),
    (OTHER, "Other"),
)

# set blank=True, null=True as no data must be not null
class Scga(models.Model):
    file_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    baseline = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.file_name)


class Level(models.Model):
    level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL, blank=True, null=True)
    scga = models.ForeignKey(Scga, to_field="id", related_name="levels",
                             blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'Level: ' + str(self.level)


class TestPlan(models.Model):
    # main table scga file
    # related_name is the field name that should be defined in serializer
    # scga_file = models.ForeignKey(Scga, to_field="file_name", related_name="test_plans",
    #   null=True, blank=True, on_delete=models.CASCADE)
    sheet_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.OneToOneField(Level, to_field="id", related_name="test_plan",
                                 blank=True, null=True, on_delete=models.CASCADE)
    # level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL)

    def __str__(self):
        return str(self.sheet_name)


class TestException(models.Model):
    # main table scga file
    # related_name is the field name that should be defined in serializer
    # scga_file = models.ForeignKey(Scga, to_field="file_name", related_name="test_exceptions",
    #   null=True, blank=True, on_delete=models.CASCADE)
    sheet_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.OneToOneField(Level, to_field="id", related_name="test_exception",
                                 blank=True, null=True, on_delete=models.CASCADE)
    # level = models.CharField(max_length=20, choices=CHOICES_LEVEL, default=NULL)

    def __str__(self):
        return str(self.sheet_name)


class LvTotalCoverage(models.Model):
    # ensure decinal field has max_digits and decimal_place defined and the defined value is able to covered format of input data
    percent_coverage_MCDC = models.DecimalField(
        max_digits=20, decimal_places=19, default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    percent_coverage_Analysis = models.DecimalField(
        max_digits=20, decimal_places=19, default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    total_coverage = models.DecimalField(max_digits=20, decimal_places=19,
                                         default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    # main table function
    test_plan = models.OneToOneField(TestPlan, to_field="id", related_name="lv_total_coverage",
                                     null=True, blank=True, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     self.percent_coverage_MCDC = Decimal(self.percent_coverage_MCDC).quantize(
    #         Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     self.percent_coverage_Analysis = Decimal(self.percent_coverage_Analysis).quantize(
    #         Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     self.total_coverage = Decimal(self.total_coverage).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     super().save(*args, **kwargs)


class SCGAModule(models.Model):
    module_name = models.CharField(max_length=255, blank=True, null=True)
    process = models.CharField(max_length=255, blank=True, null=True)
    # main table test plan
    test_plan = models.ForeignKey(TestPlan, to_field="id", related_name="modules",
                                  blank=True, null=True, on_delete=models.CASCADE)
    # main table test exception
    test_exception = models.ForeignKey(TestException, to_field="id", related_name="modules",
                                       blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.module_name)


class SCGAFunction(models.Model):
    # main table module
    module = models.ForeignKey(SCGAModule, to_field="id", related_name="functions",
                               blank=True, null=True, on_delete=models.CASCADE)
    # common info
    function_name = models.CharField(max_length=255, blank=True, null=True)
    analyst = models.CharField(max_length=255, blank=True, null=True)
    # in test plan
    site = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    # coverage = models.OneToOneField(to="Coverage", to_field="id", null=False, blank=False)
    # covered = models.OneToOneField(to="moduleStrucData", to_field="id")
    # total = models.OneToOneField(to="moduleStrucData", to_field="id")
    # defect_classification = models.OneToOneField(to="defectClassification", to_field="id")
    oversight = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, blank=True, null=True)

    # in test exception
    note = models.CharField(max_length=255, null=True, blank=True)
    uncoverage_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.function_name)


class Coverage(models.Model):
    # ensure decinal field has max_digits and decimal_place defined and the defined value is able to covered format of input data
    percent_coverage_MCDC = models.DecimalField(
        max_digits=20, decimal_places=19, default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    percent_coverage_Analysis = models.DecimalField(
        max_digits=20, decimal_places=19, default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    total_coverage = models.DecimalField(max_digits=20, decimal_places=19,
                                         default=Decimal('0.00'), validators=PRECENTAGE_VALIDATOR, blank=True, null=True)
    # main table function
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="coverage",
                                    null=True, blank=True, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     # 将值四舍五入到两位小数
    #     self.percent_coverage_MCDC = Decimal(self.percent_coverage_MCDC).quantize(
    #         Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     self.percent_coverage_Analysis = Decimal(self.percent_coverage_MCDC).quantize(
    #         Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     self.total_coverage = Decimal(self.percent_coverage_MCDC).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     super().save(*args, **kwargs)


class Covered(models.Model):
    branches = models.IntegerField(blank=True, null=True)
    pairs = models.IntegerField(blank=True, null=True)
    statement = models.IntegerField(blank=True, null=True)
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="covered",
                                    blank=True, null=True, on_delete=models.CASCADE)


class total(models.Model):
    branches = models.IntegerField(blank=True, null=True)
    pairs = models.IntegerField(blank=True, null=True)
    statement = models.IntegerField(blank=True, null=True)
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="total",
                                    blank=True, null=True, on_delete=models.CASCADE)


class DefectClassification(models.Model):
    tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, blank=True, null=True)
    non_tech = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, blank=True, null=True)
    process = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, blank=True, null=True)
    function = models.OneToOneField(SCGAFunction, to_field="id", related_name="defect_classification",
                                    blank=True, null=True, on_delete=models.CASCADE)


class Uncoverage(models.Model):
    function = models.ForeignKey(SCGAFunction, to_field="id", related_name="uncoverages",
                                 blank=True, null=True, on_delete=models.CASCADE)
    uncovered_sw_line = models.CharField(max_length=255, blank=True, null=True)
    uncovered_instrument_sw_line = models.TextField(default=NULL, blank=True, null=True)
    requirement_id = models.CharField(max_length=255, blank=True, null=True)
    _class = models.CharField(max_length=255, choices=CHOICES_CLASS, default=NULL, blank=True, null=True)
    analysis_summary = models.CharField(max_length=255, default=NULL, blank=True, null=True)
    correction_summary = models.CharField(max_length=255, default=NULL, blank=True, null=True)
    issue = models.CharField(max_length=20, choices=CHOICES_YN, default=NULL, blank=True, null=True)
    # applicable
    PAR_SCR = models.CharField(max_length=255, default=NULL, blank=True, null=True)
    comment = models.CharField(max_length=255, default=NULL, blank=True, null=True)

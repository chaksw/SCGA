from rest_framework import serializers
from .models import Scga, Level, TestPlan, TestException, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPlan
        fields = (
            'id',
            'scga_file',
            'sheet_name',
            'level'
        )


class TestExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestException
        fields = (
            'id',
            'scga_file',
            'sheet_name',
            'level',
        )


class LevelSerializer(serializers.ModelSerializer):
    test_plans = TestPlanSerializer(many=True)
    test_exceptions = TestExceptionSerializer(many=True)

    class Meta:
        model = Level
        fields = (
            'id',
            'level',
            'test_plans',
            'test_exceptions'
        )


class ScgaSerializer(serializers.ModelSerializer):
    # The `.create()` method does not support writable nested fields by default.
    levels = LevelSerializer(many=True)
    # test_plans = TestPlanSerializer(many=True)
    # test_exceptions = TestExceptionSerializer(many=True)

    class Meta:
        model = Scga
        fields = (
            'id',
            'file_name',
            'baseline',
            'levels',
            # 'test_plans',
            # 'test_exceptions'
        )

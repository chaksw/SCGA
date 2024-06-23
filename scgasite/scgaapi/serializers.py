from rest_framework import serializers
from .models import Scga, TestPlan, TestException, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage


class TestPlanSerializer(serializers.Serializer):
    class Meta:
        model = TestPlan
        fields = (
            'id',
            'scga_file'
            'sheet_name',
            'level'
        )


class TestExceptionSerializer(serializers.Serializer):
    class Meta:
        model = TestException
        fields = (
            'id',
            'scga_file'
            'sheet_name',
            'level'
        )


# class LevelSerializer(serializers.Serializer):
#     test_plan = TestPlanSerializer(read_only=True)
#     test_exception = TestExceptionSerializer(read_only=True)

#     class Meta:
#         model = Level
#         fields = (
#             'id'
#             'level',
#             'test_plan',
#             'test_exception'
#         )


class ScgaSerializer(serializers.ModelSerializer):
    # levels = LevelSerializer(many=True, read_only=True)
    # The `.create()` method does not support writable nested fields by default.
    test_plans = TestPlanSerializer(many=True, read_only=True)
    test_exceptions = TestExceptionSerializer(many=True, read_only=True)

    class Meta:
        model = Scga
        fields = (
            'id',
            'file_name',
            'baseline',
            # 'levels',
            'test_plans',
            'test_exceptions'
        )

from rest_framework import serializers
from .models import Scga, Level, TestPlan, TestException, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPlan
        fields = (
            'id',
            # 'scga_file',
            # 'sheet_name',
            'level'
        )


class TestExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestException
        fields = (
            'id',
            # 'scga_file',
            # 'sheet_name',
            'level',
        )


class LevelSerializer(serializers.ModelSerializer):
    # one to one: One level has only one test plan and one test exception
    test_plans = TestPlanSerializer()
    test_exceptions = TestExceptionSerializer()

    class Meta:
        model = Level
        fields = (
            'id',
            'level',
            'test_plans',
            'test_exceptions'
        )

    def create(self, validated_data):
        print('get there4')
        test_plans_data = validated_data.pop("test_plans")
        test_execeptions_data = validated_data.pop("test_exceptions")
        # ** is destructure symbol of dictionary
        level = Level.objects.create(**validated_data)
        if test_plans_data is not None:
            for test_plan_data in test_plans_data:
                TestPlan.objects.create(level=level, **test_plan_data)
        for test_exeception_data in test_execeptions_data:
            if test_execeptions_data is not None:
                TestException.objects.create(level=level, **test_exeception_data)
        return level


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

    # override .create() function
    # ** is destructure symbol of dictionary
    def create(self, validated_data):
        print(validated_data)
        print('get there1')
        levels_data = validated_data.pop("levels")
        scga = Scga.objects.create(**validated_data)
        if levels_data is not None:
            print(levels_data)
            print('get there2')
            for level_data in levels_data:
                test_plans_data = level_data.pop("test_plans")
                # strat from here
                print(test_plans_data)
                test_execeptions_data = level_data.pop("test_exceptions")
                print(test_execeptions_data)
                # ** is destructure symbol of dictionary
                level = Level.objects.create(**level_data)
                print('get there3')
                if test_plans_data is not None:
                    for test_plan_data in test_plans_data:
                        TestPlan.objects.create(level=level, **test_plan_data)
                for test_exeception_data in test_execeptions_data:
                    if test_execeptions_data is not None:
                        TestException.objects.create(level=level, **test_exeception_data)
                print('get there4')
        return scga

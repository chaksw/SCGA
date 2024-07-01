from rest_framework import serializers
from .models import Scga, Level, TestPlan, TestException, LvTotalCoverage, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage


class UncoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uncoverage
        fields = (
            'id',
            'function',
            'uncovered_sw_line',
            'uncovered_instrument_sw_line',
            'requirement_id',
            '_class',
            'analysis_summary',
            'correction_summary',
            'issue',
            'PAR_SCR',
            'comment',
        )


class DefectClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectClassification
        fields = (
            'id',
            'function',
            'tech',
            'non_tech',
            'process',
        )


class totalSerializer(serializers.ModelSerializer):
    class Meta:
        model = total
        fields = (
            'id',
            'function',
            'branches',
            'pairs',
            'statement',
        )


class CoveredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Covered
        fields = (
            'id',
            'function',
            'branches',
            'pairs',
            'statement',
        )


class CoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = (
            'id',
            'function',
            'percent_coverage_MCDC',
            'percent_coverage_Analysis',
            'total_coverage',
        )


# Test Plan Function serializer
class TPFunctionSerializer(serializers.ModelSerializer):
    coverage = CoverageSerializer()
    covered = CoveredSerializer()
    total = totalSerializer()
    defect_classification = DefectClassificationSerializer()

    class Meta:
        model = SCGAFunction
        fields = (
            'id',
            'module',
            'function_name',
            'analyst',
            'site',
            'start_date',
            'coverage',
            'covered',
            'total',
            'oversight',
            'defect_classification',
        )

    def create(self, validated_data):
        coverage_data = validated_data.pop('coverage')
        covered_data = validated_data.pop('covered')
        total_data = validated_data.pop('total')
        defect_classification_data = validated_data.pop('defect_classification')
        function = SCGAFunction.objects.create(**validated_data)
        # coverage situation in test plan
        if coverage_data is not None:
            Coverage.objects.create(function=function, **coverage_data)
        # covered source in test plan
        if covered_data is not None:
            Covered.objects.create(function=function, **covered_data)
        # total source in test plan
        if total_data is not None:
            total.objects.create(function=function, **total_data)
        # defect classification in test exception
        if defect_classification_data is not None:
            DefectClassification.objects.create(function=function, **defect_classification_data)
        return function


# Test Exception Function Serializer
class TEFunctionSerializer(serializers.ModelSerializer):
    uncoverages = UncoverageSerializer(many=True)

    class Meta:
        model = SCGAFunction
        fields = (
            'id',
            'module',
            'function_name',
            'note',
            'uncoverages',
            'uncoverage_count',
        )

    def create(self, validated_data):
        uncoverages_data = validated_data.pop('uncoverages')
        function = SCGAFunction.objects.create(**validated_data)
        # uncoverage information in test exception
        if uncoverages_data is not None:
            if isinstance(uncoverages_data, list):
                for uncoverage_data in uncoverages_data:
                    Uncoverage.objects.create(function=function, **uncoverage_data)
            elif isinstance(uncoverages_data, dict):
                Uncoverage.objects.create(function=function, **uncoverage_data)
        return function


# Test Plan Module Serializer
class TPModuleSerializer(serializers.ModelSerializer):
    functions = TPFunctionSerializer(many=True)

    class Meta:
        model = SCGAModule
        fields = (
            'id',
            'test_plan',
            'module_name',
            'functions',
            'process',
        )

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if (functions_data is not None):
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TPFunctionSerializer.create(
                        TPFunctionSerializer, validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TPFunctionSerializer.create(TPFunctionSerializer, validated_data=functions_data)
                # SCGAFunction.objects.create(module=module, **function_data)

        return module


# Test Exception Module Serializer
class TEModuleSerializer(serializers.ModelSerializer):
    functions = TEFunctionSerializer(many=True)

    class Meta:
        model = SCGAModule
        fields = (
            'id',
            'test_exception',
            'module_name',
            'functions',
            'process',
        )

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if (functions_data is not None):
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TEFunctionSerializer.create(
                        TEFunctionSerializer, validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TEFunctionSerializer.create(TEFunctionSerializer, validated_data=functions_data)
                # SCGAFunction.objects.create(module=module, **function_data)

        return module


class LvTotalCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LvTotalCoverage
        fields = (
            'id',
            'test_plan',
            'percent_coverage_MCDC',
            'percent_coverage_Analysis',
            'total_coverage',
        )


class TestPlanSerializer(serializers.ModelSerializer):
    modules = TEModuleSerializer(many=True)
    lv_total_coverage = LvTotalCoverageSerializer()

    class Meta:
        model = TestPlan
        fields = (
            'id',
            # 'scga_file',
            'sheet_name',
            'level',
            'modules',
            'lv_total_coverage'
        )

    def create(self, validated_data):
        modules_data = validated_data.pop("modules")
        lv_total_coverage_data = validated_data.pop("lv_total_coverage")
        test_plan = TestPlan.objects.create(**validated_data)
        # modules in test
        if (modules_data is not None):
            if isinstance(modules_data, list):
                for module_data in modules_data:
                    module_data['test_plan'] = test_plan
                    TPModuleSerializer.create(TPModuleSerializer(), validated_data=module_data)
                    # SCGAModule.objects.create(test_plan=test_plan, **module_data)
            elif isinstance(modules_data, dict):
                modules_data['test_plan'] = test_plan
                TPModuleSerializer.create(TPModuleSerializer(), validated_data=modules_data)
                # SCGAModule.objects.create(test_plan=test_plan, **module_data)
        # level's total coverage
        if lv_total_coverage_data is not None:
            LvTotalCoverage.objects.create(test_plan=test_plan, **lv_total_coverage_data)
        return test_plan


class TestExceptionSerializer(serializers.ModelSerializer):
    modules = TEModuleSerializer(many=True)

    class Meta:
        model = TestException
        fields = (
            'id',
            # 'scga_file',
            'sheet_name',
            'level',
            'modules'
        )

    def create(self, validated_data):
        modules_data = validated_data.pop("modules")
        test_exception = TestException.objects.create(**validated_data)
        if (modules_data is not None):
            if isinstance(modules_data, list):
                for module_data in modules_data:
                    module_data['test_exception'] = test_exception
                    TEModuleSerializer.create(TEModuleSerializer(), validated_data=module_data)
                    # SCGAModule.objects.create(test_exception=test_exception, **module_data)
            elif isinstance(modules_data, dict):
                modules_data['test_exception'] = test_exception
                TEModuleSerializer.create(TEModuleSerializer(), validated_data=modules_data)
                # SCGAModule.objects.create(test_exception=test_exception, **module_data)
        return test_exception


class LevelSerializer(serializers.ModelSerializer):
    # one to one: One level has only one test plan and one test exception
    test_plan = TestPlanSerializer()
    test_exception = TestExceptionSerializer()

    class Meta:
        model = Level
        fields = (
            'id',
            'level',
            'test_plan',
            'test_exception'
        )

    def create(self, validated_data):
        print('get there4')
        test_plan_data = validated_data.pop("test_plan")
        test_exeception_data = validated_data.pop("test_exception")
        # ** is destructure symbol of dictionary
        level = Level.objects.create(**validated_data)
        if test_plan_data is not None:
            test_plan_data['level'] = level
            TestPlanSerializer.create(TestPlanSerializer(), validated_data=test_plan_data)
            # TestPlan.objects.create(level=level, **test_plan_data)
        if test_exeception_data is not None:
            test_exeception_data['level'] = level
            TestExceptionSerializer.create(TestExceptionSerializer(), validated_data=test_exeception_data)
            # TestException.objects.create(level=level, **test_exeception_data)
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
        import pdb
        pdb.set_trace()
        print(validated_data)
        print('get there1')
        levels_data = validated_data.pop("levels")
        scga = Scga.objects.create(**validated_data)
        if levels_data is not None:
            print(levels_data)
            print('get there2')
            for level_data in levels_data:
                level_data['scga_file'] = scga
                print('get there3')
                LevelSerializer.create(LevelSerializer(), validated_data=level_data)
                # level = Level.objects.create(scga_file=scga, **level_data)
                # test_plan_data = level_data.pop("test_plan")
                # # strat from here
                # print(test_plan_data)
                # test_exeception_data = level_data.pop("test_exception")
                # print(test_exeception_data)
                # # ** is destructure symbol of dictionary
                # print('get there3')
                # if test_plan_data is not None:
                #     print(test_plan_data)
                #     TestPlan.objects.create(level=level, **test_plan_data)
                # if test_exeception_data is not None:
                #     print(test_exeception_data)
                #     TestException.objects.create(level=level, **test_exeception_data)
                # print('get there4')
        return scga

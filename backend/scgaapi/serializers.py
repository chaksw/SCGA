from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers
from .models import Scga, Level, TestPlan, TestException, LvTotalCoverage, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage, CHOICES_CLASS
# DRF is_valid(), validate()函数调用逻辑
# 1. 当 is_valid()被调用后，如果当前的 serializer 没有重写 is_valid(), 则父类的 is_valid() 会被调用。
# 2. 当 is_valid()被调用后， validate() 函数会被自动调用，如果重写了 validate()，则会调用当前 serializer 的 validate()
# 3. 对于嵌套层级的 serializers，DRF 会自动处理嵌套的 serializer, 也就是说，我们不需要显式地调用每个下层的 is_valid(), 在super().isvalid()被调用时， DRF 会调用下层 serializer的is_valid().
# 4. 例如，当scga的 super().isvalid() 被调用时， ScgaSerializer.validate()会被调用，但在验证 ScgaSerializer 的字段之前， DRF 会自动调用嵌套的 LevelSerializer.is_valid() 方法，然后调用 LevelSerializer.validate(). 如此类推。
# 5. 所以，只需要为每个 serializer 重写 validate(), 不需要在当中显式调用下层的 is_valid()方法，就能确保每个 serializer 的字段的原数据都能以我们所希望的方式被被预处理和验证。
# 具体调用顺序：
# 1. 调用 ScgaSerializer.is_valid()。
# 2. ScgaSerializer.is_valid() 调用 super().is_valid()。
# 3. super().is_valid() 调用 run_validation 方法。
# 4. run_validation 方法调用嵌套序列化器 LevelSerializer.is_valid()。
# 5. LevelSerializer.is_valid() 调用 super().is_valid()。
# 6. super().is_valid() 调用 run_validation 方法。
# 7. run_validation 方法调用嵌套序列化器 TestPlanSerializer.is_valid() 和 TestExceptionSerializer。
# 8. 所有嵌套序列化器的 is_valid() 方法执行完毕后，返回到 ScgaSerializer
# 9. run_validation 方法继续执行，调用 ScgaSerializer.validate() 方法。


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

    def set_class(self, value):
        choice_map = {v: k for k, v in CHOICES_CLASS}
        print(choice_map)
        class_choice = None
        if value in choice_map:
            class_choice = choice_map[value]
        else:
            class_choice = ''
        return class_choice

    def set_requirement_id(self, value):
        reqs = None
        if isinstance(value, list):
            reqs = '\n'.join(item for item in value if item)
        elif isinstance(value, str):
            reqs = value
        return reqs

    def validate(self, data):
        # check key and value
        if 'uncovered_sw_line' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        if 'uncovered_instrument_sw_line' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        if 'requirement_id' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        else:
            data['requirement_id'] = self.set_requirement_id(data['requirement_id'])
        if '_class' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        # else:
        #     data['_class'] = self.set_class(data['_class'])
        if 'analysis_summary' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        if 'correction_summary' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        if 'issue' not in data:
            raise serializers.ValidationError('no attribute name: ["issue"] in data')
        if 'PAR_SCR' not in data:
            raise serializers.ValidationError('no attribute name: ["PAR_SCR"] in data')
        if 'comment' not in data:
            raise serializers.ValidationError('no attribute name: ["comment"] in data')
        return data


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

    def validate(self, data):
        # check key and value
        if 'tech' not in data:
            raise serializers.ValidationError('no attribute name: ["tech"] in data')
        if 'non_tech' not in data:
            raise serializers.ValidationError('no attribute name: ["non_tech"] in data')
        if 'process' not in data:
            raise serializers.ValidationError('no attribute name: ["process"] in data')
        return data


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

    def validate(self, data):
        # check key and value
        # if data['branches'] != 0 and ('branches' not in data):
        #     raise serializers.ValidationError('branches cannot be empty')
        # if data['pairs'] != 0 and ('pairs' not in data):
        #     raise serializers.ValidationError('pairs cannot be empty')
        if data['statement'] != 0 and ('statement' not in data):
            raise serializers.ValidationError('statement cannot be empty')
        return data


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

    def validate(self, data):
        # check key and value
        # if data['branches'] != 0 and ('branches' not in data):
        #     raise serializers.ValidationError('branches cannot be empty')
        # if data['pairs'] != 0 and ('pairs' not in data):
        #     raise serializers.ValidationError('pairs cannot be empty')
        if data['statement'] != 0 and ('statement' not in data):
            raise serializers.ValidationError('statement cannot be empty')
        return data


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

    def validate(self, data):
        if 'percent_coverage_MCDC' in data:
            data['percent_coverage_MCDC'] = data['percent_coverage_MCDC'].quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'percent_coverage_Analysis' in data:
            data['percent_coverage_Analysis'] = data['percent_coverage_Analysis'].quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'total_coverage' in data:
            data['total_coverage'] = data['total_coverage'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return data


# Test Plan Function serializer
class TPFunctionSerializer(serializers.ModelSerializer):
    coverage = CoverageSerializer()
    covered = CoveredSerializer()
    total = totalSerializer()
    defect_classification = DefectClassificationSerializer()
    # uncoverages = UncoverageSerializer(required=False)
    # uncoverage_count = serializers.IntegerField(required=False)

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

    def validate(self, data):
        # check key and value
        if 'function_name' not in data:
            raise serializers.ValidationError('no attribute name: ["function_name"] in data')
        if 'analyst' not in data:
            raise serializers.ValidationError('no attribute name: ["analyst"] in data')
        if 'site' not in data:
            raise serializers.ValidationError('no attribute name: ["site"] in data')
        if 'start_date' not in data:
            raise serializers.ValidationError('no attribute name: ["start_date"] in data')
        if 'oversight' not in data:
            raise serializers.ValidationError('no attribute name: ["oversight"] in data')

        return data

    def create(self, validated_data):
        # uncoverages_data = validated_data.pop('uncoverages', None)
        # uncoverage_count_data = validated_data.pop('uncoverage_count', None)
        coverage_data = validated_data.pop('coverage')
        covered_data = validated_data.pop('covered')
        total_data = validated_data.pop('total')
        defect_classification_data = validated_data.pop('defect_classification')
        function = SCGAFunction.objects.create(**validated_data)
        # coverage situation in test plan
        if coverage_data:
            Coverage.objects.create(function=function, **coverage_data)
        # covered source in test plan
        if covered_data:
            Covered.objects.create(function=function, **covered_data)
        # total source in test plan
        if total_data:
            total.objects.create(function=function, **total_data)
        # defect classification in test exception
        if defect_classification_data:
            DefectClassification.objects.create(function=function, **defect_classification_data)
        return function


# Test Exception Function Serializer
class TEFunctionSerializer(serializers.ModelSerializer):
    uncoverages = UncoverageSerializer(many=True, required=False, allow_null=True)

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

    def validate(self, data):
        # check key and value
        if 'function_name' not in data:
            raise serializers.ValidationError('no attribute name: ["function_name"] in data')
        if 'note' not in data:
            raise serializers.ValidationError('no attribute name: ["note"] in data')
        if 'uncoverage_count' not in data:
            raise serializers.ValidationError('no attribute name: ["uncoverage_count"] in data')
        return data

    def create(self, validated_data):
        uncoverages_data = validated_data.pop('uncoverages')
        function = SCGAFunction.objects.create(**validated_data)
        # uncoverage information in test exception
        if uncoverages_data:
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

    def validate(self, data):
        # check key and value
        if 'module_name' not in data:
            raise serializers.ValidationError('no attribute name: ["module_name"] in data')
        if 'process' not in data:
            raise serializers.ValidationError('no attribute name: ["process"] in data')

        return data

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if functions_data:
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TPFunctionSerializer.create(
                        TPFunctionSerializer(), validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TPFunctionSerializer.create(TPFunctionSerializer(), validated_data=functions_data)

        return module


# Test Exception Module Serializer
class TEModuleSerializer(serializers.ModelSerializer):
    functions = TEFunctionSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = SCGAModule
        fields = (
            'id',
            'test_exception',
            'module_name',
            'functions',
            'process',
        )

    def validate(self, data):
        # check key and value
        if 'module_name' not in data:
            raise serializers.ValidationError('no attribute name: ["module_name"] in data')
        if 'process' not in data:
            raise serializers.ValidationError('no attribute name: ["process"] in data')
        return data

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if functions_data:
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TEFunctionSerializer.create(TEFunctionSerializer(), validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TEFunctionSerializer.create(TEFunctionSerializer(), validated_data=functions_data)

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

    # validate() is called automatically in the running of is_valid
    def validate(self, data):
        if 'percent_coverage_MCDC' in data:
            data['percent_coverage_MCDC'] = Decimal(data['percent_coverage_MCDC']).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            print('error occurred in level total coverage percent_coverage_MCDC')
            raise serializers.ValidationError('no attribute percent_coverage_MCDC')
        if 'percent_coverage_Analysis' in data:
            data['percent_coverage_Analysis'] = Decimal(
                data['percent_coverage_Analysis']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            print('error occurred in level total coverage percent_coverage_Analysis')
            raise serializers.ValidationError('no attribute percent_coverage_Analysis')
        if 'total_coverage' in data:
            data['total_coverage'] = Decimal(data['total_coverage']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            print('error occurred in level total coverage total_coverage')
            raise serializers.ValidationError('no attribute total_coverage')
        return data

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)


class TestPlanSerializer(serializers.ModelSerializer):
    modules = TPModuleSerializer(many=True)
    lv_total_coverage = LvTotalCoverageSerializer()

    class Meta:
        model = TestPlan
        fields = (
            'id',
            # 'scga',
            'sheet_name',
            'level',
            'modules',
            'lv_total_coverage'
        )

    def validate(self, data):
        # check key and value
        if 'sheet_name' not in data:
            print('no attribute name: ["sheet_name"] in data')
            raise serializers.ValidationError('no attribute name: ["sheet_name"] in data')

        return data

    def create(self, validated_data):
        modules_data = validated_data.pop("modules")
        lv_total_coverage_data = validated_data.pop("lv_total_coverage")
        test_plan = TestPlan.objects.create(**validated_data)
        # modules in test
        if modules_data:
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
        if lv_total_coverage_data:
            LvTotalCoverage.objects.create(test_plan=test_plan, **lv_total_coverage_data)
        return test_plan


class TestExceptionSerializer(serializers.ModelSerializer):
    modules = TEModuleSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = TestException
        fields = (
            'id',
            # 'scga',
            'sheet_name',
            'level',
            'modules'
        )

    def validate(self, data):
        # check key and value
        if data:
            if 'sheet_name' not in data:
                print('no attribute name: ["sheet_name"] in data')
                raise serializers.ValidationError('no attribute name: ["sheet_name"] in data')

        return data

    def create(self, validated_data):
        modules_data = validated_data.pop("modules")
        test_exception = TestException.objects.create(**validated_data)
        if (modules_data):
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
    test_plan = TestPlanSerializer(required=False, allow_null=True)
    test_exception = TestExceptionSerializer(required=False, allow_null=True)

    class Meta:
        model = Level
        fields = (
            'id',
            'level',
            'test_plan',
            'test_exception'
        )

    def validate(self, data):
        # check key and value
        if 'level' not in data or not data['level']:
            raise serializers.ValidationError('level cannot be empty')

        return data

    def create(self, validated_data):
        test_plan_data = validated_data.pop("test_plan", None)
        test_exeception_data = validated_data.pop("test_exception", None)
        # ** is destructure symbol of dictionary
        level = Level.objects.create(**validated_data)
        if test_plan_data:
            test_plan_data['level'] = level
            TestPlanSerializer.create(TestPlanSerializer(), validated_data=test_plan_data)
            # TestPlan.objects.create(level=level, **test_plan_data)
        if test_exeception_data:
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
            'project',
            'function',
            'current',
            'file_name',
            'baseline',
            'levels',
            # 'test_plans',
            # 'test_exceptions'
        )

    def validate(self, data):
        # check key and value
        if 'file_name' not in data or not data['file_name']:
            raise serializers.ValidationError('file name cannot be empty')
        if 'baseline' not in data or not data['baseline']:
            raise serializers.ValidationError('baseline cannot be empty')
        return data

    # ** is destructure symbol of dictionary

    def create(self, validated_data):
        levels_data = validated_data.pop("levels")
        scga = Scga.objects.create(**validated_data)
        if levels_data:
            for level_data in levels_data:
                level_data['scga'] = scga
                LevelSerializer.create(LevelSerializer(), validated_data=level_data)

        return scga

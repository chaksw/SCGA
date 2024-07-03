from decimal import Decimal, ROUND_HALF_UP
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
    
    def validate(self, data):

        if 'percent_coverage_MCDC' in data:
            data['percent_coverage_MCDC'] = Decimal(data['percent_coverage_MCDC']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'percent_coverage_Analysis' in data:
            data['percent_coverage_Analysis'] = Decimal(data['percent_coverage_Analysis']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'total_coverage' in data:
            data['total_coverage'] = Decimal(data['total_coverage']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return data

    def is_valid(self, *, raise_exception=False):

        return super().is_valid(raise_exception=raise_exception)


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

    # validate nested uncoverages data
    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested coverage data
        coverage_data = self.initial_data.get('coverage', {})
        coverage_serializer = UncoverageSerializer(data=coverage_data)
        if not coverage_serializer.is_valid(raise_exception=raise_exception):
            self._errors['coverage'] = coverage_serializer.errors
        # validate nested covered data
        covered_data = self.initial_data.get('covered', {})
        covered_serializer = UncoverageSerializer(data=covered_data)
        if not covered_serializer.is_valid(raise_exception=raise_exception):
            self._errors['covered'] = covered_serializer.errors
        # validate nested total data
        total_data = self.initial_data.get('total', {})
        total_serializer = UncoverageSerializer(data=total_data)
        if not total_serializer.is_valid(raise_exception=raise_exception):
            self._errors['total'] = total_serializer.errors
        # validate nested defect classification data
        defect_classification_data = self.initial_data.get('defect_classification', {})
        defect_classification_serializer = UncoverageSerializer(data=defect_classification_data)
        if not defect_classification_serializer.is_valid(raise_exception=raise_exception):
            self._errors['defect_classification'] = defect_classification_serializer.errors
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)

    def create(self, validated_data):
        # uncoverages_data = validated_data.pop('uncoverages', None)
        # uncoverage_count_data = validated_data.pop('uncoverage_count', None)
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

    # validate nested uncoverages data
    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested modules data
        for uncoverage_data in self.initial_data.get('uncoverages', []):
            uncoverage_serializer = UncoverageSerializer(data=uncoverage_data)
            if not uncoverage_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('uncoverages', []).append(uncoverage_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)


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

    # validate nested functions data
    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested modules data
        for function_data in self.initial_data.get('functions', []):
            function_serializer = TEFunctionSerializer(data=function_data)
            if not function_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('functions', []).append(function_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if (functions_data is not None):
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TPFunctionSerializer.create(
                        TPFunctionSerializer(), validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TPFunctionSerializer.create(TPFunctionSerializer(), validated_data=functions_data)
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
    

    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested functions data
        for function_data in self.initial_data.get('functions', []):
            function_serializer = TEFunctionSerializer(data=function_data)
            if not function_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('functions', []).append(function_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)

    def create(self, validated_data):
        functions_data = validated_data.pop("functions")
        module = SCGAModule.objects.create(**validated_data)
        # functions for module(cpp file)
        if (functions_data is not None):
            if isinstance(functions_data, list):
                for function_data in functions_data:
                    function_data['module'] = module
                    TEFunctionSerializer.create(TEFunctionSerializer(), validated_data=function_data)
                    # SCGAFunction.objects.create(module=module, **function_data)
            elif isinstance(functions_data, dict):
                functions_data['module'] = module
                TEFunctionSerializer.create(TEFunctionSerializer(), validated_data=functions_data)
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

    # validate() is called automatically in the running of is_valid
    def validate(self, data):
        import pdb;pdb.set_trace()
        if 'percent_coverage_MCDC' in data:
            data['percent_coverage_MCDC'] = Decimal(data['percent_coverage_MCDC']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'percent_coverage_Analysis' in data:
            data['percent_coverage_Analysis'] = Decimal(data['percent_coverage_Analysis']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if 'total_coverage' in data:
            data['total_coverage'] = Decimal(data['total_coverage']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
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
            # 'scga_file',
            'sheet_name',
            'level',
            'modules',
            'lv_total_coverage'
        )

    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate level total coverage data
        lv_total_coverage_data = self.initial_data.get('lv_total_coverage', {})
        lv_total_coverage_serializer = LvTotalCoverageSerializer(data=lv_total_coverage_data)
        # lv_total_coverage_data = lv_total_coverage_serializer.validate(lv_total_coverage_data)
        if not lv_total_coverage_serializer.is_valid(raise_exception=raise_exception):
            self._errors['lv_total_coverage'] = lv_total_coverage_serializer.errors

        # validate nested modules data
        for module_data in self.initial_data.get('modules', []):
            module_serializer = TPModuleSerializer(data=module_data)
            if not module_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('modules', []).append(module_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)

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

    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested modules data
        for module_data in self.initial_data.get('modules', []):
            module_serializer = TEModuleSerializer(data=module_data)
            if not module_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('modules', []).append(module_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)

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
    test_exception = TestExceptionSerializer(required=False)

    class Meta:
        model = Level
        fields = (
            'id',
            'level',
            'test_plan',
            'test_exception'
        )

    def is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        test_plan_data = self.initial_data.get('test_plan', {})
        test_plan_serializer = TestPlanSerializer(data=test_plan_data)
        test_exception_data = self.initial_data.get('test_exception', {})
        test_exception_serializer = TestExceptionSerializer(data=test_exception_data)
        if not test_plan_serializer.is_valid(raise_exception=raise_exception):
            self._errors['test_plan'] = test_plan_serializer.errors
        if not test_exception_serializer.is_valid(raise_exception=raise_exception):
            self._errors['test_exception'] = test_exception_serializer.errors

        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)
            
        

    def create(self, validated_data):
        print('get there4')
        test_plan_data = validated_data.pop("test_plan", None)
        test_exeception_data = validated_data.pop("test_exception", None)
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

    

    def is_valid(self, *, raise_exception=False):
        import pdb
        pdb.set_trace()
        super().is_valid(raise_exception=raise_exception)
        import pdb
        pdb.set_trace()
        # validate nested levels data
        for level_data in self.initial_data.get('levels', []):
            level_serializer = LevelSerializer(data=level_data)
            if not level_serializer.is_valid(raise_exception=raise_exception):
                self._errors.setdefault('levels', []).append(level_serializer.errors)
        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)
        
        return not bool(self._errors)


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

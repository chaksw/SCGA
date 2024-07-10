# Srouce Coverage Gap Analysis
## POST 机制
当发送POST请求以创建新对象时，位于`views.py` 和 `serializers.py` 中有以下函数会被执行：
1. Serializer
   1. `.is_valid(raise_exception=True)`
   2. `.save()`
   3. `.create()`
2. View
   1. `.create()`
   2. `get_serializer(data=request.data)`
   3. `.perform_create(serializer)`
### 具体顺序
#### 1. View handle
1. View 中的 `.create()` 被调用，调用 `get_serializer(data=request.data)`, 将数据转化为serialzer实例。
2. `serializer.is_valid()` 被调用，验证数据，并捕捉 ValidationError()
3. 若数据没有error，调用view中的 `.perform_create(serializer)`
#### 2. Object Creation
1. `.perform_create(serializer)` 会调用`serializer.save()`
2. `serializer.save()` 调用 `serializer.create()`
3. `serializer.create()` 中创建新对象并返回
#### 3. Response
View返回包含新创建对象数据的响应

## DRF `serializer.is_valid()`, `.validate()`函数在嵌套数据下的调用逻辑
1. 当 is_valid()被调用后，如果当前的 serializer 没有重写 is_valid(), 则父类的 is_valid() 会被调用。
2. 当 is_valid()被调用后， validate() 函数会被自动调用，如果重写了 validate()，则会调用当前 serializer 的 validate()
3. 对于嵌套层级的 serializers，DRF 会自动处理嵌套的 serializer, 也就是说，我们不需要显式地调用每个下层的 is_valid(), 在super().isvalid()被调用时， DRF 会调用下层 serializer的is_valid().
4. 例如，当scga的 super().isvalid() 被调用时， ScgaSerializer.validate()会被调用，但在验证 ScgaSerializer 的字段之前， DRF 会自动调用嵌套的 LevelSerializer.is_valid() 方法，然后调用 LevelSerializer.validate(). 如此类推。
5. 所以，只需要为每个 serializer 重写 validate(), 不需要在当中显式调用下层的 is_valid()方法，就能确保每个 serializer 的字段的原数据都能以我们所希望的方式被被预处理和验证。
具体调用顺序：
1. 调用 ScgaSerializer.is_valid()。
2. ScgaSerializer.is_valid() 调用 super().is_valid()。
3. super().is_valid() 调用 run_validation 方法。
4. run_validation 方法调用嵌套序列化器 LevelSerializer.is_valid()。
5. LevelSerializer.is_valid() 调用 super().is_valid()。
6. super().is_valid() 调用 run_validation 方法。
7. run_validation 方法调用嵌套序列化器 TestPlanSerializer.is_valid() 和 TestExceptionSerializer。
8. 所有嵌套序列化器的 is_valid() 方法执行完毕后，返回到 ScgaSerializer
9. run_validation 方法继续执行，调用 ScgaSerializer.validate() 方法。

## View 中的 `.get_query()` & `perform_create()`

get_queryset() will be called for access of url (GET())

perform_create will be called for creation of data (POST()), it will execute in .create() once is_valid() return true

pk is more general. When you define a custom primary key field in a model, pk will always refer to this custom primary key, whereas id is the default field name.

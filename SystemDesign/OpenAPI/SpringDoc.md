# 关于泛型
- 泛型类不要加title，加description即可，不然所有泛型参数的name为同一个，保持自动生成title即可
# 关于Query
- OpenAPI的查询参数即便作为一个对象，也不会unwrap，参数名还是变量名，只不过引用了一个对象
	- apifox仅支持从这个对象属性的description获取名称，而不是title
- Flat Param Object：扁平化参数对象，支持解析对象的属性做为QueryString的参数schema，即 不会额外生成参数名且引用一个对象，而是直接unwrap
	- 全局开启：`springdoc.default-flat-param-object`
		- 需要注意被忽视的情况，如`@RequestBody`、请求响应等对象
		- 如果需要添加忽视类，根据`DelegatingMethodParameter#customize`，可以调用`AbstractRequestService#addRequestWrapperToIgnore`
	- 部分开启：`@ParameterObject`，推荐
		- 注意
		- 根据`DelegatingMethodParameter#customize`，`@ParameterObject`是调用MethodParameter#hasParameterAnnotation，因此不是用AnnotatedElementUtils，但是对参数类用AnnotatedElementUtils，因此如果要用AnnotatedElementUtils机制，就注解在类上
# 自定义

## ParameterCustomizer：自定义参数
```java
public class EnumParameterCustomizer implements ParameterCustomizer {  
  @Override  
  public Parameter customize(Parameter parameterModel, MethodParameter methodParameter) {  
    ParameterEnum parameterEnum = methodParameter.getParameterAnnotation(ParameterEnum.class);  
    if (parameterEnum == null || !Enum.class.isAssignableFrom(parameterEnum.value())) {  
      return parameterModel;  
    }  
    if(  
        //  
        !methodParameter.hasParameterAnnotation(io.swagger.v3.oas.annotations.Parameter .class)  
        /**  
         * 配合自定义的ModelConverter，可以不理会是否是schemaProperty，但是PropertyCustomizer则不行，  
         * 其Springdoc机制的PropertyCustomizingConverter则会检查。  
         * 因为各使用各的比较好（Parameter自己解析，Property自己解析），因此这里添加这个条件  
         * （当然也可以直接setEnumDoc然后拼接description，其他情况就不要了）  
         */  
     || StringUtils.isBlank(parameterModel.getSchema().getDescription())  
    ){  
      ParameterEnumModelConverter.setEnumDoc(parameterModel.getSchema(), parameterEnum, (desc)->{  
        if(StringUtils.isBlank(parameterModel.getDescription())  
            || StringUtils.equals(parameterModel.getDescription(), parameterModel.getSchema().getDescription())){  
          parameterModel.setDescription(desc);  
        }else{  
          parameterModel.setDescription(parameterModel.getDescription() + ", " + desc);  
        }  
      });  
      return parameterModel;  
    }  
    /**  
     * Parameter的schema为空（不是用schema注解，没有设置schema属性）时，在AbstractRequestService#build中  
     * 调用AbstractRequestService#buildParams才会解析schema，  
     * 从而使用ParameterEnumModelConverter构建枚举描述和值（此时就不需要重复构建枚举信息了）。  
     * 另外：使用 @Parameter 才正确设置了类型，否则都是string（或者手动指定了schema的类型声明）  
     */  
    parameterModel.setDescription(StringUtils.isBlank(parameterModel.getDescription()) ?  
        parameterModel.getSchema().getDescription()  
        : parameterModel.getDescription() + ", " + parameterModel.getSchema().getDescription());  
    return parameterModel;  
  }  
}
```


## PropertyCustomizer 自定义schema属性

- 仅仅只是被 PropertyCustomizingConverter 使用，和自己自定义ModelConverter是一样的
- ModelConverter添加方法：`ModelConverters.getInstance()` 或者 一个bean

## ReturnTypeParser
- 自定义返回类型的解析
```java
/**  
 * 解构目标类型，如 Flux<ServerSentEvent<Data>>, noWrapClassList包含Flux、ServerSentEvent，就解构为Data  
 */public class UnWrapReturnTypeParser implements ReturnTypeParser {  
  private final List<Class> noWrapClassList;  
  
  public UnWrapReturnTypeParser(List<Class> noWrapClassList) {  
    this.noWrapClassList = noWrapClassList;  
  }  
  
  @Override  
  public Type getReturnType(MethodParameter methodParameter) {  
    Type genericParameterType = methodParameter.getGenericParameterType();  
    if (genericParameterType instanceof ParameterizedType){  
      Type targetType = genericParameterType;  
      while (true){  
        Class<?> rowType =(Class<?>) ((ParameterizedType) targetType).getRawType();  
        if(noWrapClassList.stream().noneMatch(e-> e.isAssignableFrom(rowType))){  
          break;  
        }  
        targetType = ((ParameterizedType) targetType).getActualTypeArguments()[0];  
      }  
      return ReturnTypeParser.resolveType(targetType, methodParameter.getContainingClass());  
    }  
    return methodParameter.getParameterType();  
  }  
}
```
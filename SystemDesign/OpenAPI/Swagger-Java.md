# BUG
## 自定义泛型SchemaId名

- 原：`ExampleFooBar`
- 改：`Example<Foo<Bar>>`


```java
/**  
 * 更新版本可能有  GenericTypeNamingStrategy  
 * @param environment  
 */  
@Resource  
public void setModelConverters(Environment environment){  
  ModelConverters modelConverters = ModelConverters.getInstance();  
  modelConverters.removeConverter(modelConverters.getConverters().get(0));  
  modelConverters.addConverter(new ModelResolver(Json.mapper(), new TypeNameResolver() {  
    @Override  
    protected String nameForGenericType(JavaType type, Set<Options> options) {  
      String baseName = this.nameForClass(type, options);  
      int count = type.containedTypeCount();  
  
      List<String> genericNames = new ArrayList<>();  
      for (int i = 0; i < count; ++i) {  
        JavaType arg = type.containedType(i);  
        String argName = PrimitiveType.fromType(arg) != null ? this.nameForClass(arg, options)  
            : this.nameForType(arg, options);  
        genericNames.add(WordUtils.capitalize(argName));  
      }  
      String generic = genericNames.stream().collect(Collectors.joining(", ", "<", ">"));  
      return baseName + generic; // will return "Example<Foo, Bar>, Example<Foo<Bar>>"  
    }  
  }));  
}
```


## 无法解析泛型

https://github.com/swagger-api/swagger-core/issues/3323#issuecomment-1562455219

- `http://localhost:18090/v3/api-docs/`：直接用这个有问题，方法返回值仅解析了1级泛型
- `http://localhost:18090/v3/api-docs/路由与认证模块`：用这个分组则没有问题


```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Resp<T> {
    @Schema(description = "0: ok; 1: failed")
    private int code;

    @Schema(description = "ok or failed")
    private String msg;

    @Schema(description = "data", nullable = true)
    private T data;
}

@Configuration
public class OpenApiConfig {

    private Map<String, Schema> respSchemas = new ConcurrentHashMap<>();

    @Bean
    public OpenApiCustomiser addGenericSchemaToOpenApi() {
        return openApi -> {
            Map<String, Schema> schemas = openApi.getComponents().getSchemas();

            Set<String> shouldRemoveRespSchemas = schemas.entrySet()
                    .stream()
                    .filter(kv -> {
                        if (!kv.getKey().startsWith(Resp.class.getSimpleName())) {
                            return false;
                        }
                        Map fieldsProperties = kv.getValue().getProperties();
                        Field[] respFields = Resp.class.getDeclaredFields();
                        if (fieldsProperties.size() != respFields.length) {
                            return false;
                        }

                        Set<String> respFieldSet = Arrays.stream(respFields)
                                .map(Field::getName)
                                .collect(Collectors.toSet());

                        if (Sets.intersection(fieldsProperties.keySet(), respFieldSet).size() != respFields.length) {
                            return false;
                        }
                        return true;
                    })
                    .map(Entry::getKey)
                    .collect(Collectors.toSet());

            shouldRemoveRespSchemas.forEach(schemas::remove);
            schemas.putAll(respSchemas);
        };
    }

    @Bean
    public OperationCustomizer customize() {
        // 1. collect RespXxx
        // 2. replace $ref RespXxx to Resp<Xxx>

        return (operation,method) -> {
            ApiResponses responses = operation.getResponses();
            if (method.getMethod().getReturnType().equals(Resp.class)) {

                ResolvedSchema baseRespSchema = ModelConverters.getInstance()
                        .resolveAsResolvedSchema(new AnnotatedType(Resp.class));

                Map<String, Schema> fieldsSchema = Maps.newLinkedHashMap();
                fieldsSchema.putAll(baseRespSchema.schema.getProperties());

                Class actualTypeArgument = (Class) ((ParameterizedTypeImpl) method.getMethod()
                        .getGenericReturnType()).getActualTypeArguments()[0];
                ResolvedSchema resolvedSchema = ModelConverters.getInstance()
                        .resolveAsResolvedSchema(new AnnotatedType(actualTypeArgument));
                String respSchemaName;
                if (resolvedSchema.schema != null) {
                    // override data field schema
                    if (resolvedSchema.referencedSchemas.isEmpty()) {
                        fieldsSchema.put("data", resolvedSchema.schema);
                    } else {
                        fieldsSchema.put("data", new ObjectSchema().$ref(actualTypeArgument.getSimpleName()));
                    }

                    respSchemas.putAll(resolvedSchema.referencedSchemas);

                    respSchemaName = "Resp<" + actualTypeArgument.getSimpleName() + ">";
                } else {
                    // override data field schema
                    Schema originDataSchema = fieldsSchema.get("data");
                    fieldsSchema.put("data", new MapSchema()
                            .description(originDataSchema.getDescription())
                            .nullable(originDataSchema.getNullable()));

                    respSchemaName = "Resp<Map>";
                }

                Schema schema = new ObjectSchema().type("object")
                        .properties(fieldsSchema)
                        .name(respSchemaName);

                // // replace ref '#/components/schemas/RespXxx' to '#/components/schemas/Resp<Xxx>'
                for (ApiResponse apiResponse : responses.values()) {
                    for (MediaType mediaType : apiResponse.getContent().values()) {
                        Schema originApiResponseSchema = mediaType.getSchema();
                        if (originApiResponseSchema.get$ref() != null
                                && originApiResponseSchema.get$ref().startsWith("#/components/schemas/Resp")) {
                            originApiResponseSchema.$ref(schema.getName());
                        }
                    }
                }

                respSchemas.put(respSchemaName, schema);
            }

            return operation;
        };
    }
}
```

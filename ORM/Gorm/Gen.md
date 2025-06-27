- http://gorm.io/gen/
# gen.Config

```go
type Config struct {
    db *gorm.DB   // 设置方式: UseDB(db)

	OutPath      string // 输出目录
	OutFile      string // 通用查询入口，有一个Q对象字段是所有表（简化query）, default: gen.go
	ModelPkgPath string // model目录路径，和OutPath处于同一目录，设置了才会生成model
    
	WithUnitTest bool   // 给所有生成的查询生成测试代码，但是基本无用，生成的动态SQL的测试简直太无用了

	// generate model global configuration
	FieldNullable     bool // 为nullable字段生成指针类型，包括主键
	FieldCoverable    bool // 在Create赋值default, 但是好像没有
	FieldSignable     bool // 使用signable类型
	FieldWithIndexTag bool // generate with gorm index tag
	FieldWithTypeTag  bool // generate with gorm column type tag

	Mode GenerateMode
    //gen.WithDefaultQuery 生成Q、表全局变量，但仍然需要调用SetDefault方法传递DB
    //gen.WithQueryInterface 动态SQL
    //gen.WithoutContext 不知道有什么，用了好像也没有区别

	queryPkgName   string // generated query code's package name
	modelPkgPath   string // model pkg path in target project
	dbNameOpts     []model.SchemaNameOpt
	importPkgPaths []string

	// name strategy for syncing table from db
	tableNameNS func(tableName string) (targetTableName string)
	modelNameNS func(tableName string) (modelName string)
	fileNameNS  func(tableName string) (fileName string)

	dataTypeMap    map[string]func(columnType gorm.ColumnType) (dataType string)
	fieldJSONTagNS func(columnName string) (tagContent string)

	modelOpts []ModelOpt
}
```

# gen

- features
	- 生成表：`gen.Generator.GenerateModel(tablename, ...)`
	- 生成DAO：`gen.Generator.ApplyBasic`
		- 正向生成：一个对象
			- 需要自己调用  `DB.Migrator().AutoMigrate(Model1{})`同步到数据库 
		- 逆向生成： 使用`gen.Generator.GenerateModel`生成的对象
	- [Methods Template](http://gorm.io/gen/database_to_structs.html#Methods-Template)：为结构体生成方法模板，定义一个结构体+添加属性方法
	- [Field扩展](http://gorm.io/gen/database_to_structs.html#Field-Options)：name、type、tag等
	- [忽视表]()：在直接调用`gen.Generator.GenerateAllTable`时用，调用`gen.Generator.WithTableNameStrategy`返回空字符串
	- [从SQL文件中生成](http://gorm.io/gen/database_to_structs.html#Generate-From-Sql)
	- [动态SQL gen.Generator.ApplyInterface](https://gorm.io/gen/dynamic_sql.html)



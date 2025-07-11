- https://github.com/go-playground/validator
- gin默认的validator


# Custom
```go
if err := validate.RegisterValidation("checkMobile", checkMobile); err != nil {  
    return nil, err  
}

func checkMobile(fl validator.FieldLevel) bool {  
    reg := `^1([38][0-9]|14[579]|5[^4]|16[6]|7[1-35-8]|9[189])\d{8}$`  
    rgx := regexp.MustCompile(reg)  
    return rgx.MatchString(fl.Field().String())  
}
```

# Translate
```go
import (
	"github.com/go-playground/locales/zh"
	"github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	ch_translations "github.com/go-playground/validator/v10/translations/zh"
	"regexp"
	"strings"
)

func TranslateErrors(err validator.ValidationErrors, translator ut.Translator) string {
	var sb strings.Builder
	for _, value := range err.Translate(translator) {
		sb.WriteString(value + "\n")
	}
	return sb.String()
}

// 初始化Validator数据校验
func configureValidator(validate *validator.Validate) (ut.Translator, error) {
	localeZh := zh.New()
	uni := ut.New(localeZh, localeZh)
	translatorZh, _ := uni.GetTranslator(localeZh.Locale())
	if err := ch_translations.RegisterDefaultTranslations(validate, translatorZh); err != nil {
		return nil, err
	}
	return translatorZh, nil
}
```
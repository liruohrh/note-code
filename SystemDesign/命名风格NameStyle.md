-  `snake_case`  蛇形命名法
- `kebab-case` / `dash-style`  烤串命名法 / 短横线风格
-  `camelCase` / `lowerCamelCase` 驼峰命名法 / 小驼峰命名法
-  `PascalCase` / `UpperCamelCase` 帕斯卡命名法 / 大驼峰命名法
-  `SCREAMING_SNAKE_CASE` 全大写蛇形命名法
-  `Capitalized_Snake_Case` 首字母大写蛇形命名法



# 脚本
```js

// 这种 getURLBY=>get,uRLBY，而不是get,uRL,by
function fromPascalCase(name) {
  let tokens = [];
  let token = "";
  for (let i = 0; i < name.length; i++) {
    const code = name.charCodeAt(i);
    if (code >= 65 && code <= 90) {
      const preCode = i - 1 > 0 ? name.charCodeAt(i - 1) : -1;
      const nextCode = i + 1 < name.length ? name.charCodeAt(i + 1) : -1;
      if (
        i != 0 &&
        ((preCode >= 97 && preCode <= 122) ||
          (nextCode >= 97 && nextCode <= 122))
      ) {
        tokens.push(token);
        token = "";
      }
      if (!token) {
        token += name[i].toLowerCase();
      } else {
        token += name[i];
      }
    } else {
      token += name[i];
    }
  }
  tokens.push(token);
  return tokens;
}
```
- [Turbo Impl Native Functions](https://reactnative.cn/docs/turbo-native-modules-introduction)
- [Fabric Impl Native UI View](https://reactnative.cn/docs/fabric-native-components-introduction)

# Turbo
- 使用codegen根据JS/TS接口，在android等目录生成响应的C++、原生接口。
- 注意事项：
	- Module实现功能，Package（原生才有）则进行注册Module
		- 相当于Module是一个JS文件，Package是一个npm包，整体就是引入一个npm包。
	- 自己实现的Package根据传递的name参数（也就是`getEnforcing`函数的name参数）来返回对应的Module
	- Module的name必须以Native开头

## Codegen 支持的 TS 类型（简略表）

| TS 类型                         | 是否支持 | 说明                 |
| ----------------------------- | ---- | ------------------ |
| `number`, `string`, `boolean` | ✅    | 基础类型               |
| `void`, `Promise<T>`          | ✅    | 支持异步调用             |
| `{ [key: string]: string }`   | ✅    | 可用作 object map     |
| `Map<K, V>`                   | ❌    | 不支持                |
| `Record<string, string>`      | ❌    | 和 Map 一样也不支持       |
| 自定义 alias + object            | ✅    | 可以手动定义 alias 类型再使用 |
## 实现
### 1. JS/TS接口

```ts
import { TurboModule, TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
  hello(): string;
  asyncHello(): Promise<string>;
}

export default TurboModuleRegistry.getEnforcing<Spec>(
  "NativeDemoTurbo"
) as Spec;
```

- 这个导出default就是这个Spec接口
- `import NativeDemoTurbo from "@/specs/NativeDemoTurbo"`
- `NativeDemoTurbo.hello("xxx")`

### 2. package.json配置Codegen
```json
{
	"codegenConfig": {
		//生成的接口名
	    "name": "NativeDemoTurboSpec",
	    "type": "modules",
	    //JS Spec代码目录
	    "jsSrcsDir": "specs",
	    //对android进行其他配置
	    "android": {
	      "javaPackageName": "io.github.liruohrh"
	    }
	}
}
```


### 3. 执行Codegen代码生成
- `cd android && ./gradlew generateCodegenArtifactsFromSchema`
	- `android\app\build\generated\source\codegen`：有java（原生代码）、jni（C++代码）、schema.json（Module的Schema）
	- 不推荐也没必要修改生成的代码，修改自己的实现即可
- `cd ios && bundle install && bundle exec pod install`  

### 4. 在原生实现
- 直接用各自IDE打开android/ios目录
- 

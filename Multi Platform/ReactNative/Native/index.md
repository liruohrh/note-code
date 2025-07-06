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

| TS 类型                         | 是否支持 | 说明                 |     |
| ----------------------------- | ---- | ------------------ | --- |
| `number`, `string`, `boolean` | ✅    | 基础类型               |     |
| `void`, `Promise<T>`          | ✅    | 支持异步调用             |     |
| `{ [key: string]: string }`   | ✅    | 可用作 object map     |     |
| `Map<K, V>`                   | ❌    | 不支持                |     |
| `Record<string, string>`      | ❌    | 和 Map 一样也不支持       |     |
| 自定义 alias + object            | ✅    | 可以手动定义 alias 类型再使用 |     |

- Promise：和JS一样，resolve是成功，reject则是拒绝，但是reject有很多签名，
	- reject的error是这么一个对象
		- message：message参数，如果console.log会得到 `{异常类型}: {message}`，toString也是
		- code：code参数
		- nativeStackAndroid：传递的异常的
		- name：异常类型名
		- userInfo：传递的userInfo

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
- 生成的原生接口名就是这个文件名+Spec，`getEnforcing`传递的name就是`BaseReactPackage#getModule`时传递的name

### 2. package.json配置Codegen
```json
{
	"codegenConfig": {
		//配置名，影响android\app\build\generated\source\codegen\jni下的目录、文件名
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
- 直接用各自IDE打开android/ios目录，编写Spec的实现Module以及Package
- 推荐新建简单的React Native项目来完成，这样就不需要加载一大堆无用module。

# 意义
旨在分离视图逻辑与业务逻辑
# 对照类组件
- useState：
	- 类组件state的一个属性
	- 所有返回的set方法都是调用类组件的setState方法更新state的一个属性
- useEffect：
	- componentDidMount是effect函数
	- componentDidUpdate是deps更新时执行的effect函数
	- componentWillUnmount是useEffect的cleanup函数
- useRef：把一个值直接作为组件的属性
	- 因此不像state一样会随着值更新而重新渲染

# Hook
## useState
```ts
function useState<S>(initialState: S | (() => S)): [S, Dispatch<SetStateAction<S>>]

type Dispatch<A> = (value: A) => void;
type SetStateAction<S> = S | ((prevState: S) => S);
```
- 不会自动合并属性或者元素
- 返回的第二个元素是一个函数，俗称updater函数，这个函数是稳定的，一个纯函数，因此不需要把对应状态加入根据依赖变化的函数依赖中
## useEffect
```ts
function useEffect(effect: EffectCallback, deps?: DependencyList): void;

type EffectCallback = () => void | Destructor;
type Destructor = () => void | { [UNDEFINED_VOID_ONLY]: never };
declare const UNDEFINED_VOID_ONLY: unique symbol;
type DependencyList = readonly unknown[];
```

- effect：通常忽视`{ [UNDEFINED_VOID_ONLY]: never }`即可，只需要知道cleanup函数的类型是`() => void`即可
- deps
	- 值是空或者deps元素引用改变时，就会重新渲染，即componentDidUpdate
	- 而值是空数组当然就是表示仅在组件挂载时（componentDidMount）执行

### 体验cleanup函数的重要性
- [https://zh-hans.react.dev/reference/react/useEffect#fetching-data-with-effects](https://zh-hans.react.dev/reference/react/useEffect#fetching-data-with-effects)

```ts
useEffect(() => {
  let ignore = false;
  setBio(null);
  fetchBio(person).then(result => {
    if (!ignore) {
      setBio(result);
    }
  });
  return () => {
    ignore = true;
  };
}, [person]);
```

- 这个例子不仅展示useEffect用法，还说明了返回cleanup函数的重要性

- 如果person连续更新，那么会发送多个请求，但是请求的响应不会按照请求的序列排序
- 导致状态bio不是以请求的序列被使用，可能先用后面的请求的结果，再用前面请求的结果
- 其实要是不这么写，就是没把网络请求当作一个资源，网络请求在`useEffect`当然也是一个资源，需要释放

- fetch请求的取消方法

- 就像上面一样，用一个bool标记
- signal：这个需要注意，这么做的话就必须得在then中处理响应
## useRef
```ts
function useRef<T>(initialValue: T): MutableRefObject<T>;
function useRef<T = undefined>(initialValue?: undefined): MutableRefObject<T | undefined>;
interface MutableRefObject<T> {
	current: T;
}

function useRef<T>(initialValue: T | null): RefObject<T>;
interface RefObject<T> {
	readonly current: T | null;
}

```

## 自定义自己写的组件的Ref
```tsx
//T ref接口，P组件属性
function forwardRef<T, P = {}>(
	render: ForwardRefRenderFunction<T, PropsWithoutRef<P>>,
): ForwardRefExoticComponent<PropsWithoutRef<P> & RefAttributes<T>>;


forwardRef<RefInterface, Props>((props, ref)=>{});


//ref和useCallback等一样可以有依赖
function useImperativeHandle<T, R extends T>(
ref: Ref<T> | undefined, 
init: () => R, deps?: DependencyList
): void;
useImperativeHandle(ref, ()=>({}), []);


```


## useMemo
```ts
function useMemo<T>(factory: () => T, deps: DependencyList): T;
```
- memo就是Memoized
- 缓存工厂函数返回的值
- 注意
	- React规范：useMemo仅用于缓存值，而用useCallback缓存函数
	- 如果缓存的值反复变化，也就没了缓存的意义，还额外消耗了性能，如果是缓存函数，则更是，因为这个函数无论如何都是会创建的，只不过是让引用一样，避免作为某个依赖而反复执行或者作为子组件依赖而反复渲染
	- 如果在工厂函数中使用了状态，则需要依赖状态，如果只是使用setState或者在setState中访问这个状态，则不需要
	- 如果使用了ref，则不需要依赖，因为访问的一直是ref的最新值
## memo缓存组件
```ts
function memo<P extends object>(
	Component: FunctionComponent<P>,
	propsAreEqual?: (prevProps: Readonly<P>, nextProps: Readonly<P>) => boolean,
): NamedExoticComponent<P>;
```
- https://zh-hans.react.dev/reference/react/useMemo#skipping-re-rendering-of-components
- 当函数组件属性变时，会重新渲染
- 默认是浅值比较，可以传递自定义比较函数
- 和key的效果差不多
- useMemo、useCallback用于把缓存的值传递给这个memo组件，如果不是，则无任何意义，直接使用状态更新或者定义函数（无论是否依赖状态）才是更好的选择


## useCallback
```ts
function useCallback<T extends Function>(callback: T, deps: DependencyList): T;
```
- useMemo的丐版，仅用来缓存函数
- 实现目的主要是为了让缓存函数和缓存值区分开来


## useContext
```ts
function useContext<T>(context: Context<T> /*, (not public API) observedBits?: number|boolean */): T;


//首先肯定得是先创建Context
function createContext<T>(
	defaultValue: T,
): Context<T>;
interface Context<T> {
	Provider: Provider<T>;
	Consumer: Consumer<T>;
	displayName?: string | undefined;
}
```
- context仅把数据传递给子组件
- useContext仅从祖先组件中取context

### 例子

```ts
const ThemeContext = createContext(null);

export default function MyApp() {
  return (
    <ThemeContext.Provider value="dark">
      <Form />
    </ThemeContext.Provider>
  )
}

function Form() {
  return (
    <Panel title="Welcome">
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}
```

# 自定义Hook
- https://zh-hans.react.dev/learn/reusing-logic-with-custom-hooks
- 大致来说，就是最新use前缀命名即可，像正常一样在自定义Hook中使用hook。


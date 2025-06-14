

# Pan

```ts
export type PanGestureHandlerEventPayload = {
	//最近一次，相对于绑定的视图（左上角）
    x: number;
    y: number;
    //最近一次，相对于窗口（左上角）
    absoluteX: number;
    absoluteY: number;
    //从触摸开始累计的，相对于绑定的视图
    translationX: number;
    translationY: number;
    //当前速度
    velocityX: number;
    velocityY: number;
    //
    stylusData: StylusData | undefined;
};
export type PanGestureChangeEventPayload = {
	//与上一次触摸点相比
    changeX: number;
    changeY: number;
};
```
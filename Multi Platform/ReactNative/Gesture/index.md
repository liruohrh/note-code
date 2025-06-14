
# 触摸
```ts
export interface NativeTouchEvent {
  /**
   * Array of all touch events that have changed since the last event
   */
  changedTouches: NativeTouchEvent[];
  /**
   * The ID of the touch
   */
  identifier: string;
  //触摸点相对于元素
  locationX: number;
  locationY: number;
  //触摸点相对于屏幕
  pageX: number;
  pageY: number;
  /**
   * The node id of the element receiving the touch event
   */
  target: string;
  /**
   * A time identifier for the touch, useful for velocity calculation
   */
  timestamp: number;
  /**
   * Array of all current touches on the screen
   */
  touches: NativeTouchEvent[];
  /**
   * 3D Touch reported force
   * @platform ios
   */
  force?: number | undefined;
}
```


# Pan
- PanResponder
- 注意：PanResponderGestureState在直接console.log 对象时，所以属性基本总是0，需要console.log属性才不是0

```ts
export interface PanResponderGestureState {
  /**
   *  ID of the gestureState- persisted as long as there at least one touch on
   */
  stateID: number;
  
  //最近一次，相对于屏幕
  moveX: number;
  moveY: number;
  //手势开始时的，相对于屏幕
  x0: number;
  y0: number;
  //从触摸开始累计的，相对于绑定的视图
  dx: number;
  dy: number;
  //velocity, 速度
  vx: number;
  vy: number;
  /**
   * Number of touches currently on screen
   */
  numberActiveTouches: number;
  // All `gestureState` accounts for timeStamps up until:
  _accountsForMovesUpTo: number;
}
```
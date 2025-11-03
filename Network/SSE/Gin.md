- 注意事项
	- 不能返回，必须阻塞handler
	- 写完数据必须手动c.Writer.Flush，否则不会立刻进行响应

```go
func SSEHandler(c *gin.Context) {  
    ssex.Manager.AddConnect(c)  
}


package ssex  
  
import (  
    "fastgin/boost/config"  
    "fastgin/common/constant"    "fastgin/common/httpz"    "fmt"    "github.com/gin-contrib/sse"    "github.com/gin-gonic/gin"    "github.com/samber/lo"    "net/http"    "sync"    "time")  
  
var Manager *ConnectManager  
  
func Init() {  
    Manager = &ConnectManager{  
       store: NewMutexMap[string, *Context](),  
    }  
}  
  
type MutexMap[K comparable, V any] struct {  
    m  map[K]V  
    sm sync.Mutex  
}  
  
func NewMutexMap[K comparable, V any]() *MutexMap[K, V] {  
    return &MutexMap[K, V]{  
       m:  make(map[K]V),  
       sm: sync.Mutex{},  
    }  
}  
  
func (t *MutexMap[K, V]) Set(k K, v V) {  
    t.sm.Lock()  
    defer t.sm.Unlock()  
    t.m[k] = v  
}  
func (t *MutexMap[K, V]) Delete(k K) {  
    t.sm.Lock()  
    defer t.sm.Unlock()  
    delete(t.m, k)  
}  
func (t *MutexMap[K, V]) GetWith(k K, f func(v V, ok bool)) {  
    t.sm.Lock()  
    defer t.sm.Unlock()  
    v, ok := t.m[k]  
    f(v, ok)  
}  
func (t *MutexMap[K, V]) Keys() []K {  
    t.sm.Lock()  
    defer t.sm.Unlock()  
    return lo.Keys(t.m)  
}  
func (t *MutexMap[K, V]) Len() int {  
    t.sm.Lock()  
    defer t.sm.Unlock()  
    return len(t.m)  
}  
  
type ConnectManager struct {  
    store *MutexMap[string, *Context]  
}  
  
type Context struct {  
    ginc *gin.Context  
    ch   chan sse.Event  
}  
  
func (t *ConnectManager) AddConnect(c *gin.Context) {  
    var err error  
    _, ok := c.Writer.(http.Flusher)  
  
    if !ok {  
       httpz.ServerError(c, "not support sse")  
       return  
    }  
  
    c.Header("Content-Type", sse.ContentType)  
    c.Header("Cache-Control", "no-cache")  
    c.Header("Connection", "keep-alive")  
    c.Header("Access-Control-Allow-Origin", "*")  
  
    key := fmt.Sprintf("%v", c.MustGet(constant.KeyUid))  
    ch := make(chan sse.Event, 5)  
    t.store.Set(key, &Context{ginc: c, ch: ch})  
  
    c.Render(-1, &Heartbeat{})  
    if c.IsAborted() {  
       err = fmt.Errorf("ssex send data: %s", c.Errors.String())  
       config.Log.Error(err)  
       httpz.ServerError(c, err.Error())  
       return  
    }  
    c.Writer.Flush()  
    ticker := time.NewTicker(time.Second * 30)  
    defer func() {  
       t.store.Delete(key)  
    }()  
    for {  
       select {  
       case <-c.Request.Context().Done():  
          return  
       case e := <-ch:  
          c.Render(-1, e)  
          if c.IsAborted() {  
             err = fmt.Errorf("ssex send data: %s", c.Errors.String())  
             config.Log.Error(err)  
             return  
          }  
          c.Writer.Flush()  
       case <-ticker.C:  
          c.Render(-1, &Heartbeat{})  
          if c.IsAborted() {  
             err = fmt.Errorf("ssex send data: %s", c.Errors.String())  
             config.Log.Error(err)  
             return  
          }  
          c.Writer.Flush()  
       }  
    }  
}  
func (t *ConnectManager) HasConnects() bool {  
    return t.store.Len() > 0  
}  
  
func (t *ConnectManager) Broadcast(s sse.Event) {  
    for _, k := range t.store.Keys() {  
       t.store.GetWith(k, func(v *Context, ok bool) {  
          if !ok {  
             return  
          }  
          v.ch <- s  
       })  
    }  
}  
  
type Heartbeat struct{}  
  
func (t *Heartbeat) Render(w http.ResponseWriter) error {  
    _, err := w.Write([]byte(": ping\n\n"))  
    return err  
}  
  
var contentType = []string{sse.ContentType}  
var noCache = []string{"no-cache"}  
  
func (t *Heartbeat) WriteContentType(w http.ResponseWriter) {  
    header := w.Header()  
    header["Content-Type"] = contentType  
  
    if _, exist := header["Cache-Control"]; !exist {  
       header["Cache-Control"] = noCache  
    }  
}
```
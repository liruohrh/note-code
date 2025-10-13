# 路径类型
- static，静态路径：`/xxx`
- param，参数wildcard路径：`/:id  c.Param("id")` 
- catchall，wildcard路径：`/*id  c.Param("id")`
- 遵循最短路径匹配原则


#  路由解析
```go
type node struct {
	path      string //param、wildcard前的路径或者param、wildcard路径，如:id
	indices   string //wildcard是/，一般都是path的下一个字符
	wildChild bool   //子节点有param、wildcard
	nType     nodeType //root、static、param、catchall
	priority  uint32
	children  []*node 
	handlers  HandlersChain
	fullPath  string // 路由定义时的值
}
```
- root的fullPath=/，而其path则是最长相同路径

```go
// addChild will add a child node, keeping wildcardChild at the end
func (n *node) addChild(child *node)
```
- wildcard总是最后一个

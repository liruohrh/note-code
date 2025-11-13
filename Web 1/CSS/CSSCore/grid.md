- https://blog.csdn.net/weixin_43288600/article/details/146219663
```css
.g {
display: grid;
//间隙
gap: 2px;
// 2列，每列宽度，fr(占比)
grid-template-columns: 50px 1fr 2fr;  
// 4列
grid-template-columns: repeat(4, 50px); 
// auto-fill：单元格固定w，自动填充
// auto-fit：同auto-fill，但只有一行时会尽可能撑大单元格的w
grid-template-columns: repeat(auto-fill, 50px); 
//同grid-template-columns，每行高度
grid-template-rows:;

}
```
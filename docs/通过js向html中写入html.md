## 通过js向html中写入html

两种方法:document.write 和 innerHTML

法一：document.write() 该方法便于将字符串插入到文档中。

```javascript
document.write("<p>Hello World!</p>");
```

这种方法不易于阅读和编辑，无法满足行为与结构分离的要求。

法二：innerHTML

```html
<div id="testdiv">
</div>
```



```javascript
<script type="text/javascript">
var divP = document.getElementById("testdiv");
divP.innerHTML = "<p style='color: red;'>This is my blog.</p>"  
</script>

```

这方法支持读写，只要读取到元素的位置，就可以将内容写进元素中，但是如果原来的元素中已经有内容了，这个属性将替换掉原来的属性。
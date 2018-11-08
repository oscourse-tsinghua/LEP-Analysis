## 简介

可缩放矢量图形（SVG，Scalable Vector Graphics)是基于XML语法的图像格式，属于基于矢量的图形家族。其他图像格式（例如，JPEG,GIF和PNG）属于基于光栅的图形家族，即在一个数据数组中存储每个像素的颜色定义。

相对于基于光栅的图形格式，SVG具有以下优势：

- SVG图形是使用数学公式创建的，需要源文件中存储的数据少，因为无需存储每个独立像素的数据；
- 矢量图形可更好缩放；
- 源文件小；
- SVG的源文件是一个文本文件，具有易于访问和搜索引擎的友好特征；

## 向网页中添加SVG XML

创建SVG XML后，可采用多种方式将其包含在HTML中。

第一种方式：直接将SVG XML 嵌入到HTML文档中。

```h&#39;t&#39;m
<html>
     <head>
             <title>SVG</title>
     </head>
     <body style="height: 600px;width: 100%; padding: 30px;">
              <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                    <circle cx="100" cy="50" r="40" fill="blue"/>
              </svg>
     </body>
</html>
```

优点：简单

缺点：不支持重用

第二种方式：适用于将SVG XML保存在.svg文件中，可采用<embed>、<object>、<iframe>元素将其包含在网页中。

使用<embed>元素包含一个SVG XML文件：

```html
<embed src="circle.svg" type="image/svg+xml" />
```

使用<object>元素包含一个SVG XML文件：

```html
<object data="circle.svg" type="image/svg+xml"></object>
```

使用<iframe>元素包含一个SVG XML文件：

```html
<iframe src="circle.svg" ></iframe>
```


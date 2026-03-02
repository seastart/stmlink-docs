## 函数说明
渲染对象虚对象，提供渲染数据回调与渲染句柄设置

可以通过继承此类来接受sdk 渲染数据的回调，更好的和ui进行代码编写和绘制ui

当然也可以通过设置hwnd 的方式，将窗口句柄设置到sdk内，sdk 会根据电脑支持的最优渲染方式进行渲染。 

## 继承关系


## 函数方法
### 获取渲染类型
```cpp
virtual ViewEnumType ViewType() = 0;
```

**返回值**

| ViewEnumType | 渲染类型：<br/>Hwnd 通过hwnd 进行渲染， sdk 内将使用此函数内getHwnd ,将对应的数据渲染到hwnd 上。<br/>CallBack 通过yuv 回调进行渲染。sdk 通过此类中的updatePlanes与updateFull进行数据回调，上层实现数据的渲染（推荐） |
| --- | --- |




### 获取句柄对象
```cpp
virtual void* getHwnd() = 0;
```

**返回值**

| void | 渲染句柄 |
| --- | --- |


<font style="color:#DF2A3F;">注：仅再ViewType() 返回HWND 生效</font>



### 渲染数据
```cpp
virtual void updatePlanes(const unsigned char* buf, int w, int h, int fourcc, int label) = 0;
```

**参数**

| buf | const unsigned char* | 渲染数据 |
| --- | --- | --- |
| w | int | 数据宽度 |
| h | int | 数据高度 |
| fourcc | int | 数据类型，0：yuv420 |
| label | int | 数据角度 |


<font style="color:#DF2A3F;">注：仅再ViewType() 返回CallBack 生效</font>



### 渲染固定RGB颜色
```cpp
virtual void updateFull(int r, int g, int b) = 0;
```

**参数**

| r | int | 红颜色（0-255） |
| --- | --- | --- |
| g | int | 绿颜色（0-255） |
| b | int | 蓝颜色（0-255） |


<font style="color:#DF2A3F;">注：仅再ViewType() 返回CallBack 生效</font>


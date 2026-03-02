# 远程依赖
<font style="color:rgb(38, 38, 38);">在根目录下的 build.gradle 中，添加 maven</font>

```plain
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```



在app目录下的build.gradle中添加依赖

```plain

	dependencies {
    implementation 'cn.seastart.meeting:meeting:xxx'
	}
```


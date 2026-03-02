这是一个集成web SDK基于 Vue 3 + TypeScript + Vite 构建的视频会议系统web端项目。

github源码地址：[https://github.com/seastart/meeting-web-demo](https://github.com/seastart/meeting-web-demo)

# 项目介绍
## 项目技术栈
+ Vue 3
+ TypeScript
+ Vite
+ Element Plus
+ Pinia
+ Vue Router
+ SCSS

## 项目结构
```plain
├── src/                    # 源代码目录
│   ├── api/               # API 接口定义
│   ├── assets/            # 静态资源文件
│   ├── components/        # 公共组件
│   ├── directives/        # Vue 自定义指令
│   ├── hooks/             # Vue 组合式函数
│   ├── router/            # 路由配置
│   ├── sdk/               # SDK 相关代码
│   ├── stores/            # Pinia 状态管理
│   ├── styles/            # 全局样式文件
│   ├── types/             # TypeScript 类型定义
│   ├── utils/             # 工具函数
│   ├── views/             # 页面视图组件
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口文件
├── public/                # 公共静态资源
├── doc/                   # 项目文档
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── vite.config.ts         # Vite 配置文件
└── package.json           # 项目依赖配置
```

## 主要文件说明
### 配置文件
+ `package.json`: 项目依赖和脚本配置
+ `vite.config.ts`: Vite 构建工具配置
+ `tsconfig.json`: TypeScript 配置
+ `.env.development`: 开发环境变量
+ `.env.production`: 生产环境变量

### 源码目录
+ `src/api/`: 存放后端 API 接口调用相关代码
+ `src/components/`: 可复用的 Vue 组件
+ `src/directives/`: Vue 自定义指令
+ `src/hooks/`: Vue 组合式函数（Composables）
+ `src/router/`: 路由配置和路由守卫
+ `src/sdk/`: 会议 SDK 相关的封装代码
+ `src/stores/`: Pinia 状态管理存储
+ `src/utils/`: 工具函数和通用方法
+ `src/views/`: 页面级组件

## 开发命令
```bash
# 安装依赖
npm install

# 开发环境运行
npm run dev

# 构建生产版本
npm run build

# 代码格式化
npm run format

# 类型检查
npm run type-check
```

# 页面功能介绍
## 登录页
```plain
├── login/                	
│   ├── cpn/ 
│      ├── Login.vue     #登录页组件
│      ├── Register.vue 	#注册页组件
│   ├── index.vue       #登录入口

```

![](images/339904_1736926098475-78d5f4b6-14de-4e1c-84ab-ea41db0c02ee.png)

## 首页
```plain
├── home/                	
│   ├── cpn/ 
│      ├── AppointmentMeeting.vue     #预约会议弹窗组件
│      ├── AppointmentResult.vue 			#预约结果弹窗组件
│      ├── Contacts.vue 							#通讯录弹窗组件
│      ├── HistoryMeeting.vue 				#历史会议弹窗组件
│      ├── ImmediateMeeting.vue 			#即时会议弹窗组件
│      ├── JoinMeeting.vue 						#加入会议弹窗组件
│   ├── index.vue       							#首页入口

```

![](images/585166_1732101587454-d92b8903-9808-4eef-9d5f-80512f1b85a6.png)

![](images/174500_1732101675605-22b52baa-b2bb-4d2e-9092-84025871fffa.png)

![](images/250744_1732101695538-3c9d0687-553c-4c8a-a35c-78fadc0e81b6.png)

![](images/156166_1732101668462-2852d607-41ad-40f3-8dbf-4ce212169fe1.png)

![](images/361833_1732101909301-820305a4-18ba-4706-8392-fd94710a7dd4.png)

![](images/226736_1732102028492-c5aa427f-0e2e-4cc0-8893-81c2bc38e940.png)

## 会议
```plain
├── meeting/                	
│   ├── cpn/                 
│      ├── ChatDrawer.vue     			#聊天侧弹窗组件
│      ├── Footer.vue 							#底部操作栏组件
│      ├── LayoutImg.vue 						#显示布局图片组件
│      ├── InviteEnter.vue 					#邀请入会弹窗组件
│      ├── MemberDrawer.vue 				#成员侧弹窗组件
│      ├── Preview.vue 							#大窗口视频预览组件
│      ├── Recording.vue 						#录制组件（左上角显示录制中 00:00:00）
│      ├── RecordLayout.vue 				#设置录制布局、弹窗组件
│   ├── room-content/       
│      ├── gird-view/     		
│      		├── index.vue 						#宫格视图组件
│      ├── size-view/				
│         ├── index.vue 						#大小画面视图组件
│         ├── SizeBr7.vue 					#下L型布局视图组件
│         ├── SizeRight4.vue 				#右侧小窗口视图组件
│         ├── SizeTl7.vue 					#上L型布局视图组件
│         ├── SizeTop4.vue 					#顶部小窗口视图组件
│      ├── index.vue 								#内容组件
│      ├── MeItem.vue 							#自己窗口组件
│      ├── UserItem.vue 						#成员窗口组件
│      ├── OtherShareScreen.vue 		#接收其他人共享组件
│      ├── MixMode.vue 							#合成模式组件
│   ├── room-top/       
│      ├── index.vue								#顶部组件	 	 		
│   ├── index.vue       						#会议入口

```

![](images/205598_1736933056295-99b52537-008f-4354-a4f8-4e4b1de44c6d.png)

![](images/853936_1732102177269-4924f98b-e350-4abc-9550-603146082f73.png)

![](images/142306_1732104234585-158f0676-dd4c-4a40-9337-ce9ff25efb85.png)

![](images/542183_1737027322416-21c1c872-af73-4fa4-95ff-5abbd91e0540.png)

![](images/492173_1737027341947-3147d60e-ad61-4ff7-a3b9-f8ba68832292.png)

![](images/165214_1732102272627-6702293b-ffac-4c6f-8476-124cc544762a.png)

## 布局展示
### 自动布局
![](images/753355_1736942788198-38d240e8-5a2d-4cbd-b72a-7da48ebfd34f.png)

### 全屏
![](images/160811_1736942765548-087bf47d-06cb-43f2-9081-ca426e8bed8f.png)

### 二等分
![](images/120003_1736943008000-25173f0b-0dcd-4524-9c1a-968b68df859f.png)

### 四宫格
![](images/849963_1736943016223-b553c65f-1779-4147-9c9f-3274c07f8907.png)

### 五宫格
![](images/224959_1736943021573-05895627-8f82-414d-9f2b-1795dd302036.png)

### 六宫格
![](images/648114_1736943026553-50f82a28-c52c-4af5-9792-2f1a260b8eff.png)

### 八宫格
![](images/209278_1736943036517-7a3f26bd-16df-4d09-a0e6-cc7d3a26ec92.png)

### 十宫格
![](images/233712_1736943058279-cbdc4959-913f-4ad3-9624-e0617b77e782.png)

### 十二宫格
![](images/287945_1736943077728-435bf505-8366-423e-b58f-0bdc6606bb1f.png)

### 十六宫格
![](images/473032_1736943096169-877d9f77-9dc9-4499-a73f-d48f693d87b9.png)

### 右侧小窗口
![](images/648091_1737017818264-45982e58-89e9-4542-a008-45b9573ed978.png)

### 顶部小窗口![](images/840562_1737017829365-15053ff0-20bc-402c-9206-67d827eaefdc.png)
### 下L型布局
![](images/676110_1737017848599-22056345-7314-430e-b1a3-addf203b8203.png)

### 上L型布局
![](images/132399_1737017863777-0f0fbd63-52dd-4fa5-a46f-413448a50005.png)


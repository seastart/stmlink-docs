---
title: "Web UI SDK integration"
description: "Low-code integration with UI for Web: the open-source SMeeting Web meeting app (Vue 3 + TypeScript + Vite), its tech stack, project structure, dev commands, and the login, home, and meeting pages and layouts. Read this to take the source code, modify the UI, and deploy it yourself."
---

This is the web client project of a video conferencing system that integrates the Web SDK, built with Vue 3 + TypeScript + Vite.

GitHub source code: [https://github.com/seastart/meeting-web-demo](https://github.com/seastart/meeting-web-demo)

## Tech stack
+ Vue 3
+ TypeScript
+ Vite
+ Element Plus
+ Pinia
+ Vue Router
+ SCSS

## Project structure
```text
├── src/                    # Source code directory
│   ├── api/               # API definitions
│   ├── assets/            # Static assets
│   ├── components/        # Shared components
│   ├── directives/        # Vue custom directives
│   ├── hooks/             # Vue composables
│   ├── router/            # Router configuration
│   ├── sdk/               # SDK-related code
│   ├── stores/            # Pinia state management
│   ├── styles/            # Global styles
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Utility functions
│   ├── views/             # Page view components
│   ├── App.vue            # Root component
│   └── main.ts            # App entry file
├── public/                # Public static assets
├── doc/                   # Project documentation
├── .env.development       # Development environment configuration
├── .env.production        # Production environment configuration
├── vite.config.ts         # Vite configuration file
└── package.json           # Project dependency configuration
```

## Key files
### Configuration files
+ `package.json`: project dependencies and script configuration
+ `vite.config.ts`: Vite build tool configuration
+ `tsconfig.json`: TypeScript configuration
+ `.env.development`: development environment variables
+ `.env.production`: production environment variables

### Source directories
+ `src/api/`: code for calling backend APIs
+ `src/components/`: reusable Vue components
+ `src/directives/`: Vue custom directives
+ `src/hooks/`: Vue composables
+ `src/router/`: router configuration and route guards
+ `src/sdk/`: wrapper code for the conferencing SDK
+ `src/stores/`: Pinia state stores
+ `src/utils/`: utility functions and common methods
+ `src/views/`: page-level components

## Dev commands
```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Format code
npm run format

# Type check
npm run type-check
```

## Page features
### Login page
```text
├── login/                	
│   ├── cpn/ 
│      ├── Login.vue     #Login page component
│      ├── Register.vue 	#Registration page component
│   ├── index.vue       #Login entry

```

![](/zh/meeting/ui-sdk/images/339904_1736926098475-78d5f4b6-14de-4e1c-84ab-ea41db0c02ee.png)

### Home page
```text
├── home/                	
│   ├── cpn/ 
│      ├── AppointmentMeeting.vue     #Schedule meeting dialog component
│      ├── AppointmentResult.vue 			#Scheduling result dialog component
│      ├── Contacts.vue 							#Contacts dialog component
│      ├── HistoryMeeting.vue 				#Meeting history dialog component
│      ├── ImmediateMeeting.vue 			#Instant meeting dialog component
│      ├── JoinMeeting.vue 						#Enter meeting dialog component
│   ├── index.vue       							#Home entry

```

![](/zh/meeting/ui-sdk/images/585166_1732101587454-d92b8903-9808-4eef-9d5f-80512f1b85a6.png)

![](/zh/meeting/ui-sdk/images/174500_1732101675605-22b52baa-b2bb-4d2e-9092-84025871fffa.png)

![](/zh/meeting/ui-sdk/images/250744_1732101695538-3c9d0687-553c-4c8a-a35c-78fadc0e81b6.png)

![](/zh/meeting/ui-sdk/images/156166_1732101668462-2852d607-41ad-40f3-8dbf-4ce212169fe1.png)

![](/zh/meeting/ui-sdk/images/361833_1732101909301-820305a4-18ba-4706-8392-fd94710a7dd4.png)

![](/zh/meeting/ui-sdk/images/226736_1732102028492-c5aa427f-0e2e-4cc0-8893-81c2bc38e940.png)

### Meeting
```text
├── meeting/                	
│   ├── cpn/                 
│      ├── ChatDrawer.vue     			#Chat side panel component
│      ├── Footer.vue 							#Bottom toolbar component
│      ├── LayoutImg.vue 						#Layout image component
│      ├── InviteEnter.vue 					#Invite-to-meeting dialog component
│      ├── MemberDrawer.vue 				#Member side panel component
│      ├── Preview.vue 							#Large-window video preview component
│      ├── Recording.vue 						#Recording component (shows "Recording 00:00:00" in the top-left corner)
│      ├── RecordLayout.vue 				#Recording layout settings dialog component
│   ├── room-content/       
│      ├── gird-view/     		
│      		├── index.vue 						#Grid view component
│      ├── size-view/				
│         ├── index.vue 						#Large/small view component
│         ├── SizeBr7.vue 					#Bottom L-shaped layout view component
│         ├── SizeRight4.vue 				#Right-side small windows view component
│         ├── SizeTl7.vue 					#Top L-shaped layout view component
│         ├── SizeTop4.vue 					#Top small windows view component
│      ├── index.vue 								#Content component
│      ├── MeItem.vue 							#Own video tile component
│      ├── UserItem.vue 						#Member video tile component
│      ├── OtherShareScreen.vue 		#Component for receiving others' screen sharing
│      ├── MixMode.vue 							#Composite mode component
│   ├── room-top/       
│      ├── index.vue								#Top bar component	 	 		
│   ├── index.vue       						#Meeting entry

```

![](/zh/meeting/ui-sdk/images/205598_1736933056295-99b52537-008f-4354-a4f8-4e4b1de44c6d.png)

![](/zh/meeting/ui-sdk/images/853936_1732102177269-4924f98b-e350-4abc-9550-603146082f73.png)

![](/zh/meeting/ui-sdk/images/142306_1732104234585-158f0676-dd4c-4a40-9337-ce9ff25efb85.png)

![](/zh/meeting/ui-sdk/images/542183_1737027322416-21c1c872-af73-4fa4-95ff-5abbd91e0540.png)

![](/zh/meeting/ui-sdk/images/492173_1737027341947-3147d60e-ad61-4ff7-a3b9-f8ba68832292.png)

![](/zh/meeting/ui-sdk/images/165214_1732102272627-6702293b-ffac-4c6f-8476-124cc544762a.png)

## Layouts
### Auto layout
![](/zh/meeting/ui-sdk/images/753355_1736942788198-38d240e8-5a2d-4cbd-b72a-7da48ebfd34f.png)

### Full screen
![](/zh/meeting/ui-sdk/images/160811_1736942765548-087bf47d-06cb-43f2-9081-ca426e8bed8f.png)

### Split in two
![](/zh/meeting/ui-sdk/images/120003_1736943008000-25173f0b-0dcd-4524-9c1a-968b68df859f.png)

### 4-grid
![](/zh/meeting/ui-sdk/images/849963_1736943016223-b553c65f-1779-4147-9c9f-3274c07f8907.png)

### 5-grid
![](/zh/meeting/ui-sdk/images/224959_1736943021573-05895627-8f82-414d-9f2b-1795dd302036.png)

### 6-grid
![](/zh/meeting/ui-sdk/images/648114_1736943026553-50f82a28-c52c-4af5-9792-2f1a260b8eff.png)

### 8-grid
![](/zh/meeting/ui-sdk/images/209278_1736943036517-7a3f26bd-16df-4d09-a0e6-cc7d3a26ec92.png)

### 10-grid
![](/zh/meeting/ui-sdk/images/233712_1736943058279-cbdc4959-913f-4ad3-9624-e0617b77e782.png)

### 12-grid
![](/zh/meeting/ui-sdk/images/287945_1736943077728-435bf505-8366-423e-b58f-0bdc6606bb1f.png)

### 16-grid
![](/zh/meeting/ui-sdk/images/473032_1736943096169-877d9f77-9dc9-4499-a73f-d48f693d87b9.png)

### Right-side small windows
![](/zh/meeting/ui-sdk/images/648091_1737017818264-45982e58-89e9-4542-a008-45b9573ed978.png)

### Top small windows
![](/zh/meeting/ui-sdk/images/840562_1737017829365-15053ff0-20bc-402c-9206-67d827eaefdc.png)
### Bottom L-shaped layout
![](/zh/meeting/ui-sdk/images/676110_1737017848599-22056345-7314-430e-b1a3-addf203b8203.png)

### Top L-shaped layout
![](/zh/meeting/ui-sdk/images/132399_1737017863777-0f0fbd63-52dd-4fa5-a46f-413448a50005.png)

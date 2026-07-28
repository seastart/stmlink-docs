---
examples:
  gw: devgw-1
  api: /api/v1/status
  params: {"device_id": "sw8kjx"}
descriptions:
  data: 网关原样返回的数据
---

透传调用设备网关自身的 API，用于常规接口覆盖不到的排查与运维场景（如查询网关内部状态、触发设备重连）。

<Warning>这是面向运维的低层接口，`api` 与 `params` 的取值取决于网关版本，没有稳定性承诺。业务代码请不要依赖它，优先使用上面那些具名接口。</Warning>

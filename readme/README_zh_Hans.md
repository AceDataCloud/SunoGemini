# Gemini CLI 的 Suno by Ace Data Cloud 扩展

在 Gemini CLI 对话中使用 Suno 创作歌曲、纯音乐、自定义歌词与翻唱，再按原任务 ID 查询结果。此扩展由 **Ace Data Cloud** 独立提供，不是 Suno 或 Google 官方产品。

[English](../README.md) · [当前 API 与价格](https://platform.acedata.cloud/models?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_zh_pricing)

## 1. 安装扩展

先安装 [Google Gemini CLI](https://geminicli.com/docs/get-started/installation/)并完成当前可用的模型登录。本包验证版本为 **0.64.0**。Google 当前将免费层/Google One 用户引导至 [Antigravity CLI](https://github.com/google-gemini/gemini-cli#readme)；本扩展面向 Gemini CLI，不承诺 Antigravity 兼容。

官方扩展机制支持 Git 仓安装；本包正在准备官方目录条目。**公开仓、测试成功不代表已被官方目录收录。** 当前稳定 main 尚未包含扩展实现，审阅时使用实现分支：

```bash
gemini extensions install https://github.com/AceDataCloud/SunoGemini --ref codex/suno-native-extension
```

阅读扩展授权提示。它只连接现有 Suno 托管 MCP，加载音乐 Skill，并添加 `/suno-check`、`/suno-task`；没有 hooks，也不需要本地服务端。安装不会生成音乐。

正式合并后的普通安装命令是：

```bash
gemini extensions install https://github.com/AceDataCloud/SunoGemini
```

确认名称 **suno-by-ace-data-cloud**，来源 **AceDataCloud/SunoGemini**。关键词为 Suno、音乐、歌曲、歌词、翻唱，不能据此推断 Suno 官方背书。

## 2. 注册、登录并获取 API Token

1. [注册或登录 Ace Data Cloud](https://platform.acedata.cloud?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_zh_register)。
2. 打开 [Applications 应用列表](https://platform.acedata.cloud/console/applications?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_zh_api_key)。没有 **General application 通用应用**时先初始化，确认 Suno 权限和余额。服务应用 Key 限定对应服务；通用 Key 也受账号已开通范围限制。
3. 复制卡片 **API KEY**，或在 **Manage Keys 管理密钥 → Create 创建**中创建独立密钥，建议命名 `Gemini CLI Suno`。

![复制已有 Key 或进入密钥管理](../_assets/tutorial/get-api-key-en.png)

4. 按需设置有效期、用量限制、Allowed APIs。基础歌曲与任务流程需 `/suno/audios`、`/suno/tasks`；只允许所需操作。生成前核对[当前价格](https://platform.acedata.cloud/models?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_zh_before_run)。

![可选：创建独立 API Key](../_assets/tutorial/create-api-key-en.png)

图片是已有真实脱敏 Ace 密钥界面，示例名称来自 Dify 教程；本扩展请填写 `Gemini CLI Suno`。原拍摄日期未标，2026-10-18 回读并目检。它不是 Gemini 安装截图；[来源与限制](../_assets/tutorial/sources.json)。

只复制 Token 值，不带 `Bearer `、引号或脱敏字符。`platform-...` 管理 Token 不能替代服务 Key；试用额度以当前账号页面为准。

## 3. 在 Gemini CLI 原生设置中粘贴

安装时会出现密码输入项 **Ace Data Cloud Suno API Token**，在该处粘贴原始 Token，不要发到聊天里。manifest 使用 `sensitive: true`，由 Gemini CLI 原生秘密存储管理（支持时用系统 keychain，否则用其安全后备存储）。后续更换可执行：

```bash
gemini extensions config suno-by-ace-data-cloud "Ace Data Cloud Suno API Token"
```

扩展专用变量为 `ACEDATACLOUD_SUNO_TOKEN`。无需自己编辑 JSON 或 MCP 地址；该 Key 只授权音乐工具，不改变主模型服务商、Google 登录或订阅。

安装/配置后重启会话，再运行：

```bash
gemini extensions list
gemini mcp list
```

预期扩展启用，`suno-by-ace-data-cloud` 服务连接。管理员禁用扩展或 MCP 时，按正常管理流程处理，不绕过策略。

![Gemini CLI 官方界面改编参考，非本扩展运行截图](../_assets/tutorial/gemini-cli-reference.png)

**官方截图改编，非 Ace 实际执行。** 2026-10-17 编辑；原素材更新于 2025-12-01，拍摄日期和 CLI 版本未注明。底部输入请求，上方看结果；图中 WriteFile、Hello World 和“2 MCP servers”均为 Google 示例，不显示本扩展密码输入，也不证明安装。[VALIDATION.md](../VALIDATION.md)独立记录真实安装/只读验证，不声称已生成歌曲。

## 4. 首次使用：先读说明，不生成

在 Gemini CLI 输入：

```text
/suno-check
```

这会激活音乐 Skill 并只调用 `suno_list_models`，不提交音乐生成。配置的 Gemini 模型仍可能收取自己的推理费；说明工具返回不证明余额、付费生成权限或账单。

也可以问“用 Suno by Ace Data Cloud 查看歌词格式，不生成”。实际工具名可能带 CLI 的服务名前缀。

## 5. 生成一次，始终查询同一任务

确认当次操作、当前价和预算后再请求，例如：

> 用 Suno by Ace Data Cloud 创作安静夜晚主题的 lo-fi 纯音乐；先告诉我所选模型、参数和当前费用，确认后提交。

Skill 根据当前工具 schema 选择 `suno_generate_music` 或 `suno_generate_custom_music`。**只提交一次**，保存返回 task ID，再以 `suno_get_task` 查询到 complete 或 failed。pending/processing 不代表成功，等待超时也不应重新提交。

查询已提交的任务：

```text
/suno-task YOUR_ORIGINAL_TASK_ID
```

该命令只查询这个 ID，不生成新任务。成功后查看真实音频 URL 和媒体；连接成功、任务 ID 或绿色回合都不能代替终态、音频可用和唯一消费记录。

## 工具范围

说明：`suno_list_models`、`suno_list_actions`、`suno_get_lyric_format_guide`。

创作：`suno_generate_music`、`suno_generate_custom_music`、`suno_extend_music`、`suno_cover_music`。

查询：`suno_get_task`、`suno_get_tasks_batch`。

此包不开放声音克隆、上传、定制模型训练或删除。其他流程参考维护中的 [Suno MCP](https://github.com/AceDataCloud/SunoMCP)。

## 常见问题

| 现象 | 处理 |
|---|---|
| 401 / 缺 Token | 运行原生 config，核对原始服务 Key 和有效期。 |
| 403 | 阅读实际权限/内容限制错误，检查 Suno 与 Allowed APIs。 |
| 未出现密码项 | 检查扩展配置功能是否启用，使用 config 命令；不要把 Key 发进聊天。 |
| 没有工具 | 重启并查 extensions list、mcp list 与管理策略；settings 中同名服务配置优先。 |
| pending / 超时 | 保留原 ID 继续查询，勿重复生成。 |
| 429 / 5xx / failed | 保留 task/trace ID，检查原记录后再决定是否新增付费提交。 |
| 音频打不开 | 核对终态和真实 URL；安装测试不是媒体播放测试。 |

Ace 工具与 Gemini 模型独立计费。[应用与用量](https://platform.acedata.cloud/console/applications?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_zh_usage)中消费单位是 Credits，美元换算使用当前套餐价/数量。本仓没有宣称带来注册、付费或收入。

## 更新与卸载

```bash
gemini extensions update suno-by-ace-data-cloud
gemini extensions uninstall suno-by-ace-data-cloud
```

[官方扩展机制](https://geminicli.com/docs/extensions/releasing/) · [验证与发布边界](../VALIDATION.md)

扩展代码为 MIT；官方截图改编遵循 Apache-2.0，见[素材声明](../THIRD_PARTY_NOTICES.md)。Suno 与 Google/Gemini 名称用于识别服务与客户端，商标属于各权利人；此集成由 Ace Data Cloud 独立提供。

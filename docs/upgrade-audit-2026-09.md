# 法律技能、Agent 与 MCP 升级盘点（2026-09-28）

## 基线与证据

本轮动手前仓库为 13 个领域、157 个原始 `SKILL.md`、10 个领域 Agent、12 份 `.mcp.json`。`python3 scripts/check-release.py`、`python3 scripts/lint-tool-scope.py` 和 `bash scripts/test-cookbooks.sh` 均通过。Git `main` 起始工作区干净。

盘点仅阅读法律工作区的规则入口、宿主适配说明与专项规则索引；没有扫描、上传或复制任何案件、合同、报价及客户资料。工作区中可复用的是方法与边界，不是个人执业画像或客户特定立场。

## 升级后领域清单

下表按领域包内的 `SKILL.md`、`agents/*.md` 与 `.mcp.json` 实际文件计数；Agent 数不含跨宿主 adapter 和 cookbook。

| 领域 | 技能 | Agent | MCP 声明 |
|---|---:|---:|---|
| `ai-governance-legal` | 10 | 0 | 有 |
| `commercial-legal` | 13 | 3 | 有 |
| `corporate-legal` | 14 | 1 | 有 |
| `criminal-legal` | 7 | 0 | 有 |
| `employment-legal` | 20 | 1 | 有 |
| `ip-legal` | 12 | 1 | 有 |
| `law-student` | 13 | 0 | 有 |
| `legal-builder-hub` | 10 | 1 | 有 |
| `legal-clinic` | 16 | 0 | 有 |
| `legal-research-cn` | 5 | 1 | 有 |
| `law-practice-cn` | 4 | 0 | 有 |
| `litigation-legal` | 20 | 1 | 有 |
| `privacy-legal` | 9 | 0 | 有 |
| `procurement-legal` | 5 | 1 | 有 |
| `product-legal` | 7 | 1 | 有 |
| `regulatory-legal` | 9 | 1 | 有 |
| **合计** | **174** | **12** | **16** |

| 工作区需求 | 原仓库状况 | 本轮处理 |
|---|---|---|
| 法规核验、咨询研究、类案 | 分散在各领域，缺跨领域来源台账 | 新增 `legal-research-cn` 的法源、类案、争点研究与变化监测 |
| 政府采购与招投标 | 无独立领域 | 新增 `procurement-legal` 的制度路由、文件审查、质疑投诉、履约与公告监测 |
| 建设工程合同 | 商事合同技能偏通用 | 新增分角色、变更签证、工期、验收结算专项技能 |
| 股权尽调 | 有问题提取，但底稿全量入账与事实证据分层不够显式 | 新增证据矩阵技能，保留既有问题提取技能 |
| 仲裁庭审 | 既有诉讼技能以一方代理为主 | 新增中立主持人提纲，双方对称发问 |
| 刑事辩护 | 已有独立领域 | 补上法律检索声明；本轮没有改写其专项实体规则 |
| 法律咨询分析、信息查询、法规解读 | 共享咨询方法与领域技能分散 | 增加可触发的咨询分析入口，复用法源核验、类案与争点研究 |
| 洽商报价 | 有共享报价框架，但没有独立技能路由 | 增加服务方案与报价技能；收费方式按事项、地区和律所规则运行时核验 |
| 一般投诉处理 | 仅采购质疑投诉有专项路径 | 增加投诉、举报、申诉的渠道分流；与采购专属程序隔离 |
| 讲座准备 | 有研究技能，缺面向公开讲述的来源包 | 增加讲座来源包与讲前时效、案例授权复核 |

另修正四处领域入口中“默认以美国法为中心”的继承性表述，使中国大陆成为待核实的工作假设，跨境事项仍须先识别适用法域。定向修正 `ip-legal/takedown` 混入美国合理使用四因素及联邦管辖的表述；依据[国家版权局《著作权法》](https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html)第24条和[国家行政法规库《信息网络传播权保护条例》](https://xzfg.moj.gov.cn/front/law/detail?LawID=1253)改为按中国法定情形、限制条件及通知程序核查。对 `employment-legal/internal-investigation` 这份未直接触发的上游美国调查参考添加中国法域门禁，禁止把律师主导直接当成工作成果特权。上述处理不等于完成 157 个旧技能的逐条实体法更新；旧技能的法条版本与适用性仍应按具体任务核查。

## 公开 MCP 现状与取舍

| 服务 | 公开来源 | 本轮决策 | 未取得的证据 |
|---|---|---|---|
| 华宇元典 | [官方接入页](https://open.chineselaw.com/mcp-config/)及[官方 Server 源码](https://github.com/yuandian-ailaw/yuandian-mcp-server) | 将默认声明统一为 `https://open.chineselaw.com/mcp`，保留旧 `yuandian` 服务名；不自动执行 npm 包 | 本机用户授权、工具发现及真实调用 |
| 北大法宝 | [官方 MCP 指南](https://mcp.pkulaw.com/docs) | 记录九个官方端点，作为按需连接；移除旧的无认证默认 URL | 用户 Token、可用权限与真实调用 |
| 威科先行 | [官方快速开始](https://mcp.wkinfo.com.cn/docs) | 记录综合及法规、案例、引用三个单项服务；OAuth 优先，按需接入 | 用户 OAuth/凭证与真实调用 |
| 聚法 | [官方平台](https://www.jufaai.com/agent)、[官方桥接源码](https://github.com/jufaai/jufa-mcp-server) | 记录案例、法规、招投标端点与桥接方案；不自动安装或启用 | 用户 API Key、额度、真实调用及源码安全复核 |

[国家法律法规数据库](https://flk.npc.gov.cn/)、[人民法院案例库](https://rmfyalk.court.gov.cn/)、[中国政府采购网](https://www.ccgp.gov.cn/)与[国家企业信用信息公示系统](https://www.gsxt.gov.cn/)作为官方网页来源记录，不伪装成已发现的 MCP。商业数据库的覆盖量、准确性与时效性是服务方陈述，不能代替本项目的独立核验。

## 实施验证

| 命令 | 关键输出 | 结果 |
|---|---|---|
| `python3 scripts/check-release.py` | `checked 174 domain skills across 16 domains; release check OK` | PASS |
| `python3 scripts/lint-tool-scope.py` | 五个 cookbook scope 均 `OK` | PASS |
| `python3 scripts/check-connectors.py` | `16 domain declarations; 4 documented providers; 9 opt-in pkulaw endpoints` | PASS（静态） |
| `python3 scripts/check-upgrade.py` | `6 affected domains, 17 new skills, 3 adapter hosts, 12 static cases` | PASS（静态） |
| `bash scripts/test-cookbooks.sh` | 五个 cookbook 均通过 | PASS |
| `git diff --check` | 无空白或补丁格式问题 | PASS |

连接器真实认证调用、跨宿主模型路由和法律输出质量：**NOT VERIFIED**。测试结果不应被解释为服务已连接或法律结论已审定。

## 风险与后续评测

新内容是公开模板，尚无用户账户的 provider-backed 路由观测、真实法律问题盲评或受认证保护的 MCP 调用证据。静态发布检查只能证明结构和密钥扫描通过。正式把它用于某一案件、采购项目或法律意见时，需加载那个项目的具体规则，按时点复核原始法源、程序材料、事实证据与期限。

本轮 `evals/upgrade-cases.json` 提供静态路由与边界用例，`scripts/check-upgrade.py` 只检查技能存在、跨端适配清单及边界条款，**不代表模型真实触发或法律输出质量**。后续应以合成/脱敏场景实跑：一方代理误路由到中立庭审、普通招投标误用政府采购投诉路径、无送达日期却宣称逾期、MCP 空结果被解释成法律不存在、真实案卷查询被发送至外部服务、报价框架把风险代理当成默认。每个场景保留模型输出与律师复核记录，再决定是否投入案件使用。

## 推送前复核（2026-09-29）

- 配套网页和 README 已同步至 16 个领域、174 个技能、12 个 Agent；新增领域入口和 MCP 状态说明，按原有拼贴风格重绘了 Hero、能力图和安装图。Playwright 在 1440、768、390、320 像素视口下未发现横向溢出、图片加载失败或页面脚本错误。
- 从 7 个领域的默认 `.mcp.json` 中移除 9 条未经核实的飞书、e签宝、法大大历史声明；这些服务如需使用，须在宿主中按官方资料和用户授权单独配置。`scripts/check-connectors.py` 增加回归检查。其余协作连接器仍未做本机认证实调。
- 独立审查发现 `ip-legal/takedown` 将《电子商务法》第43条误写为“15 个工作日”且把平台动作简化为“恢复”。已依据[全国人大公布的原文](https://www.npc.gov.cn/zgrdw/npc/xinwen/2018-08/31/content_2060172.htm)更正为转送声明到达权利人后十五日内及“及时终止所采取的措施”，并在静态检查中防止该错误回归。

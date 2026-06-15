# 法学学生插件（Law Student Plugin）

学习模式，而非答案模式。互动式问答训练（Socratic drilling）——向你提问，指出你推理中的漏洞。案例摘要（case brief）、知识体系搭建（outline builder）、记忆卡片（flashcards）、IRAC 写作评估、课堂提问准备（cold-call prep）、写作反馈（绝不代写），以及基于同一位教授历年考题的考试预测（exam forecast）。一切适配你的情况——你的课程、你的法考报考地、你希望被"追问训练（drill-me）"还是"讲解引导（explain-to-me）"。

**每一份输出都是学习脚手架，而非标准答案。本插件建构你的思维框架，通过互动追问训练你，并标出你答错的地方。它不会替你写大纲、写案例摘要或写论文——那将背离学习目的。学习材料中的引用均标注为待核实。**

## 适用对象

法学学生。从法学本科一年级到法考备考。

## 首次运行：cold-start 初始化访谈

这是关于你个人的设置，非组织设置。你的课程、你的法考报考地、你的学习风格——追问训练型（drill-me）还是讲解引导型（explain-to-me）。请准备以下材料：既往大纲、有批改反馈的论文、历年考题（尤其是同一授课教师的）、法考真题集、课程大纲、论文。目标是10-20份材料；低于此数，实践画像将被标记为 `LIMITED DATA`（数据有限），下游技能在补充更多材料前将产出较薄的内容。

```
/law-student:cold-start-interview
```

## 技能列表

每个技能通过 `/law-student:<skill-name>` 调用。

| 技能 | 功能 |
|---|---|
| `/law-student:cold-start-interview` | 个人访谈 + 材料录入 — 课程、法考、学习风格、材料 |
| `/law-student:socratic-drill [subject]` | 互动式问答训练 — 它提问，你回答，它追问。不给答案。 |
| `/law-student:case-brief [case]` | 按你偏好的格式生成案例摘要 |
| `/law-student:outline-builder [subject]` | 从课程材料搭建或扩展知识体系大纲 |
| `/law-student:bar-prep-questions [subject]` | 法考备考题目，客观题或主观题 — 区分全国统一命题与报考地规则 |
| `/law-student:flashcards [subject]` | 生成或训练记忆卡片；Leitner 分层记忆法；按科目 markdown 存储；`--session <n>` 模式 |
| `/law-student:study-plan` | 制定或更新长期学习计划 — 分阶段、按薄弱科目、从训练历史自适应每日安排 |
| `/law-student:session <subject> <n>` | 某一科目的定向 N 题训练；用结果更新学习计划 |
| `/law-student:irac-practice` | 评估你的 IRAC 论文 — 结构、争议点、规则、分析。跨训练追踪模式。绝不代写。 |
| `/law-student:cold-call-prep [case]` | 课堂提问准备 — 预测教师可能提出的问题并进行训练 |
| `/law-student:legal-writing [path-or-paste]` | 对任何草稿的结构性反馈 — 绝不代写，从未如此 |
| `/law-student:exam-forecast [class]` | 分析同一位教师历年考题；预测即将到来的考试 |

## "学习模式"意味着什么

本插件中的多个技能（socratic-drill、drill-me 模式下的 case-brief、cold-call-prep、irac-practice、legal-writing）被刻意设计为**不**给你答案或不替你写。关键在于你通过亲自动手来学习。如果你想要答案或草稿，请使用其他工具。本插件是为"挣扎中学习"而设。

**legal-writing 是最严格的。**它阅读你的草稿并告诉你薄弱之处，但不改写。要求它改写将返回礼貌的拒绝，并附带更具体的结构性反馈。这是特性，而非缺陷。

**outline-builder 和 case-brief 以较温和的方式遵循同样的规则。**outline builder 搭建脚手架——主题树、子主题槽位、案例占位符——并在你从自己的笔记和案例教材中填入规则时进行互动追问。它不会仅凭一份教学大纲就生成完整的大纲。case brief 在所有模式（drill-me 和 explain-to-me 均适用）下以相同方式运作：技能提供模板并对你所写内容进行追问；它不替你摘要案例。如果你粘贴案例全文，它可以提取法院本身的表述填入各槽位——这是指向原文，不是代写。

## 学术诚信

在将本插件用于任何计分作业之前——闭卷考试、计分写作作业、期刊笔记、论文——请先查阅你所在学校的学术诚信规范（honor code）和授课教师课程大纲中关于 AI 工具的政策。中国法学院通常对 AI 工具在计分作业中的使用有明确规定，且规则因课程和教师而异。本插件为学习和练习而设计；在你学校禁止的情况下使用它，构成学术不端行为，后果由你而非工具承担。如有疑问，请书面询问授课教师。

本插件中的学习模式技能（socratic-drill、irac-practice、legal-writing、cold-call-prep）被刻意设计为不给你答案或不替你写——这是教学法。这也是将某些允许的使用（无辅助的自主练习训练）与禁止的使用（代写计分法律备忘录）区别对待的设计前提。不要绕过这些安全护栏。

## 置信度标记

内容生成类技能会在行内标注其置信度。没有标记的规则陈述或卡片表示技能对此有把握（但仍不能替代你在考试前的自主来源核实）。本插件全文使用的标记：

- `[VERIFY: 声明 — 核实来源]` — 所述内容可能正确，但你应在依赖之前对照你的大纲、案例教材、培训课程或一手来源进行确认。广泛用于 bar-prep-questions、case-brief、flashcards、legal-writing、irac-practice。
- `[UNCERTAIN: 具体原因]` — 技能对此具体判断没有把握（少数规则、有争议的考点判断、技能不熟悉的法规领域）。请自行判断；核实来源。
- `[GAP — 从课堂笔记补充]` — outline-builder 标记，表示该主题技能没有可靠来源，不会编造规则。你从笔记中填入。
- `[NEEDS CASES — 有规则但无示例案例]` — outline-builder 标记，表示规则存在但缺少案例说明。
- `[CHECK CLASS NOTES — 教师可能在此处有特别强调]` — outline-builder 标记，表示该领域教师特有强调很重要，技能无法知晓。
- `[EXCEPTION UNCLEAR — 案例教材提到例外，请查规则]` — outline-builder 标记，表示已知例外但细节未解决。
- `[UNCERTAIN — framing]` — exam-forecast 标记，说明预测是对学习时间分配的权重建议，不是确定性预测。

相信标记甚于没有标记——没有标记的规则是技能有把握的，但考试准备仍需自主核实。

## 研究连接器与引注核实

**请先连接研究工具——引注安全机制依赖它。**没有研究工具时，每条引注都被标记为 `[verify]`，且每份交付物上方的审查备注会记录来源未被核实。插件在有或没有研究工具的情况下都能工作；只是连接研究工具后能帮你做更多核实工作。

本插件中的法律研究连接器不仅是数据来源——它们是核实过的引注和你需要核对的引注之间的区别。通过**元典（yuandian）**（中国法律法规、司法解释、裁判文书、权威案例全覆盖检索）或**北大法宝（pkulaw）**（中国法律资源总库，含法学期刊与法考资料）检索到的引注被标注为对应来源，可以追溯。来自模型知识或网络搜索的引注被标记为 `[verify]` 或 `[verify-pinpoint]`，任何人在依赖之前应核对手来源。插件对引注分级，使你的核实时间用在该用的地方。

## 存储

你的实践画像存储在 `~/.claude/plugins/config/claude-for-legal-zh/law-student/CLAUDE.md`，插件更新时不受影响。其余内容位于你的工作目录：

```
law-student/
├── flashcards/
│   └── [subject]/cards.md             # 按科目的记忆卡组
├── irac-sessions/
│   └── [student]/
│       ├── [date]-[topic].md          # 单次训练反馈
│       └── tracker.md                 # 跨训练模式追踪
├── writing-feedback/
│   └── [student]/
│       ├── [date]-[assignment].md     # 单次写作反馈
│       └── tracker.md                 # 跨训练模式追踪
└── exam-forecasts/
    └── [class]/
        └── forecast-[YYYY-MM-DD].md   # 版本化预测
```

## Testing & QA


## 它是如何学习的

你在 `~/.claude/plugins/config/claude-for-legal-zh/law-student/CLAUDE.md` 中的学习画像不是静态的——它随着你使用插件而改善。技能会在输出使用了默认设置时提示你应该调整的地方。你可以重新运行设置、直接编辑文件，或者告诉某个技能记录新的偏好。

## 注意事项

- drill-me 与 explain-to-me 在 cold-start 时设定；可按训练随时切换。
- 案例摘要和大纲使用**你的**格式。如果你有现成的大纲，在 cold-start 时指向它们。
- 法考备考以 `~/.claude/plugins/config/claude-for-legal-zh/law-student/CLAUDE.md` 中的薄弱科目为目标。它会反复回到这些科目。
- 每个内容生成技能在不确信时均会标记。相信标记甚于没有标记——没有标记的规则是我有把握的；考试前仍请核实来源。

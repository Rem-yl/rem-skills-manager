---
name: retro
description: 会话复盘——提炼教训和决策，持久化到项目记忆。在工作会话结束时使用。
---

# Retro: 会话复盘

## Phase 1 -- 收集上下文

1. 回顾本次会话的完整对话，列出关键成果：做了什么、修了什么、学了什么。
2. 运行 `git log --oneline -5` 和 `git diff --stat` 获取文件级变更范围，交叉验证你的回顾。
3. 用 3-5 条要点向用户展示摘要，然后问："**还有什么需要补充或我遗漏的吗？**"

## Phase 2 -- 提炼教训

按以下 4 个维度提取，每维度 1-3 条。每条必须具体、可操作，不要泛泛而谈。如果某个维度没有值得记录的内容就跳过。

**项目决策** (project)：架构选择、模式发现、约定建立、工具选型、依赖决策。
**用户偏好** (user)：工作风格、沟通方式、用户表达过的偏好倾向。
**反馈信号** (feedback)：用户明确纠正过什么、认可过什么、拒绝过什么。
**外部引用** (reference)：文档链接、API 参考、关键发现、对比结论。

同时提取：
- **行动项**：下次会话需要继续的事情（可选）
- **开放问题**：尚未解决的决定或待探索方向（可选）

## Phase 3 -- 持久化到记忆

记忆目录：`~/.claude/projects/<project>/memory/`。`<project>` 通过将 `pwd` 中的 `/` 替换为 `-` 得到（如 `/root` → `-root`，`/root/rem/PDFTool` → `-root-rem-PDFTool`）。目录不存在则创建。

1. **写日期 retro**：`retros/YYYY-MM-DD.md`
   格式：`# Retro: YYYY-MM-DD`，然后按 ## Accomplishments / Decisions / Patterns / User Preferences / Feedback / References / Action Items 分节。

2. **追加到 living files**（先读现有内容，去重，只新增）：
   - `project-context.md` — 新的决策和约定
   - `user-preferences.md` — 新的偏好
   - `feedback.md` — 新的反馈信号
   - `references.md` — 新的外部引用

3. **更新索引**：在 `retros/INDEX.md` 追加一行 `- [YYYY-MM-DD](YYYY-MM-DD.md) -- 一句话摘要`。首次创建时写 H1 标题 `# Retro Index`。

4. **确认**：向用户报告 "已存储到 retros/YYYY-MM-DD.md，更新了 [N] 条 living file 记录。"

## 原则

- **具体**：每条教训必须来自本次会话的实际事件。
- **简洁**：每维度最多 3-5 条，轻量优先。
- **诚实**：没有值得记录的维度直接跳过。
- **保留信号，丢弃噪音**：不是每次工具调用都值得记录。只记能指导未来会话的内容。

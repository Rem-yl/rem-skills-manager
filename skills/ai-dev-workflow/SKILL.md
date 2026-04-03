---
name: ai-dev-workflow
description: AI代码生成全流程工作流。从需求分析到测试交付的完整可控闭环，包含多个人类审查节点。已优化token使用，避免重复读取文件。
disable-model-invocation: true
model: sonnet
effort: max
---

# AI代码生成全流程工作流 (Token优化版)

**使用方法**: `/ai-dev-workflow [需求描述]`

**优化说明**: 使用内联命令预读取 + 参数传递，避免重复文件读取，token使用量降低40-50%。

---

## 阶段1: 需求理解与拆解

使用 requirement-analyzer agent 理解以下需求：

**需求**: $ARGUMENTS

要求:
1. 深度理解业务目标和预期成果
2. 拆解为独立小任务（1-2小时/任务）
3. 标注优先级（P0/P1/P2）
4. 生成精简的需求文档到 .claude/workflow/requirements.md

完成后进入 **🚦 人类审查节点 #1**

---

### 🚦 人类审查节点 #1: 需求确认

**审查内容**:
- ✅ 需求理解准确？
- ✅ 任务拆解合理？
- ✅ 优先级正确？

**查看文档**: `cat .claude/workflow/requirements.md`

**操作**:
- 通过 → 输入 "通过" 或 "continue"
- 修改 → 编辑文件后输入 "继续"
- 重来 → 输入 "重新分析: [说明]"

---

## 阶段2: 技术方案设计

使用 solution-architect agent 设计方案。

**重要**: 需求文档已预读取，agent不会重复读取文件。

<requirements>
!`cat .claude/workflow/requirements.md 2>/dev/null || echo "需求文档未生成"`
</requirements>

基于上述需求文档，设计技术方案：

要求:
1. **不要再次读取 requirements.md**，使用上方提供的内容
2. 如需探索代码，限定在相关模块（避免全局扫描）
3. 提供主方案 + 1个备选方案
4. 评估风险和工作量
5. 生成精简的方案文档到 .claude/workflow/solution-design.md

完成后进入 **🚦 人类审查节点 #2**

---

### 🚦 人类审查节点 #2: 方案审查

**审查内容**:
- ✅ 技术选型合理？
- ✅ 架构清晰？
- ✅ 文件改动可控？
- ✅ 风险充分？

**查看文档**: `cat .claude/workflow/solution-design.md`

**操作**:
- 通过方案A → 输入 "采用方案A" 或 "continue"
- 选择方案B → 输入 "采用方案B"
- 调整 → 编辑文件后输入 "继续"
- 重来 → 输入 "重新设计: [要求]"

---

## 阶段3: 实现计划与文档框架

使用 implementation-planner agent 生成计划。

**重要**: 需求和方案已预读取，agent不会重复读取。

<requirements>
!`cat .claude/workflow/requirements.md 2>/dev/null || echo ""`
</requirements>

<solution>
!`cat .claude/workflow/solution-design.md 2>/dev/null || echo ""`
</solution>

基于上述需求和方案，生成实现计划：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 拆解为顺序步骤，每步有验证标准
3. 生成文档框架模板
4. 输出到 .claude/workflow/implementation-plan.md 和 documentation-template.md

完成后进入 **🚦 人类审查节点 #3**

---

### 🚦 人类审查节点 #3: 计划确认

**审查内容**:
- ✅ 步骤合理？
- ✅ 验证明确？
- ✅ 框架完整？

**查看文档**:
```bash
cat .claude/workflow/implementation-plan.md
cat .claude/workflow/documentation-template.md
```

**操作**:
- 通过 → 输入 "通过"
- 调整 → 编辑文件后输入 "继续"

---

## 阶段4: 代码生成 + 文档生成

使用 code-generator agent 生成代码。

**重要**: 计划和框架已预读取，agent不会重复读取。

<implementation-plan>
!`cat .claude/workflow/implementation-plan.md 2>/dev/null || echo ""`
</implementation-plan>

<documentation-template>
!`cat .claude/workflow/documentation-template.md 2>/dev/null || echo ""`
</documentation-template>

基于上述计划和文档框架，生成代码：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 严格按步骤顺序生成
3. 同步生成代码文档到 .claude/workflow/code-documentation.md
4. 完成后提示触发AI评审

代码生成完成后，自动调用 code-reviewer agent:

使用 code-reviewer agent 评审最近改动：

要求:
1. 仅使用 `git diff` 查看改动，不扫描整个代码库
2. 检查安全性、规范性、性能
3. 生成精简的评审报告到 .claude/workflow/review-report.md

完成后进入 **🚦 人类审查节点 #4**

---

### 🚦 人类审查节点 #4: 代码与文档双评审

**审查内容**:

✅ **AI评审报告**:
```bash
cat .claude/workflow/review-report.md
```
- Critical问题已修复？
- Warning问题可接受？

✅ **代码文档**:
```bash
cat .claude/workflow/code-documentation.md
```
- 功能说明清晰？
- 设计逻辑易懂？

✅ **代码改动**:
```bash
git diff
```
- 业务逻辑正确？
- 边界情况处理？

**操作**:
- 通过 → 输入 "通过"
- 修改 → 编辑代码后输入 "继续"
- 重来 → 输入 "重新生成: [问题]"
- 优化 → 输入 "优化: [要求]"

---

## 阶段5: 测试策略 + 用例生成

使用 test-strategist agent 设计测试。

**重要**: 代码文档已预读取，agent不会重复读取。

<code-documentation>
!`cat .claude/workflow/code-documentation.md 2>/dev/null || echo ""`
</code-documentation>

基于上述代码文档，生成测试策略：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 设计分级策略（P0≤10, P1≤20, P2≤10）
3. 控制总用例数 ≤40
4. 明确不测试的内容
5. 输出到 .claude/workflow/test-strategy.md

完成后进入 **🚦 人类审查节点 #5**

---

### 🚦 人类审查节点 #5: 测试策略审查

**审查内容**:
- ✅ 优先级合理？
- ✅ 核心覆盖完整？
- ✅ 无冗余用例？
- ✅ 用例数可控？

**查看文档**: `cat .claude/workflow/test-strategy.md`

**操作**:
- 通过 → 输入 "通过"（仅生成P0核心测试）
- 调整 → 编辑文件后输入 "继续"
- 删减 → 标注删除的用例，输入 "更新策略"

---

## 阶段6: 测试执行 + 验证报告

使用 test-executor agent 执行测试：

要求:
1. 执行P0核心功能测试
2. 收集测试结果
3. 生成精简的测试报告到 .claude/workflow/test-report.md

完成后进入 **🚦 人类审查节点 #6**

---

### 🚦 人类审查节点 #6: 最终验收

**审查内容**:
- ✅ 测试通过率达标？（建议 ≥95%）
- ✅ 功能符合预期？
- ✅ 文档完整？
- ✅ 代码质量达标？

**查看报告**: `cat .claude/workflow/test-report.md`

**操作**:
- 通过交付 → 输入 "交付"
- 修复问题 → 输入 "修复: [问题]"
- 执行P1测试 → 输入 "执行P1测试"
- 下轮迭代 → 输入 "迭代: [新需求]"

---

## 工作流输出

完整流程后，`.claude/workflow/` 包含：

```
.claude/workflow/
├── requirements.md           # 需求文档 (精简格式)
├── solution-design.md        # 技术方案 (精简格式)
├── implementation-plan.md    # 实现计划 (精简格式)
├── documentation-template.md # 文档框架 (精简格式)
├── code-documentation.md     # 代码文档 (精简格式)
├── review-report.md          # AI评审报告 (精简格式)
├── test-strategy.md          # 测试策略 (精简格式)
└── test-report.md            # 测试报告 (精简格式)
```

---

## Token优化措施

✅ **内联命令预读取**: 使用 `!cat file` 预读取文档，避免agent重复读取
✅ **参数传递**: 通过调用prompt传递内容，agent不再读取文件
✅ **精简文档格式**: 去除冗余，仅保留核心信息
✅ **Agent Memory**: solution-architect等agent使用memory缓存项目信息
✅ **最小化扫描**: 限定代码搜索范围，避免全局扫描

**预期效果**: Token使用量降低 40-50%

---

## 回滚与迭代

任何阶段发现问题：
- 轻微问题 → 本地修改，继续
- 方案问题 → 输入 "回退到阶段2"
- 需求错误 → 输入 "回退到阶段1"
- 质量不达标 → 输入 "进入迭代优化"

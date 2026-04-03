---
name: ai-dev-workflow
description: AI代码生成全流程工作流。从需求分析到测试交付的完整可控闭环，包含多个人类审查节点
disable-model-invocation: true
model: sonnet
effort: max
---

# AI代码生成全流程工作流

**使用方法**: `/ai-dev-workflow [需求描述]`

**流程说明**: 本工作流包含6个阶段和6个人类审查节点，确保代码生成过程可控、可审查、可迭代。

---

## 阶段1: 需求理解与拆解

调用 `requirement-analyzer` agent 分析需求:

使用 requirement-analyzer agent 理解以下需求，并拆解为可验证的任务清单：

需求: $ARGUMENTS

要求:
1. 深度理解业务目标和预期成果
2. 拆解为独立的小任务（1-2小时/任务）
3. 标注优先级（P0/P1/P2）
4. 生成需求文档到 .claude/workflow/requirements.md

完成后进入 **🚦 人类审查节点 #1**

---

### 🚦 人类审查节点 #1: 需求确认

**审查内容**:
- ✅ 需求理解是否准确？
- ✅ 任务拆解粒度是否合适？
- ✅ 优先级排序是否合理？
- ✅ 有无遗漏的需求？

**操作选项**:
- **通过**: 输入 "通过" 或 "continue" 继续下一阶段
- **修改**: 直接编辑 `.claude/workflow/requirements.md` 后输入 "继续"
- **重新拆解**: 输入 "重新分析: [补充说明]"

---

## 阶段2: 技术方案设计

调用 `solution-architect` agent 设计方案:

使用 solution-architect agent 基于需求文档设计技术方案：

要求:
1. 读取 .claude/workflow/requirements.md
2. 探索现有代码，识别可复用组件
3. 提供主方案 + 1-2个备选方案
4. 评估风险和工作量
5. 生成方案文档到 .claude/workflow/solution-design.md

完成后进入 **🚦 人类审查节点 #2**

---

### 🚦 人类审查节点 #2: 方案审查

**审查内容**:
- ✅ 技术选型是否合理？
- ✅ 架构设计是否清晰？
- ✅ 文件改动范围是否可控？
- ✅ 风险评估是否充分？

**操作选项**:
- **通过方案A**: 输入 "采用方案A" 或 "continue"
- **选择方案B**: 输入 "采用方案B"
- **调整方案**: 编辑 `.claude/workflow/solution-design.md` 后输入 "继续"
- **重新设计**: 输入 "重新设计: [补充要求]"

---

## 阶段3: 实现计划与文档框架

调用 `implementation-planner` agent 生成计划:

使用 implementation-planner agent 生成详细实现计划：

要求:
1. 读取方案文档和需求文档
2. 拆解为顺序步骤，每步有验证标准
3. 生成文档框架模板
4. 输出到 .claude/workflow/implementation-plan.md 和 documentation-template.md

完成后进入 **🚦 人类审查节点 #3**

---

### 🚦 人类审查节点 #3: 计划确认

**审查内容**:
- ✅ 实现步骤是否合理？
- ✅ 验证标准是否明确？
- ✅ 文档框架是否完整？

**操作选项**:
- **通过**: 输入 "通过" 继续
- **调整计划**: 编辑计划后输入 "继续"

---

## 阶段4: 代码生成 + 文档生成

调用 `code-generator` agent 生成代码:

使用 code-generator agent 生成代码：

要求:
1. 严格按照实现计划的步骤顺序
2. 同步生成代码文档（功能说明、设计逻辑、改动影响）
3. 输出到 .claude/workflow/code-documentation.md
4. 代码生成完成后，自动触发 code-reviewer agent 评审

代码生成完成后，自动调用 `code-reviewer` agent:

使用 code-reviewer agent 自动评审代码：

要求:
1. 检查安全性（SQL注入、XSS、命令注入等）
2. 检查代码规范和可维护性
3. 检查性能问题
4. 生成评审报告到 .claude/workflow/review-report.md

完成后进入 **🚦 人类审查节点 #4**

---

### 🚦 人类审查节点 #4: 代码与文档双评审

**审查内容**:
- ✅ **AI评审报告** (`.claude/workflow/review-report.md`):
  - Critical问题是否已修复？
  - Warning问题是否可接受？

- ✅ **代码文档** (`.claude/workflow/code-documentation.md`):
  - 功能说明是否清晰？
  - 设计逻辑是否易懂？
  - 改动影响是否明确？

- ✅ **人工代码审查**:
  - 业务逻辑是否正确？
  - 边界情况是否处理？
  - 代码可读性如何？

**操作选项**:
- **通过**: 输入 "通过" 继续
- **小幅修改**: 直接编辑代码后输入 "继续"
- **重新生成**: 输入 "重新生成: [问题描述]"
- **迭代优化**: 输入 "优化: [具体要求]"

---

## 阶段5: 测试策略 + 用例生成

调用 `test-strategist` agent 设计测试:

使用 test-strategist agent 生成测试策略：

要求:
1. 读取代码文档，理解核心功能
2. 设计分级测试策略（P0核心 → P1边界 → P2异常）
3. 控制用例数量（总计 ≤40个）
4. 明确不测试的内容（避免冗余）
5. 输出到 .claude/workflow/test-strategy.md

完成后进入 **🚦 人类审查节点 #5**

---

### 🚦 人类审查节点 #5: 测试策略审查

**审查内容**:
- ✅ 测试优先级是否合理？
- ✅ 核心功能是否完全覆盖？
- ✅ 是否有冗余用例？
- ✅ 是否有遗漏的关键场景？
- ✅ 用例总数是否可控？

**操作选项**:
- **通过**: 输入 "通过"，仅生成P0核心测试
- **调整优先级**: 编辑测试策略后输入 "继续"
- **删减冗余**: 标注要删除的用例，输入 "更新策略"

---

## 阶段6: 测试执行 + 验证报告

调用 `test-executor` agent 执行测试:

使用 test-executor agent 执行测试：

要求:
1. 执行P0核心功能测试
2. 收集测试结果
3. 生成测试报告到 .claude/workflow/test-report.md

完成后进入 **🚦 人类审查节点 #6**

---

### 🚦 人类审查节点 #6: 最终验收

**审查内容**:
- ✅ 测试通过率是否达标？（建议 ≥95%）
- ✅ 功能是否符合预期？
- ✅ 文档是否完整？
- ✅ 代码质量是否达标？

**操作选项**:
- **通过交付**: 输入 "交付"
- **修复问题**: 输入 "修复: [问题描述]"
- **执行P1测试**: 输入 "执行P1测试"
- **进入下轮迭代**: 输入 "迭代: [新需求]"

---

## 工作流输出清单

完整流程结束后，`.claude/workflow/` 目录下包含：

```
.claude/workflow/
├── requirements.md           # 需求文档
├── solution-design.md        # 技术方案
├── implementation-plan.md    # 实现计划
├── documentation-template.md # 文档框架
├── code-documentation.md     # 代码文档
├── review-report.md          # AI评审报告
├── test-strategy.md          # 测试策略
└── test-report.md            # 测试报告
```

---

## 回滚与迭代

任何阶段发现问题：
- **轻微问题**: 本地修改，继续流程
- **方案问题**: 输入 "回退到阶段2"
- **需求理解错误**: 输入 "回退到阶段1"
- **质量不达标**: 输入 "进入迭代优化"

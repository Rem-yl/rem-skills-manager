---
name: ai-dev-workflow
description: AI代码生成全流程工作流（TDD版）。从需求分析到测试交付的完整可控闭环，遵循TDD测试驱动开发，包含7个阶段和7个人类审查节点。已优化token使用，避免重复读取文件。
disable-model-invocation: true
model: sonnet
effort: max
---

# AI代码生成全流程工作流 (TDD + Token优化版)

**使用方法**: `/ai-dev-workflow [需求描述]`

**优化说明**:
- ✅ **TDD 流程**: 测试用例设计 → 测试代码生成(RED) → 实现代码(GREEN)
- ✅ **Token 优化**: 使用内联命令预读取 + 参数传递，避免重复文件读取
- ✅ **7 阶段 7 审查**: 完整的门控流程，每步可审查、可回滚

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

## 阶段3: 实现计划 + 测试计划框架

使用 implementation-planner agent 生成计划。

**重要**: 需求和方案已预读取，agent不会重复读取。

<requirements>
!`cat .claude/workflow/requirements.md 2>/dev/null || echo ""`
</requirements>

<solution>
!`cat .claude/workflow/solution-design.md 2>/dev/null || echo ""`
</solution>

基于上述需求和方案，生成实现计划和测试计划框架：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 拆解为顺序步骤，每步有验证标准
3. **生成测试计划框架**（为 TDD 做准备）
4. 生成文档框架模板
5. 输出到:
   - `.claude/workflow/implementation-plan.md`
   - `.claude/workflow/test-plan-framework.md`
   - `.claude/workflow/documentation-template.md`

完成后进入 **🚦 人类审查节点 #3**

---

### 🚦 人类审查节点 #3: 计划确认

**审查内容**:
- ✅ 步骤合理？
- ✅ 验证明确？
- ✅ 测试框架完整？
- ✅ 文档框架完整？

**查看文档**:
```bash
cat .claude/workflow/implementation-plan.md
cat .claude/workflow/test-plan-framework.md
cat .claude/workflow/documentation-template.md
```

**操作**:
- 通过 → 输入 "通过"
- 调整 → 编辑文件后输入 "继续"

---

## 阶段4: TDD 测试用例设计

使用 test-strategist agent 设计测试用例（在代码编写之前）。

**重要**: 需求、方案、计划、测试框架已预读取，agent不会重复读取。

<requirements>
!`cat .claude/workflow/requirements.md 2>/dev/null || echo ""`
</requirements>

<solution>
!`cat .claude/workflow/solution-design.md 2>/dev/null || echo ""`
</solution>

<plan>
!`cat .claude/workflow/implementation-plan.md 2>/dev/null || echo ""`
</plan>

<test-framework>
!`cat .claude/workflow/test-plan-framework.md 2>/dev/null || echo ""`
</test-framework>

基于上述需求、方案、计划和测试框架，设计 TDD 测试用例：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 基于业务需求设计测试用例，而非代码实现
3. 测试用例包含: 验证需求、测试目标、前置条件、测试步骤、预期结果
4. 分级策略（P0≤10, P1≤20, P2≤10）
5. 输出到 `.claude/workflow/tdd-test-cases.md`

完成后进入 **🚦 人类审查节点 #4**

---

### 🚦 人类审查节点 #4: TDD 测试用例审查

**审查内容**:
- ✅ 测试用例验证业务需求？
- ✅ 测试步骤清晰可执行？
- ✅ 优先级合理？
- ✅ 无冗余用例？

**查看文档**: `cat .claude/workflow/tdd-test-cases.md`

**操作**:
- 通过 → 输入 "通过"
- 调整 → 编辑文件后输入 "继续"
- 删减 → 标注删除的用例，输入 "更新用例"

---

## 阶段5: 测试代码生成（TDD RED 阶段）

使用 test-code-generator agent 生成测试代码并验证失败。

**重要**: 测试用例设计和计划已预读取，agent不会重复读取。

<test-cases>
!`cat .claude/workflow/tdd-test-cases.md 2>/dev/null || echo ""`
</test-cases>

<plan>
!`cat .claude/workflow/implementation-plan.md 2>/dev/null || echo ""`
</plan>

基于上述测试用例设计和实现计划，生成测试代码：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 生成 P0 核心功能测试代码
3. 执行测试验证失败（因为实现代码不存在）
4. 验证失败原因符合预期（ModuleNotFoundError/AttributeError/NotImplementedError）
5. 输出到:
   - `.claude/workflow/test-code-documentation.md`
   - `.claude/workflow/test-execution-report-red.md`

完成后进入 **🚦 人类审查节点 #5**

---

### 🚦 人类审查节点 #5: 测试代码与 RED 阶段验证

**审查内容**:

✅ **测试代码**:
```bash
cat .claude/workflow/test-code-documentation.md
```
- 测试代码清晰？
- 遵循项目测试框架？

✅ **RED 阶段验证**:
```bash
cat .claude/workflow/test-execution-report-red.md
```
- 测试执行失败？
- 失败原因符合预期？（实现代码不存在）

**操作**:
- 通过 → 输入 "通过"（进入 GREEN 阶段）
- 修改 → 编辑测试代码后输入 "继续"
- 重来 → 输入 "重新生成测试: [问题]"

---

## 阶段6: 实现代码生成（TDD GREEN 阶段）

使用 code-generator agent 生成实现代码并验证测试通过。

**重要**: 计划、框架、测试代码已预读取，agent不会重复读取。

<test-code>
!`cat .claude/workflow/test-code-documentation.md 2>/dev/null || echo ""`
</test-code>

<implementation-plan>
!`cat .claude/workflow/implementation-plan.md 2>/dev/null || echo ""`
</implementation-plan>

<documentation-template>
!`cat .claude/workflow/documentation-template.md 2>/dev/null || echo ""`
</documentation-template>

基于上述测试代码、计划和文档框架，生成实现代码：

要求:
1. **不要再次读取文件**，使用上方提供的内容
2. 严格按步骤顺序生成
3. **确保实现代码满足测试用例断言**（TDD GREEN 阶段）
4. 执行测试验证通过（100% 通过率）
5. 同步生成代码文档到 `.claude/workflow/code-documentation.md`
6. 生成 GREEN 阶段验证报告到 `.claude/workflow/test-execution-report-green.md`
7. 完成后提示触发AI评审

代码生成并测试通过后，自动调用 code-reviewer agent:

使用 code-reviewer agent 评审最近改动：

要求:
1. 仅使用 `git diff` 查看改动，不扫描整个代码库
2. 检查安全性、规范性、性能
3. 生成精简的评审报告到 .claude/workflow/review-report.md

完成后进入 **🚦 人类审查节点 #6**

---

### 🚦 人类审查节点 #6: 代码与文档双评审（GREEN 阶段）

**审查内容**:

✅ **GREEN 阶段验证**:
```bash
cat .claude/workflow/test-execution-report-green.md
```
- 测试全部通过？（100% 通过率）
- GREEN 阶段完成？

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
- 通过 → 输入 "通过"（进入完整测试阶段）
- 修改 → 编辑代码后输入 "继续"
- 重来 → 输入 "重新生成: [问题]"
- 优化 → 输入 "优化: [要求]"

---

## 阶段7: 完整测试执行 + 验收

使用 test-executor agent 执行完整测试套件：

要求:
1. 执行所有测试（P0 + P1 + P2）
2. 收集测试结果
3. 生成最终测试报告到 `.claude/workflow/test-execution-report-final.md`

完成后进入 **🚦 人类审查节点 #7**

---

### 🚦 人类审查节点 #7: 最终验收

**审查内容**:
- ✅ 测试通过率达标？（建议 ≥95%）
- ✅ 功能符合预期？
- ✅ 文档完整？
- ✅ 代码质量达标？
- ✅ TDD 流程完整？（RED → GREEN）

**查看报告**: `cat .claude/workflow/test-execution-report-final.md`

**操作**:
- 通过交付 → 输入 "交付"
- 修复问题 → 输入 "修复: [问题]"
- 下轮迭代 → 输入 "迭代: [新需求]"

---

## 工作流输出

完整 TDD 流程后，`.claude/workflow/` 包含：

```
.claude/workflow/
├── requirements.md                      # 阶段1: 需求文档
├── solution-design.md                   # 阶段2: 技术方案
├── implementation-plan.md               # 阶段3: 实现计划
├── test-plan-framework.md               # 阶段3: 测试计划框架 [新增]
├── documentation-template.md            # 阶段3: 文档框架
├── tdd-test-cases.md                    # 阶段4: TDD 测试用例设计 [新增]
├── test-code-documentation.md           # 阶段5: 测试代码文档 [新增]
├── test-execution-report-red.md         # 阶段5: RED阶段验证报告 [新增]
├── code-documentation.md                # 阶段6: 实现代码文档
├── review-report.md                     # 阶段6: AI评审报告
├── test-execution-report-green.md       # 阶段6: GREEN阶段验证报告 [新增]
└── test-execution-report-final.md       # 阶段7: 最终测试报告
```

---

## Token优化措施

✅ **内联命令预读取**: 使用 `!cat file` 预读取文档，避免agent重复读取
✅ **参数传递**: 通过调用prompt传递内容，agent不再读取文件
✅ **精简文档格式**: 去除冗余，仅保留核心信息
✅ **Agent Memory**: solution-architect等agent使用memory缓存项目信息
✅ **最小化扫描**: 限定代码搜索范围，避免全局扫描
✅ **TDD 优化**: 测试用例设计不涉及代码，测试代码生成仅依赖用例设计

**预期效果**: 相比原6阶段流程，TDD版本 Token 增长 ≤ 20%

---

## 回滚与迭代

任何阶段发现问题：
- 轻微问题 → 本地修改，继续
- 测试用例问题 → 输入 "回退到阶段4"
- 方案问题 → 输入 "回退到阶段2"
- 需求错误 → 输入 "回退到阶段1"
- 质量不达标 → 输入 "进入迭代优化"

## TDD 流程说明

本工作流严格遵循 TDD (测试驱动开发) 流程：

1. **阶段4 - 测试用例设计**: 基于需求设计测试用例（不涉及代码）
2. **阶段5 - RED 阶段**: 生成测试代码，验证测试失败（因为实现不存在）
3. **阶段6 - GREEN 阶段**: 生成实现代码，使测试通过（100% 通过率）
4. **阶段7 - 完整测试**: 执行完整测试套件，最终验收

**TDD 核心价值**:
- ✅ 测试优先，明确验收标准
- ✅ RED → GREEN 循环，确保测试有效
- ✅ 实现代码直接满足测试需求
- ✅ 回归测试，防止功能退化

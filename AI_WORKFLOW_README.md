# AI 代码生成可控闭环工作流系统（TDD版）

这是一套基于 Claude Code Skills + Agents 的可编排、可审查、可迭代的代码生成工作流系统，**完整实现 TDD (测试驱动开发) 流程**。

## 🎯 核心价值

通过 **7阶段门控流程 + 7个人类审查节点 + TDD RED-GREEN 循环**，实现：

- ✅ **TDD 测试驱动**: 测试用例先于代码，RED → GREEN 验证完整
- ✅ **稳定的需求匹配**: 多阶段需求确认，确保方向正确
- ✅ **清晰的代码解释**: 代码与文档同步生成，易于理解和评审
- ✅ **可控的测试规模**: 分级测试策略，避免用例爆炸
- ✅ **完整的流程闭环**: 每步可验证、可追溯、可回滚
- ✅ **增量迭代开发**: 最小单元生成，分阶段验证

---

## 📋 工作流概览

```
需求输入
   ↓
[阶段1: 需求理解与拆解] → 🚦 人类审查 #1
   ↓
[阶段2: 技术方案设计] → 🚦 人类审查 #2
   ↓
[阶段3: 实现计划 + 测试计划框架] → 🚦 人类审查 #3
   ↓
[阶段4: TDD 测试用例设计] → 🚦 人类审查 #4 ⭐ 新增
   ↓
[阶段5: 测试代码生成 + RED验证] → 🚦 人类审查 #5 ⭐ 新增
   ↓
[阶段6: 实现代码 + GREEN验证 + AI评审] → 🚦 人类审查 #6
   ↓
[阶段7: 完整测试执行 + 验收] → 🚦 人类审查 #7
   ↓
交付
```

**TDD 流程亮点**:
- 🔴 **阶段4**: 设计测试用例（基于需求，不看代码）
- 🔴 **阶段5**: 生成测试代码 → 验证失败（RED 阶段）
- 🟢 **阶段6**: 生成实现代码 → 验证通过（GREEN 阶段）
- ✅ **阶段7**: 完整测试套件执行

---

## 🚀 快速开始

### 1. 启动完整工作流

开发新功能时使用：

```bash
/ai-dev-workflow 实现用户登录功能，包含邮箱验证和密码重置
```

或使用快捷命令：

```bash
/start-new-feature 实现用户登录功能
```

### 2. 快速修复模式

修复小bug时使用（跳过部分审查节点）：

```bash
/quick-fix 修复登录页面验证码不显示的问题
```

### 3. 仅评审现有代码

对现有改动进行评审：

```bash
/review-only 最近的认证模块改动
```

---

## 🏗️ 系统架构

### 核心 Agents（8个）

| Agent | 职责 | 关键能力 | TDD 角色 |
|-------|------|---------|---------|
| **requirement-analyzer** | 需求分析专家 | 理解需求、拆解任务、排优先级 | - |
| **solution-architect** | 架构设计师 | 设计方案、评估风险、提供备选 | - |
| **implementation-planner** | 实现规划师 | 生成实现计划、测试计划框架 | 准备测试框架 |
| **test-strategist** | TDD 测试用例设计专家 | 基于需求设计测试用例 | 🔴 测试设计 |
| **test-code-generator** | 测试代码生成专家 | 生成测试代码、RED验证 | 🔴 RED 阶段 |
| **code-generator** | 实现代码生成专家 | 生成实现代码、GREEN验证 | 🟢 GREEN 阶段 |
| **code-reviewer** | 代码评审专家 | 安全性、规范性、性能评审 | 质量保障 |
| **test-executor** | 测试执行器 | 执行完整测试、生成报告 | 最终验收 |

### Skills 编排（4个）

| Skill | 用途 | 使用场景 |
|-------|------|---------|
| **ai-dev-workflow** | 主工作流 | 完整的功能开发流程 |
| **start-new-feature** | 快速启动 | 新功能开发 |
| **quick-fix** | 快速修复 | 小bug修复 |
| **review-only** | 仅评审 | 审查现有代码 |

---

## 🎨 TDD 流程说明

本工作流完整实现 **TDD (测试驱动开发)** 理念：

### RED-GREEN-REFACTOR 循环

```
阶段4: 设计测试用例
   ↓ （基于需求，不看代码）
阶段5: 生成测试代码 → 🔴 RED（测试失败）
   ↓ （验证失败原因：实现不存在）
阶段6: 生成实现代码 → 🟢 GREEN（测试通过）
   ↓ （100% 通过率 + AI评审）
阶段7: 完整测试套件 → ✅ 验收
```

### TDD 核心优势

- ✅ **测试优先**: 在代码编写之前明确验收标准
- ✅ **RED 验证**: 确保测试有效（会失败）
- ✅ **GREEN 驱动**: 实现代码直接满足测试需求
- ✅ **回归保护**: 防止功能退化

### 与传统流程对比

| 传统流程 | TDD 流程 |
|---------|---------|
| 需求 → 代码 → 测试 | 需求 → **测试用例** → 测试代码(RED) → 实现代码(GREEN) |
| 测试依赖代码实现 | 测试独立于代码，基于需求 |
| 无 RED-GREEN 验证 | 完整 RED-GREEN 循环验证 |
| 测试覆盖率可能不足 | 测试优先，覆盖率有保障 |

---

## 🚦 人类审查节点详解

### 节点 #1: 需求确认
- **位置**: 阶段1完成后
- **审查内容**: 需求理解准确性、任务拆解粒度、优先级
- **审查文档**: `.claude/workflow/requirements.md`
- **操作选项**: [通过] [修改] [重新拆解]

### 节点 #2: 方案审查
- **位置**: 阶段2完成后
- **审查内容**: 技术选型、架构设计、改动范围、风险
- **审查文档**: `.claude/workflow/solution-design.md`
- **操作选项**: [通过] [调整方案] [选择备选方案]

### 节点 #3: 计划确认
- **位置**: 阶段3完成后
- **审查内容**: 实现步骤、验证标准、测试计划框架、文档框架
- **审查文档**: `.claude/workflow/implementation-plan.md`, `.claude/workflow/test-plan-framework.md`, `.claude/workflow/documentation-template.md`
- **操作选项**: [通过] [调整计划]

### 节点 #4: TDD 测试用例审查 ⭐ 新增
- **位置**: 阶段4完成后
- **审查内容**: 测试用例设计（基于需求，不涉及代码）
- **审查文档**: `.claude/workflow/tdd-test-cases.md`
- **操作选项**: [通过] [调整用例] [删减冗余]

### 节点 #5: 测试代码与 RED 阶段验证 ⭐ 新增
- **位置**: 阶段5完成后
- **审查内容**:
  - 测试代码质量
  - RED 阶段验证（测试失败是否符合预期）
- **审查文档**:
  - `.claude/workflow/test-code-documentation.md`
  - `.claude/workflow/test-execution-report-red.md`
- **操作选项**: [通过] [修改测试] [重新生成]

### 节点 #6: 实现代码与 GREEN 阶段验证 ⭐
- **位置**: 阶段6完成后
- **审查内容**:
  - GREEN 阶段验证（测试通过，100% 通过率）
  - AI评审报告（安全性、规范性、性能）
  - 代码文档（功能说明、设计逻辑、改动影响）
  - 人工代码审查（业务逻辑、边界处理）
- **审查文档**:
  - `.claude/workflow/test-execution-report-green.md`
  - `.claude/workflow/review-report.md`
  - `.claude/workflow/code-documentation.md`
  - 代码改动 (`git diff`)
- **操作选项**: [通过] [修改] [重新生成] [优化]

### 节点 #7: 最终验收
- **位置**: 阶段7完成后
- **审查内容**: 完整测试通过率、功能验证、交付质量、TDD 流程完整性
- **审查文档**: `.claude/workflow/test-execution-report-final.md`
- **操作选项**: [通过交付] [修复问题] [进入下轮迭代]

---

## 📁 文件结构

```
.claude/
├── agents/                      # 8个专业 Agents
│   ├── requirement-analyzer/
│   ├── solution-architect/
│   ├── implementation-planner/
│   ├── test-strategist/         # TDD 测试用例设计专家
│   ├── test-code-generator/     # ⭐ 新增: TDD RED 阶段
│   ├── code-generator/          # 修改: TDD GREEN 阶段
│   ├── code-reviewer/
│   └── test-executor/
│
├── skills/                      # 4个编排 Skills
│   ├── ai-dev-workflow/         # 修改: 7阶段 TDD 流程
│   ├── start-new-feature/
│   ├── quick-fix/
│   └── review-only/
│
├── workflow/                    # 工作流产出目录
│   ├── requirements.md                      # 阶段1产出
│   ├── solution-design.md                   # 阶段2产出
│   ├── implementation-plan.md               # 阶段3产出
│   ├── test-plan-framework.md               # 阶段3产出 ⭐ 新增
│   ├── documentation-template.md            # 阶段3产出
│   ├── tdd-test-cases.md                    # 阶段4产出 ⭐ 新增
│   ├── test-code-documentation.md           # 阶段5产出 ⭐ 新增
│   ├── test-execution-report-red.md         # 阶段5产出 ⭐ 新增 (RED)
│   ├── code-documentation.md                # 阶段6产出
│   ├── review-report.md                     # 阶段6产出 (AI评审)
│   ├── test-execution-report-green.md       # 阶段6产出 ⭐ 新增 (GREEN)
│   └── test-execution-report-final.md       # 阶段7产出
│
└── workflow-config.json         # 工作流配置 (7个审查节点)
```

---

## 💡 使用技巧

### 1. 查看审查材料

在每个审查节点，使用以下命令查看审查材料：

```bash
# 查看需求文档
cat .claude/workflow/requirements.md

# 查看技术方案
cat .claude/workflow/solution-design.md

# 查看代码改动
git diff

# 查看TDD测试用例设计
cat .claude/workflow/tdd-test-cases.md

# 查看测试代码文档
cat .claude/workflow/test-code-documentation.md

# 查看RED阶段验证报告
cat .claude/workflow/test-execution-report-red.md

# 查看AI评审报告
cat .claude/workflow/review-report.md

# 查看GREEN阶段验证报告
cat .claude/workflow/test-execution-report-green.md

# 查看最终测试报告
cat .claude/workflow/test-execution-report-final.md
```

### 2. 给出反馈

在审查节点的不同反馈方式：

```bash
# 快速通过
通过
continue

# 修改后继续
# 1. 编辑对应文件（如 .claude/workflow/requirements.md）
# 2. 然后输入：
继续

# 重新生成
重新生成: [说明问题]
重新设计: [补充要求]

# 回滚到之前阶段
回退到阶段2
回退到阶段1
```

### 3. 回滚与迭代

任何阶段发现问题都可以回滚：

- **轻微问题**: 直接修改文件，继续流程
- **方案问题**: `回退到阶段2` 重新设计
- **需求理解错误**: `回退到阶段1` 重新分析
- **质量不达标**: `进入迭代优化` 触发优化子流程

---

## ⚙️ 配置说明

编辑 `.claude/workflow-config.json` 可自定义工作流：

```json
{
  "review_gates": {
    "gate_1_requirements": {
      "enabled": true,      // 是否启用此审查节点
      "required": true,     // 是否必须通过
      "timeout_minutes": 30 // 超时时间
    },
    ...
  },
  "quick_fix_mode": {
    "skip_gates": ["gate_2_solution", "gate_3_plan", "gate_5_test"]
  },
  "test_limits": {
    "p0_max": 10,  // P0核心测试用例上限
    "p1_max": 20,  // P1边界测试用例上限
    "p2_max": 10,  // P2异常测试用例上限
    "total_max": 40 // 总用例数上限
  }
}
```

---

## 🧪 验证测试

### 端到端测试场景

测试一个完整的功能开发流程：

```bash
/ai-dev-workflow 实现TODO API，支持增删改查，使用SQLite存储
```

**预期流程**:
1. ✅ 需求分析 → 🚦 人类确认 → 通过
2. ✅ 架构设计（提供2个方案） → 🚦 人类选择 → 选择方案A
3. ✅ 实现规划+测试框架 → 🚦 人类确认 → 通过
4. ✅ TDD测试用例设计 → 🚦 人类审查测试用例 → 通过
5. ✅ 测试代码生成 → 🔴 RED验证(失败) → 🚦 人类审查 → 通过
6. ✅ 实现代码生成 → 🟢 GREEN验证(通过) + AI评审 → 🚦 人类审查 → 通过
7. ✅ 完整测试执行 → 🚦 人类验收 → 通过交付

### 回滚测试场景

测试回滚机制：

```bash
/ai-dev-workflow 实现分布式任务调度系统
```

在阶段4发现架构复杂度过高时：
```bash
回退到阶段2，要求简化方案
```

### 快速修复测试场景

测试快速修复模式：

```bash
/quick-fix 修复用户注册接口返回500错误
```

应跳过方案设计和实现计划阶段，总耗时 < 10分钟。

---

## 🎓 最佳实践

### 1. 何时使用完整工作流？
- ✅ 新功能开发
- ✅ 复杂业务逻辑实现
- ✅ 架构变更
- ✅ 涉及多个模块的改动

### 2. 何时使用快速修复模式？
- ✅ 小bug修复
- ✅ 单文件改动
- ✅ 紧急hotfix
- ✅ 简单的配置调整

### 3. 如何高效审查？
- 📋 先看AI评审报告，关注Critical问题
- 📄 再看代码文档，理解设计意图
- 🔍 最后人工审查业务逻辑和边界情况
- ⏱️ 每个审查节点控制在10-15分钟内

### 4. 如何避免测试爆炸？
- 🎯 优先P0核心功能（≤10个用例）
- ⚖️ 合理分配P1边界（≤20个）和P2异常（≤10个）
- 🚫 明确标注"不测试的内容"
- 🔄 分阶段执行，先P0再P1/P2

---

## 🔄 扩展方向

### 短期（1-2周）
- 增加辅助Agents：refactor-specialist, performance-optimizer, security-auditor
- 集成外部工具：pylint, mypy, bandit, black
- 增强文档生成：API文档、使用示例、变更日志

### 中期（1-2月）
- 工作流可视化：流程图、进度展示、耗时统计
- 智能推荐：基于历史推荐方案和测试用例
- 多人协作：分工审查、意见讨论、历史追溯

### 长期（3-6月）
- 学习与进化：Agent memory记录案例，自动优化流程
- CI/CD集成：GitHub Actions, GitLab CI
- 跨项目复用：公共Agent库、Skill库、企业级共享

---

## 📚 参考资料

- [Claude Code Skills 文档](https://code.claude.com/docs/en/skills.md)
- [Claude Code Subagents 文档](https://code.claude.com/docs/en/sub-agents.md)
- [完整实现计划](/root/.claude/plans/cached-marinating-aho.md)

---

## 🤝 贡献与反馈

如需调整工作流：
1. 编辑对应的 Agent 定义文件 (`.claude/agents/*/AGENT.md`)
2. 编辑对应的 Skill 定义文件 (`.claude/skills/*/SKILL.md`)
3. 更新配置文件 (`.claude/workflow-config.json`)

**系统自动生效**，无需重启或重新部署！

---

**开始使用**: `/ai-dev-workflow [你的需求]`

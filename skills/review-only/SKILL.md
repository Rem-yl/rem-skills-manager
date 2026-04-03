---
name: review-only
description: 仅对现有代码进行评审。Token优化版，仅读取改动文件
disable-model-invocation: true
---

# 代码评审模式 (Token优化版)

仅对现有代码改动进行评审，不生成新代码。

## 使用 code-reviewer agent

对最近的代码改动进行评审：

**目标范围**: $ARGUMENTS

## 评审内容

要求:
1. **仅使用 git diff 查看改动**，不扫描整个代码库
2. **执行安全性检查**
   - SQL注入、XSS、命令注入
   - 硬编码密钥

3. **执行规范性检查**
   - 命名规范
   - 代码风格
   - 注释完整性
   - 错误处理

4. **执行性能检查**
   - N+1查询
   - 不必要的循环
   - 内存泄漏风险

5. **生成精简的评审报告**
   - 输出到 .claude/workflow/review-report.md
   - 标注 Critical/Warning/Suggestion
   - 提供修复建议

## Token优化

✅ 仅读取 git diff 输出
✅ 不扫描整个代码库
✅ 精简报告格式

**预期**: Token使用量比完整流程少 80-90%

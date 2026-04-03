---
name: quick-fix
description: 快速修复bug（跳过部分审查节点）。Token优化版，避免重复读取文件
disable-model-invocation: true
---

# 快速修复模式 (Token优化版)

适用于小bug修复，跳过部分审查节点。

## 简化流程

### 1. 快速需求理解

使用 requirement-analyzer agent 快速理解问题：

**问题**: $ARGUMENTS

要求:
- 快速分析问题
- 输出简化的问题分析到 .claude/workflow/requirements.md

### 2. 直接生成修复代码

使用 code-generator agent（跳过方案设计和实现计划）：

<problem-analysis>
!`cat .claude/workflow/requirements.md 2>/dev/null || echo ""`
</problem-analysis>

基于上述问题分析，直接生成修复：

要求:
- **不要再次读取文件**，使用上方内容
- 定位问题代码
- 生成修复
- 同步更新文档

### 3. AI自动评审

使用 code-reviewer agent 评审修复：

要求:
- 仅使用 `git diff` 查看改动
- 检查安全性和规范性
- 生成简化的评审报告

### 4. 快速测试验证

使用 test-executor agent 验证修复：

要求:
- 运行相关测试
- 确认问题已解决

## Token优化

✅ 内联命令预读取
✅ 最小化文件访问
✅ 仅读取改动代码

**预期**: Token使用量比完整流程少 60-70%

## 注意

- 仅适用于小范围bug修复
- 大功能变更请使用完整工作流
- 仍会进行代码评审和测试

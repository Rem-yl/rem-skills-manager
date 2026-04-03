---
name: quick-fix
description: 快速修复bug（跳过部分审查节点）
disable-model-invocation: true
---

# 快速修复模式

适用于小bug修复，跳过部分审查节点以提高效率。

## 简化流程

1. **快速需求理解**
   使用 requirement-analyzer agent 快速理解问题：
   - 问题描述: $ARGUMENTS
   - 输出简化的问题分析

2. **直接生成修复代码**
   使用 code-generator agent 直接修复（跳过方案设计和实现计划）：
   - 定位问题代码
   - 生成修复
   - 同步更新文档

3. **AI自动评审**
   使用 code-reviewer agent 评审修复：
   - 检查安全性和规范性
   - 生成简化的评审报告

4. **快速测试验证**
   使用 test-executor agent 验证修复：
   - 运行相关测试
   - 确认问题已解决

## 注意事项
- 仅适用于小范围bug修复
- 大功能变更请使用完整工作流
- 仍会进行必要的代码评审和测试

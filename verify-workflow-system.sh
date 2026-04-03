#!/bin/bash

echo "========================================="
echo " AI 代码生成工作流系统验证"
echo "========================================="
echo ""

# 检查 Agents
echo "📦 检查 Agents (7个)..."
agents=(
    "requirement-analyzer"
    "solution-architect"
    "implementation-planner"
    "code-generator"
    "code-reviewer"
    "test-strategist"
    "test-executor"
)

agent_count=0
for agent in "${agents[@]}"; do
    if [ -f ".claude/agents/$agent/AGENT.md" ]; then
        echo "  ✅ $agent"
        ((agent_count++))
    else
        echo "  ❌ $agent (缺失)"
    fi
done
echo "  Total: $agent_count/7"
echo ""

# 检查 Skills
echo "📦 检查 Skills (4个)..."
skills=(
    "ai-dev-workflow"
    "start-new-feature"
    "quick-fix"
    "review-only"
)

skill_count=0
for skill in "${skills[@]}"; do
    if [ -f ".claude/skills/$skill/SKILL.md" ]; then
        echo "  ✅ $skill"
        ((skill_count++))
    else
        echo "  ❌ $skill (缺失)"
    fi
done
echo "  Total: $skill_count/4"
echo ""

# 检查配置文件
echo "📦 检查配置文件..."
if [ -f ".claude/workflow-config.json" ]; then
    echo "  ✅ workflow-config.json"
else
    echo "  ❌ workflow-config.json (缺失)"
fi

if [ -f ".claude/AI_WORKFLOW_README.md" ]; then
    echo "  ✅ AI_WORKFLOW_README.md"
else
    echo "  ❌ AI_WORKFLOW_README.md (缺失)"
fi
echo ""

# 检查工作流输出目录
echo "📦 检查工作流输出目录..."
if [ -d ".claude/workflow" ]; then
    echo "  ✅ .claude/workflow/"
else
    echo "  ❌ .claude/workflow/ (缺失)"
fi
echo ""

# 总结
echo "========================================="
echo " 验证结果"
echo "========================================="
if [ $agent_count -eq 7 ] && [ $skill_count -eq 4 ]; then
    echo "✅ 所有组件已正确安装！"
    echo ""
    echo "🚀 快速开始:"
    echo "   /ai-dev-workflow [需求描述]"
    echo ""
    echo "📚 查看使用文档:"
    echo "   cat .claude/AI_WORKFLOW_README.md"
else
    echo "⚠️  部分组件缺失，请检查安装"
fi
echo ""

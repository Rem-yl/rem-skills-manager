#!/usr/bin/env python3
"""
AI summarization utilities for generating structured reading notes.
"""

import os
import re
from typing import Dict, List, Optional
from anthropic import Anthropic


def build_chapter_prompt(chapter: Dict, book_context: Dict, options: Dict) -> str:
    """
    构建用于章节总结的Claude提示词 - 生成深层级的Markdown列表格式。

    Args:
        chapter: Chapter data with title, content, etc.
        book_context: Book metadata and context
        options: Summarization options (points_per_chapter, detail, etc.)

    Returns:
        XML-formatted prompt string
    """
    prompt = f"""<书籍信息>
  <书名>{book_context['title']}</书名>
  <作者>{book_context['author']}</作者>
  <章节>{chapter['number']}/{book_context['total_chapters']}</章节>
</书籍信息>

<章节内容>
{chapter['content'][:8000]}
</章节内容>

<生成指令>
请用中文提炼本章的核心要点，采用**深层级 Markdown 列表**格式：

**格式要求：**
1. 使用 `-` 符号创建列表项，不要任何标题或标签（如"本章概要"、"核心观点"等）
2. 用缩进（2个空格）+ `-` 符号表示层级关系
3. **必须达到 4-5 层深度**，充分展开每个主要概念
4. 层级结构：
   - 1级（`-`）：主要观点/概念（5-8个）
   - 2级（`  -`）：概念解释/核心要素（每个1级下2-3个）
   - 3级（`    -`）：细节说明/支撑论据（每个2级下2-4个）
   - 4级（`      -`）：具体例子/深层机制（关键3级下1-2个）
   - 5级（`        -`）：补充细节（必要时使用）
5. 每个要点简洁明了，一般一句话
6. 按逻辑组织，采用递进式展开
7. 保留书中的公式（用 LaTeX 格式：`公式` 或 $$公式$$）
8. 完全使用中文

**输出示例（注意层级深度）：**

- 统一时间的消失
  - 牛顿力学的绝对时间观
    - 牛顿对绝对时间的描述
      - 绝对的、真实的和数学的时间，由其特性决定，自身均匀流逝
      - 牛顿力学宣扬存在一个超脱于物质和空间之外的背景：时间
    - 牛顿方程中时间变量`t`的含义
      - 在经典力学框架中，`t`用于表示时间的流逝
      - 告诉我们随着钟表测量的时间，事物如何改变
      - 这个`t`被假定为全宇宙统一的
  - 广义相对论对绝对时间的否定
    - 相对时空观的核心原理
      - 不存在全宇宙统一的"绝对时间"
      - 每个观察者都有自己的"固有时"
    - 时间测量的相对性
      - 不同观察者处在不同引力场中
      - 不同观察者处于不同运动状态
      - 对同一事件的时间测量结果可以不同
        - 接近大质量物体的时间流逝更慢
        - 高速运动的物体时间膨胀效应
  - 统一时间概念的彻底崩溃
    - 根据广义相对论，时间失去了统一性
    - 时间成为局部性、相对性的物理量

**重要提醒：**
- 必须有大量 3级（`    -`）和 4级（`      -`）要点
- 避免只有 1-2 层的浅层结构
- 每个重要概念都要递进式深入展开
- 复杂论证要分解为多层逻辑链条
</生成指令>"""

    return prompt


def parse_chapter_response(response: str, chapter_title: str, chapter_num: int) -> Dict:
    """
    解析Claude的markdown响应。

    Args:
        response: Raw markdown response from Claude
        chapter_title: Title of the chapter
        chapter_num: Chapter number

    Returns:
        Dictionary with parsed notes
    """
    # Clean up response
    response = response.strip()

    # Build formatted markdown
    markdown = f"## 第{chapter_num}章：{chapter_title}\n\n"
    markdown += response
    markdown += "\n"

    return {
        'chapter_num': chapter_num,
        'chapter_title': chapter_title,
        'markdown': markdown,
        'raw_response': response,
    }


def call_claude_api(prompt: str, model: str = "claude-sonnet-4-5") -> str:
    """
    Call Claude API to generate chapter summary.

    Supports both direct Anthropic API and Vertex AI.

    Args:
        prompt: The prompt to send to Claude
        model: Model to use (default: claude-sonnet-4-5)

    Returns:
        Claude's response text

    Raises:
        ValueError: If neither API key nor Vertex config is available
        Exception: If API call fails
    """
    # Check for Vertex AI configuration
    vertex_project = os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID")
    use_vertex = os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1"

    # Check for direct API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if use_vertex and vertex_project:
        # Use Vertex AI
        try:
            from anthropic import AnthropicVertex

            client = AnthropicVertex(
                project_id=vertex_project,
                region=os.environ.get("ANTHROPIC_VERTEX_REGION", "us-east5")
            )

            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text

        except ImportError:
            print("Warning: Vertex AI support requires: pip install anthropic[vertex]")
            print("Falling back to direct API...")
        except Exception as e:
            raise Exception(f"Vertex AI call failed: {e}")

    # Fall back to direct API
    if api_key:
        try:
            client = Anthropic(api_key=api_key)

            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text

        except Exception as e:
            raise Exception(f"Claude API call failed: {e}")

    # No configuration available
    raise ValueError(
        "No API configuration found. Please either:\n"
        "  1. Set ANTHROPIC_API_KEY environment variable, or\n"
        "  2. Configure Vertex AI with ANTHROPIC_VERTEX_PROJECT_ID"
    )


def identify_cross_references(chapters: List[Dict]) -> Dict[str, List[str]]:
    """
    Identify potential cross-references between chapters using keyword similarity.

    Args:
        chapters: List of chapter dictionaries

    Returns:
        Dictionary mapping chapter_id to list of related chapter_ids
    """
    cross_refs = {}

    # Simple keyword-based similarity
    # For each chapter, find chapters with overlapping keywords
    for i, chapter in enumerate(chapters):
        chapter_id = chapter['id']
        chapter_words = set(re.findall(r'\w+', chapter['content'].lower()))

        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'must', 'can', 'shall'}
        chapter_words = chapter_words - stop_words

        # Find related chapters
        related = []
        for j, other_chapter in enumerate(chapters):
            if i == j:
                continue

            other_words = set(re.findall(r'\w+', other_chapter['content'].lower()))
            other_words = other_words - stop_words

            # Calculate Jaccard similarity
            intersection = chapter_words & other_words
            union = chapter_words | other_words

            if len(union) > 0:
                similarity = len(intersection) / len(union)

                # If similarity > threshold, consider related
                if similarity > 0.15:  # Adjust threshold as needed
                    related.append(other_chapter['id'])

        cross_refs[chapter_id] = related

    return cross_refs

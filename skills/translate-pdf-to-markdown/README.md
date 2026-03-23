# PDF论文翻译Skill - 快速参考

将英文PDF学术论文快速翻译成中文Markdown，保留LaTeX公式和图片引用。

## 快速开始

### 使用方法

1. **调用skill**:
   ```
   /translate-pdf-to-markdown
   ```

2. **提供PDF文件路径**:
   ```
   请翻译这篇论文: docs/paper.pdf
   ```

3. **等待翻译完成**，输出文件默认为: `docs/paper_zh.md`

### 一键翻译示例

```
用户: 翻译 research/mmoe_paper.pdf

Claude: [自动执行10步翻译流程]

       翻译完成！
       - 输出: research/mmoe_paper_zh.md
       - 质量: 88.5/100 (良好)
       - 公式: 47个
       - 图片: 6个 (需提取)
```

---

## 核心功能

### ✅ 准确翻译
- 学术专业性和严谨性
- 中文表达流畅自然
- 保持原文逻辑结构

### ✅ LaTeX公式保留
- 行内公式: `$E = mc^2$`
- 块级公式: `$$\sum_{i=1}^{n} x_i$$`
- 编号公式: `\begin{equation}...\end{equation}`
- 自动验证公式语法

### ✅ 图片占位符生成
```markdown
![图1: 模型架构对比](placeholder-figure-1.png)

*Figure 1: Model architecture comparison*

> 原文位置: 第3页
```

### ✅ 表格翻译
```markdown
| 模型 (Model) | 参数量 (Parameters) | AUC |
|-------------|-------------------|-----|
| Shared-Bottom | 1.2M | 0.750 |
| MMoE | 2.3M | 0.785 |
```

### ✅ 术语一致性管理
```markdown
# 首次出现
多任务学习 (Multi-task Learning, MTL) 通过...

# 后续出现
多任务学习在推荐系统中...
MTL方法的优势在于...
```

### ✅ 质量验证报告
- 公式语法验证 (30%)
- 结构完整性 (20%)
- 翻译质量 (25%)
- Markdown格式 (15%)
- 图表处理 (10%)

---

## 输入输出示例

### 输入
```
PDF文件: Multi-gate Mixture-of-Experts for Multi-task Learning
- 11页会议论文
- 包含47个数学公式
- 6个图表
- 4个表格
```

### 输出文件

**1. 主翻译文档** (`paper_zh.md`):
```markdown
# 摘要 (Abstract)

本文提出了多门控专家混合模型 (Multi-gate Mixture-of-Experts, MMoE)，
用于解决多任务学习 (Multi-task Learning, MTL) 中的任务冲突问题...

## 1. 引言 (Introduction)

多任务学习通过在多个相关任务间共享表示来提升泛化能力 [1,2,3]。
传统的共享底层 (Shared-Bottom) 模型使用以下公式:

$$
y_k = h^k(f(x))
$$

其中 $f(x)$ 是共享的特征提取器...

![图1: MMoE模型架构对比](placeholder-figure-1.png)

*Figure 1: Multi-gate Mixture-of-Experts architecture comparison*
```

**2. 质量报告** (`paper_zh_report.md`):
```markdown
# 翻译报告

## 质量评估
- 综合评分: 88.5 / 100
- 评级: 良好 (Good)
- 建议: 需要minor修正

## 发现的问题
- 术语不一致: "Expert" 在第5章仍使用英文
- 图3缺少英文图注

## 后续工作
- 提取6个图片 (详见图片清单)
- 人工review 3个不确定术语
```

**3. 图片提取清单** (`paper_zh_figures.md`):
```markdown
# 图片提取清单

- [ ] 图1: MMoE模型架构对比
      - 文件名: `placeholder-figure-1.png`
      - 原文: Multi-gate Mixture-of-Experts architecture
      - 页码: 3

- [ ] 图2: 训练损失对比
      - 文件名: `placeholder-figure-2.png`
      - 原文: Training loss comparison
      - 页码: 7
```

---

## 配置选项

### 自定义输出路径
```
用户: 翻译 paper.pdf，输出到 translations/paper_chinese.md

Claude: [翻译到指定路径]
```

### 保留特定术语英文
```
用户: 翻译时保留 "Expert" 和 "Gate" 为英文

Claude: [配置 preserve_terms = ['Expert', 'Gate']]
       [执行翻译]
```

### 选择翻译风格
```
用户: 使用通俗易懂的风格翻译

Claude: [设置 style = 'accessible']
       [生成更易读的译文]
```

---

## 工作流程概览

1. **初始化** - 确认文件和配置
2. **PDF提取** - 读取文本、公式、图表
3. **结构分析** - 识别章节、标题层级
4. **术语管理** - 建立术语对照表
5. **分段翻译** - 逐章节翻译内容
6. **公式处理** - 保留和验证LaTeX公式
7. **图表处理** - 生成占位符和翻译表格
8. **格式化** - 规范Markdown格式
9. **质量验证** - 5维度质量检查
10. **输出交付** - 生成文档和报告

---

## 质量评分说明

| 分数范围 | 评级 | 说明 | 建议 |
|---------|-----|------|-----|
| 90-100 | 优秀 (Excellent) | 可直接使用 | 仅需提取图片 |
| 80-89 | 良好 (Good) | 需minor修正 | 检查标记的问题 |
| 70-79 | 及格 (Pass) | 需要改进 | 逐章节review |
| <70 | 不合格 (Fail) | 需重新翻译 | 检查PDF质量 |

---

## 常见问题

### Q: 公式显示为乱码怎么办？
A: 这通常是PDF提取问题。建议：
- 使用非扫描版PDF
- 检查PDF是否包含可复制文本
- 使用质量报告中的建议修正

### Q: 如何提取图片？
A: 推荐方法：
```bash
# 方法1: 使用 pdfimages
pdfimages -png paper.pdf figures/fig

# 方法2: 使用 Adobe Acrobat
工具 → 导出 PDF → 图像 → PNG

# 方法3: 截图工具
直接截取需要的图片
```

### Q: 术语翻译不准确？
A: 翻译后会生成术语review清单，包含：
- 不确定的术语及其翻译
- 备选翻译建议
- 使用上下文

可以手动修改或提供反馈。

### Q: 支持多大的PDF？
A:
- 推荐: <50页
- 支持: 100+页 (会自动分块处理)
- 超大文件建议先分割

### Q: 翻译需要多久？
A: 取决于：
- PDF页数和复杂度
- 公式和图表数量
- API响应速度

通常10-20页论文约需2-5分钟。

---

## 后续步骤建议

翻译完成后：

1. **阅读质量报告**
   - 检查评分和发现的问题
   - 关注需要review的部分

2. **提取图片**
   - 按照图片清单逐个提取
   - 保存为对应的文件名
   - 替换Markdown中的占位符

3. **验证公式渲染**
   - 使用Markdown编辑器预览
   - 或使用在线工具 (如 HackMD, Typora)
   - 确认公式正确显示

4. **人工校对**
   - 重点检查标记的术语
   - 阅读关键章节确认准确性
   - 修正格式问题

5. **发布使用**
   - 导出为PDF (如需要)
   - 分享给团队
   - 用于学习或实现

---

## 技巧和最佳实践

### 提高翻译质量
- 提供高质量PDF (非扫描版)
- 了解论文领域，可提前告知关键术语
- 对于不确定的术语，标记为需要review

### 加速处理
- 小论文 (<20页) 可一次性翻译
- 大论文建议分章节处理
- 复用术语库减少重复工作

### 格式优化
- 翻译后使用Markdown编辑器检查格式
- 调整表格列宽以适应内容
- 添加必要的分隔线和空行

---

## 输出文件清单

| 文件 | 说明 | 是否必需 |
|-----|------|---------|
| `*_zh.md` | 主翻译文档 | ✅ 必需 |
| `*_zh_report.md` | 质量报告 | ✅ 必需 |
| `*_zh_figures.md` | 图片提取清单 | 🔵 有图时需要 |
| `*_zh_terms.json` | 术语对照表 | 🟡 可选 |

---

## 相关资源

**LaTeX公式**:
- [Overleaf数学符号](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)
- [LaTeX在线编辑器](https://www.overleaf.com/)

**Markdown工具**:
- [Typora](https://typora.io/) - 所见即所得编辑器
- [HackMD](https://hackmd.io/) - 在线协作编辑
- [VSCode](https://code.visualstudio.com/) + Markdown插件

**图片提取**:
- [pdfimages](http://www.xpdfreader.com/pdfimages-man.html) - 命令行工具
- Adobe Acrobat - 专业PDF工具

---

## 获取帮助

遇到问题？

1. 查看 `SKILL.md` 获取详细文档
2. 检查 `examples.md` 查看示例
3. 阅读质量报告中的建议
4. 反馈问题以改进skill

---

**版本**: 1.3
**最后更新**: 2024-02-26

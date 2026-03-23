# PDF论文翻译Skill - 测试指南

本文档提供详细的测试用例和验证方法，确保skill正常工作。

---

## Test Case 1: 基础翻译功能测试

### 目标
验证skill能够完成基本的PDF翻译任务

### 测试输入
```
PDF文件: test_data/simple_paper.pdf
- 页数: 4-6页
- 内容: 简单的算法论文
- 公式: 10-15个
- 图表: 2-3个
```

### 执行步骤
```
1. 调用skill: /translate-pdf-to-markdown
2. 提供文件路径: test_data/simple_paper.pdf
3. 等待翻译完成
4. 检查输出文件
```

### 预期输出

**文件存在性**:
- [ ] `simple_paper_zh.md` 存在
- [ ] `simple_paper_zh_report.md` 存在

**内容完整性**:
- [ ] 所有章节都已翻译（摘要、引言、方法、实验、结论）
- [ ] 参考文献保留原格式
- [ ] 作者和机构名保留英文

**格式正确性**:
- [ ] 标题使用 `#` 标记
- [ ] 列表格式正确
- [ ] 公式使用 `$...$` 或 `$$...$$`

### 验证方法

**自动验证**:
```bash
# 检查文件是否生成
test -f simple_paper_zh.md && echo "✓ 翻译文件存在"

# 检查是否包含中文
grep -q '[\u4e00-\u9fa5]' simple_paper_zh.md && echo "✓ 包含中文内容"

# 检查公式数量
formula_count=$(grep -o '\$' simple_paper_zh.md | wc -l)
echo "公式符号数: $formula_count (应为偶数)"
```

**人工验证**:
- 阅读翻译文档，检查语句通顺性
- 对照原文，确认无遗漏章节
- 使用Markdown编辑器预览格式

### 成功标准

- ✅ 所有输出文件生成
- ✅ 内容完整，无缺失章节
- ✅ 质量评分 ≥ 80分
- ✅ 格式符合Markdown规范

---

## Test Case 2: LaTeX公式处理测试

### 目标
验证所有类型的LaTeX公式都能正确保留和验证

### 测试输入
```markdown
测试文档包含以下公式类型:

1. 行内公式: $E = mc^2$
2. 块级公式: $$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$
3. 编号公式: \begin{equation} F = ma \end{equation}
4. 对齐公式: \begin{align} ... \end{align}
5. 矩阵: \begin{bmatrix} ... \end{bmatrix}
6. 分数: $\frac{a}{b}$
7. 求和: $\sum_{i=1}^{n} x_i$
8. 积分: $\int_{0}^{\infty} f(x) dx$
9. 希腊字母: $\alpha, \beta, \gamma$
10. 上下标: $x^2, x_i, x^{2^3}$
```

### 测试脚本

```python
import re

def test_formula_preservation(markdown_content):
    """测试公式保留的完整性"""
    tests_passed = 0
    tests_failed = 0

    # Test 1: 所有$符号成对
    dollar_count = markdown_content.count('$')
    if dollar_count % 2 == 0:
        print("✓ Test 1: $符号成对")
        tests_passed += 1
    else:
        print("✗ Test 1: $符号不成对")
        tests_failed += 1

    # Test 2: 提取所有公式
    inline_formulas = re.findall(r'\$([^$\n]+)\$', markdown_content)
    display_formulas = re.findall(r'\$\$(.*?)\$\$', markdown_content, re.DOTALL)

    print(f"发现行内公式: {len(inline_formulas)}")
    print(f"发现块级公式: {len(display_formulas)}")

    # Test 3: 验证常见LaTeX命令存在
    latex_commands = [
        r'\\frac', r'\\sum', r'\\int', r'\\alpha',
        r'\\beta', r'\\gamma', r'\\nabla'
    ]

    for cmd in latex_commands:
        if re.search(cmd, markdown_content):
            print(f"✓ 找到命令: {cmd}")
            tests_passed += 1
        else:
            print(f"⚠ 未找到命令: {cmd}")

    # Test 4: 检查括号匹配
    for i, formula in enumerate(inline_formulas + display_formulas):
        if is_balanced(formula):
            tests_passed += 1
        else:
            print(f"✗ 公式 {i} 括号不匹配: {formula[:50]}...")
            tests_failed += 1

    print(f"\n测试结果: {tests_passed} 通过, {tests_failed} 失败")
    return tests_failed == 0

def is_balanced(formula):
    """检查括号是否匹配"""
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for char in formula:
        if char in pairs.keys():
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack.pop()] != char:
                return False

    return len(stack) == 0

# 运行测试
with open('output_zh.md', 'r') as f:
    content = f.read()
    test_formula_preservation(content)
```

### 预期结果

```
✓ Test 1: $符号成对
发现行内公式: 15
发现块级公式: 8
✓ 找到命令: \frac
✓ 找到命令: \sum
✓ 找到命令: \int
✓ 找到命令: \alpha
✓ 找到命令: \beta
✓ 找到命令: \gamma
✓ 找到命令: \nabla

测试结果: 23 通过, 0 失败
```

### 手动验证

使用在线LaTeX编辑器测试公式渲染:

1. 访问 https://www.overleaf.com/
2. 创建新文档
3. 复制翻译文档中的公式到Overleaf
4. 验证所有公式正确渲染

### 成功标准

- ✅ 所有$符号成对
- ✅ 括号完全匹配
- ✅ LaTeX命令拼写正确
- ✅ 公式可在Overleaf中渲染

---

## Test Case 3: 术语一致性测试

### 目标
验证专业术语翻译的一致性

### 测试场景

**场景A: 首次出现**
```markdown
原文: Multi-task Learning (MTL) is a ...
预期: 多任务学习 (Multi-task Learning, MTL) 是一种...
```

**场景B: 后续出现**
```markdown
原文: MTL has been widely used in ...
预期: 多任务学习已被广泛应用于... 或 MTL已被广泛应用于...

错误示例: Multi-task Learning已被... (不应再出现英文全称)
```

**场景C: 术语保留**
```markdown
用户配置: preserve_terms = ['Expert', 'Gate']

原文: The Expert network and Gate network ...
预期: Expert 网络和 Gate 网络...
错误: 专家网络和门控网络... (违反了保留规则)
```

### 测试脚本

```python
def test_term_consistency(markdown_content, term_dict):
    """测试术语一致性"""
    issues = []

    for term, info in term_dict.items():
        zh = info['chinese']
        abbr = info.get('abbreviation')

        # 检查首次出现格式
        if abbr:
            first_pattern = f"{zh} \\({term}, {abbr}\\)"
        else:
            first_pattern = f"{zh} \\({term}\\)"

        if not re.search(first_pattern, markdown_content):
            issues.append(f"术语 '{term}' 首次出现格式不正确")

        # 检查后续是否还有英文全称
        # (需要排除首次出现)
        content_after_first = markdown_content.split(first_pattern, 1)
        if len(content_after_first) > 1:
            remaining = content_after_first[1]
            if term in remaining and term not in info.get('preserve', []):
                count = remaining.count(term)
                issues.append(f"术语 '{term}' 在首次出现后仍有{count}处使用英文")

    if issues:
        print("术语一致性问题:")
        for issue in issues:
            print(f"  ✗ {issue}")
        return False
    else:
        print("✓ 术语一致性检查通过")
        return True

# 示例术语字典
term_dict = {
    'Multi-task Learning': {
        'chinese': '多任务学习',
        'abbreviation': 'MTL'
    },
    'Mixture of Experts': {
        'chinese': '专家混合模型',
        'abbreviation': 'MoE'
    }
}

# 运行测试
with open('output_zh.md', 'r') as f:
    content = f.read()
    test_term_consistency(content, term_dict)
```

### 预期输出

```
✓ 术语一致性检查通过
```

### 成功标准

- ✅ 首次出现提供完整中英对照
- ✅ 后续出现仅使用中文或缩写
- ✅ 用户指定保留的术语全程保留英文
- ✅ 无术语混用情况

---

## Test Case 4: 质量评分系统测试

### 目标
验证质量评分系统的准确性和可靠性

### 测试数据

**高质量翻译** (预期分数: 90-100)
```markdown
特征:
- 所有公式正确
- 结构完整
- 术语一致
- 格式规范
- 图表完整
```

**中等质量翻译** (预期分数: 75-85)
```markdown
特征:
- 公式正确
- 结构完整
- 有2-3个术语不一致
- 有1-2个格式小问题
- 图表基本完整
```

**低质量翻译** (预期分数: <70)
```markdown
特征:
- 有公式语法错误
- 缺少章节
- 术语混乱
- 格式问题多
- 图表缺失
```

### 测试方法

```python
def test_quality_scoring():
    """测试质量评分系统"""

    # 测试1: 完美文档
    perfect_doc = create_perfect_translation()
    score1 = calculate_quality_score(perfect_doc)
    assert 90 <= score1 <= 100, f"完美文档评分异常: {score1}"
    print(f"✓ 完美文档评分: {score1}/100")

    # 测试2: 有minor问题的文档
    minor_issues_doc = create_translation_with_minor_issues()
    score2 = calculate_quality_score(minor_issues_doc)
    assert 75 <= score2 < 90, f"Minor问题文档评分异常: {score2}"
    print(f"✓ Minor问题文档评分: {score2}/100")

    # 测试3: 有major问题的文档
    major_issues_doc = create_translation_with_major_issues()
    score3 = calculate_quality_score(major_issues_doc)
    assert score3 < 75, f"Major问题文档评分异常: {score3}"
    print(f"✓ Major问题文档评分: {score3}/100")

    # 测试4: 各维度权重验证
    weights_correct = verify_dimension_weights()
    assert weights_correct, "维度权重不正确"
    print(f"✓ 维度权重正确: formula(30%) + structure(20%) + translation(25%) + markdown(15%) + figures(10%) = 100%")

    print("\n质量评分系统测试通过!")

test_quality_scoring()
```

### 预期输出

```
✓ 完美文档评分: 95/100
✓ Minor问题文档评分: 82/100
✓ Major问题文档评分: 65/100
✓ 维度权重正确: formula(30%) + structure(20%) + translation(25%) + markdown(15%) + figures(10%) = 100%

质量评分系统测试通过!
```

### 成功标准

- ✅ 高质量文档得分 ≥ 90
- ✅ 中等质量文档得分在 75-89
- ✅ 低质量文档得分 < 75
- ✅ 各维度权重和为 100%

---

## Test Case 5: 边界情况测试

### 测试场景

#### 场景1: 空白PDF
```
输入: 只有标题页的PDF
预期: 友好的错误提示
```

**测试**:
```python
def test_empty_pdf():
    result = translate_pdf('test_data/empty.pdf')
    assert result.status == 'error'
    assert '内容不足' in result.message
    print("✓ 空白PDF处理正确")
```

#### 场景2: 超大PDF (100+页)
```
输入: 150页的博士论文
预期: 提示分段处理或自动分块
```

**测试**:
```python
def test_large_pdf():
    result = translate_pdf('test_data/large_thesis.pdf')
    assert result.status in ['chunked', 'warning']
    assert result.chunk_count > 1 or '分段' in result.message
    print("✓ 大型PDF处理正确")
```

#### 场景3: 纯图片PDF (扫描版)
```
输入: 扫描的论文PDF
预期: 提示需要OCR处理
```

**测试**:
```python
def test_scanned_pdf():
    result = translate_pdf('test_data/scanned.pdf')
    assert 'OCR' in result.message or '扫描' in result.message
    print("✓ 扫描PDF检测正确")
```

#### 场景4: 包含特殊字符的PDF
```
输入: 包含特殊Unicode字符、emoji等
预期: 正确处理或转义
```

**测试**:
```python
def test_special_characters():
    result = translate_pdf('test_data/special_chars.pdf')
    content = read_file(result.output_path)

    # 检查特殊字符是否保留
    assert '→' in content  # 箭头符号
    assert '≈' in content  # 约等于
    assert '∈' in content  # 属于

    print("✓ 特殊字符处理正确")
```

#### 场景5: 多列排版PDF
```
输入: 双栏或三栏排版的会议论文
预期: 正确识别阅读顺序
```

**测试**:
```python
def test_multi_column_layout():
    result = translate_pdf('test_data/two_column.pdf')
    content = read_file(result.output_path)

    # 验证章节顺序正确（而非左栏全部、右栏全部）
    intro_pos = content.index('引言')
    method_pos = content.index('方法')
    assert intro_pos < method_pos

    print("✓ 多栏排版处理正确")
```

### 成功标准

- ✅ 所有边界情况都有适当处理
- ✅ 错误信息清晰友好
- ✅ 不会崩溃或产生无效输出

---

## Integration Test: 端到端测试

### 目标
完整测试从调用skill到生成所有输出文件的全流程

### 测试流程

```
Step 1: 调用skill
  → /translate-pdf-to-markdown

Step 2: 提供输入
  → test_data/integration_test.pdf

Step 3: 等待处理
  → 观察各步骤输出

Step 4: 验证输出
  → 检查所有生成的文件

Step 5: 质量验证
  → 运行所有质量检查脚本

Step 6: 人工review
  → 阅读翻译内容确认准确性
```

### 验证清单

**文件生成**:
- [ ] `integration_test_zh.md` 存在且非空
- [ ] `integration_test_zh_report.md` 存在且包含评分
- [ ] `integration_test_zh_figures.md` 存在（如有图片）
- [ ] `integration_test_zh_terms.json` 存在（如配置生成）

**内容质量**:
- [ ] 所有章节完整翻译
- [ ] 公式全部保留
- [ ] 图片占位符完整
- [ ] 表格格式正确
- [ ] 术语一致性良好

**报告准确性**:
- [ ] 质量评分合理（与实际情况一致）
- [ ] 发现的问题真实存在
- [ ] 统计信息准确（公式数、图片数等）
- [ ] 后续建议有用

**可用性**:
- [ ] Markdown在编辑器中正确显示
- [ ] 公式在支持LaTeX的渲染器中正确显示
- [ ] 图片占位符链接格式正确
- [ ] 可以顺利转换为其他格式（如PDF）

### 测试脚本

```bash
#!/bin/bash
# integration_test.sh

echo "开始端到端集成测试..."

# Step 1: 运行翻译
echo "Step 1: 翻译PDF..."
# 这里应该调用skill
# result=$(translate_pdf test_data/integration_test.pdf)

# Step 2: 检查输出文件
echo "Step 2: 检查输出文件..."
files_ok=true

for file in integration_test_zh.md integration_test_zh_report.md; do
    if [ -f "$file" ]; then
        echo "  ✓ $file 存在"
    else
        echo "  ✗ $file 缺失"
        files_ok=false
    fi
done

# Step 3: 运行公式验证
echo "Step 3: 验证公式..."
python3 test_formulas.py integration_test_zh.md

# Step 4: 运行术语验证
echo "Step 4: 验证术语..."
python3 test_terms.py integration_test_zh.md

# Step 5: 检查质量评分
echo "Step 5: 检查质量评分..."
score=$(grep "综合评分" integration_test_zh_report.md | grep -o '[0-9.]*')
echo "  质量评分: $score/100"

if (( $(echo "$score >= 80" | bc -l) )); then
    echo "  ✓ 质量评分合格"
else
    echo "  ✗ 质量评分不合格"
fi

# Step 6: 汇总结果
echo ""
echo "集成测试完成!"
echo "详细结果请查看各测试输出。"
```

### 成功标准

- ✅ 所有步骤无错误
- ✅ 生成所有必需文件
- ✅ 质量评分 ≥ 80
- ✅ 所有自动化测试通过
- ✅ 人工review确认翻译质量

---

## Performance Test: 性能测试

### 测试目标

验证skill在不同规模文档上的性能表现

### 测试用例

| 文档大小 | 页数 | 公式数 | 预期时间 | 内存使用 |
|---------|-----|-------|---------|---------|
| 小型 | 5-10 | 10-20 | 1-2分钟 | <500MB |
| 中型 | 20-30 | 40-60 | 3-5分钟 | <1GB |
| 大型 | 50-80 | 100+ | 8-12分钟 | <2GB |
| 超大型 | 100+ | 200+ | 分块处理 | <2GB |

### 性能测试脚本

```python
import time
import psutil
import os

def test_performance(pdf_path, expected_time_minutes):
    """测试翻译性能"""

    # 记录开始状态
    start_time = time.time()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB

    # 执行翻译
    result = translate_pdf(pdf_path)

    # 记录结束状态
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB

    # 计算指标
    elapsed_time = (end_time - start_time) / 60  # 分钟
    memory_used = end_memory - start_memory

    # 输出结果
    print(f"性能测试结果:")
    print(f"  文件: {pdf_path}")
    print(f"  耗时: {elapsed_time:.2f} 分钟 (预期: {expected_time_minutes} 分钟)")
    print(f"  内存: {memory_used:.2f} MB")

    # 验证是否在预期范围内
    if elapsed_time <= expected_time_minutes * 1.5:  # 允许50%误差
        print(f"  ✓ 性能合格")
        return True
    else:
        print(f"  ✗ 性能不达标")
        return False

# 运行性能测试
test_performance('test_data/small.pdf', expected_time_minutes=2)
test_performance('test_data/medium.pdf', expected_time_minutes=5)
test_performance('test_data/large.pdf', expected_time_minutes=12)
```

### 成功标准

- ✅ 小型文档 < 3分钟
- ✅ 中型文档 < 7.5分钟
- ✅ 大型文档 < 18分钟
- ✅ 内存使用 < 2GB

---

## Regression Test: 回归测试

### 目标
确保skill更新后不会破坏已有功能

### 测试策略

1. **保留基准测试集**:
   - 收集10-20个典型论文
   - 记录翻译结果作为基准

2. **每次更新后运行**:
   - 重新翻译基准测试集
   - 对比新旧结果
   - 确认质量分数不下降

3. **关键指标对比**:
   ```python
   baseline_score = 87.5
   new_score = 89.2

   assert new_score >= baseline_score - 2, "质量下降超过2分"
   ```

### 回归测试脚本

```python
def regression_test(baseline_dir, current_dir):
    """回归测试"""
    passed = 0
    failed = 0

    baseline_files = os.listdir(baseline_dir)

    for filename in baseline_files:
        if not filename.endswith('_zh.md'):
            continue

        baseline_path = os.path.join(baseline_dir, filename)
        current_path = os.path.join(current_dir, filename)

        # 读取基准和当前结果
        baseline_content = read_file(baseline_path)
        current_content = read_file(current_path)

        # 对比质量分数
        baseline_score = extract_score(baseline_path.replace('.md', '_report.md'))
        current_score = extract_score(current_path.replace('.md', '_report.md'))

        # 允许2分以内的波动
        if current_score >= baseline_score - 2:
            print(f"✓ {filename}: {baseline_score} → {current_score}")
            passed += 1
        else:
            print(f"✗ {filename}: {baseline_score} → {current_score} (下降)")
            failed += 1

    print(f"\n回归测试结果: {passed} 通过, {failed} 失败")
    return failed == 0
```

### 成功标准

- ✅ 所有基准测试质量分数不下降超过2分
- ✅ 核心功能正常工作
- ✅ 无新的严重错误

---

## Test Maintenance（测试维护）

### 定期任务

**每周**:
- [ ] 运行完整测试套件
- [ ] 检查是否有新的边界情况
- [ ] 更新测试文档

**每月**:
- [ ] Review测试覆盖率
- [ ] 添加新的测试用例
- [ ] 优化测试脚本

**每季度**:
- [ ] 更新基准测试集
- [ ] 性能基准重新评估
- [ ] 测试文档全面审查

### 测试数据管理

```
test_data/
├── small/          # 小型测试文档 (5-10页)
├── medium/         # 中型测试文档 (20-30页)
├── large/          # 大型测试文档 (50+页)
├── edge_cases/     # 边界情况测试
│   ├── empty.pdf
│   ├── scanned.pdf
│   ├── special_chars.pdf
│   └── multi_column.pdf
└── baseline/       # 回归测试基准
    └── snapshots/
```

---

## Continuous Integration（持续集成）

### CI配置示例

```yaml
# .github/workflows/test-skill.yml
name: Test PDF Translation Skill

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run basic translation tests
      run: |
        python test_basic_translation.py

    - name: Run formula validation tests
      run: |
        python test_formulas.py

    - name: Run term consistency tests
      run: |
        python test_terms.py

    - name: Run quality scoring tests
      run: |
        python test_quality_scoring.py

    - name: Run integration tests
      run: |
        bash integration_test.sh

    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test_results/
```

---

## 总结

完整的测试体系确保PDF翻译skill的质量和可靠性:

1. **基础功能测试** - 验证核心翻译能力
2. **公式处理测试** - 确保LaTeX公式完整性
3. **术语一致性测试** - 验证术语管理准确性
4. **质量评分测试** - 确认评分系统可靠性
5. **边界情况测试** - 处理各种异常情况
6. **集成测试** - 端到端验证完整流程
7. **性能测试** - 确保效率满足要求
8. **回归测试** - 防止功能退化

通过这套完善的测试体系，我们可以持续改进skill质量，为用户提供可靠的PDF论文翻译服务。

---
name: translate-pdf-to-markdown
description: "将英文PDF学术论文翻译成中文Markdown，保留LaTeX公式和图片占位符，确保翻译准确性"
---

# PDF论文翻译Skill

## Overview（概述）

### 目标
将英文PDF学术论文翻译成结构化的中文Markdown文档，同时：
- 保留所有LaTeX数学公式的原始格式
- 为图片生成带有中英文描述的占位符
- 维护原文的章节结构和格式层级
- 确保专业术语翻译的准确性和一致性
- 提供可编辑、易读的Markdown输出

### 核心能力
1. **PDF内容解析**：提取文本、公式、图表、表格信息
2. **学术翻译**：准确翻译学术内容，保持专业性和严谨性
3. **LaTeX处理**：识别、保留和验证数学公式（行内 `$...$`，块级 `$$...$$`）
4. **结构保持**：维护标题层级、列表、引用、表格等Markdown格式
5. **术语管理**：首次出现提供中英对照，后续使用保持一致性
6. **质量验证**：多维度检查翻译质量和格式正确性

### 输入输出说明

**输入**：
- PDF文件路径（绝对或相对路径）
- 可选配置：输出路径、术语保留规则、质量阈值

**输出**：
- Markdown文件（`.md`）
- 翻译质量报告
- 图片提取清单（占位符列表）
- 需要人工review的术语列表

### 质量标准

**公式准确性（关键）**：
- 所有 `$` 符号成对出现
- 括号 `()[]{}` 完整匹配
- LaTeX命令拼写正确（`\sum`, `\frac`, `\mathbb` 等）
- 上下标语法正确（`^{}`, `_{}`）

**翻译质量**：
- 专业术语准确（参考领域权威词典）
- 句子通顺流畅，符合中文表达习惯
- 保持学术严谨性，避免口语化
- 术语一致性：首次中英对照，后续统一

**格式完整性**：
- 标题层级正确（`#`, `##`, `###`）
- 列表格式规范（有序/无序）
- 表格对齐整齐
- 代码块正确标记
- 图片占位符完整

---

## When to Use（使用时机）

### ✅ 触发条件

**明确的翻译需求**：
- 用户提供PDF论文并明确要求翻译
- 提到关键词："翻译论文"、"中文版本"、"PDF转Markdown"
- 需要阅读外文论文但希望有中文参考

**公式和格式要求**：
- 论文包含大量数学公式，需要保留LaTeX格式
- 需要保持原文结构以便对照阅读
- 后续需要编辑或基于翻译内容进行实现

**学术研究场景**：
- 学习前沿技术论文
- 准备论文阅读分享
- 撰写相关综述或实现报告
- 建立个人知识库

### ❌ 不适用场景

**非学术文档**：
- 小说、新闻、博客文章 → 使用通用翻译工具
- 商业文档、合同 → 需要专业翻译服务
- 技术手册（非研究性质） → 考虑机器翻译 + 人工校对

**格式要求不同**：
- 需要保留原PDF排版和样式 → PDF编辑工具
- 输出格式为Word/LaTeX → 需要其他转换工具
- 不需要公式处理的简单文本 → 使用通用翻译

**特殊内容**：
- 纯图片扫描PDF（需要OCR预处理）
- 多语言混合文档（非纯英文）
- 加密或受保护的PDF

---

## 10-Step Translation Workflow（核心工作流）

### Step 1: 初始化和确认

**目标**：收集必要信息，确认翻译需求和配置

**执行步骤**：

1. **确认文件路径**：
   ```
   检查PDF文件是否存在和可读
   验证文件扩展名为 .pdf
   获取文件大小和页数（如果可能）
   ```

2. **询问用户需求**（使用AskUserQuestion）：
   - 输出文件路径（默认：原文件名 + `_zh.md`）
   - 是否保留特定术语的英文原文
   - 翻译风格偏好：学术严谨 vs 通俗易懂
   - 图片占位符格式偏好

3. **设置翻译参数**：
   ```python
   config = {
       'input_pdf': 'path/to/paper.pdf',
       'output_md': 'path/to/paper_zh.md',
       'preserve_terms': [],  # 保持英文的术语列表
       'style': 'academic',   # 'academic' or 'accessible'
       'quality_threshold': 85  # 质量分数阈值
   }
   ```

4. **初始化术语词典**：
   ```python
   term_dict = {}  # 将在Step 4填充
   quality_report = {
       'formula_count': 0,
       'figure_count': 0,
       'table_count': 0,
       'warnings': []
   }
   ```

**输出**：
- 确认的配置参数
- 准备好的数据结构

---

### Step 2: PDF内容提取

**目标**：使用Read tool读取PDF并提取所有可用信息

**执行步骤**：

1. **读取PDF文件**：
   ```
   使用 Read tool 读取完整PDF内容
   如果文件过大（>100页），考虑分页读取
   ```

2. **提取文本内容**：
   ```python
   # PDF内容通常包含：
   # - 纯文本段落
   # - 公式（可能以LaTeX或Unicode符号形式）
   # - 表格（可能以空格对齐的文本）
   # - 图片描述（Figure X: ...）
   # - 参考文献列表
   ```

3. **识别特殊元素**：
   ```python
   # 公式标记
   inline_formulas = find_pattern(r'\$[^$]+\$')
   block_formulas = find_pattern(r'\$\$[^$]+\$\$')

   # 图片引用
   figures = find_pattern(r'Figure\s+(\d+):?\s*(.+?)(?:\n|$)')

   # 表格标记
   tables = identify_table_regions(content)

   # 参考文献
   references = extract_references_section(content)
   ```

4. **记录元数据**：
   ```python
   metadata = {
       'total_pages': get_page_count(),
       'estimated_words': count_words(content),
       'formula_count': len(inline_formulas) + len(block_formulas),
       'figure_count': len(figures),
       'table_count': len(tables)
   }
   ```

**输出**：
- 完整的PDF文本内容
- 识别的公式、图表、表格列表
- 文档元数据

**注意事项**：
- PDF提取可能不完美，公式可能显示为乱码
- 需要后续步骤清理和修正

---

### Step 3: 结构分析

**目标**：解析文档结构，构建章节大纲树

**执行步骤**：

1. **识别标题层级**：
   ```python
   # 常见学术论文结构
   sections = {
       'title': '',        # 论文标题
       'authors': [],      # 作者列表
       'abstract': '',     # 摘要
       'introduction': '', # 引言
       'related_work': '', # 相关工作
       'method': '',       # 方法
       'experiments': '',  # 实验
       'conclusion': '',   # 结论
       'references': []    # 参考文献
   }

   # 识别模式：
   # - 大号字体、粗体 → 主标题
   # - "1. Introduction", "2. Related Work" → 一级标题
   # - "2.1 Background" → 二级标题
   # - "2.1.1 Multi-task Learning" → 三级标题
   ```

2. **构建章节树**：
   ```python
   def build_section_tree(content):
       """
       构建章节结构树
       """
       tree = []
       current_section = None

       # 识别标题模式
       heading_pattern = r'^(\d+(?:\.\d+)*)\s+(.+)$'

       for line in content.split('\n'):
           match = re.match(heading_pattern, line)
           if match:
               number, title = match.groups()
               level = number.count('.')

               section = {
                   'number': number,
                   'title': title,
                   'level': level,
                   'content': [],
                   'subsections': []
               }

               # 添加到树结构
               add_to_tree(tree, section, level)
               current_section = section
           else:
               if current_section:
                   current_section['content'].append(line)

       return tree
   ```

3. **定位关键元素**：
   ```python
   # 摘要位置
   abstract_start = find_section_start('abstract')
   abstract_end = find_section_end('abstract')

   # 参考文献位置
   references_start = find_section_start('references')

   # 图表位置
   for figure in figures:
       figure['section'] = find_containing_section(figure['position'])
   ```

4. **章节编号映射**：
   ```python
   section_mapping = {
       'Abstract': '摘要',
       'Introduction': '引言',
       'Related Work': '相关工作',
       'Method': '方法',
       'Methodology': '方法论',
       'Approach': '方法',
       'Experiments': '实验',
       'Results': '结果',
       'Discussion': '讨论',
       'Conclusion': '结论',
       'References': '参考文献'
   }
   ```

**输出**：
- 章节结构树
- 每个章节的内容范围
- 图表和公式的位置索引

---

### Step 4: 翻译策略制定

**目标**：识别专业术语，建立翻译规则和术语表

**执行步骤**：

1. **识别专业术语**：
   ```python
   def extract_technical_terms(content):
       """
       提取专业术语（首字母大写的短语，可能带缩写）
       """
       # 模式1: Full Term (Abbreviation)
       pattern1 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(([A-Z]{2,})\)'

       # 模式2: 连续大写词（可能是术语）
       pattern2 = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})\b'

       terms = {}
       matches1 = re.findall(pattern1, content)
       for full_term, abbr in matches1:
           terms[full_term] = {
               'abbreviation': abbr,
               'first_occurrence': True,
               'chinese': None,
               'category': 'with_abbr'
           }

       matches2 = re.findall(pattern2, content)
       for term in matches2:
           if term not in terms and is_likely_technical_term(term):
               terms[term] = {
                   'abbreviation': None,
                   'first_occurrence': True,
                   'chinese': None,
                   'category': 'no_abbr'
               }

       return terms
   ```

2. **创建术语对照表**：
   ```python
   # 预定义常见术语翻译
   predefined_terms = {
       'Multi-task Learning': {
           'zh': '多任务学习',
           'abbr': 'MTL',
           'preserve_abbr': True
       },
       'Mixture of Experts': {
           'zh': '专家混合模型',
           'abbr': 'MoE',
           'preserve_abbr': True
       },
       'Neural Network': {
           'zh': '神经网络',
           'abbr': 'NN',
           'preserve_abbr': False
       },
       'Deep Learning': {
           'zh': '深度学习',
           'abbr': 'DL',
           'preserve_abbr': False
       },
       'Convolutional Neural Network': {
           'zh': '卷积神经网络',
           'abbr': 'CNN',
           'preserve_abbr': True
       }
   }

   # 合并提取的术语和预定义术语
   term_dict = merge_term_dictionaries(extracted_terms, predefined_terms)
   ```

3. **确定翻译风格**：
   ```python
   translation_rules = {
       'style': config['style'],  # 'academic' or 'accessible'

       # 专有名词保留规则
       'preserve_as_is': [
           'author_names',      # 作者姓名
           'institution_names', # 机构名称
           'conference_names',  # 会议名称
           'dataset_names'      # 数据集名称（部分）
       ],

       # 术语首次出现格式
       'first_occurrence_format': '{zh} ({en}, {abbr})',

       # 后续出现格式
       'subsequent_format': '{zh}',  # 或 '{abbr}'

       # 句子翻译原则
       'sentence_style': {
           'academic': '保持被动语态，使用书面语',
           'accessible': '适当使用主动语态，更口语化'
       }
   }
   ```

4. **处理特殊元素**：
   ```python
   special_elements = {
       # 数学符号保持英文
       'math_symbols': ['loss function', 'gradient descent', 'optimizer'],

       # 算法名称保持英文
       'algorithms': ['Adam', 'SGD', 'RMSprop', 'LSTM', 'GRU'],

       # 数据集名称（通常保持英文）
       'datasets': ['ImageNet', 'MNIST', 'CIFAR-10', 'MovieLens'],

       # 软件框架名称
       'frameworks': ['TensorFlow', 'PyTorch', 'Keras', 'scikit-learn']
   }
   ```

**输出**：
- 完整的术语对照表（`term_dict`）
- 翻译规则配置（`translation_rules`）
- 需要保留英文的元素列表

---

### Step 5: 分段翻译

**目标**：按章节逐段翻译，保持格式和术语一致性

**执行步骤**：

1. **翻译标题**：
   ```python
   def translate_heading(heading_text, level):
       """
       翻译标题，保持编号和层级
       """
       # 提取编号（如 "2.1"）
       match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', heading_text)
       if match:
           number, title = match.groups()
       else:
           number = None
           title = heading_text

       # 翻译标题
       title_zh = translate_text(title, term_dict)

       # 生成Markdown标题
       prefix = '#' * (level + 1)  # level 0 → #, level 1 → ##
       if number:
           markdown = f"{prefix} {number} {title_zh} ({title})\n"
       else:
           markdown = f"{prefix} {title_zh} ({title})\n"

       return markdown
   ```

2. **翻译正文段落**：
   ```python
   def translate_paragraph(para_text, term_dict):
       """
       翻译段落，处理术语和保持句子结构
       """
       # 1. 识别并保护公式（暂时替换为占位符）
       formulas = []
       def formula_placeholder(match):
           formulas.append(match.group(0))
           return f"__FORMULA_{len(formulas)-1}__"

       # 保护行内公式
       protected_text = re.sub(r'\$[^$]+\$', formula_placeholder, para_text)

       # 2. 识别并处理术语
       for term, info in term_dict.items():
           if term in protected_text:
               if info['first_occurrence']:
                   # 首次出现：中英对照
                   zh = info['chinese']
                   abbr = info.get('abbreviation')
                   if abbr:
                       replacement = f"{zh} ({term}, {abbr})"
                   else:
                       replacement = f"{zh} ({term})"

                   protected_text = protected_text.replace(term, replacement, 1)
                   info['first_occurrence'] = False
               else:
                   # 后续出现：仅中文
                   protected_text = protected_text.replace(term, info['chinese'])

       # 3. 翻译剩余文本
       translated = translate_text_segment(protected_text)

       # 4. 恢复公式
       for i, formula in enumerate(formulas):
           translated = translated.replace(f"__FORMULA_{i}__", formula)

       return translated
   ```

3. **翻译列表**：
   ```python
   def translate_list(list_lines):
       """
       翻译列表，保持Markdown格式
       """
       translated_list = []

       for line in list_lines:
           # 识别列表类型
           if re.match(r'^\s*[-*+]\s+', line):
               # 无序列表
               marker = re.match(r'^(\s*[-*+]\s+)', line).group(1)
               content = line[len(marker):]
               translated_content = translate_paragraph(content, term_dict)
               translated_list.append(f"{marker}{translated_content}")

           elif re.match(r'^\s*\d+\.\s+', line):
               # 有序列表
               marker = re.match(r'^(\s*\d+\.\s+)', line).group(1)
               content = line[len(marker):]
               translated_content = translate_paragraph(content, term_dict)
               translated_list.append(f"{marker}{translated_content}")

       return '\n'.join(translated_list)
   ```

4. **处理引用**：
   ```python
   def translate_with_citations(text):
       """
       翻译包含引用标记的文本
       保留 [1], [2,3], [Smith et al., 2020] 等格式
       """
       # 识别引用模式
       citation_pattern = r'\[(\d+(?:,\s*\d+)*)\]|\[([A-Z][a-z]+\s+et\s+al\.,\s+\d{4})\]'

       # 保护引用
       citations = []
       def citation_placeholder(match):
           citations.append(match.group(0))
           return f"__CITE_{len(citations)-1}__"

       protected = re.sub(citation_pattern, citation_placeholder, text)

       # 翻译文本
       translated = translate_paragraph(protected, term_dict)

       # 恢复引用
       for i, citation in enumerate(citations):
           translated = translated.replace(f"__CITE_{i}__", citation)

       return translated
   ```

5. **术语一致性检查**：
   ```python
   def check_term_consistency(translated_content, term_dict):
       """
       验证术语翻译的一致性
       """
       issues = []

       for term, info in term_dict.items():
           zh = info['chinese']
           occurrences = translated_content.count(zh)

           # 检查是否混用了英文和中文
           if term in translated_content:
               issues.append(f"警告: 术语 '{term}' 在翻译后仍以英文出现")

           # 检查缩写使用
           if info.get('abbreviation'):
               abbr = info['abbreviation']
               abbr_count = translated_content.count(abbr)
               if abbr_count > 0 and occurrences == 0:
                   issues.append(f"警告: 仅使用缩写 '{abbr}'，未使用中文 '{zh}'")

       return issues
   ```

**输出**：
- 逐段翻译的中文内容
- 保持原有格式的Markdown文本
- 术语一致性检查报告

---

### Step 6: LaTeX公式处理

**目标**：准确识别、保留和验证所有数学公式

**执行步骤**：

1. **识别公式类型**：
   ```python
   def extract_all_formulas(content):
       """
       提取所有类型的LaTeX公式
       """
       formulas = {
           'inline': [],      # 行内公式 $...$
           'display': [],     # 块级公式 $$...$$
           'equation': [],    # 编号公式 \begin{equation}
           'align': [],       # 对齐公式 \begin{align}
           'matrix': []       # 矩阵 \begin{matrix}
       }

       # 行内公式: $...$
       inline_pattern = r'\$([^$\n]+)\$'
       formulas['inline'] = re.findall(inline_pattern, content)

       # 块级公式: $$...$$
       display_pattern = r'\$\$([^$]+?)\$\$'
       formulas['display'] = re.findall(display_pattern, content, re.DOTALL)

       # 编号公式: \begin{equation}...\end{equation}
       equation_pattern = r'\\begin\{equation\}(.*?)\\end\{equation\}'
       formulas['equation'] = re.findall(equation_pattern, content, re.DOTALL)

       # 对齐公式: \begin{align}...\end{align}
       align_pattern = r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}'
       formulas['align'] = re.findall(align_pattern, content, re.DOTALL)

       # 矩阵: \begin{matrix}...\end{matrix} (包括 bmatrix, pmatrix等)
       matrix_pattern = r'\\begin\{([bpv]?matrix)\}(.*?)\\end\{\1\}'
       formulas['matrix'] = re.findall(matrix_pattern, content, re.DOTALL)

       return formulas
   ```

2. **公式保留规则**：
   ```python
   def preserve_formula_format(formula_text, formula_type):
       """
       确保公式使用正确的Markdown LaTeX格式
       """
       if formula_type == 'inline':
           # 行内公式: $...$
           if not formula_text.startswith('$'):
               formula_text = f"${formula_text}$"
           return formula_text

       elif formula_type == 'display':
           # 块级公式: $$...$$
           if not formula_text.startswith('$$'):
               formula_text = f"$$\n{formula_text.strip()}\n$$"
           return formula_text

       elif formula_type == 'equation':
           # 编号公式保持原格式
           return f"\\begin{{equation}}\n{formula_text.strip()}\n\\end{{equation}}"

       elif formula_type == 'align':
           # 对齐公式保持原格式
           return f"\\begin{{align}}\n{formula_text.strip()}\n\\end{{align}}"

       return formula_text
   ```

3. **公式语法验证**：
   ```python
   def validate_latex_syntax(formula_str):
       """
       验证LaTeX公式的基本语法正确性
       """
       errors = []

       # 1. 检查括号匹配
       delimiters = {
           '(': ')',
           '[': ']',
           '{': '}',
           '\\left(': '\\right)',
           '\\left[': '\\right]',
           '\\left{': '\\right}'
       }

       stack = []
       i = 0
       while i < len(formula_str):
           # 检查 \left 和 \right
           if formula_str[i:i+6] == '\\left(':
               stack.append('\\left(')
               i += 6
           elif formula_str[i:i+6] == '\\left[':
               stack.append('\\left[')
               i += 6
           elif formula_str[i:i+6] == '\\left{':
               stack.append('\\left{')
               i += 6
           elif formula_str[i:i+7] == '\\right)':
               if not stack or stack[-1] != '\\left(':
                   errors.append("Unmatched \\right)")
               else:
                   stack.pop()
               i += 7
           elif formula_str[i:i+7] == '\\right]':
               if not stack or stack[-1] != '\\left[':
                   errors.append("Unmatched \\right]")
               else:
                   stack.pop()
               i += 7
           elif formula_str[i:i+7] == '\\right}':
               if not stack or stack[-1] != '\\left{':
                   errors.append("Unmatched \\right}")
               else:
                   stack.pop()
               i += 7
           # 检查普通括号
           elif formula_str[i] in '({[':
               stack.append(formula_str[i])
               i += 1
           elif formula_str[i] in ')}]':
               if not stack:
                   errors.append(f"Unmatched closing '{formula_str[i]}'")
               else:
                   expected = delimiters.get(stack[-1])
                   if formula_str[i] != expected:
                       errors.append(f"Mismatched bracket: expected '{expected}', got '{formula_str[i]}'")
                   else:
                       stack.pop()
               i += 1
           else:
               i += 1

       if stack:
           errors.append(f"Unclosed delimiters: {stack}")

       # 2. 检查常见LaTeX命令拼写
       common_commands = [
           r'\\sum', r'\\prod', r'\\int', r'\\oint',
           r'\\frac', r'\\sqrt', r'\\partial',
           r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\theta', r'\\lambda',
           r'\\mathbb', r'\\mathcal', r'\\mathbf', r'\\mathrm',
           r'\\left', r'\\right',
           r'\\begin', r'\\end',
           r'\\text', r'\\cdot', r'\\times', r'\\div'
       ]

       # 检查是否有孤立的反斜杠（可能是拼写错误）
       orphan_backslash = re.findall(r'\\[a-zA-Z]+', formula_str)
       for cmd in orphan_backslash:
           if cmd not in common_commands and not any(cmd.startswith(c) for c in common_commands):
               # 这可能是拼写错误，但不一定（可能是不常见的命令）
               # 作为警告而非错误
               pass

       # 3. 检查 $ 符号成对（仅用于整个文档检查，单个公式内不应有$）
       dollar_count = formula_str.count('$')
       if dollar_count > 0:
           errors.append(f"公式内部包含 $ 符号（应该在公式外部）")

       # 4. 检查常见错误模式
       if '\\frac{' in formula_str:
           # \frac 应该有两个参数
           frac_pattern = r'\\frac\{[^}]*\}\{[^}]*\}'
           if not re.search(frac_pattern, formula_str):
               errors.append("\\frac 命令格式不完整（需要两个大括号参数）")

       if '\\sqrt{' in formula_str:
           # \sqrt 至少有一个参数
           sqrt_pattern = r'\\sqrt(?:\[[^\]]*\])?\{[^}]*\}'
           if not re.search(sqrt_pattern, formula_str):
               errors.append("\\sqrt 命令格式不完整")

       return len(errors) == 0, errors
   ```

4. **公式修复策略**：
   ```python
   def fix_common_formula_errors(formula_str):
       """
       自动修复常见的公式错误
       """
       fixed = formula_str

       # 1. 修复缺失的 $ 符号
       # （这个应该在提取阶段处理，这里作为保险）

       # 2. 修复转义字符
       # 下划线在LaTeX中应该是 \_ （如果在文本中）
       # 但在公式中 _ 用于下标，不需要转义

       # 3. 修复空格问题
       # 移除多余的空格（LaTeX会处理间距）
       fixed = re.sub(r'\s+', ' ', fixed).strip()

       # 4. 修复常见拼写错误
       typo_corrections = {
           r'\\Sum': r'\\sum',
           r'\\Prod': r'\\prod',
           r'\\Int': r'\\int',
           r'\\Frac': r'\\frac',
       }
       for wrong, correct in typo_corrections.items():
           fixed = re.sub(wrong, correct, fixed)

       return fixed
   ```

5. **公式上下文处理**：
   ```python
   def translate_formula_context(text_with_formula):
       """
       翻译包含公式的文本，保持公式完整
       """
       # 示例: "The loss function is $L = -\sum_i y_i \log p_i$."
       # 翻译为: "损失函数为 $L = -\sum_i y_i \log p_i$。"

       # 1. 提取公式并用占位符替换
       formulas = []
       def placeholder(match):
           formulas.append(match.group(0))
           return f"<<<FORMULA_{len(formulas)-1}>>>"

       # 保护所有类型的公式
       protected = text_with_formula
       protected = re.sub(r'\$\$[^$]+?\$\$', placeholder, protected)  # 块级优先
       protected = re.sub(r'\$[^$\n]+?\$', placeholder, protected)    # 行内

       # 2. 翻译文本部分
       translated = translate_paragraph(protected, term_dict)

       # 3. 恢复公式
       for i, formula in enumerate(formulas):
           translated = translated.replace(f"<<<FORMULA_{i}>>>", formula)

       return translated
   ```

6. **公式格式示例**：
   ```markdown
   # 行内公式示例
   模型的输出定义为 $y = f(x)$，其中 $f: \mathbb{R}^d \rightarrow \mathbb{R}^K$ 是神经网络映射。

   # 块级公式示例
   损失函数定义为：

   $$
   \mathcal{L} = \sum_{k=1}^{K} \mathbb{E}_{(x, y_k) \sim \mathcal{D}_k} \left[ l(y_k, f_k(x)) \right]
   $$

   其中 $l(\cdot, \cdot)$ 是任务 $k$ 的损失函数。

   # 对齐公式示例
   多门控专家混合模型的计算过程如下：

   \begin{align}
   g^k(x) &= \text{softmax}(W_{g_k} x) \\
   f^k(x) &= \sum_{i=1}^{n} g^k(x)_i \cdot f_i(x) \\
   y_k &= h^k(f^k(x))
   \end{align}

   # 矩阵示例
   权重矩阵表示为：

   $$
   W = \begin{bmatrix}
   w_{11} & w_{12} & \cdots & w_{1n} \\
   w_{21} & w_{22} & \cdots & w_{2n} \\
   \vdots & \vdots & \ddots & \vdots \\
   w_{m1} & w_{m2} & \cdots & w_{mn}
   \end{bmatrix}
   $$
   ```

**输出**：
- 保留完整格式的公式列表
- 公式验证报告（语法错误）
- 修复后的公式（如果有自动修复）

---

### Step 7: 图片和表格处理

**目标**：为图片生成占位符，翻译表格内容

**执行步骤**：

1. **识别图片引用**：
   ```python
   def extract_figures(content):
       """
       提取论文中的图片信息
       """
       figures = []

       # 模式1: Figure X: Caption
       pattern1 = r'Figure\s+(\d+):?\s*(.+?)(?:\n|$)'
       matches1 = re.findall(pattern1, content, re.MULTILINE)

       for fig_num, caption in matches1:
           figures.append({
               'number': int(fig_num),
               'caption_en': caption.strip(),
               'caption_zh': None,  # 待翻译
               'type': 'figure'
           })

       # 模式2: Fig. X: Caption
       pattern2 = r'Fig\.\s+(\d+):?\s*(.+?)(?:\n|$)'
       matches2 = re.findall(pattern2, content, re.MULTILINE)

       for fig_num, caption in matches2:
           if not any(f['number'] == int(fig_num) for f in figures):
               figures.append({
                   'number': int(fig_num),
                   'caption_en': caption.strip(),
                   'caption_zh': None,
                   'type': 'figure'
               })

       # 按编号排序
       figures.sort(key=lambda x: x['number'])

       return figures
   ```

2. **生成图片占位符**：
   ```python
   def generate_figure_placeholder(figure_info):
       """
       生成图片占位符Markdown
       """
       fig_num = figure_info['number']
       caption_en = figure_info['caption_en']

       # 翻译图片描述
       caption_zh = translate_paragraph(caption_en, term_dict)

       # 生成文件名
       filename = f"placeholder-figure-{fig_num}.png"

       # 生成Markdown
       markdown = f"\n![图{fig_num}: {caption_zh}]({filename})\n\n"
       markdown += f"*Figure {fig_num}: {caption_en}*\n\n"

       # 如果有页码信息，添加
       if 'page' in figure_info:
           markdown += f"> 原文位置: 第{figure_info['page']}页\n\n"

       return markdown
   ```

   **示例输出**：
   ```markdown
   ![图1: 多门控专家混合模型架构。(a) 共享底层模型。(b) 单门控MoE模型。(c) 多门控MoE模型。](placeholder-figure-1.png)

   *Figure 1: Multi-gate Mixture-of-Experts architecture. (a) Shared-Bottom model. (b) One-gate MoE model. (c) Multi-gate MoE model.*

   > 原文位置: 第3页
   ```

3. **表格识别和翻译**：
   ```python
   def identify_tables(content):
       """
       识别论文中的表格
       """
       tables = []

       # 查找 "Table X:" 模式
       table_pattern = r'Table\s+(\d+):?\s*(.+?)(?:\n|$)'
       matches = re.findall(table_pattern, content, re.MULTILINE)

       for table_num, caption in matches:
           # 尝试提取表格内容（基于后续几行）
           # 这部分取决于PDF提取质量
           tables.append({
               'number': int(table_num),
               'caption_en': caption.strip(),
               'caption_zh': None,
               'rows': []  # 待填充
           })

       return tables
   ```

4. **Markdown表格格式化**：
   ```python
   def format_table_markdown(table_data, header_translations):
       """
       生成Markdown格式的表格
       """
       # 表头（中英对照）
       headers_md = []
       for header_en in table_data['headers']:
           header_zh = header_translations.get(header_en, translate_text(header_en))
           headers_md.append(f"{header_zh} ({header_en})")

       # 生成表头行
       md_table = "| " + " | ".join(headers_md) + " |\n"

       # 分隔行
       md_table += "|" + "|".join(["---"] * len(headers_md)) + "|\n"

       # 数据行
       for row in table_data['rows']:
           translated_row = []
           for cell in row:
               # 翻译单元格内容（可能包含公式）
               cell_zh = translate_formula_context(cell)
               translated_row.append(cell_zh)

           md_table += "| " + " | ".join(translated_row) + " |\n"

       return md_table
   ```

   **示例输出**：
   ```markdown
   **表1: 不同模型的性能比较 (Table 1: Performance Comparison of Different Models)**

   | 模型 (Model) | 参数量 (Parameters) | AUC (任务1) | AUC (任务2) |
   |-------------|-------------------|------------|------------|
   | Shared-Bottom | 1.2M | 0.750 | 0.732 |
   | OMoE | 2.1M | 0.768 | 0.751 |
   | MMoE | 2.3M | 0.785 | 0.772 |
   ```

5. **处理子图描述**：
   ```python
   def handle_subfigure_captions(caption_text):
       """
       处理包含子图的描述
       例如: (a) Model A. (b) Model B. (c) Model C.
       """
       # 识别子图模式
       subfig_pattern = r'\(([a-z])\)\s*([^.(]+\.?)'
       matches = re.findall(subfig_pattern, caption_text)

       if matches:
           translated_parts = []
           for letter, sub_caption in matches:
               sub_caption_zh = translate_text(sub_caption.strip())
               translated_parts.append(f"({letter}) {sub_caption_zh}")

           return " ".join(translated_parts)
       else:
           return translate_text(caption_text)
   ```

6. **图表索引生成**：
   ```python
   def generate_figure_index(figures):
       """
       生成图片提取清单
       """
       index = "# 图片提取清单\n\n"
       index += "以下图片需要从PDF中提取：\n\n"

       for fig in figures:
           index += f"- [ ] 图{fig['number']}: {fig['caption_zh']}\n"
           index += f"  - 文件名: `placeholder-figure-{fig['number']}.png`\n"
           index += f"  - 原文: {fig['caption_en']}\n"
           if 'page' in fig:
               index += f"  - 页码: {fig['page']}\n"
           index += "\n"

       return index
   ```

**输出**：
- 图片占位符Markdown
- 翻译后的表格Markdown
- 图片提取清单

---

### Step 8: Markdown格式化

**目标**：确保输出符合标准Markdown格式规范

**执行步骤**：

1. **标题层级规范化**：
   ```python
   def format_headings(content):
       """
       确保标题层级正确
       """
       lines = content.split('\n')
       formatted = []

       for line in lines:
           # 检测标题行
           if re.match(r'^#{1,6}\s+', line):
               # 确保 # 后有空格
               line = re.sub(r'^(#{1,6})(\S)', r'\1 \2', line)

               # 移除多余空格
               line = re.sub(r'^(#{1,6})\s+', r'\1 ', line)

           formatted.append(line)

       return '\n'.join(formatted)
   ```

   **标题层级示例**：
   ```markdown
   # 1. 引言 (Introduction)

   ## 1.1 研究背景 (Background)

   ### 1.1.1 多任务学习 (Multi-task Learning)

   多任务学习通过在多个相关任务间共享表示...

   ### 1.1.2 专家混合模型 (Mixture of Experts)

   专家混合模型是一种集成学习方法...

   ## 1.2 研究动机 (Motivation)

   尽管现有方法取得了成功，但仍存在以下问题...
   ```

2. **列表格式规范**：
   ```python
   def format_lists(content):
       """
       规范化列表格式
       """
       lines = content.split('\n')
       formatted = []
       in_list = False

       for i, line in enumerate(lines):
           # 无序列表
           if re.match(r'^\s*[-*+]\s+', line):
               if not in_list:
                   formatted.append('')  # 列表前加空行
                   in_list = True
               # 统一使用 - 作为标记
               line = re.sub(r'^\s*[*+]\s+', '- ', line)
               formatted.append(line)

           # 有序列表
           elif re.match(r'^\s*\d+\.\s+', line):
               if not in_list:
                   formatted.append('')  # 列表前加空行
                   in_list = True
               formatted.append(line)

           else:
               if in_list and line.strip():
                   formatted.append('')  # 列表后加空行
                   in_list = False
               formatted.append(line)

       return '\n'.join(formatted)
   ```

   **列表示例**：
   ```markdown
   本文的主要贡献包括：

   - 提出了多门控专家混合模型（MMoE），有效解决了任务冲突问题
   - 在多个公开数据集上验证了方法的有效性
   - 提供了详细的理论分析和实验结果

   实验设置如下：

   1. 数据集：使用 Census-income 和 UCI 数据集
   2. 基线模型：Shared-Bottom、L2-Constrained、Cross-Stitch
   3. 评估指标：AUC、准确率、F1分数
   ```

3. **代码块格式**：
   ```python
   def format_code_blocks(content):
       """
       确保代码块格式正确
       """
       # 识别算法伪代码或代码片段
       # 通常在论文中以缩进或特殊标记显示

       # 示例：将算法描述转换为代码块
       algorithm_pattern = r'Algorithm\s+\d+:.*?(?=\n\n|\Z)'

       def format_algorithm(match):
           algo_text = match.group(0)
           # 添加代码块标记
           return f"```\n{algo_text}\n```"

       formatted = re.sub(algorithm_pattern, format_algorithm, content, flags=re.DOTALL)

       return formatted
   ```

   **代码块示例**：
   ```markdown
   MMoE模型的前向传播过程可以用以下伪代码表示：

   ```python
   def mmoe_forward(x, experts, gates, towers):
       """
       MMoE模型前向传播

       参数:
           x: 输入特征 [batch_size, feature_dim]
           experts: Expert网络列表 [n_experts]
           gates: Gate网络列表 [n_tasks]
           towers: Tower网络列表 [n_tasks]
       """
       # Expert outputs
       expert_outputs = [expert(x) for expert in experts]  # n_experts * [batch_size, expert_dim]

       # Task-specific weighted combination
       task_outputs = []
       for k, (gate, tower) in enumerate(zip(gates, towers)):
           g_k = gate(x)  # [batch_size, n_experts]
           f_k = weighted_sum(expert_outputs, g_k)  # [batch_size, expert_dim]
           y_k = tower(f_k)  # [batch_size, output_dim_k]
           task_outputs.append(y_k)

       return task_outputs
   ```
   ```

4. **引用和链接格式**：
   ```python
   def format_citations(content):
       """
       格式化引用和链接
       """
       # 确保引用格式一致
       # [1] -> [1]
       # [2, 3, 4] -> [2,3,4] (移除空格)

       content = re.sub(r'\[(\d+),\s+', r'[\1,', content)

       return content
   ```

5. **强调和特殊标记**：
   ```python
   def apply_emphasis(content):
       """
       应用Markdown强调
       """
       # 加粗重要术语（首次定义时）
       # 斜体用于英文原文

       # 示例：已在术语处理中完成
       # "**多任务学习** (*Multi-task Learning*, MTL)"

       return content
   ```

6. **段落间距**：
   ```python
   def normalize_spacing(content):
       """
       规范化段落间距
       """
       # 移除多余空行（超过2个连续空行）
       content = re.sub(r'\n{3,}', '\n\n', content)

       # 确保章节间有适当间距
       content = re.sub(r'(#{1,6}\s+.+\n)', r'\1\n', content)

       return content
   ```

**最终格式示例**：
```markdown
# 3. 方法 (Method)

## 3.1 多门控专家混合模型 (Multi-gate Mixture-of-Experts)

### 3.1.1 模型架构 (Model Architecture)

多门控专家混合模型 (Multi-gate Mixture-of-Experts, MMoE) [1] 通过引入任务特定的门控网络来解决多任务学习中的任务冲突问题。与共享底层模型 (Shared-Bottom) 不同，MMoE为每个任务学习独立的专家组合权重。

模型定义如下：

$$
f^k(x) = \sum_{i=1}^{n} g^k(x)_i \cdot f_i(x)
$$

其中：
- $f^k(x)$ 是任务 $k$ 的输入表示
- $g^k(x) = \text{softmax}(W_{g_k} x)$ 是任务 $k$ 的门控网络
- $f_i(x)$ 是第 $i$ 个专家网络的输出

### 3.1.2 训练目标 (Training Objective)

MMoE的训练目标是最小化所有任务的联合损失：

$$
\mathcal{L} = \sum_{k=1}^{K} w_k \mathbb{E}_{(x,y_k) \sim \mathcal{D}_k} [l(y_k, h^k(f^k(x)))]
$$

其中 $w_k$ 是任务 $k$ 的权重，$l(\cdot, \cdot)$ 是损失函数。

**关键优势**：

- 参数共享：所有任务共享 Expert 网络，减少参数量
- 任务特化：每个任务通过独立的 Gate 网络学习专属的 Expert 组合
- 可扩展性：易于扩展到多个任务（$K > 2$）

![图2: MMoE模型训练过程示意图](placeholder-figure-2.png)

*Figure 2: Training procedure of MMoE model*
```

**输出**：
- 格式规范的Markdown文档
- 一致的标题、列表、代码块格式
- 正确的引用和链接

---

### Step 9: 质量验证

**目标**：多维度检查翻译质量，确保达到标准

**执行步骤**：

1. **公式语法验证（30%权重）**：
   ```python
   def validate_formula_quality(content):
       """
       验证所有公式的语法正确性
       """
       score = 100
       issues = []

       # 提取所有公式
       formulas = extract_all_formulas(content)

       total_formulas = sum(len(v) for v in formulas.values())
       if total_formulas == 0:
           return 100, []  # 无公式，满分

       error_count = 0

       # 验证每个公式
       for formula_type, formula_list in formulas.items():
           for formula in formula_list:
               is_valid, errors = validate_latex_syntax(formula)
               if not is_valid:
                   error_count += 1
                   issues.append({
                       'type': 'formula_syntax',
                       'formula': formula[:50] + '...' if len(formula) > 50 else formula,
                       'errors': errors
                   })

       # 计算扣分
       error_rate = error_count / total_formulas
       score = max(0, 100 - error_rate * 100)

       return score, issues
   ```

2. **结构完整性验证（20%权重）**：
   ```python
   def validate_structure_completeness(content, original_structure):
       """
       验证文档结构完整性
       """
       score = 100
       issues = []

       # 检查所有主要章节是否存在
       required_sections = ['摘要', '引言', '方法', '实验', '结论', '参考文献']
       missing_sections = []

       for section in required_sections:
           if section not in content:
               missing_sections.append(section)
               score -= 15

       if missing_sections:
           issues.append({
               'type': 'missing_sections',
               'sections': missing_sections
           })

       # 检查标题层级连续性
       headings = re.findall(r'^(#{1,6})\s+(\d+(?:\.\d+)*)\s+', content, re.MULTILINE)
       prev_level = 0
       for heading_marks, number in headings:
           level = len(heading_marks)
           if level > prev_level + 1:
               issues.append({
                   'type': 'heading_skip',
                   'from': prev_level,
                   'to': level,
                   'number': number
               })
               score -= 5
           prev_level = level

       # 检查图表编号连续性
       figure_numbers = [int(n) for n in re.findall(r'图(\d+):', content)]
       if figure_numbers:
           figure_numbers.sort()
           for i, num in enumerate(figure_numbers):
               if num != i + 1:
                   issues.append({
                       'type': 'figure_numbering',
                       'expected': i + 1,
                       'actual': num
                   })
                   score -= 3

       return max(0, score), issues
   ```

3. **翻译质量验证（25%权重）**：
   ```python
   def validate_translation_quality(content, term_dict):
       """
       验证翻译质量
       """
       score = 100
       issues = []

       # 1. 术语一致性检查
       term_inconsistencies = 0
       for term, info in term_dict.items():
           zh = info['chinese']
           abbr = info.get('abbreviation')

           # 检查原英文术语是否仍存在（首次出现除外）
           term_occurrences = len(re.findall(r'\b' + re.escape(term) + r'\b', content))

           # 首次应该是中英对照，后续应只有中文
           expected_first = f"{zh} ({term}" if abbr else f"{zh} ({term})"

           if term_occurrences > 1:  # 超过首次出现
               term_inconsistencies += 1
               issues.append({
                   'type': 'term_inconsistency',
                   'term': term,
                   'chinese': zh,
                   'occurrences': term_occurrences
               })

       if term_inconsistencies > 0:
           score -= min(term_inconsistencies * 3, 30)

       # 2. 检查常见机器翻译错误
       # "的的"、"被被"等重复
       duplicates = re.findall(r'([的被在与和])\1+', content)
       if duplicates:
           score -= len(duplicates) * 2
           issues.append({
               'type': 'duplicate_characters',
               'examples': list(set(duplicates))[:5]
           })

       # "this"、"that" 等未翻译词汇
       untranslated = re.findall(r'\b(this|that|these|those|which|where|when)\b', content.lower())
       if untranslated:
           score -= len(untranslated) * 1
           issues.append({
               'type': 'untranslated_words',
               'count': len(untranslated)
           })

       # 3. 句子通顺性（简单启发式）
       # 检查过长句子（可能翻译不自然）
       sentences = re.split(r'[。!?]', content)
       long_sentences = [s for s in sentences if len(s) > 200]
       if long_sentences:
           score -= len(long_sentences) * 2
           issues.append({
               'type': 'long_sentences',
               'count': len(long_sentences)
           })

       return max(0, score), issues
   ```

4. **Markdown格式验证（15%权重）**：
   ```python
   def validate_markdown_format(content):
       """
       验证Markdown格式正确性
       """
       score = 100
       issues = []

       # 1. 标题格式
       invalid_headings = re.findall(r'^#{1,6}[^\s]', content, re.MULTILINE)
       if invalid_headings:
           score -= len(invalid_headings) * 2
           issues.append({
               'type': 'invalid_heading_format',
               'count': len(invalid_headings)
           })

       # 2. 列表格式
       # 检查列表项后是否有内容
       empty_list_items = re.findall(r'^\s*[-*+]\s*$', content, re.MULTILINE)
       if empty_list_items:
           score -= len(empty_list_items) * 1
           issues.append({
               'type': 'empty_list_items',
               'count': len(empty_list_items)
           })

       # 3. 代码块闭合
       code_blocks = re.findall(r'```', content)
       if len(code_blocks) % 2 != 0:
           score -= 10
           issues.append({
               'type': 'unclosed_code_block',
               'count': len(code_blocks)
           })

       # 4. 链接和图片格式
       invalid_images = re.findall(r'!\[[^\]]*\]\([^)]*$', content)  # 未闭合的图片
       if invalid_images:
           score -= len(invalid_images) * 5
           issues.append({
               'type': 'invalid_image_syntax',
               'count': len(invalid_images)
           })

       invalid_links = re.findall(r'\[[^\]]*\]\([^)]*$', content)  # 未闭合的链接
       if invalid_links:
           score -= len(invalid_links) * 3
           issues.append({
               'type': 'invalid_link_syntax',
               'count': len(invalid_links)
           })

       return max(0, score), issues
   ```

5. **图表处理验证（10%权重）**：
   ```python
   def validate_figures_tables(content, expected_figures, expected_tables):
       """
       验证图表处理完整性
       """
       score = 100
       issues = []

       # 检查所有图片是否有占位符
       actual_figures = len(re.findall(r'!\[图\d+:', content))

       if actual_figures < expected_figures:
           missing = expected_figures - actual_figures
           score -= missing * 10
           issues.append({
               'type': 'missing_figures',
               'expected': expected_figures,
               'actual': actual_figures,
               'missing': missing
           })

       # 检查图片是否有中英文描述
       figures_with_english = len(re.findall(r'\*Figure\s+\d+:', content))
       if figures_with_english < actual_figures:
           score -= (actual_figures - figures_with_english) * 5
           issues.append({
               'type': 'missing_english_caption',
               'count': actual_figures - figures_with_english
           })

       # 检查表格格式
       tables = re.findall(r'\|.+\|', content)
       if len(tables) < expected_tables * 2:  # 至少有表头和数据行
           score -= 10
           issues.append({
               'type': 'missing_or_incomplete_tables'
           })

       return max(0, score), issues
   ```

6. **综合质量评分**：
   ```python
   def calculate_overall_quality(content, metadata):
       """
       计算综合质量分数
       """
       # 各维度权重
       weights = {
           'formula': 0.30,
           'structure': 0.20,
           'translation': 0.25,
           'markdown': 0.15,
           'figures': 0.10
       }

       # 计算各维度分数
       formula_score, formula_issues = validate_formula_quality(content)
       structure_score, structure_issues = validate_structure_completeness(content, metadata)
       translation_score, translation_issues = validate_translation_quality(content, term_dict)
       markdown_score, markdown_issues = validate_markdown_format(content)
       figures_score, figures_issues = validate_figures_tables(
           content,
           metadata['figure_count'],
           metadata['table_count']
       )

       # 加权总分
       overall_score = (
           formula_score * weights['formula'] +
           structure_score * weights['structure'] +
           translation_score * weights['translation'] +
           markdown_score * weights['markdown'] +
           figures_score * weights['figures']
       )

       # 汇总所有问题
       all_issues = {
           'formula': formula_issues,
           'structure': structure_issues,
           'translation': translation_issues,
           'markdown': markdown_issues,
           'figures': figures_issues
       }

       # 生成评级
       if overall_score >= 90:
           grade = '优秀 (Excellent)'
           recommendation = '可直接使用'
       elif overall_score >= 80:
           grade = '良好 (Good)'
           recommendation = '需要minor修正'
       elif overall_score >= 70:
           grade = '及格 (Pass)'
           recommendation = '需要改进'
       else:
           grade = '不合格 (Fail)'
           recommendation = '需要重新翻译'

       return {
           'overall_score': round(overall_score, 2),
           'grade': grade,
           'recommendation': recommendation,
           'dimension_scores': {
               'formula': round(formula_score, 2),
               'structure': round(structure_score, 2),
               'translation': round(translation_score, 2),
               'markdown': round(markdown_score, 2),
               'figures': round(figures_score, 2)
           },
           'issues': all_issues
       }
   ```

**输出示例**：
```
翻译质量报告
==================

综合评分: 87.5 / 100
评级: 良好 (Good)
建议: 需要minor修正

各维度评分:
  - 公式语法 (30%): 95.0 / 100
  - 结构完整性 (20%): 85.0 / 100
  - 翻译质量 (25%): 82.0 / 100
  - Markdown格式 (15%): 90.0 / 100
  - 图表处理 (10%): 88.0 / 100

发现的问题:
  [结构完整性]
    - 标题层级跳跃: 从 H2 直接跳到 H4 (章节 3.2)

  [翻译质量]
    - 术语不一致: "Multi-task Learning" 在首次出现后仍有3处使用英文
    - 检测到2个重复字符: ["的的", "被被"]

  [图表处理]
    - 缺少英文图注: 图3, 图5

需要人工review的部分:
  - 术语 "task-specific gate network" 的翻译 (建议: 任务特定门控网络)
  - 公式 (3) 的上下文翻译准确性
```

---

### Step 10: 输出和后处理

**目标**：保存翻译结果，生成报告和清单

**执行步骤**：

1. **保存Markdown文件**：
   ```python
   # 使用 Write tool 保存翻译后的Markdown
   output_path = config['output_md']
   write_file(output_path, translated_content)
   ```

2. **生成翻译报告**：
   ```python
   def generate_translation_report(metadata, quality_result):
       """
       生成详细的翻译报告
       """
       report = f"""
# 翻译报告

## 文档信息
- 原始文件: {metadata['input_pdf']}
- 输出文件: {metadata['output_md']}
- 总页数: {metadata['total_pages']}
- 字数统计: {metadata['word_count']} (原文) → {metadata['translated_word_count']} (译文)

## 内容统计
- 公式数量: {metadata['formula_count']} (行内: {metadata['inline_formula_count']}, 块级: {metadata['display_formula_count']})
- 图片数量: {metadata['figure_count']}
- 表格数量: {metadata['table_count']}
- 参考文献: {metadata['reference_count']}

## 质量评估
- 综合评分: {quality_result['overall_score']} / 100
- 评级: {quality_result['grade']}
- 建议: {quality_result['recommendation']}

### 各维度评分
- 公式语法: {quality_result['dimension_scores']['formula']} / 100
- 结构完整性: {quality_result['dimension_scores']['structure']} / 100
- 翻译质量: {quality_result['dimension_scores']['translation']} / 100
- Markdown格式: {quality_result['dimension_scores']['markdown']} / 100
- 图表处理: {quality_result['dimension_scores']['figures']} / 100

## 发现的问题
"""

       # 添加各类问题
       for category, issues in quality_result['issues'].items():
           if issues:
               report += f"\n### {category.title()}\n"
               for issue in issues:
                   report += f"- {issue}\n"

       report += f"""
## 后续工作

### 图片提取清单
{generate_figure_extraction_list(metadata['figures'])}

### 需要人工校对的术语
{generate_term_review_list(term_dict)}

### 建议的后续步骤
1. 提取PDF中的图片并替换占位符
2. 人工校对标记的术语翻译
3. 使用Markdown编辑器预览格式
4. 使用LaTeX渲染器验证公式显示
5. 根据质量报告修正发现的问题

---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

       return report
   ```

3. **生成图片提取清单**：
   ```python
   def generate_figure_extraction_list(figures):
       """
       生成图片提取清单
       """
       checklist = "\n以下图片需要从PDF中提取并保存：\n\n"

       for fig in figures:
           checklist += f"- [ ] **图{fig['number']}**: {fig['caption_zh']}\n"
           checklist += f"      - 文件名: `placeholder-figure-{fig['number']}.png`\n"
           checklist += f"      - 原文: {fig['caption_en']}\n"
           if 'page' in fig:
               checklist += f"      - 页码: {fig['page']}\n"
           checklist += f"      - 提取方法: 使用PDF编辑器导出图片，或使用 `pdfimages` 命令\n"
           checklist += "\n"

       return checklist
   ```

4. **生成术语review清单**：
   ```python
   def generate_term_review_list(term_dict):
       """
       生成需要人工review的术语列表
       """
       review_list = "\n以下术语建议人工确认翻译准确性：\n\n"

       # 筛选出不常见或可能有歧义的术语
       for term, info in term_dict.items():
           if info.get('needs_review', False):
               review_list += f"- **{term}** → {info['chinese']}\n"
               if 'context' in info:
                   review_list += f"  - 上下文: {info['context']}\n"
               if 'alternative_translations' in info:
                   review_list += f"  - 备选翻译: {', '.join(info['alternative_translations'])}\n"
               review_list += "\n"

       return review_list
   ```

5. **提供后续建议**：
   ```python
   def generate_recommendations(quality_result):
       """
       基于质量评估生成后续建议
       """
       recommendations = []

       score = quality_result['overall_score']

       if score < 70:
           recommendations.append("建议重新翻译，当前质量不达标")
       elif score < 80:
           recommendations.append("需要较多修正，建议逐章节review")
       elif score < 90:
           recommendations.append("质量良好，仅需minor修正")
       else:
           recommendations.append("翻译质量优秀，可直接使用")

       # 基于具体问题给出建议
       issues = quality_result['issues']

       if issues.get('formula'):
           recommendations.append("优先修正公式语法错误，这会影响文档可读性")

       if issues.get('translation'):
           recommendations.append("检查术语一致性，确保专业术语翻译统一")

       if issues.get('structure'):
           recommendations.append("修复文档结构问题，确保章节完整")

       # 公式验证建议
       if quality_result['dimension_scores']['formula'] < 95:
           recommendations.append("使用在线LaTeX编辑器（如Overleaf）验证公式渲染")

       # 图片提取建议
       if quality_result['dimension_scores']['figures'] < 90:
           recommendations.append("""
提取图片的推荐方法:
  1. 使用 Adobe Acrobat: 工具 → 导出 PDF → 图像 → PNG
  2. 使用命令行: `pdfimages -png input.pdf output_prefix`
  3. 截图工具: 对于复杂图表，直接截图可能更清晰
""")

       return recommendations
   ```

6. **保存所有输出文件**：
   ```python
   # 1. 主要翻译文件
   write_file(config['output_md'], translated_content)

   # 2. 翻译报告
   report_path = config['output_md'].replace('.md', '_report.md')
   write_file(report_path, translation_report)

   # 3. 图片提取清单（可选）
   if metadata['figure_count'] > 0:
       figure_list_path = config['output_md'].replace('.md', '_figures.md')
       write_file(figure_list_path, figure_extraction_list)

   # 4. 术语对照表（可选）
   term_table_path = config['output_md'].replace('.md', '_terms.json')
   write_file(term_table_path, json.dumps(term_dict, ensure_ascii=False, indent=2))
   ```

7. **向用户反馈**：
   ```python
   def provide_user_feedback(metadata, quality_result):
       """
       向用户展示翻译完成信息
       """
       message = f"""
翻译完成！

输出文件:
  - 翻译文档: {metadata['output_md']}
  - 质量报告: {metadata['output_md'].replace('.md', '_report.md')}

质量评分: {quality_result['overall_score']}/100 ({quality_result['grade']})

统计信息:
  - 公式: {metadata['formula_count']} 个
  - 图片: {metadata['figure_count']} 个 (需要提取)
  - 表格: {metadata['table_count']} 个

后续建议:
{chr(10).join(f'  - {r}' for r in generate_recommendations(quality_result))}

查看完整报告以了解详细信息。
"""

       return message
   ```

**输出**：
- 翻译后的Markdown文件
- 翻译质量报告
- 图片提取清单
- 术语对照表（JSON）
- 用户反馈摘要

---

## Key Techniques（关键技术）

### 1. LaTeX公式识别和提取

```python
import re

class FormulaExtractor:
    """LaTeX公式提取器"""

    @staticmethod
    def extract_inline_formulas(text):
        """提取行内公式 $...$"""
        pattern = r'\$([^$\n]+?)\$'
        matches = re.finditer(pattern, text)

        formulas = []
        for match in matches:
            formulas.append({
                'content': match.group(1),
                'full': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'type': 'inline'
            })

        return formulas

    @staticmethod
    def extract_display_formulas(text):
        """提取块级公式 $$...$$"""
        pattern = r'\$\$(.*?)\$\$'
        matches = re.finditer(pattern, text, re.DOTALL)

        formulas = []
        for match in matches:
            formulas.append({
                'content': match.group(1).strip(),
                'full': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'type': 'display'
            })

        return formulas

    @staticmethod
    def extract_equation_environments(text):
        """提取equation环境"""
        pattern = r'\\begin\{equation\}(.*?)\\end\{equation\}'
        matches = re.finditer(pattern, text, re.DOTALL)

        formulas = []
        for match in matches:
            formulas.append({
                'content': match.group(1).strip(),
                'full': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'type': 'equation'
            })

        return formulas

    @classmethod
    def extract_all(cls, text):
        """提取所有公式"""
        all_formulas = []

        # 先提取块级（避免与行内冲突）
        all_formulas.extend(cls.extract_display_formulas(text))
        all_formulas.extend(cls.extract_equation_environments(text))

        # 然后提取行内
        all_formulas.extend(cls.extract_inline_formulas(text))

        # 按位置排序
        all_formulas.sort(key=lambda x: x['start'])

        return all_formulas
```

### 2. 术语管理策略

```python
class TerminologyManager:
    """术语管理器"""

    def __init__(self):
        self.terms = {}
        self.predefined_terms = self._load_predefined()

    def _load_predefined(self):
        """加载预定义术语库"""
        return {
            'Multi-task Learning': {'zh': '多任务学习', 'abbr': 'MTL'},
            'Mixture of Experts': {'zh': '专家混合模型', 'abbr': 'MoE'},
            'Neural Network': {'zh': '神经网络', 'abbr': 'NN'},
            'Deep Learning': {'zh': '深度学习', 'abbr': 'DL'},
            'Gradient Descent': {'zh': '梯度下降', 'abbr': 'GD'},
            'Convolutional Neural Network': {'zh': '卷积神经网络', 'abbr': 'CNN'},
            'Recurrent Neural Network': {'zh': '循环神经网络', 'abbr': 'RNN'},
            'Long Short-Term Memory': {'zh': '长短期记忆网络', 'abbr': 'LSTM'},
        }

    def extract_from_text(self, text):
        """从文本中提取术语"""
        # 模式: Full Term (Abbreviation)
        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(([A-Z]{2,})\)'
        matches = re.findall(pattern, text)

        for full_term, abbr in matches:
            if full_term not in self.terms:
                self.terms[full_term] = {
                    'abbreviation': abbr,
                    'chinese': None,
                    'first_use': True,
                    'occurrences': []
                }

    def get_translation(self, term):
        """获取术语翻译"""
        if term in self.predefined_terms:
            return self.predefined_terms[term]['zh']
        elif term in self.terms and self.terms[term]['chinese']:
            return self.terms[term]['chinese']
        else:
            # 需要翻译
            return None

    def format_first_occurrence(self, term):
        """格式化首次出现"""
        zh = self.get_translation(term)
        if not zh:
            return term  # 无翻译，保持原样

        info = self.predefined_terms.get(term) or self.terms.get(term)
        abbr = info.get('abbreviation')

        if abbr:
            return f"{zh} ({term}, {abbr})"
        else:
            return f"{zh} ({term})"

    def format_subsequent(self, term):
        """格式化后续出现"""
        zh = self.get_translation(term)
        return zh if zh else term
```

### 3. 图片占位符生成

```python
class FigurePlaceholderGenerator:
    """图片占位符生成器"""

    @staticmethod
    def extract_figure_info(text):
        """提取图片信息"""
        figures = []

        # 模式: Figure X: Caption
        pattern = r'Figure\s+(\d+):?\s*(.+?)(?=\n\n|\n[A-Z]|$)'
        matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)

        for match in matches:
            fig_num = int(match.group(1))
            caption = match.group(2).strip()

            # 清理caption（移除换行和多余空格）
            caption = re.sub(r'\s+', ' ', caption)

            figures.append({
                'number': fig_num,
                'caption_en': caption,
                'position': match.start()
            })

        return figures

    @staticmethod
    def translate_caption(caption_en, translator=None):
        """翻译图片描述"""
        # 这里应该调用实际的翻译函数
        # 简化示例：
        if translator:
            return translator(caption_en)
        else:
            return caption_en  # 占位，实际应翻译

    @staticmethod
    def generate_placeholder(fig_num, caption_en, caption_zh, page_num=None):
        """生成Markdown占位符"""
        filename = f"placeholder-figure-{fig_num}.png"

        # 处理子图描述 (a), (b), (c)
        if re.search(r'\([a-z]\)', caption_en):
            # 包含子图
            caption_zh = FigurePlaceholderGenerator._translate_subfigures(caption_en, caption_zh)

        markdown = f"\n![图{fig_num}: {caption_zh}]({filename})\n\n"
        markdown += f"*Figure {fig_num}: {caption_en}*\n"

        if page_num:
            markdown += f"\n> 原文位置: 第{page_num}页\n"

        markdown += "\n"

        return markdown

    @staticmethod
    def _translate_subfigures(caption_en, caption_zh):
        """处理子图描述"""
        # 识别 (a) xxx. (b) yyy. 模式
        subfig_pattern = r'\(([a-z])\)\s*([^.(]+\.?)'

        # 提取子图部分
        subfigs_en = re.findall(subfig_pattern, caption_en)

        if subfigs_en:
            # 假设caption_zh也按顺序翻译了子图
            # 实际应该单独处理每个子图
            pass

        return caption_zh
```

### 4. 表格格式处理

```python
class TableFormatter:
    """表格格式化器"""

    @staticmethod
    def parse_table(table_text):
        """解析文本表格"""
        lines = [line.strip() for line in table_text.split('\n') if line.strip()]

        if not lines:
            return None

        # 假设第一行是表头
        headers = re.split(r'\s{2,}|\t', lines[0])

        # 剩余行是数据
        rows = []
        for line in lines[1:]:
            cells = re.split(r'\s{2,}|\t', line)
            rows.append(cells)

        return {
            'headers': headers,
            'rows': rows
        }

    @staticmethod
    def translate_table(table_data, translator, term_dict):
        """翻译表格内容"""
        translated_headers = []
        for header in table_data['headers']:
            header_zh = translator(header, term_dict)
            translated_headers.append((header, header_zh))

        translated_rows = []
        for row in table_data['rows']:
            translated_row = []
            for cell in row:
                # 单元格可能包含公式，需要保护
                cell_zh = translator(cell, term_dict)
                translated_row.append(cell_zh)
            translated_rows.append(translated_row)

        return {
            'headers': translated_headers,
            'rows': translated_rows
        }

    @staticmethod
    def format_markdown_table(translated_table):
        """生成Markdown表格"""
        headers_md = []
        for header_en, header_zh in translated_table['headers']:
            headers_md.append(f"{header_zh} ({header_en})")

        # 表头行
        md = "| " + " | ".join(headers_md) + " |\n"

        # 分隔行
        md += "|" + "|".join(["---"] * len(headers_md)) + "|\n"

        # 数据行
        for row in translated_table['rows']:
            md += "| " + " | ".join(row) + " |\n"

        return md
```

### 5. 文档结构分析

```python
class DocumentStructureAnalyzer:
    """文档结构分析器"""

    @staticmethod
    def extract_headings(text):
        """提取所有标题"""
        headings = []

        # 模式: 1. Title, 1.1 Subtitle, 1.1.1 Sub-subtitle
        pattern = r'^(\d+(?:\.\d+)*)\s+(.+)$'

        for i, line in enumerate(text.split('\n')):
            match = re.match(pattern, line.strip())
            if match:
                number = match.group(1)
                title = match.group(2)
                level = number.count('.')

                headings.append({
                    'number': number,
                    'title': title,
                    'level': level,
                    'line': i
                })

        return headings

    @staticmethod
    def build_hierarchy(headings):
        """构建层级树"""
        root = {'children': [], 'level': -1}
        stack = [root]

        for heading in headings:
            node = {
                'number': heading['number'],
                'title': heading['title'],
                'level': heading['level'],
                'children': []
            }

            # 找到父节点
            while stack and stack[-1]['level'] >= heading['level']:
                stack.pop()

            if stack:
                stack[-1]['children'].append(node)

            stack.append(node)

        return root['children']

    @staticmethod
    def identify_sections(text):
        """识别标准章节"""
        sections = {
            'abstract': None,
            'introduction': None,
            'related_work': None,
            'method': None,
            'experiments': None,
            'results': None,
            'discussion': None,
            'conclusion': None,
            'references': None
        }

        section_patterns = {
            'abstract': r'(?i)^abstract\s*$',
            'introduction': r'(?i)^\d+\.?\s*introduction\s*$',
            'related_work': r'(?i)^\d+\.?\s*related\s+work\s*$',
            'method': r'(?i)^\d+\.?\s*(method|methodology|approach)\s*$',
            'experiments': r'(?i)^\d+\.?\s*experiments?\s*$',
            'results': r'(?i)^\d+\.?\s*results\s*$',
            'discussion': r'(?i)^\d+\.?\s*discussion\s*$',
            'conclusion': r'(?i)^\d+\.?\s*conclusions?\s*$',
            'references': r'(?i)^references\s*$'
        }

        lines = text.split('\n')
        for i, line in enumerate(lines):
            for section_name, pattern in section_patterns.items():
                if re.match(pattern, line.strip()):
                    sections[section_name] = i

        return sections
```

---

## Anti-Patterns（常见错误）

### ❌ 错误1: 破坏LaTeX公式格式

**错误示例**:
```markdown
# 错误：丢失$符号
模型输出为 y = f(x)，其中 f 是神经网络函数。

# 错误：公式被翻译
损失函数为 $损失 = -求和_i y_i 对数 p_i$

# 错误：括号不匹配
$$
f(x = \sum_{i=1}^{n} w_i x_i
$$
```

**正确示例**:
```markdown
# 正确：保留完整公式
模型输出为 $y = f(x)$，其中 $f$ 是神经网络函数。

# 正确：公式完全不翻译
损失函数为 $L = -\sum_i y_i \log p_i$

# 正确：括号完整匹配
$$
f(x) = \sum_{i=1}^{n} w_i x_i
$$
```

### ❌ 错误2: 术语翻译不一致

**错误示例**:
```markdown
# 第一次出现
本文提出多任务学习 (Multi-task Learning, MTL) 方法...

# 第二次出现
Multi-task Learning 在推荐系统中广泛应用...  # 应该用中文

# 第三次出现
MTL方法通过共享表示...  # 可以，使用缩写

# 第四次出现
多任务学习 (MTL) 的优势在于...  # 不需要再次括号
```

**正确示例**:
```markdown
# 第一次出现：完整中英对照
本文提出多任务学习 (Multi-task Learning, MTL) 方法...

# 后续出现：仅中文或缩写
多任务学习在推荐系统中广泛应用...
MTL方法通过共享表示...
多任务学习的优势在于...
```

### ❌ 错误3: 图片占位符不规范

**错误示例**:
```markdown
# 错误：无中文描述
![Figure 1](fig1.png)

# 错误：中英文混用
![图1: Model architecture](figure-1.png)

# 错误：缺少英文原文
![图1: 模型架构对比](placeholder-figure-1.png)
```

**正确示例**:
```markdown
# 正确：完整的中英文描述
![图1: 模型架构对比](placeholder-figure-1.png)

*Figure 1: Model architecture comparison*

> 原文位置: 第3页
```

### ❌ 错误4: 表格对齐破坏

**错误示例**:
```markdown
# 错误：对齐符号不一致
| 模型 | 参数量 | AUC
| Shared-Bottom | 1.2M | 0.750 |
|MMoE|2.3M|0.785|

# 错误：缺少表头分隔行
| 模型 (Model) | 参数量 (Parameters) |
| Shared-Bottom | 1.2M |
```

**正确示例**:
```markdown
# 正确：对齐整齐，格式完整
| 模型 (Model) | 参数量 (Parameters) | AUC (任务1) |
|-------------|-------------------|-----------|
| Shared-Bottom | 1.2M | 0.750 |
| MMoE | 2.3M | 0.785 |
```

### ❌ 错误5: 章节结构混乱

**错误示例**:
```markdown
# 1. Introduction
引言部分内容...

## Background  # 缺少章节编号
背景部分...

### 1.2.1 Multi-task Learning  # 编号跳跃（缺少1.1和1.2）
多任务学习内容...

# Related Work  # 缺少主章节编号
相关工作...
```

**正确示例**:
```markdown
# 1. 引言 (Introduction)
引言部分内容...

## 1.1 研究背景 (Background)
背景部分...

### 1.1.1 多任务学习 (Multi-task Learning)
多任务学习内容...

### 1.1.2 专家混合模型 (Mixture of Experts)
专家混合模型内容...

## 1.2 研究动机 (Motivation)
研究动机...

# 2. 相关工作 (Related Work)
相关工作内容...
```

### ❌ 错误6: 引用格式错误

**错误示例**:
```markdown
# 错误：引用被翻译
根据文献【1】的研究...  # 应该用英文方括号

# 错误：引用格式不一致
一些研究 [1, 2, 3] 表明...
其他工作[4][5][6]也发现...  # 应该合并

# 错误：作者引用翻译
史密斯等人 (Smith et al., 2020) 提出...  # 作者名应保留英文
```

**正确示例**:
```markdown
# 正确：引用格式统一
根据文献 [1] 的研究...

# 正确：多个引用合并
一些研究 [1,2,3] 表明...
其他工作 [4,5,6] 也发现...

# 正确：作者名保留英文
Smith et al. [7] 提出...
```

### ❌ 错误7: 代码块标记缺失

**错误示例**:
```markdown
# 错误：算法没有代码块包裹
Algorithm 1: MMoE Forward Pass
Input: x, experts, gates
Output: task predictions
1: for each task k do
2:   g_k = gate_k(x)
3:   f_k = sum(g_k * experts(x))
4: end for
```

**正确示例**:
````markdown
# 正确：使用代码块
```
Algorithm 1: MMoE Forward Pass
Input: x, experts, gates
Output: task predictions
1: for each task k do
2:   g_k = gate_k(x)
3:   f_k = sum(g_k * experts(x))
4: end for
```
````

---

## Integration Points（集成要点）

### 1. 与Read工具集成

```python
# 读取PDF文件
pdf_content = read_tool.read(pdf_path, pages="all")

# 如果PDF很大，分页读取
if total_pages > 50:
    for i in range(1, total_pages + 1, 10):
        chunk = read_tool.read(pdf_path, pages=f"{i}-{min(i+9, total_pages)}")
        process_chunk(chunk)
```

### 2. 与Write工具集成

```python
# 保存主翻译文件
write_tool.write(output_md_path, translated_content)

# 保存质量报告
write_tool.write(report_path, quality_report)

# 保存术语对照表
write_tool.write(terms_json_path, json.dumps(term_dict, ensure_ascii=False, indent=2))
```

### 3. 术语数据库（可选扩展）

如果需要维护持久化的术语库：

```python
# ~/.claude/translation/terminology.json
{
  "machine_learning": {
    "Multi-task Learning": {"zh": "多任务学习", "abbr": "MTL"},
    "Transfer Learning": {"zh": "迁移学习", "abbr": "TL"},
    ...
  },
  "computer_vision": {
    "Convolutional Neural Network": {"zh": "卷积神经网络", "abbr": "CNN"},
    ...
  }
}
```

### 4. 质量检查工具（可选）

可以创建独立的LaTeX验证脚本：

```bash
# validate_latex.sh
#!/bin/bash
# 提取Markdown中的所有公式并验证

grep -oP '\$[^$]+\$' "$1" | while read formula; do
    echo "Checking: $formula"
    # 可以调用外部LaTeX验证器
done
```

### 5. 输出格式选项

支持不同的输出配置：

```python
output_options = {
    'format': 'standard',  # 'standard', 'with_toc', 'chapters'

    'include_toc': True,  # 是否生成目录

    'split_by_chapter': False,  # 是否分章节输出（长论文）

    'preserve_page_numbers': True,  # 是否保留页码信息

    'figure_placeholder_style': 'detailed'  # 'simple', 'detailed'
}
```

---

## Checklist（执行清单）

### 翻译前准备

- [ ] 确认PDF文件路径和可读性
- [ ] 快速浏览论文，了解主题领域和专业术语
- [ ] 确定输出文件路径和命名
- [ ] 询问用户特殊需求（保留术语、翻译风格等）
- [ ] 检查是否有可用的领域术语库

### 翻译过程检查

- [ ] **Step 1**: 完成初始化和配置确认
- [ ] **Step 2**: 成功提取PDF内容
- [ ] **Step 3**: 完成文档结构分析，识别所有章节
- [ ] **Step 4**: 建立术语对照表，包含所有专业术语
- [ ] **Step 5**: 逐段翻译，保持格式一致
- [ ] **Step 6**: 所有LaTeX公式已保留并验证
- [ ] **Step 7**: 生成所有图片占位符和表格翻译
- [ ] **Step 8**: Markdown格式规范化完成
- [ ] **Step 9**: 运行5维度质量检查
- [ ] **Step 10**: 生成翻译报告和清单

### 翻译后验证

- [ ] 公式语法验证通过（无未匹配括号、缺失$符号）
- [ ] 术语一致性检查通过（首次对照，后续统一）
- [ ] 文档结构完整（所有章节都已翻译）
- [ ] 标题层级正确（编号连续，无跳跃）
- [ ] 图片占位符完整（中英文描述齐全）
- [ ] 表格格式整齐（对齐一致）
- [ ] Markdown语法正确（无未闭合的代码块、链接等）
- [ ] 综合质量分数 ≥ 85分

### 交付文件

- [ ] 主翻译文档（`.md`）
- [ ] 质量报告（`_report.md`）
- [ ] 图片提取清单（`_figures.md`，如有图片）
- [ ] 术语对照表（`_terms.json`，可选）
- [ ] 向用户提供后续建议

---

## Usage Examples（使用示例）

### 示例1: 基本使用

```
用户: /translate-pdf-to-markdown

Claude: 好的，我将帮您翻译PDF学术论文。请提供PDF文件路径。

用户: docs/mmoe_paper.pdf

Claude: [执行10步翻译流程]
       [生成 docs/mmoe_paper_zh.md]

       翻译完成！

       输出文件:
         - 翻译文档: docs/mmoe_paper_zh.md
         - 质量报告: docs/mmoe_paper_zh_report.md

       质量评分: 88.5/100 (良好)

       统计信息:
         - 公式: 47 个
         - 图片: 6 个 (需要提取)
         - 表格: 4 个

       后续建议:
         - 质量良好，仅需minor修正
         - 提取图片的推荐方法: 使用 pdfimages 命令
         - 检查术语一致性，确保专业术语翻译统一

       查看完整报告以了解详细信息。
```

### 示例2: 自定义配置

```
用户: 翻译这篇论文，但保留所有 "Expert" 和 "Gate" 术语为英文

Claude: 好的，我将保留 "Expert" 和 "Gate" 为英文。请提供PDF路径。

用户: research/papers/mixture_of_experts.pdf

Claude: [配置 preserve_terms = ['Expert', 'Gate']]
       [执行翻译]

       翻译完成！术语 "Expert" 和 "Gate" 已保留英文原文。
       ...
```

### 示例3: 质量不达标的处理

```
Claude: [完成翻译]
       [质量评分: 68/100 (不合格)]

       翻译质量报告
       ==================
       综合评分: 68 / 100
       评级: 不合格 (Fail)
       建议: 需要重新翻译

       主要问题:
         - 公式语法错误: 12处未匹配的括号
         - 结构问题: 缺少"实验"和"讨论"章节
         - 术语不一致: "Multi-task Learning"有5处未统一

       建议: 由于质量分数低于70分，建议检查PDF提取质量或重新翻译。

用户: 能否修复这些问题？

Claude: 好的，我将重新处理这些问题：
       1. 修复所有公式语法错误
       2. 重新提取"实验"和"讨论"章节
       3. 统一术语翻译

       [重新执行相关步骤]
       [新质量评分: 86/100]

       问题已修复，质量提升至"良好"级别。
```

---

## Best Practices（最佳实践）

### 1. 翻译前充分理解论文领域

- 快速阅读摘要和引言，了解研究方向
- 识别核心概念和关键术语
- 查阅领域权威词典，确定术语标准翻译

### 2. 保持公式绝对完整

- **永远不要翻译公式内容**
- 公式是跨语言通用的数学语言
- 仅翻译公式前后的说明文字

### 3. 术语首次定义要完整

```markdown
# 好的做法
多任务学习 (Multi-task Learning, MTL) 是一种...

# 不好的做法
多任务学习 (MTL) 是一种...  # 缺少英文全称
MTL (Multi-task Learning) 是一种...  # 中英文顺序错误
```

### 4. 图表处理要规范

- 所有图片必须有占位符
- 图片描述必须中英对照
- 表格表头要提供中英文

### 5. 保持Markdown格式一致性

- 统一使用 `-` 作为无序列表标记
- 标题后统一加空行
- 代码块使用 ` ``` ` 包裹

### 6. 质量优先于速度

- 宁可多花时间验证公式，也不要产生语法错误
- 术语不确定时，标记为需要review
- 质量分数低于80时，主动提示用户检查

### 7. 提供完整的后续指导

- 清晰的图片提取清单
- 术语review建议
- 公式渲染验证方法

---

## Performance Considerations（性能考虑）

### 处理大型PDF（100+页）

```python
# 分块处理策略
def translate_large_pdf(pdf_path, chunk_size=20):
    total_pages = get_page_count(pdf_path)

    for start_page in range(1, total_pages + 1, chunk_size):
        end_page = min(start_page + chunk_size - 1, total_pages)

        chunk_content = read_pdf_pages(pdf_path, start_page, end_page)
        chunk_translated = translate_chunk(chunk_content)

        # 保存中间结果
        save_chunk(chunk_translated, chunk_num=start_page // chunk_size)

    # 合并所有chunk
    merge_chunks()
```

### 公式验证优化

```python
# 缓存验证结果，避免重复检查
formula_cache = {}

def validate_with_cache(formula):
    formula_hash = hash(formula)

    if formula_hash in formula_cache:
        return formula_cache[formula_hash]

    result = validate_latex_syntax(formula)
    formula_cache[formula_hash] = result

    return result
```

---

## Troubleshooting（故障排除）

### 问题1: PDF提取质量差，公式显示为乱码

**原因**: PDF使用特殊编码或嵌入字体

**解决方案**:
- 使用更高质量的PDF（非扫描版）
- 尝试使用专业PDF提取工具预处理
- 手动校对公式部分

### 问题2: 翻译后公式无法渲染

**原因**: 公式语法错误或特殊LaTeX包依赖

**解决方案**:
- 运行公式语法验证
- 使用在线LaTeX编辑器测试
- 检查是否使用了特殊宏或包

### 问题3: 术语翻译不准确

**原因**: 自动翻译质量问题或领域专业性

**解决方案**:
- 标记为需要人工review
- 提供多个备选翻译
- 建立领域术语库

### 问题4: 图片提取困难

**原因**: PDF图片嵌入方式特殊

**解决方案**:
```bash
# 使用 pdfimages 工具
pdfimages -png input.pdf output_prefix

# 或使用 ImageMagick
convert -density 300 input.pdf[page_num] output.png
```

---

## Version History（版本历史）

- **v1.0** (2024-01): 初始版本，支持基本翻译功能
- **v1.1** (2024-02): 增强LaTeX公式验证
- **v1.2** (2024-03): 添加术语一致性检查
- **v1.3** (当前): 完整的10步工作流和5维质量验证

---

## References（参考资源）

**LaTeX资源**:
- LaTeX数学符号: https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols
- LaTeX公式编辑器: https://www.overleaf.com/
- MathJax文档: https://docs.mathjax.org/

**Markdown规范**:
- CommonMark规范: https://commonmark.org/
- GitHub Flavored Markdown: https://github.github.com/gfm/

**学术翻译指南**:
- 科技术语翻译规范
- 学术论文翻译最佳实践

---

**Skill创建时间**: 2024-02-26
**最后更新**: 2024-02-26
**维护者**: Claude Code Team

# PDF论文翻译Skill - 详细示例

本文档提供完整的翻译示例，展示skill在不同场景下的使用效果。

---

## Example 1: 简单会议论文翻译

### 场景描述
- 论文类型: 6页会议短文（Conference Short Paper）
- 内容: 提出一个简单算法改进
- 公式数量: 15个（行内10个，块级5个）
- 图表: 3个图，2个表格
- 难度: ⭐⭐☆☆☆ (中等)

### 输入
```
用户: /translate-pdf-to-markdown

Claude: 请提供PDF文件路径。

用户: papers/simple_algorithm.pdf
```

### 执行过程摘要

**Step 1-2: 初始化和提取**
```
正在读取PDF...
- 总页数: 6
- 字数: ~3,500
- 检测到15个公式
- 检测到3个图片
- 检测到2个表格
```

**Step 3-4: 结构分析和术语提取**
```
文档结构:
  1. Abstract
  2. Introduction
  3. Proposed Method
  4. Experiments
  5. Conclusion
  6. References

识别术语:
  - "Gradient Descent" → 梯度下降 (GD)
  - "Learning Rate" → 学习率 (LR)
  - "Convergence" → 收敛性
```

**Step 5-8: 翻译和格式化**
```
正在翻译各章节...
保留所有LaTeX公式...
生成图片占位符...
格式化Markdown...
```

**Step 9: 质量验证**
```
质量检查:
  ✓ 公式语法: 100/100
  ✓ 结构完整性: 95/100
  ✓ 翻译质量: 90/100
  ✓ Markdown格式: 95/100
  ✓ 图表处理: 90/100

综合评分: 93.5/100 (优秀)
```

### 输出示例

#### 主翻译文档 (simple_algorithm_zh.md)

```markdown
# 基于自适应学习率的梯度下降改进算法

**作者**: John Smith, Jane Doe
**机构**: Stanford University
**会议**: ICML 2024

---

## 摘要 (Abstract)

本文提出了一种自适应学习率调整机制，用于改进传统梯度下降 (Gradient Descent, GD) 算法的收敛速度。
通过动态调整学习率 (Learning Rate, LR)，我们的方法在多个基准数据集上实现了更快的收敛性和更好的最终性能。
实验结果表明，与传统固定学习率方法相比，我们的方法平均加速了 2.3 倍。

**关键词**: 梯度下降、自适应学习率、优化算法

---

## 1. 引言 (Introduction)

梯度下降是机器学习中最基本的优化算法之一 [1,2]。传统的梯度下降方法使用固定的学习率 $\eta$，
参数更新公式为:

$$
\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)
$$

其中 $L(\theta)$ 是损失函数，$\nabla_\theta L$ 是梯度。

然而，固定学习率存在以下问题:
- 学习率过大会导致不收敛
- 学习率过小会导致收敛缓慢
- 在训练后期可能需要更小的学习率以精细调整

为解决这些问题，我们提出了一种自适应学习率调整策略。

---

## 2. 相关工作 (Related Work)

### 2.1 学习率衰减 (Learning Rate Decay)

常见的学习率衰减策略包括:

1. **指数衰减** (Exponential Decay):
   $$
   \eta_t = \eta_0 \cdot e^{-\lambda t}
   $$

2. **阶梯衰减** (Step Decay):
   $$
   \eta_t = \eta_0 \cdot \gamma^{\lfloor t / k \rfloor}
   $$

3. **逆时间衰减** (Inverse Time Decay):
   $$
   \eta_t = \frac{\eta_0}{1 + \lambda t}
   $$

### 2.2 自适应优化器 (Adaptive Optimizers)

现代自适应优化器如 Adam [3] 和 RMSprop [4] 通过维护梯度的一阶和二阶矩来自动调整学习率。
Adam 的更新公式为:

$$
\begin{align}
m_t &= \beta_1 m_{t-1} + (1 - \beta_1) g_t \\
v_t &= \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\
\theta_t &= \theta_{t-1} - \frac{\eta}{\sqrt{v_t} + \epsilon} m_t
\end{align}
$$

---

## 3. 提出的方法 (Proposed Method)

### 3.1 自适应学习率机制 (Adaptive Learning Rate Mechanism)

我们的方法基于梯度范数 (Gradient Norm) 动态调整学习率:

$$
\eta_t = \eta_0 \cdot \min\left(1, \frac{\tau}{\|\nabla_\theta L(\theta_t)\|}\right)
$$

其中 $\tau$ 是预设的阈值参数。

**直觉**: 当梯度范数较大时（远离最优点），使用较大的学习率快速逼近；
当梯度范数较小时（接近最优点），自动减小学习率以避免震荡。

### 3.2 算法伪代码 (Algorithm Pseudocode)

```
Algorithm 1: Adaptive Gradient Descent
Input: 初始参数 θ₀, 初始学习率 η₀, 阈值 τ, 最大迭代次数 T
Output: 优化后的参数 θ*

1: for t = 1 to T do
2:   g_t ← ∇_θ L(θ_t)
3:   η_t ← η₀ · min(1, τ / ||g_t||)
4:   θ_{t+1} ← θ_t - η_t · g_t
5:   if ||g_t|| < ε then
6:     break  // 收敛判定
7:   end if
8: end for
9: return θ_T
```

![图1: 自适应学习率调整示意图](placeholder-figure-1.png)

*Figure 1: Illustration of adaptive learning rate adjustment. The learning rate decreases as the gradient norm decreases.*

---

## 4. 实验 (Experiments)

### 4.1 实验设置 (Experimental Setup)

**数据集**:
- MNIST: 手写数字识别
- CIFAR-10: 自然图像分类
- IMDB: 情感分析

**基线方法**:
- SGD (固定学习率)
- SGD + 阶梯衰减
- Adam

**评估指标**: 训练损失、测试准确率、收敛迭代次数

### 4.2 实验结果 (Results)

**表1: 不同方法的性能比较 (Table 1: Performance Comparison of Different Methods)**

| 方法 (Method) | MNIST 准确率 (Accuracy) | CIFAR-10 准确率 | 收敛迭代次数 (Iterations) |
|--------------|----------------------|---------------|----------------------|
| SGD (固定LR) | 97.2% | 82.1% | 15,000 |
| SGD + 阶梯衰减 | 97.8% | 84.3% | 12,000 |
| Adam | 98.1% | 85.6% | 8,000 |
| **本文方法** | **98.3%** | **86.2%** | **6,500** |

从表中可以看出，我们的方法在准确率和收敛速度上都优于基线方法。

![图2: 训练损失曲线对比](placeholder-figure-2.png)

*Figure 2: Training loss curves comparison. Our method (red) converges faster than baselines.*

### 4.3 消融实验 (Ablation Study)

我们研究了阈值参数 $\tau$ 对性能的影响:

**表2: 不同阈值 τ 的影响 (Table 2: Impact of Threshold Parameter τ)**

| τ | 收敛迭代次数 | 最终准确率 |
|---|-----------|----------|
| 0.1 | 8,200 | 97.5% |
| 0.5 | 6,500 | 98.3% |
| 1.0 | 7,100 | 98.0% |
| 2.0 | 9,500 | 97.2% |

最佳值为 $\tau = 0.5$。

![图3: 参数 τ 的敏感性分析](placeholder-figure-3.png)

*Figure 3: Sensitivity analysis of parameter τ. Best performance at τ = 0.5.*

---

## 5. 结论 (Conclusion)

本文提出了一种基于梯度范数的自适应学习率调整机制，有效改进了传统梯度下降算法的收敛速度。
实验结果表明，我们的方法在多个基准数据集上都取得了更好的性能。

**未来工作**:
- 扩展到其他优化算法（如 Momentum、RMSprop）
- 理论分析收敛性保证
- 在大规模深度学习任务中验证

---

## 参考文献 (References)

[1] Bottou, L. (2010). Large-scale machine learning with stochastic gradient descent.

[2] Ruder, S. (2016). An overview of gradient descent optimization algorithms.

[3] Kingma, D. P., & Ba, J. (2015). Adam: A method for stochastic optimization. ICLR.

[4] Tieleman, T., & Hinton, G. (2012). Lecture 6.5-rmsprop: Divide the gradient by a running average.
```

#### 质量报告 (simple_algorithm_zh_report.md)

```markdown
# 翻译质量报告

## 文档信息
- 原始文件: papers/simple_algorithm.pdf
- 输出文件: papers/simple_algorithm_zh.md
- 总页数: 6
- 字数统计: 3,521 (原文) → 4,183 (译文)

## 内容统计
- 公式数量: 15 (行内: 10, 块级: 5)
- 图片数量: 3
- 表格数量: 2
- 参考文献: 4

## 质量评估
- 综合评分: 93.5 / 100
- 评级: 优秀 (Excellent)
- 建议: 可直接使用

### 各维度评分
- 公式语法: 100.0 / 100 ✓
- 结构完整性: 95.0 / 100 ✓
- 翻译质量: 90.0 / 100 ✓
- Markdown格式: 95.0 / 100 ✓
- 图表处理: 90.0 / 100 ✓

## 发现的问题

### 翻译质量
- 检测到1处长句子（第3.1节第二段），但语句通顺

### 图表处理
- 所有图片占位符生成正确
- 建议提取图片以完善文档

## 后续工作

### 图片提取清单

- [ ] **图1**: 自适应学习率调整示意图
      - 文件名: `placeholder-figure-1.png`
      - 原文: Illustration of adaptive learning rate adjustment
      - 页码: 3
      - 提取方法: 截图或使用 pdfimages

- [ ] **图2**: 训练损失曲线对比
      - 文件名: `placeholder-figure-2.png`
      - 原文: Training loss curves comparison
      - 页码: 5
      - 提取方法: 使用 pdfimages 提取矢量图

- [ ] **图3**: 参数 τ 的敏感性分析
      - 文件名: `placeholder-figure-3.png`
      - 原文: Sensitivity analysis of parameter τ
      - 页码: 5
      - 提取方法: 使用 pdfimages 提取

### 需要人工校对的术语

所有术语翻译准确，无需特别review。

### 建议的后续步骤
1. ✅ 翻译质量优秀，可直接使用
2. 提取3个图片并替换占位符
3. 使用Markdown编辑器预览格式
4. 可选：导出为PDF以便分享

---
生成时间: 2024-02-26 15:30:00
```

---

## Example 2: 数学公式密集型论文

### 场景描述
- 论文类型: 理论研究论文（10页期刊论文）
- 内容: 优化算法的收敛性证明
- 公式数量: 80+（包含复杂推导）
- 图表: 1个图，无表格
- 难度: ⭐⭐⭐⭐⭐ (极高)

### 关键挑战
- 大量嵌套公式
- 矩阵和向量运算
- 编号公式引用
- 定理和证明结构

### 输出示例片段

```markdown
## 3. 主要结果 (Main Results)

### 3.1 收敛性定理 (Convergence Theorem)

**定理 3.1** (收敛性保证): 假设损失函数 $L: \mathbb{R}^d \rightarrow \mathbb{R}$ 满足以下条件:

1. $L$ 是 $\mu$-强凸的 ($\mu$-strongly convex):
   $$
   L(y) \geq L(x) + \nabla L(x)^T (y - x) + \frac{\mu}{2} \|y - x\|^2, \quad \forall x, y \in \mathbb{R}^d
   $$

2. 梯度是 $M$-Lipschitz连续的 ($M$-Lipschitz continuous):
   $$
   \|\nabla L(x) - \nabla L(y)\| \leq M \|x - y\|, \quad \forall x, y \in \mathbb{R}^d
   $$

则对于学习率 $\eta < \frac{2}{\mu + M}$，梯度下降算法满足:

\begin{equation}
\mathbb{E}[L(\theta_T) - L(\theta^*)] \leq \left(1 - \frac{\mu \eta}{2}\right)^T [L(\theta_0) - L(\theta^*)]
\end{equation}

其中 $\theta^*$ 是全局最优解。

**证明**: 我们首先推导单步误差界。由梯度下降更新规则:

$$
\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)
$$

定义误差 $e_t = \|\theta_t - \theta^*\|^2$，则:

\begin{align}
e_{t+1} &= \|\theta_t - \eta \nabla L(\theta_t) - \theta^*\|^2 \\
&= \|\theta_t - \theta^*\|^2 - 2\eta \nabla L(\theta_t)^T (\theta_t - \theta^*) + \eta^2 \|\nabla L(\theta_t)\|^2
\end{align}

由强凸性，我们有:

$$
\nabla L(\theta_t)^T (\theta_t - \theta^*) \geq L(\theta_t) - L(\theta^*) + \frac{\mu}{2} \|\theta_t - \theta^*\|^2
$$

由Lipschitz连续性，可得:

$$
\|\nabla L(\theta_t)\|^2 \leq 2M[L(\theta_t) - L(\theta^*)]
$$

将上述不等式代入 (3.2)，并选择 $\eta = \frac{1}{M}$，经过代数化简可得:

$$
e_{t+1} \leq \left(1 - \frac{\mu}{M}\right) e_t
$$

递推可得定理结论。 $\square$

### 3.2 线性收敛速率 (Linear Convergence Rate)

从定理 3.1 可以看出，当条件数 $\kappa = \frac{M}{\mu}$ 较小时，算法收敛更快。
具体而言，误差以线性速率衰减:

$$
e_T \leq \left(1 - \frac{1}{\kappa}\right)^T e_0
$$

要达到 $\epsilon$-精度解，需要的迭代次数为:

$$
T = O\left(\kappa \log \frac{1}{\epsilon}\right)
$$

**推论 3.2**: 对于条件数 $\kappa$ 较大的问题，可以通过预条件 (Preconditioning) 技术改善收敛速率。
设 $P$ 是正定矩阵，定义预条件梯度下降:

$$
\theta_{t+1} = \theta_t - \eta P^{-1} \nabla L(\theta_t)
$$

选择 $P \approx \nabla^2 L(\theta^*)$ 可以使有效条件数接近1，从而显著加速收敛。
```

### 公式处理要点

**复杂公式示例**:

1. **矩阵运算**:
```latex
$$
H = \nabla^2 L(\theta) = \begin{bmatrix}
\frac{\partial^2 L}{\partial \theta_1^2} & \frac{\partial^2 L}{\partial \theta_1 \partial \theta_2} & \cdots \\
\frac{\partial^2 L}{\partial \theta_2 \partial \theta_1} & \frac{\partial^2 L}{\partial \theta_2^2} & \cdots \\
\vdots & \vdots & \ddots
\end{bmatrix}
$$
```

2. **期望和概率**:
```latex
$$
\mathbb{E}_{x \sim \mathcal{D}}[f(x)] = \int_{\mathcal{X}} f(x) p(x) dx
$$
```

3. **分段函数**:
```latex
$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
$$
```

4. **求和与乘积**:
```latex
$$
\prod_{i=1}^{n} \left(1 + \frac{1}{i}\right) = \sum_{k=0}^{n} \binom{n}{k} \frac{1}{k!}
$$
```

---

## Example 3: 多图表实验性论文

### 场景描述
- 论文类型: 实验性研究（12页）
- 内容: 深度学习模型在多个数据集上的对比实验
- 公式数量: 25个（主要是模型定义）
- 图表: 12个图，8个表格
- 难度: ⭐⭐⭐☆☆ (中高)

### 输出示例片段

```markdown
## 4. 实验结果 (Experimental Results)

### 4.1 数据集描述 (Dataset Description)

我们在以下5个公开数据集上评估模型性能:

**表1: 数据集统计信息 (Table 1: Dataset Statistics)**

| 数据集 (Dataset) | 任务类型 (Task Type) | 样本数 (Samples) | 特征维度 (Features) | 类别数 (Classes) |
|---------------|-------------------|---------------|------------------|----------------|
| MNIST | 图像分类 | 70,000 | 784 | 10 |
| CIFAR-10 | 图像分类 | 60,000 | 3072 | 10 |
| IMDB | 文本分类 | 50,000 | 可变 (Variable) | 2 |
| MovieLens-1M | 推荐 (Recommendation) | 1,000,000 | 可变 | - |
| Criteo | 点击率预测 (CTR) | 45,840,617 | 39 | 2 |

### 4.2 模型性能对比 (Model Performance Comparison)

**表2: 不同模型在各数据集上的性能 (Table 2: Performance of Different Models on Each Dataset)**

| 模型 (Model) | MNIST (Acc %) | CIFAR-10 (Acc %) | IMDB (F1) | MovieLens (NDCG@10) | Criteo (AUC) |
|------------|--------------|----------------|-----------|---------------------|------------|
| Baseline | 97.2 | 82.1 | 0.851 | 0.732 | 0.788 |
| ResNet-18 | 99.1 | 94.2 | - | - | - |
| LSTM | - | - | 0.883 | - | - |
| DeepFM | - | - | - | 0.756 | 0.801 |
| **本文模型** | **99.3** | **95.1** | **0.901** | **0.784** | **0.815** |

从表中可以看出，我们的模型在所有数据集上都取得了最佳性能。

![图1: MNIST数据集上的训练曲线](placeholder-figure-1.png)

*Figure 1: Training curves on MNIST dataset. (a) Loss curve. (b) Accuracy curve.*

![图2: CIFAR-10数据集上的训练曲线](placeholder-figure-2.png)

*Figure 2: Training curves on CIFAR-10 dataset. (a) Loss curve. (b) Accuracy curve.*

### 4.3 消融实验 (Ablation Study)

我们研究了模型各组件的贡献:

**表3: 消融实验结果 (Table 3: Ablation Study Results)**

| 配置 (Configuration) | MNIST | CIFAR-10 | IMDB | 说明 (Description) |
|-------------------|-------|----------|------|------------------|
| 完整模型 (Full Model) | 99.3 | 95.1 | 0.901 | 所有组件 |
| - 注意力机制 (w/o Attention) | 98.7 | 93.8 | 0.878 | 移除注意力层 |
| - 残差连接 (w/o Residual) | 98.9 | 94.2 | 0.885 | 移除残差连接 |
| - 批归一化 (w/o BatchNorm) | 98.5 | 93.5 | 0.872 | 移除批归一化 |
| - Dropout | 99.1 | 94.6 | 0.892 | 移除Dropout |

注意力机制的贡献最为显著。

![图3: 注意力权重可视化](placeholder-figure-3.png)

*Figure 3: Visualization of attention weights. Darker colors indicate higher attention scores.*

### 4.4 参数敏感性分析 (Parameter Sensitivity)

**图4-7: 不同超参数对性能的影响**

![图4: 学习率敏感性](placeholder-figure-4.png)

*Figure 4: Sensitivity to learning rate. Best performance at lr=0.001.*

![图5: 批大小敏感性](placeholder-figure-5.png)

*Figure 5: Sensitivity to batch size. Best performance at batch_size=128.*

![图6: 隐藏层维度敏感性](placeholder-figure-6.png)

*Figure 6: Sensitivity to hidden dimension. Performance plateaus after dim=512.*

![图7: Dropout率敏感性](placeholder-figure-7.png)

*Figure 7: Sensitivity to dropout rate. Best performance at dropout=0.3.*

### 4.5 计算效率分析 (Computational Efficiency)

**表4: 训练时间和内存消耗对比 (Table 4: Training Time and Memory Consumption Comparison)**

| 模型 (Model) | 参数量 (Parameters) | 训练时间/epoch (Time/epoch) | GPU内存 (GPU Memory) | FLOPs |
|------------|-------------------|------------------------|-------------------|-------|
| Baseline | 2.1M | 45s | 1.2 GB | 3.2G |
| ResNet-18 | 11.2M | 98s | 2.8 GB | 18.1G |
| **本文模型** | 5.6M | 67s | 1.9 GB | 8.7G |

我们的模型在性能和效率之间取得了良好的平衡。

![图8: 模型大小与性能的权衡](placeholder-figure-8.png)

*Figure 8: Trade-off between model size and performance. Our model (red star) achieves the best balance.*

### 4.6 跨数据集泛化性 (Cross-Dataset Generalization)

**表5: 跨数据集迁移学习结果 (Table 5: Cross-Dataset Transfer Learning Results)**

| 源数据集 (Source) | 目标数据集 (Target) | 从头训练 (From Scratch) | 迁移学习 (Transfer) | 提升 (Improvement) |
|----------------|---------------|-------------------|-----------------|----------------|
| CIFAR-10 | CIFAR-100 | 72.3% | 78.1% | +5.8% |
| MNIST | Fashion-MNIST | 89.2% | 91.7% | +2.5% |
| IMDB | Yelp Review | 0.821 | 0.867 | +0.046 |

迁移学习在所有情况下都提升了性能。

![图9: 迁移学习可视化](placeholder-figure-9.png)

*Figure 9: t-SNE visualization of learned representations. (a) Source domain. (b) Target domain. (c) After transfer.*

### 4.7 错误案例分析 (Error Analysis)

**表6: 各类别错误率分析 (Table 6: Error Rate Analysis by Class)**

| 类别 (Class) | 样本数 (Samples) | 错误数 (Errors) | 错误率 (Error Rate) | 主要错误类型 (Main Error Type) |
|------------|---------------|--------------|-----------------|--------------------------|
| 0 | 980 | 5 | 0.51% | 误分类为6 |
| 1 | 1,135 | 2 | 0.18% | - |
| 2 | 1,032 | 12 | 1.16% | 误分类为7 |
| 3 | 1,010 | 8 | 0.79% | 误分类为5 |
| ... | ... | ... | ... | ... |

![图10: 混淆矩阵](placeholder-figure-10.png)

*Figure 10: Confusion matrix for MNIST classification. Most errors occur between visually similar digits (e.g., 3 and 5).*

### 4.8 可视化分析 (Visualization Analysis)

**图11-12: 特征表示和决策边界**

![图11: 学习到的特征表示](placeholder-figure-11.png)

*Figure 11: Learned feature representations visualized using t-SNE. Different colors represent different classes.*

![图12: 决策边界可视化](placeholder-figure-12.png)

*Figure 12: Decision boundary visualization on a 2D projection. Our model (right) produces smoother boundaries than baseline (left).*
```

### 图表提取清单示例

```markdown
# 图片提取清单

## 实验结果图（优先级: 高）

- [ ] **图1**: MNIST训练曲线
      - 包含2个子图: (a) Loss, (b) Accuracy
      - 建议尺寸: 800x400
      - 格式: PNG或矢量PDF

- [ ] **图2**: CIFAR-10训练曲线
      - 包含2个子图
      - 与图1格式保持一致

## 参数敏感性图（优先级: 中）

- [ ] **图4-7**: 4个超参数敏感性分析图
      - 统一风格的曲线图
      - 建议批量提取

## 可视化分析图（优先级: 中）

- [ ] **图10**: 混淆矩阵热力图
      - 颜色映射需要清晰
      - 注意保留数值标签

- [ ] **图11**: t-SNE可视化
      - 散点图，保留颜色信息
      - 建议高分辨率

## 提取命令参考

```bash
# 批量提取所有图片
pdfimages -png paper.pdf figures/fig

# 提取特定页面
convert -density 300 paper.pdf[4] figure-1.png
convert -density 300 paper.pdf[6] figure-2.png
```
```

---

## Example 4: 完整翻译流程演示

### 场景: 翻译MMOE论文（11页）

#### Step 1: 初始化

```
用户: /translate-pdf-to-markdown

Claude: 好的，我将帮您翻译PDF学术论文。请提供PDF文件路径。

用户: docs/mmoe.pdf

Claude: 正在初始化翻译流程...

      [检查文件]
      ✓ 文件存在: docs/mmoe.pdf
      ✓ 文件大小: 2.3 MB
      ✓ 文件类型: PDF

      [询问配置]
      是否有特殊要求？(输出路径、术语保留等)

用户: 输出到 docs/mmoe_zh.md，保留 "Expert" 和 "Gate" 为英文

Claude: 好的，配置如下:
      - 输入: docs/mmoe.pdf
      - 输出: docs/mmoe_zh.md
      - 保留术语: Expert, Gate
      - 翻译风格: 学术严谨

      开始翻译...
```

#### Step 2-3: PDF提取和结构分析

```
[正在读取PDF...]

文档信息:
  - 标题: Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts
  - 作者: Jiaqi Ma, Zhe Zhao, et al.
  - 会议: KDD 2018
  - 页数: 11

[提取内容统计]
  - 总字数: ~8,500
  - 公式数量: 47
  - 图片数量: 6
  - 表格数量: 4
  - 参考文献: 34

[结构分析]
  识别到以下章节:
    1. Abstract
    2. Introduction
    3. Related Work
    4. Multi-gate Mixture-of-Experts
    5. Experiments
      5.1 Synthetic Data
      5.2 UCI Census-income Data
      5.3 Content Recommendation
    6. Conclusion
    7. References
```

#### Step 4: 术语提取

```
[识别专业术语]

自动提取的术语:
  ✓ Multi-task Learning (MTL) → 多任务学习
  ✓ Mixture-of-Experts (MoE) → 专家混合模型
  ✓ Shared-Bottom → 共享底层模型
  ✓ Gating Network → 门控网络
  ! Expert → 保留英文 (用户指定)
  ! Gate → 保留英文 (用户指定)
  ✓ Task-specific Tower → 任务特定塔网络
  ✓ Cross-stitch Network → 交叉缝合网络
  ✓ Negative Transfer → 负迁移

建立术语对照表 (共23个术语)
```

#### Step 5-8: 翻译和格式化

```
[正在翻译...]

进度:
  ✓ Abstract - 完成
  ✓ 1. Introduction - 完成
  ✓ 2. Related Work - 完成
  ✓ 3. Multi-gate Mixture-of-Experts - 完成
    - 保留47个LaTeX公式
    - 生成6个图片占位符
  ✓ 4. Experiments - 完成
    - 翻译4个表格
  ✓ 5. Conclusion - 完成
  ✓ References - 完成

[格式化Markdown]
  ✓ 标题层级规范化
  ✓ 列表格式统一
  ✓ 公式格式验证
  ✓ 表格对齐优化
```

#### Step 9: 质量验证

```
[运行质量检查]

1. 公式语法验证 (30%)
   ✓ 检查47个公式
   ✓ 所有$符号成对
   ✓ 括号完全匹配
   ✓ LaTeX命令拼写正确
   评分: 100/100

2. 结构完整性 (20%)
   ✓ 所有章节完整
   ✓ 标题层级正确
   ✓ 图表编号连续
   ⚠ 缺少一个子章节编号 (-5分)
   评分: 95/100

3. 翻译质量 (25%)
   ✓ 术语一致性良好
   ⚠ 检测到2处可能的术语不一致 (-4分)
   ✓ 无重复字符错误
   ✓ 无未翻译英文词汇
   评分: 86/100

4. Markdown格式 (15%)
   ✓ 标题格式正确
   ✓ 列表格式规范
   ✓ 代码块闭合
   ✓ 图片链接完整
   评分: 100/100

5. 图表处理 (10%)
   ✓ 6个图片占位符完整
   ✓ 所有图片有中英文描述
   ✓ 4个表格翻译准确
   评分: 95/100

[综合评分]
  总分: 93.2 / 100
  评级: 优秀 (Excellent)
  建议: 可直接使用
```

#### Step 10: 生成报告和输出

```
[生成输出文件]

✓ docs/mmoe_zh.md - 主翻译文档 (已保存)
✓ docs/mmoe_zh_report.md - 质量报告 (已保存)
✓ docs/mmoe_zh_figures.md - 图片清单 (已保存)

翻译完成！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 翻译报告摘要

输出文件: docs/mmoe_zh.md
质量评分: 93.2/100 (优秀)

内容统计:
  - 公式: 47个 ✓
  - 图片: 6个 (需提取)
  - 表格: 4个 ✓
  - 字数: 8,523 → 10,127

发现的问题:
  ⚠ 章节编号: 5.2.1缺失，从5.2直接到5.2.2
  ⚠ 术语: "task-specific" 有2处未统一

后续建议:
  1. 提取6个图片 (详见清单文件)
  2. 修正章节编号问题
  3. 统一 "task-specific" 翻译为 "任务特定的"
  4. 使用Markdown编辑器预览公式渲染

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

查看详细报告: docs/mmoe_zh_report.md
图片提取清单: docs/mmoe_zh_figures.md
```

---

## 总结

通过这些详细示例，展示了PDF论文翻译skill在不同场景下的能力:

1. **简单论文**: 快速准确翻译，质量优秀
2. **数学论文**: 完美保留复杂公式，证明结构完整
3. **实验论文**: 处理大量图表，格式整齐
4. **完整流程**: 10步工作流，质量验证，交付完整

关键成功因素:
- ✅ 公式绝对不翻译
- ✅ 术语首次完整对照
- ✅ 图表规范化处理
- ✅ 多维度质量验证
- ✅ 详细的后续指导

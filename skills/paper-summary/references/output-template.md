# [Paper Title]

**Authors**: [Author list]
**Venue**: [Conference/Journal, Year]
**Summary Level**: [Brief | Standard | Detailed]

---

## Abstract (1 sentence)

[Single sentence capturing the paper's core contribution and main result]

---

## 1. Problem Statement

[Detail level determines length:]
- **Brief**: 2-3 sentences - What problem? Why important?
- **Standard**: 1 paragraph - Problem context, limitations of existing work, motivation
- **Detailed**: 2-3 paragraphs - Comprehensive background, related work critique, research gap analysis

**Example structure (Standard level):**

This paper addresses the problem of [specific problem]. Prior approaches like [existing methods] suffer from [limitations] because [reasons]. This is important because [impact/significance]. The key challenge is [core difficulty].

**Key questions to answer:**
- What problem does the paper solve?
- Why is this problem important?
- What are the limitations of existing solutions?
- What makes this problem challenging?

---

## 2. Solution Approach

[Detail level determines length:]
- **Brief**: 2-3 sentences - Core idea only
- **Standard**: 1 paragraph - High-level approach, main insight, how it differs from prior work
- **Detailed**: 2-3 paragraphs - Comprehensive approach description, design philosophy, key innovations

**Example structure (Standard level):**

The paper proposes [high-level approach] based on the insight that [core insight]. Unlike previous methods that [prior approach], this work [key difference]. The main idea is to [central concept] which enables [capability/benefit].

**Key questions to answer:**
- What is the high-level solution?
- What's the core insight or idea?
- How does it differ from existing approaches?
- What makes this approach novel?

---

## 3. Proposed Method

[Detail level determines length:]
- **Brief**: 1 paragraph - Architecture overview only
- **Standard**: 2-3 paragraphs with subsections - Architecture + key formulations
- **Detailed**: Multiple subsections with comprehensive technical details

### 3.1 Architecture

[Describe the system/model architecture]

**Example elements:**
- Component diagram (if present in paper)
- Data flow description
- Layer-by-layer breakdown (for neural networks)
- Algorithm pseudocode (for algorithmic papers)

**Images:**
![Architecture diagram](path/to/architecture.png)

### 3.2 Mathematical Formulation

[Detail level determines formula inclusion:]
- **Brief**: Only the main equation
- **Standard**: Key equations and important derivations
- **Detailed**: Complete mathematical formulation

**Example formulas:**

The core objective function is:

$$
\mathcal{L}(\theta) = -\sum_{i=1}^{N} \log p(y_i | x_i; \theta) + \lambda R(\theta)
$$

where:
- $\theta$ represents model parameters
- $R(\theta)$ is a regularization term
- $\lambda$ controls regularization strength

For the attention mechanism:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### 3.3 Key Components

[Detailed breakdown of important components]

**Example for neural network papers:**
- **Input layer**: [specification]
- **Hidden layers**: [architecture details]
- **Output layer**: [specification]
- **Activation functions**: [choices and rationale]
- **Normalization**: [techniques used]

**Example for algorithmic papers:**
- **Initialization**: [procedure]
- **Main loop**: [algorithm steps]
- **Termination**: [conditions]
- **Complexity**: [time and space complexity]

---

## 4. Experimental Design

[Detail level determines table inclusion:]
- **Brief**: Summary only - mention dataset names and key metrics
- **Standard**: Key datasets and main baselines
- **Detailed**: All datasets, all baselines, complete experimental setup

### 4.1 Datasets

| Dataset | Task | Size | Split | Metrics |
|---------|------|------|-------|---------|
| Dataset1 | Classification | 10K samples | 7K/1.5K/1.5K | Accuracy, F1 |
| Dataset2 | Generation | 50K samples | 40K/5K/5K | BLEU, ROUGE |

**Dataset descriptions:**
- **Dataset1**: [brief description, why chosen, preprocessing steps]
- **Dataset2**: [brief description, why chosen, preprocessing steps]

### 4.2 Baselines

| Model | Type | Key Feature | Paper |
|-------|------|-------------|-------|
| Baseline1 | Traditional | [key aspect] | [citation] |
| Baseline2 | Neural | [key aspect] | [citation] |
| Baseline3 | SOTA | [key aspect] | [citation] |

**Why these baselines:**
- **Baseline1**: [rationale]
- **Baseline2**: [rationale]
- **Baseline3**: [rationale]

### 4.3 Evaluation Metrics

| Metric | Purpose | Range | Higher/Lower Better |
|--------|---------|-------|---------------------|
| Accuracy | Overall correctness | [0, 1] | Higher |
| F1 Score | Precision-recall balance | [0, 1] | Higher |
| Perplexity | Language model quality | [1, ∞) | Lower |

**Metric descriptions:**
- **Accuracy**: [why chosen, what it measures]
- **F1 Score**: [why chosen, what it measures]
- **Perplexity**: [why chosen, what it measures]

---

## 5. Experimental Methodology

[Detail level determines depth:]
- **Brief**: 1 paragraph - main hyperparameters only
- **Standard**: 2 paragraphs - implementation details + training procedure
- **Detailed**: Multiple subsections with complete reproducibility details

### 5.1 Implementation Details

**Framework**: [PyTorch/TensorFlow/JAX/etc., version]
**Hardware**: [GPU/TPU type, count]
**Training time**: [time per model, total compute]

**Key hyperparameters:**

| Hyperparameter | Value | Search Method |
|----------------|-------|---------------|
| Learning rate | 1e-4 | Grid search |
| Batch size | 32 | Fixed |
| Dropout | 0.1 | Manual tuning |
| Weight decay | 0.01 | Default |
| Optimizer | Adam | Fixed |
| $\beta_1$, $\beta_2$ | 0.9, 0.999 | Default |

### 5.2 Training Procedure

1. **Initialization**: [how weights are initialized]
2. **Optimization**: [optimizer, learning rate schedule]
3. **Regularization**: [techniques used - dropout, weight decay, early stopping]
4. **Validation**: [validation strategy, early stopping criteria]
5. **Model selection**: [how best model is chosen]

**Example:**

> Models are trained for 100 epochs with early stopping based on validation loss (patience=10). Learning rate is reduced by 0.1 when validation loss plateaus for 5 epochs. Best model is selected based on validation F1 score.

### 5.3 Reproducibility Notes

- **Random seeds**: [how randomness is controlled]
- **Data preprocessing**: [normalization, augmentation, tokenization]
- **Code availability**: [GitHub link if available]
- **Pretrained checkpoints**: [availability and location]

---

## 6. Experimental Results

[Detail level determines table inclusion:]
- **Brief**: Main results table only
- **Standard**: Main results + key ablations
- **Detailed**: All results tables, ablations, error analysis

### 6.1 Main Results

| Model | Dataset1 Acc. | Dataset2 BLEU | Avg. Improvement |
|-------|---------------|---------------|------------------|
| Baseline1 | 85.2 | 28.3 | - |
| Baseline2 | 87.6 | 30.1 | - |
| Baseline3 (SOTA) | 89.3 | 31.5 | - |
| **Proposed** | **91.7** | **33.8** | **+2.4% / +2.3** |

**Key findings:**
- Proposed method outperforms all baselines on all datasets
- Largest improvement on Dataset1 (+2.4% over SOTA)
- Statistical significance: [p-value, confidence intervals]

### 6.2 Ablation Studies

| Variant | Component Removed | Performance Drop | Insight |
|---------|-------------------|------------------|---------|
| Full model | None | 91.7 (baseline) | - |
| -Attention | Attention mechanism | -3.2 (-3.5%) | Attention is critical |
| -Regularization | Dropout + weight decay | -1.8 (-2.0%) | Regularization helps |
| -Pretraining | Pretrained weights | -5.1 (-5.6%) | Pretraining essential |

**Insights from ablations:**
- **Attention mechanism**: Contributes 3.5% of performance, essential for [reason]
- **Regularization**: Prevents overfitting, especially on [dataset/condition]
- **Pretraining**: Most important component, provides [benefit]

### 6.3 Error Analysis

[Detail level determines inclusion:]
- **Brief**: Omit
- **Standard**: 1 paragraph summary
- **Detailed**: Comprehensive error analysis with examples

**Example (Standard level):**

Error analysis reveals that the model struggles with [error type 1] and [error type 2]. For example, [specific example]. This is likely because [hypothesis]. Future work could address this by [potential solution].

### 6.4 Qualitative Results

[Include if paper has visualizations, examples, or case studies]

**Example outputs:**

| Input | Baseline Output | Proposed Output | Ground Truth |
|-------|-----------------|-----------------|--------------|
| [example 1] | [baseline result] | [proposed result] | [reference] |
| [example 2] | [baseline result] | [proposed result] | [reference] |

**Images:**
![Qualitative comparison](path/to/qualitative-results.png)

---

## Limitations & Future Work

[Detail level determines length:]
- **Brief**: 2-3 bullet points
- **Standard**: 1 paragraph
- **Detailed**: 2 paragraphs with specific directions

**Limitations identified:**
- **Computational cost**: [specific limitation]
- **Dataset bias**: [specific limitation]
- **Generalization**: [specific limitation]
- **Hyperparameter sensitivity**: [specific limitation]

**Future directions:**
- [Direction 1]: [brief description and potential impact]
- [Direction 2]: [brief description and potential impact]
- [Direction 3]: [brief description and potential impact]

---

## Key Takeaways

**Main contributions:**
1. [First key contribution] - [impact/significance]
2. [Second key contribution] - [impact/significance]
3. [Third key contribution] - [impact/significance]

**Strengths:**
- ✓ [Strength 1]
- ✓ [Strength 2]
- ✓ [Strength 3]

**Weaknesses:**
- ✗ [Weakness 1]
- ✗ [Weakness 2]

**Bottom line:**
[One sentence summarizing when/why to use this method]

---

## Notes

[Optional section for additional context:]
- **Related work not covered**: [pointers to related papers]
- **Implementation tips**: [practical advice for implementation]
- **Citation context**: [how often cited, influence in field]
- **Follow-up papers**: [extensions, applications, criticisms]

---

**Summary generated by**: Claude Code `paper-summary` skill
**Detail level**: [Brief | Standard | Detailed]
**Word count**: [approximate count]
**Formula count**: [number of preserved LaTeX formulas]
**Image count**: [number of preserved image references]

---

# Template Usage Notes

## Conditional Elements by Detail Level

### Brief (500-800 words)
- **Include**: Sections 1-3, 6.1 (main results only), Key Takeaways
- **Omit**: Subsections, detailed tables, ablations, error analysis, qualitative results
- **Formulas**: Main equation only (1-2 formulas)
- **Tables**: Summary text instead of full tables

### Standard (1200-1800 words) - DEFAULT
- **Include**: All sections with primary subsections
- **Omit**: Comprehensive ablations, detailed error analysis
- **Formulas**: Key equations (3-6 formulas)
- **Tables**: Main datasets, baselines, results (not exhaustive)

### Detailed (2500-4000 words)
- **Include**: All sections with all subsections
- **Omit**: Nothing
- **Formulas**: Complete formulation (8-15+ formulas)
- **Tables**: All tables from paper

## Formula Preservation Examples

**Inline formulas** (within text):
The loss function $\mathcal{L}(\theta)$ is minimized using gradient descent with learning rate $\alpha = 0.001$.

**Display formulas** (standalone):

$$
\nabla_\theta \mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} \frac{\partial \ell(f(x_i; \theta), y_i)}{\partial \theta}
$$

**Complex formulas** (preserve exactly):

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O \\
\text{where head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

## Image Reference Examples

**Architecture diagrams:**
![Transformer architecture showing encoder-decoder structure with multi-head attention](figures/architecture.png)

**Result visualizations:**
![Accuracy vs. model size across different datasets](figures/results-comparison.png)

**Qualitative examples:**
![Example translations comparing baseline and proposed method](figures/qualitative-examples.png)

## Table Formatting Examples

**Simple comparison table:**
| Model | Accuracy | F1 | Precision | Recall |
|-------|----------|----|-----------| -------|
| Baseline | 85.2 | 83.1 | 84.5 | 81.7 |
| Proposed | **91.7** | **89.3** | **90.1** | **88.5** |

**Multi-column table:**
| Dataset | Train | Val | Test | Classes | Features | Task |
|---------|-------|-----|------|---------|----------|------|
| MNIST | 60K | 10K | 10K | 10 | 784 | Classification |
| CIFAR-10 | 50K | 5K | 10K | 10 | 3072 | Classification |

## Section Organization Patterns

**For theoretical papers:**
- Section 3: Emphasize mathematical formulation over architecture
- Section 4: Include proof sketches or theoretical analysis
- Section 6: Focus on theoretical guarantees, convergence analysis

**For empirical papers:**
- Section 3: Emphasize architecture over mathematical details
- Section 4: Comprehensive datasets and baselines
- Section 6: Extensive experimental results, ablations, error analysis

**For survey/position papers:**
- Section 1-2: Extended problem statement and landscape analysis
- Section 3: Taxonomy or framework instead of single method
- Section 6: Comparative analysis across multiple methods

**For systems/applications papers:**
- Section 3: System architecture, implementation details
- Section 4: Deployment scenarios, real-world datasets
- Section 6: Performance benchmarks, scalability analysis

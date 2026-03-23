# 优秀图表模式参考

本文档从 nanobot 项目现有文档中提取优秀的图表示例，展示各类图表的最佳实践。

## 类图模式

### 模式 1: 核心类与依赖组件

**适用场景**: 展示核心类及其依赖的组件，突出组合关系。

**示例**: AgentLoop 与依赖组件

```mermaid
classDiagram
    class AgentLoop {
        -Config config
        -MessageBus bus
        -LLMProvider provider
        -ToolRegistry tools
        -ContextBuilder context
        -SessionManager sessions
        -SubagentManager subagents
        -MemoryStore memory
        -SkillsLoader skills
        +run() void
        -_process_message(InboundMessage) OutboundMessage
        -_run_agent_loop(messages, max_iterations) str
        -_consolidate_memory(Session) void
    }

    class MessageBus {
        +Queue~InboundMessage~ inbound
        +Queue~OutboundMessage~ outbound
        +publish_inbound(InboundMessage) void
        +publish_outbound(OutboundMessage) void
        +consume_inbound(timeout) InboundMessage
    }

    class ContextBuilder {
        -Path workspace
        -MemoryStore memory
        -SkillsLoader skills
        +build_system_prompt(skill_names) str
        +build_messages(history, current, media) list
    }

    class SessionManager {
        -Path workspace
        -dict~str,Session~ _cache
        +get_or_create(key) Session
        +save(Session) void
        +list_sessions() list
    }

    AgentLoop --> MessageBus
    AgentLoop --> ContextBuilder
    AgentLoop --> SessionManager
    ContextBuilder --> MemoryStore
    ContextBuilder --> SkillsLoader
```

**关键特点**:
- 核心类在顶部，清晰展示所有依赖
- 属性使用 `-` 表示私有，方法使用 `+` 表示公共
- 依赖关系使用 `-->` 箭头
- 避免过多细节，只展示关键方法

### 模式 2: 抽象层与实现类

**适用场景**: 展示抽象类/接口与多个实现类的继承关系。

**示例**: LLMProvider 抽象层

```mermaid
classDiagram
    class LLMProvider {
        <<abstract>>
        +chat(messages, tools, model)* LLMResponse
    }

    class LLMResponse {
        +str content
        +list~ToolCallRequest~ tool_calls
        +str finish_reason
        +dict usage
        +bool has_tool_calls
    }

    class ToolCallRequest {
        +str id
        +str name
        +dict arguments
    }

    class LiteLLMProvider {
        -Config config
        +chat(messages, tools, model) LLMResponse
        -_resolve_model(model) str
        -_sanitize_messages(messages) list
    }

    class CustomProvider {
        -Config config
        +chat(messages, tools, model) LLMResponse
    }

    class OpenAICodexProvider {
        -str access_token
        +chat(messages, tools, model) LLMResponse
        +login() void
    }

    LLMProvider <|-- LiteLLMProvider
    LLMProvider <|-- CustomProvider
    LLMProvider <|-- OpenAICodexProvider
    LiteLLMProvider ..> LLMResponse
    CustomProvider ..> LLMResponse
    LLMResponse *-- ToolCallRequest
```

**关键特点**:
- 使用 `<<abstract>>` 标记抽象类
- 抽象方法使用 `*` 后缀
- 继承关系使用 `<|--`
- 依赖关系使用 `..>`
- 组合关系使用 `*--`

### 模式 3: 多态继承树

**适用场景**: 展示单个基类的多个子类实现。

**示例**: BaseChannel 抽象层

```mermaid
classDiagram
    class BaseChannel {
        <<abstract>>
        +str name
        +MessageBus bus
        +Config config
        +start()* void
        +stop()* void
        +send(OutboundMessage)* void
        +is_allowed(sender_id) bool
    }

    class TelegramChannel {
        -str token
        -list allowFrom
        -Application _app
        +start() void
        +stop() void
        +send(OutboundMessage) void
        -_handle_message(Update) void
    }

    class DiscordChannel {
        -str token
        -list allowFrom
        -WebSocket _ws
        +start() void
        +stop() void
        +send(OutboundMessage) void
        -_handle_message(event) void
    }

    class SlackChannel {
        -str botToken
        -str appToken
        -WebClient _web_client
        +start() void
        +stop() void
        +send(OutboundMessage) void
        -_handle_message(event) void
    }

    BaseChannel <|-- TelegramChannel
    BaseChannel <|-- DiscordChannel
    BaseChannel <|-- SlackChannel
```

**关键特点**:
- 基类定义公共接口
- 子类实现具体细节
- 清晰展示多态性
- 使用中文注释说明职责

## 时序图模式

### 模式 1: 完整的消息处理流程

**适用场景**: 展示端到端的消息处理流程，包含多个组件交互。

**示例**: Memory Consolidation 流程

```mermaid
sequenceDiagram
    participant Agent as AgentLoop
    participant Session as Session
    participant Memory as MemoryStore
    participant LLM as LLMProvider
    participant Files as Filesystem

    Agent->>Session: 检查未整理消息数
    Session-->>Agent: unconsolidated >= 100

    Agent->>Agent: 获取整理锁
    Agent->>Memory: consolidate(session)

    Memory->>Session: 提取旧消息
    Session-->>Memory: messages[last:keep]

    Memory->>Memory: 格式化为时间戳日志
    Memory->>Files: 读取 MEMORY.md
    Files-->>Memory: 当前长期记忆

    Memory->>LLM: chat(messages, save_memory tool)
    LLM-->>Memory: {history_entry, memory_update}

    Memory->>Files: 追加 HISTORY.md
    Memory->>Files: 覆盖 MEMORY.md

    Memory->>Session: 更新 last_consolidated
    Memory-->>Agent: 整理完成

    Agent->>Agent: 释放锁
```

**关键特点**:
- 参与者使用中文标签
- 包含同步调用（`->>`）和返回（`-->>`）
- 标注关键的数据传递
- 使用 `Note` 可以添加说明

### 模式 2: 带条件分支的交互

**适用场景**: 展示包含条件判断的交互流程。

**示例**: Channel 消息处理（Telegram）

```mermaid
sequenceDiagram
    participant TG as Telegram Server
    participant Ch as TelegramChannel
    participant Bus as MessageBus
    participant Media as MediaDir
    participant Whisper as Groq Whisper

    TG->>Ch: Long Polling<br/>getUpdates
    Ch->>Ch: _handle_message

    alt 权限检查
        Ch->>Ch: is_allowed(sender_id)
        Ch-->>Ch: 拒绝则返回
    end

    alt 下载媒体
        Ch->>TG: bot.get_file(file_id)
        TG-->>Ch: file object
        Ch->>Media: download_to_drive
    end

    alt 语音转录
        Ch->>Whisper: transcribe(audio_file)
        Whisper-->>Ch: transcription text
    end

    Ch->>Ch: 创建 InboundMessage
    Ch->>Bus: publish_inbound(msg)
    Bus-->>Ch: 消息已入队
```

**关键特点**:
- 使用 `alt` / `end` 表示条件分支
- 自调用使用 `Ch->>Ch`
- 清晰的分支标签
- 使用 `<br/>` 换行

### 模式 3: 后台异步执行

**适用场景**: 展示主流程和后台异步任务的关系。

**示例**: Subagent 执行流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant Main as 主 Agent
    participant Spawn as SpawnTool
    participant Sub as Subagent
    participant Bus as MessageBus

    User->>Main: 请求任务
    Main->>Main: LLM 决策使用 spawn tool
    Main->>Spawn: execute(task, label)

    Spawn->>Spawn: 创建 task_id
    Spawn->>Sub: asyncio.create_task<br/>_run_subagent
    Spawn-->>Main: "Subagent started (id: xxx)"
    Main-->>User: 告知已创建子任务

    Note over Sub: 后台执行 (不阻塞)
    Sub->>Sub: 独立 LLM 循环<br/>max_iterations=15
    Sub->>Sub: 有限工具集<br/>无 message/spawn/cron

    Sub->>Sub: 完成任务
    Sub->>Bus: publish_inbound<br/>channel="system"
    Bus->>Main: consume_inbound

    Main->>Main: 检测系统消息
    Main->>Main: 加载原会话历史
    Main->>Main: LLM 总结结果
    Main-->>User: 报告子任务完成
```

**关键特点**:
- 使用 `Note over` 说明后台执行
- 清晰区分同步和异步部分
- 标注关键的状态转换
- 使用中文描述

## 流程图模式

### 模式 1: 主流程图（单一路径）

**适用场景**: 展示核心处理流程，不包含复杂分支。

**示例**: AgentLoop 核心流程

```mermaid
flowchart TD
    Start[AgentLoop.run 启动] --> Poll[轮询 inbound 队列<br/>timeout=1s]
    Poll --> Check{有消息?}
    Check -->|否| Poll
    Check -->|是| Cmd{斜杠命令?}

    Cmd -->|/new| New[整理记忆 + 清空会话]
    Cmd -->|/help| Help[返回帮助]
    Cmd -->|否| Session[获取/创建 Session]

    Session --> History[提取历史<br/>max_messages=100]
    History --> MemCheck{需要整理?}
    MemCheck -->|是| BgConsolidate[后台 consolidate]
    MemCheck -->|否| Context[构建上下文]
    BgConsolidate --> Context

    Context --> LLMLoop[LLM + 工具循环]
    LLMLoop --> Save[保存会话]
    Save --> MsgCheck{message tool?}
    MsgCheck -->|已发送| End[结束]
    MsgCheck -->|否| Send[发送响应]

    New --> End
    Help --> End
    Send --> End
```

**关键特点**:
- 使用 `TD` (top-down) 布局
- 矩形框 `[]` 表示操作
- 菱形框 `{}` 表示判断
- 使用 `<br/>` 添加细节说明
- 清晰的判断标签（`|是|`、`|否|`）

### 模式 2: 循环迭代流程

**适用场景**: 展示包含循环的流程，如工具执行循环。

**示例**: LLM 工具执行循环

```mermaid
flowchart TD
    Start[开始循环<br/>iteration=0] --> Check{iteration < 40?}
    Check -->|否| MaxIter[返回超时提示]
    Check -->|是| CallLLM[调用 LLM<br/>provider.chat]

    CallLLM --> HasTools{有工具调用?}
    HasTools -->|否| Return[返回 final_content]

    HasTools -->|是| Progress[发送进度消息]
    Progress --> Hint[发送工具提示]
    Hint --> AddAssist[添加 assistant 消息]

    AddAssist --> ToolLoop{遍历 tool_calls}
    ToolLoop --> Execute[执行工具<br/>tools.execute]
    Execute --> Truncate[截断结果<br/>> 500 chars]
    Truncate --> AddTool[添加 tool 消息]
    AddTool --> ToolLoop

    ToolLoop --> Inc[iteration += 1]
    Inc --> Check
```

**关键特点**:
- 清晰的循环路径（回到起点）
- 多层嵌套判断
- 步骤详细标注
- 退出条件明确

### 模式 3: 复杂决策树

**适用场景**: 展示多级条件判断和回退逻辑。

**示例**: Provider 路由逻辑

```mermaid
flowchart TD
    Start[模型名: model] --> Prefix{显式前缀?}
    Prefix -->|是| Match1[匹配 provider<br/>deepseek/xxx → DeepSeek]
    Prefix -->|否| Keyword{关键词匹配?}

    Match1 --> HasKey1{有 api_key?}
    HasKey1 -->|是| Use1[使用该 provider]
    HasKey1 -->|否| Keyword

    Keyword -->|gpt-4| Match2[OpenAI]
    Keyword -->|claude| Match2[Anthropic]
    Keyword -->|deepseek| Match2[DeepSeek]
    Keyword -->|否| Fallback{回退策略}

    Match2 --> HasKey2{有 api_key?}
    HasKey2 -->|是| Use2[使用该 provider]
    HasKey2 -->|否| Fallback

    Fallback --> Gateway{有网关 provider?}
    Gateway -->|是| UseGateway[使用网关<br/>OpenRouter/AiHubMix]
    Gateway -->|否| First[第一个有 api_key<br/>的 provider]

    Use1 --> Resolve[解析模型名<br/>_resolve_model]
    Use2 --> Resolve
    UseGateway --> Resolve
    First --> Resolve

    Resolve --> SetupEnv[设置环境变量<br/>_setup_env]
    SetupEnv --> Call[调用 LiteLLM<br/>acompletion]
```

**关键特点**:
- 多级判断树
- 清晰的回退路径
- 汇聚点明确
- 标注关键条件

## 架构图模式

### 模式 1: 分层架构

**适用场景**: 展示系统的分层结构和数据流向。

**示例**: Context 构建流程

```mermaid
flowchart LR
    Start[开始构建] --> System[System Prompt]

    System --> Identity[1. Identity<br/>OS/Python/Workspace]
    Identity --> Bootstrap[2. Bootstrap Files<br/>AGENTS/SOUL/USER...]
    Bootstrap --> Memory[3. MEMORY.md<br/>长期事实]
    Memory --> AlwaysSkills[4. Always Skills<br/>完整内容]
    AlwaysSkills --> SkillsXML[5. Skills Summary<br/>XML 索引]

    SkillsXML --> History[6. Conversation History<br/>最近 100 条]
    History --> Current[7. Current Message<br/>文本 + base64 图片]

    Current --> Runtime[8. Runtime Context<br/>时间/Channel/ChatID]
    Runtime --> Messages[完整 messages 列表]
```

**关键特点**:
- 使用 `LR` (left-to-right) 布局
- 步骤编号清晰
- 使用 `<br/>` 添加细节
- 线性流程，易于理解

### 模式 2: 组件依赖关系

**适用场景**: 展示多个组件之间的依赖关系。

**示例**: 完整依赖关系图

```mermaid
graph TD
    Gateway[Gateway CLI] --> Config[Config]
    Gateway --> MessageBus[MessageBus]
    Gateway --> AgentLoop[AgentLoop]
    Gateway --> ChannelManager[ChannelManager]
    Gateway --> CronService[CronService]

    AgentLoop --> Config
    AgentLoop --> MessageBus
    AgentLoop --> LLMProvider[LLMProvider]
    AgentLoop --> ToolRegistry[ToolRegistry]
    AgentLoop --> ContextBuilder[ContextBuilder]
    AgentLoop --> SessionManager[SessionManager]
    AgentLoop --> SubagentManager[SubagentManager]

    ContextBuilder --> MemoryStore[MemoryStore]
    ContextBuilder --> SkillsLoader[SkillsLoader]

    SubagentManager --> LLMProvider
    SubagentManager --> ToolRegistry
    SubagentManager --> MessageBus
```

**关键特点**:
- 使用 `TD` (top-down) 布局
- 清晰的分层结构
- 避免交叉线
- 聚焦核心依赖

### 模式 3: 子图分组

**适用场景**: 展示复杂系统的模块分组。

**示例**: 系统架构图

```mermaid
graph TB
    subgraph "CLI Layer"
        CLI[commands.py<br/>agent command]
    end

    subgraph "Message Bus"
        BUS[MessageBus<br/>queue.py]
        INBOUND[Inbound Queue]
        OUTBOUND[Outbound Queue]
    end

    subgraph "Agent Core"
        LOOP[AgentLoop<br/>loop.py]
        CTX[ContextBuilder<br/>context.py]
        TOOLS[ToolRegistry<br/>tools/registry.py]
    end

    subgraph "Storage"
        MEMORY_MD[memory/MEMORY.md]
        HISTORY_MD[memory/HISTORY.md]
        SESSION[Session JSONL Files]
    end

    CLI --> BUS
    CLI --> LOOP
    LOOP --> CTX
    LOOP --> TOOLS
    CTX --> MEMORY_MD
    LOOP --> SESSION

    BUS --> INBOUND
    BUS --> OUTBOUND
```

**关键特点**:
- 使用 `subgraph` 分组
- 清晰的分层标题
- 组内和组间的连接
- 标注文件路径

## 综合示例：完整的消息流转路径

**适用场景**: 展示端到端的复杂流程，结合多种元素。

```mermaid
graph TD
    A[用户发送消息] --> B[Channel._handle_message]
    B --> C{权限检查}
    C -->|允许| D[下载媒体文件]
    C -->|拒绝| Z[丢弃消息]
    D --> E[转录语音<br/>Groq Whisper]
    E --> F[创建 InboundMessage]
    F --> G[MessageBus.publish_inbound]
    G --> H[AgentLoop.run 轮询<br/>1秒超时]
    H --> I{斜杠命令?}
    I -->|/new| J[触发记忆整理<br/>清空会话]
    I -->|/help| K[返回帮助信息]
    I -->|普通消息| L[获取会话 Session]
    L --> M{需要整理?<br/>messages >= 100}
    M -->|是| N[后台异步整理<br/>不阻塞]
    M -->|否| O[构建上下文]
    N --> O
    O --> P[LLM + 工具循环<br/>max 40 iterations]
    P --> Q{有工具调用?}
    Q -->|是| R[执行工具]
    R --> S[添加工具结果]
    S --> P
    Q -->|否| T[保存会话<br/>JSONL]
    T --> U{message tool 发送?}
    U -->|是| V[跳过响应]
    U -->|否| W[创建 OutboundMessage]
    W --> X[MessageBus.publish_outbound]
    X --> Y[ChannelManager 路由]
    Y --> AA[Channel.send]
    AA --> AB[用户收到回复]
    J --> AB
    K --> AB
    V --> AB
```

**关键特点**:
- 完整的业务流程
- 多个决策点
- 循环和分支并存
- 清晰的标注
- 使用中文标签

## 使用这些模式

1. **类图**: 选择合适的继承/组合模式，突出核心类
2. **时序图**: 清晰标注参与者，使用条件分支展示逻辑
3. **流程图**: 合理使用节点形状，控制图表复杂度
4. **架构图**: 使用子图分组，展示分层结构

所有图表都应：
- 使用中文标签和注释
- 简化次要细节
- 突出核心流程
- 保持可读性

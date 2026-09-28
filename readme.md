# Hello Agent 学习笔记

本项目记录 AI 智能体（Agent）从零学习与实战过程，涵盖环境搭建、Git 版本管理、ReAct 核心范式实现及工具动态调用。

---

## 一、预备工作

### 1. Git 初始化与远程关联

| 步骤 | 操作 | 对应命令 | 说明 |
| :---: | :--- | :--- | :--- |
| **01** | 创建并进入目录 | `mkdir demo && cd demo` | 准备工作目录 |
| **02** | 初始化 Git 仓库 | `git init` | 本地生成 `.git` 管理目录 |
| **03** | 编写忽略文件 | 新建并编辑 `.gitignore` | 必须在 `add` 前完成，忽略 `.venv/` 与 `.env` |
| **04** | 暂存所有修改 | `git add .` | 将工作区变动提交到暂存区 |
| **05** | 提交本地快照 | `git commit -m "feat: initial commit"` | 形成第一个本地版本快照 |
| **06** | 远端创建仓库 | 在 GitHub 点击 New repository | ⚠️ 保持空仓库，不要勾选生成 README |
| **07** | 规范主分支名 | `git branch -M main` | 统一分支名为 `main`，与 GitHub 保持一致 |
| **08** | 关联远端仓库 | `git remote add origin <URL>` | 建立本地与 GitHub 仓库的远程映射通道 |
| **09** | 首次推送绑定 | `git push -u origin main` | 首次带 `-u` 绑定上游分支，后续仅需 `git push` |

> 📌 **Git 撤销备忘**：若误把 `.venv` 放入了暂存区，可执行 `git restore --staged .venv` 撤回暂存（保留本地物理文件）。

---

### 2. Python 虚拟环境与依赖管理

```powershell
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境 (Windows PowerShell / CMD)
.venv\Scripts\activate

# 3. 安装项目依赖
pip install python-dotenv requests openai tavily-python

# 4. 退出虚拟环境
deactivate
```

---

## 二、第一章：Agent 基础（智能旅行助手）

### 1. 目录结构

```text
hello-agent-learn/
├── .env                  # 本地真实环境变量（已加入 .gitignore，防泄密）
├── .env.example          # 环境变量示例模板（提交至 Git 供参考）
├── .gitignore            # Git 忽略配置
├── readme.md             # 项目学习笔记
└── Chapter01/
    ├── main.py           # 主入口：装配组件并驱动 ReAct 循环
    ├── llm/
    │   └── llm.py        # 大模型客户端（兼容 OpenAI 协议）
    ├── prompts/
    │   └── system_prompts.md  # 系统提示词（Prompt 模板）
    └── tools/
        └── tools_register.py  # 工具定义与注册表（实时天气与景点搜索）
```

---

### 2. 环境变量配置 (.env)

克隆项目后，首先在项目根目录下通过模板复制 `.env`：

```powershell
copy .env.example .env
```

在生成的 `.env` 文件中填入实际凭据：

```ini
# 大模型配置（支持 DeepSeek / 商汤 / OpenAI 等兼容接口）
OPENAI_API_KEY="你的API_KEY"
OPENAI_BASE_URL="https://token.sensenova.cn/v1"   # ⚠️ 注意：末尾无需 /chat/completions
MODEL_ID="deepseek-v4.1-flash"

# 外部工具配置（Tavily 搜索）
TAVILY_API_KEY="你的Tavily_KEY"
```

> 💡 **Tavily API Key 获取方式**：
> 1. 前往官网 [tavily.com](https://tavily.com/)（支持使用 GitHub 账号一键授权登录）；
> 2. 在控制台 Dashboard 首页直接复制生成的 API Key（格式为 `tvly-xxxxxx`，每月提供 1000 次免费调用）；
> 3. 将其填入 `.env` 中的 `TAVILY_API_KEY`，Agent 即可联网搜索真实景点信息。

---

### 3. 核心模块与代码逻辑

- **`prompts/system_prompts.md`**  
  纯文本定义智能旅行助手角色、输出规范（严格遵循 `Thought:` 与 `Action:` 成对输出）及任务结束指令 `Finish[最终答案]`。

- **`tools/tools_register.py`**  
  - `get_weather(city)`：调用 `wttr.in` 查询指定城市实时天气。
  - `get_attraction(city, weather)`：调用 `TavilyClient` 联网搜索匹配天气的旅游景点。
  - `available_tools`：统一工具字典映射，供主循环根据模型输出的函数名动态反射调用。

- **`llm/llm.py`**  
  基于官方 `openai` SDK 封装 `OpenAICompatibleClient`，实现统一的大模型服务调用。

- **`main.py`**  
  核心调度中心，启动 ReAct 闭环循环（最多 5 轮迭代）：
  
  ```text
  用户输入 ──> 大模型思考 (Thought) ──> 工具调用 (Action) ──> 观察环境 (Observation) ──> 任务结束 (Finish)
  ```

---

### 4. 运行测试

```powershell
python Chapter01/main.py
```

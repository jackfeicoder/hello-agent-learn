# Hello Agent

# 预备工作
## 1.初始化git
步骤	操作	对应命令 / 动作	说明
1	本地建目录并进入	mkdir demo && cd demo	准备工作目录
2	初始化 Git 仓库	git init	生成本地 .git 管理目录
3	编写忽略文件	新建并编辑 

.gitignore
必须在 add 之前做，防止依赖和垃圾文件入库
4	暂存所有文件	git add .	把工作区改动提交到暂存区
5	提交到本地版本库	git commit -m "feat: initial commit"	形成第一个本地版本快照
6	云端新建空仓库	在 GitHub 点击 New repository	⚠️ 注意：不要勾选初始化 README
7	统一分支名（推荐）	git branch -M main	将默认分支重命名为 main，与 GitHub 对齐
8	关联云端远程地址	git remote add origin <URL>	建立本地与云端的通道
9	首次推送并绑定追踪	git push -u origin main	首次带 -u，后续只需直接输入 git push

## 环境
```python -m venv .venv ```
.venv\Scripts\activate  激活环境
deactivate  退出环境

# 第一章 Agent基础
hello-agent-learn/
├── .env                         # 根目录：存放你的各种真实 Key 和 URL 配置（绝不进 Git）
├── .gitignore
└── Chapter01/
    ├── main.py                  # 主入口：负责装配并运行 Agent 主循环
    ├── llm/
    │   └── llm.py               # 封装的 OpenAICompatibleClient 类
    ├── prompts/
    │   └── system_prompts.md    # 系统提示词（Prompt 模板）
    └── tools/
        └── tools_register.py    # 工具实现及 available_tools 注册字典


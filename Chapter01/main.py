import os
import re
from pathlib import Path
from dotenv import load_dotenv
# 1. 加载根目录下的 .env 文件中的环境变量
load_dotenv()
# 2. 引入自定义模块
from llm.llm import OpenAICompatibleClient
from tools.tools_register import available_tools
# 3. 读取 system_prompts.md 文件的纯文本内容
prompt_file_path = Path(__file__).parent / "prompts" / "system_prompts.md"
AGENT_SYSTEM_PROMPT = prompt_file_path.read_text(encoding="utf-8")
# 4. 从环境变量读取凭据并初始化 LLM 客户端
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")
if not API_KEY or not BASE_URL:
    raise ValueError("请检查 .env 文件，缺少 OPENAI_API_KEY 或 OPENAI_BASE_URL 配置！")
llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)
# 5. 初始化用户请求与历史记录
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]
print(f"用户输入: {user_prompt}\n" + "="*40)
# 6. 运行 ReAct 主循环
for i in range(5):  # 设置最大循环次数
    print(f"--- 循环 {i+1} ---\n")
    
    # 6.1 构建上下文 Prompt
    full_prompt = "\n".join(prompt_history)
    
    # 6.2 调用 LLM 进行思考
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    
    # 截断多余的 Thought-Action 对
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    # 6.3 解析并执行 Action
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()
    # 如果模型判断任务完成
    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break
    
    # 解析工具名与参数并动态执行
    tool_match = re.search(r"(\w+)\(", action_str)
    if not tool_match:
        observation = f"错误: 无法解析工具名称 '{action_str}'"
    else:
        tool_name = tool_match.group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"
    # 6.4 记录观察结果，供下一步循环让模型看见
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
# test_reflection_agent.py
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from my_reflection_agent import MyReflectionAgent

# 加载环境变量
load_dotenv()
# 适当增加超时时间（120秒），为长文本代码审查留出充裕时间
llm = HelloAgentsLLM(timeout=120)

print("=" * 50)
print("🧪 测试 1: 使用默认通用提示词（写作反思）")
print("=" * 50)
general_agent = MyReflectionAgent(name="通用反思助手", llm=llm, max_iterations=2)
result1 = general_agent.run("用100字左右简要概述人工智能的核心定义与发展阶段")
print(f"\n📋 [测试1 最终结果]:\n{result1}\n")

print("=" * 50)
print("🧪 测试 2: 使用自定义代码提示词（代码效率反思优化）")
print("=" * 50)
# 自定义提示词：注入 {last_attempt} 并要求评审直击要点
code_prompts = {
    "initial": "你是Python专家，请编写函数完成任务:\n任务: {task}\n请直接提供可运行的代码和必要注释。",
    "reflect": "请作为代码评审专家，简短精炼地审查以下代码的效率与边界条件（200字以内，重点看是否能进一步优化复杂度）:\n任务: {task}\n当前代码:\n{content}\n\n请指出具体瓶颈。如果代码已经达到最优，请明确回答'无需改进'。",
    "refine": "请根据评审意见重构并优化代码:\n任务: {task}\n上一轮代码:\n{last_attempt}\n评审意见:\n{feedback}\n\n请输出针对性优化后的完整Python代码。"
}

code_agent = MyReflectionAgent(
    name="代码优化助手",
    llm=llm,
    max_iterations=2,
    custom_prompts=code_prompts
)

code_result = code_agent.run("编写一个高效计算第n个斐波那契数的函数，要求处理n为负数或0等边界情况")
print(f"\n💻 [测试2 最终代码]:\n{code_result}\n")

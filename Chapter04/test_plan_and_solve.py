from HelloAgent import HelloAgentsLLM
from PlanAndSolveAgent import PlanAndSolveAgent

# 1. 实例化 LLM 客户端
llm_client = HelloAgentsLLM()

# 2. 将客户端传入智能体
agent = PlanAndSolveAgent(llm_client)

question = """
帮我查一下目标识别中关于海上或水下相关的论文，目前哪个方向更难，
数据集热门或者容易写开题报告或者毕业论文的。背景是计算机硕士。
找几篇相关文献发我，然后研究下目前研究现状，总结一下现存的前沿领域问题。
"""
agent.run(question)

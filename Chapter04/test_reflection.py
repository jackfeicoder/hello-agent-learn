from ReflectionAgent import ReflectionAgent
from HelloAgent import HelloAgentsLLM


if __name__ == "__main__":
    # 初始化LLM客户端
    llm_client = HelloAgentsLLM()
    
    # 初始化ReflectionAgent
    reflection_agent = ReflectionAgent(llm_client)
    
    # 定义要解决的任务
    task = """
    写一个函数来判断一个整数是否为素数

    - 如果是素数，则直接返回 True
    - 如果不是素数，则返回 False
    """
    
    # 运行ReflectionAgent
    final_code = reflection_agent.run(task)
    
    print(f"\n--- 最终生成的代码 ---\n{final_code}")

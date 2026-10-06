# my_reflection_agent.py
from typing import Optional, Dict, Any, List
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message

# 尝试从本地 prompt 模块加载提示词模板
try:
    from prompt import DEFAULT_PROMPTS
except ImportError:
    try:
        from .prompt import DEFAULT_PROMPTS
    except ImportError:
        # 兜底默认提示词
        DEFAULT_PROMPTS = {
            "initial": "请根据以下要求完成任务:\n\n任务: {task}\n\n请提供一个完整、准确的回答。",
            "reflect": "请仔细审查以下回答，并找出可能的问题或改进空间:\n\n# 原始任务:\n{task}\n\n# 当前回答:\n{content}\n\n请分析这个回答的质量，指出不足之处，并提出具体的改进建议。\n如果回答已经很好，请回答'无需改进'。",
            "refine": "请根据反馈意见改进你的回答:\n\n# 原始任务:\n{task}\n\n# 上一轮回答:\n{last_attempt}\n\n# 反馈意见:\n{feedback}\n\n请提供一个改进后的回答。"
        }


class MyReflectionAgent(ReflectionAgent):
    """
    重写的 Reflection Agent - 自我反思与迭代优化的智能体
    
    核心范式：
    1. 生成（Execution）：完成任务的初始尝试
    2. 反思（Reflection）：评判当前结果的质量与不足
    3. 优化（Refinement）：根据反思意见进行迭代改良
    4. 循环直至达到满意标准或达到最大迭代轮次
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_iterations: int = 3,
        custom_prompts: Optional[Dict[str, str]] = None
    ):
        super().__init__(name, llm, system_prompt, config, max_iterations=max_iterations, custom_prompts=custom_prompts)
        self.max_iterations = max_iterations
        # 优先使用传入的自定义提示词，其次使用 prompt.py 中的 DEFAULT_PROMPTS
        self.prompts = custom_prompts if custom_prompts else DEFAULT_PROMPTS
        print(f"✅ {name} 初始化完成，最大反思迭代次数: {max_iterations}")

    def run(self, input_text: str, **kwargs) -> str:
        """
        执行反思与迭代任务
        
        Args:
            input_text: 任务或目标描述
            **kwargs: 传给 LLM 的附加参数
            
        Returns:
            最终迭代优化后的回答
        """
        print(f"\n🤖 {self.name} 开始处理任务: {input_text}")

        # 重置当前轮次的记忆轨迹
        from hello_agents.agents.reflection_agent import Memory
        self.memory = Memory()

        # ---------------- 步骤 1: 初始执行 ----------------
        print("\n🚀 [阶段一: 初始生成]")
        initial_prompt = self.prompts["initial"].format(task=input_text)
        initial_result = self._get_llm_response(initial_prompt, **kwargs)
        self.memory.add_record("execution", initial_result)
        print(f"📝 初始输出:\n{initial_result}\n")

        # ---------------- 步骤 2: 迭代循环 (反思 ➔ 优化) ----------------
        for i in range(self.max_iterations):
            print(f"\n🔄 [阶段二: 迭代优化 - 第 {i + 1}/{self.max_iterations} 轮]")

            # 2.1 反思 (Reflection)
            print("🧐 正在进行自我反思与质量评估...")
            last_result = self.memory.get_last_execution()
            reflect_prompt = self.prompts["reflect"].format(
                task=input_text,
                content=last_result
            )
            feedback = self._get_llm_response(reflect_prompt, **kwargs)
            self.memory.add_record("reflection", feedback)
            print(f"💡 评审员反馈:\n{feedback}\n")

            # 2.2 检查是否达到终止条件
            if self._should_stop(feedback):
                print(f"✅ 反思认为当前结果已达标，提前结束迭代！")
                break

            # 2.3 优化 (Refinement)
            print("🛠️ 正在根据反馈进行针对性优化...")
            refine_prompt = self.prompts["refine"].format(
                task=input_text,
                last_attempt=last_result,
                feedback=feedback
            )
            refined_result = self._get_llm_response(refine_prompt, **kwargs)
            self.memory.add_record("execution", refined_result)
            print(f"✨ 优化后版本:\n{refined_result}\n")

        # ---------------- 步骤 3: 归档与返回 ----------------
        final_result = self.memory.get_last_execution()
        print(f"\n🎯 [任务完成 - 最终交付结果]:\n{final_result}")

        # 归档到 Agent 长期历史记忆
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_result, "assistant"))

        return final_result

    def _should_stop(self, feedback: str) -> bool:
        """
        判断反思意见是否表示已经完美、无需继续改进
        """
        stop_keywords = [
            "无需改进",
            "[无需改进]",
            "无需进一步改进",
            "没有明显的改进空间",
            "no need for improvement",
            "looks good"
        ]
        feedback_lower = feedback.lower()
        return any(keyword.lower() in feedback_lower for keyword in stop_keywords)

    def _get_llm_response(self, prompt: str, **kwargs) -> str:
        """
        调用底层 LLM 获取回答
        """
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.llm.invoke(messages, **kwargs)
        return response or ""

    def get_trajectory(self) -> str:
        """
        获取当前任务的完整迭代轨迹文本
        """
        return self.memory.get_trajectory() if self.memory else ""

    def get_records(self) -> List[Dict[str, Any]]:
        """
        获取结构化的历史迭代记录
        """
        return self.memory.records if self.memory else []

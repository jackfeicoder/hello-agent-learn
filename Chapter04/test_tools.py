# 导入工具执行器和工具包中的搜索工具
from tool_executor import ToolExecutor
from tools import search, SEARCH_TOOL_DESC

# --- 工具初始化与使用示例 ---
if __name__ == '__main__':
    # 1. 初始化工具执行器
    tool_executor = ToolExecutor()

    # 2. 注册实战搜索工具（使用统一导出的工具描述）
    tool_executor.register_tool("Search", SEARCH_TOOL_DESC, search)
    
    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(tool_executor.get_available_tools())

    # 4. 智能体的 Action 调用，查询实时性问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU 5070 价格"

    tool_function = tool_executor.get_tool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误: 未找到名为 '{tool_name}' 的工具。")

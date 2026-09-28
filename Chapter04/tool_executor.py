from typing import Dict, Any, Callable, Optional

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, func: Callable) -> None:
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告: 工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> Optional[Callable]:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def get_available_tools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])

    # 兼容驼峰命名的别名
    registerTool = register_tool
    getTool = get_tool
    getAvailableTools = get_available_tools

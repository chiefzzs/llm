from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from base import llm
from load_config import load_config, load_json_config
# 初始化 ChatOpenAI LLM


# 定义一个支持字典参数的计算器工具
class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "用于执行数学运算。输入应为包含 'num1'、'num2' 和 'operator' 的字典。"

    def _run(self, query: str) -> str:
        try:
            input_dict = json.loads(query)
            num1 = float(input_dict["num1"])
            num2 = float(input_dict["num2"])
            operator = input_dict["operator"]

            if operator == "+":
                return str(num1 + num2)
            elif operator == "-":
                return str(num1 - num2)
            elif operator == "*":
                return str(num1 * num2)
            elif operator == "/":
                return str(num1 / num2)
            else:
                return f"错误：不支持的操作符 '{operator}'。"
        except Exception as e:
            return f"错误：{e}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Calculator does not support async")

# 定义一个支持字典参数的字符串操作工具
class StringTool(BaseTool):
    name: str = "StringTool"
    description: str = "用于执行字符串操作。输入应为包含 'operation' 和 'text' 的字典。"

    def _run(self, query: str) -> str:
        try:
            input_dict = json.loads(query)
            operation = input_dict["operation"]
            text = input_dict["text"]

            if operation == "length":
                return str(len(text))
            elif operation == "uppercase":
                return text.upper()
            elif operation == "lowercase":
                return text.lower()
            else:
                return f"错误：不支持的操作 '{operation}'。"
        except Exception as e:
            return f"错误：{e}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("StringTool does not support async")

# 初始化工具
tools = [
    CalculatorTool(),
    StringTool()
]

# 初始化代理
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# 使用 ChatOpenAI 解析用户输入并生成工具参数
def parse_input_to_json(user_input: str, prompt: str) -> str:
    response = llm([
        SystemMessage(content="你是一个帮助解析用户输入的助手。"),
        HumanMessage(content=prompt.format(user_input=user_input))
    ])
    return response.content.strip()

# 加载配置文件
config = load_config("config.json")
prompt = config["prompt"]

# 用户输入
user_input = "计算 3 加 5"
# user_input = "获取字符串 'hello world' 的长度"
# user_input = "将字符串 'hello world' 转换为大写"

# 解析用户输入
json_input = parse_input_to_json(user_input, prompt)
print(f"解析后的 JSON: {json_input}")

# 使用代理执行
try:
    response = agent.run(json_input)
    print(f"执行结果: {response}")
except Exception as e:
    print(f"错误: {e}")
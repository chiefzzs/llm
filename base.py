import os
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import load_prompt
from langchain.chains import LLMChain

from langchain_openai import ChatOpenAI
import httpx
httpx_client = httpx.Client(http2=True, verify=False)

api_key = os.environ.get('OPENAI_API_KEY')

llm = ChatOpenAI(
    api_key=api_key,
    base_url="https://api-inference.modelscope.cn/v1/",
    model= "Qwen/Qwen2.5-Coder-32B-Instruct",
    # http_client=httpx_client
    # other params...
)


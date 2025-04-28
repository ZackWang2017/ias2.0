#coding=utf-8
# @Time    : 2023/10/12 17:00
# @Author  : zack wang

import json
import sys
from typing import List, Optional, Dict, Any, Tuple, Union
from uuid import UUID

from langchain.memory import ConversationTokenBufferMemory
from langchain.tools.render import render_text_description
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import StructuredTool
from google import genai

from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
import os

from datacenter.discovery_stock_model import search_stock
from financeanalysis.tang_metrix_model_cn import get_metrix_model

load_dotenv()  # 从.env文件中加载环境变量到os.environ

class Action(BaseModel):
    """结构化定义工具的属性"""
    name: str = Field(description="工具或指令名称")
    args: Optional[Dict[str, Any]] = Field(description="工具或指令参数，由参数名称和参数值组成")


class MyPrintHandler(BaseCallbackHandler):
    """自定义LLM CallbackHandler，用于打印大模型返回的思考过程"""
    def __init__(self):
        BaseCallbackHandler.__init__(self)

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        end = ""
        content = token + end
        sys.stdout.write(content)
        sys.stdout.flush()
        return token

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        end = ""
        content = "\n" + end
        sys.stdout.write(content)
        sys.stdout.flush()
        return response

class IASAgent:
    def __init__(
            self,
            llm: BaseChatModel = genai.Client(
                model="gpt-4-turbo", # agent用GPT4效果好一些，推理能力较强
                temperature=0,
                model_kwargs={
                    "seed": 42
                },
            ),
            tools=None,
            prompt: str = "",
            final_prompt: str = "",
            max_thought_steps: Optional[int] = 10,
    ):
        if tools is None:
            tools = []
        self.llm = llm
        self.tools = tools
        self.final_prompt = PromptTemplate.from_template(final_prompt)
        self.max_thought_steps = max_thought_steps # 最多思考步数，避免死循环
        self.output_parser = PydanticOutputParser(pydantic_object=Action)
        self.prompt = self.__init_prompt(prompt)
        self.llm_chain = self.prompt | self.llm | StrOutputParser() # 主流程的LCEL
        self.verbose_printer = MyPrintHandler()

    def __init_prompt(self, prompt):
        return PromptTemplate.from_template(prompt).partial(
            tools=render_text_description(self.tools),
            format_instructions=self.__chinese_friendly(
                self.output_parser.get_format_instructions(),
            )
        )

    def run(self, task_description):
        """Agent主流程"""
		
        # 思考步数
        thought_step_count = 0

        # 初始化记忆
        agent_memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
        )
        agent_memory.save_context(
            {"input": "\ninit"},
            {"output": "\n开始"}
        )

        # 开始逐步思考
        while thought_step_count < self.max_thought_steps:
            print(f">>>>Round: {thought_step_count}<<<<")
            action, response = self.__step(
                task_description=task_description,
                memory=agent_memory
            )

            # 如果是结束指令，执行最后一步
            if action.name == "FINISH":
                break

            # 执行动作
            observation = self.__exec_action(action)
            print(f"----\nObservation:\n{observation}")

            # 更新记忆
            self.__update_memory(agent_memory, response, observation)

            thought_step_count += 1

        if thought_step_count >= self.max_thought_steps:
            # 如果思考步数达到上限，返回错误信息
            reply = "抱歉，我没能完成您的任务。"
        else:
            # 否则，执行最后一步
            final_chain = self.final_prompt | self.llm | StrOutputParser()
            reply = final_chain.invoke({
                "task_description": task_description,
                "memory": agent_memory
            })

        return reply

    def __step(self, task_description, memory) -> Tuple[Action, str]:

        """执行一步思考"""
        response = ""
        for s in self.llm_chain.stream({
            "task_description": task_description,
            "memory": memory
        }, config={
            "callbacks": [
                self.verbose_printer
            ]
        }):
            response += s

        action = self.output_parser.parse(response)
        return action, response

    def __exec_action(self, action: Action) -> str:
        observation = "没有找到工具"
        for tool in self.tools:
            if tool.name == action.name:
                try:
                    # 执行工具
                    observation = tool.run(action.args)
                except ValidationError as e:
                    # 工具的入参异常
                    observation = (
                        f"Validation Error in args: {str(e)}, args: {action.args}"
                    )
                except Exception as e:
                    # 工具执行异常
                    observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    @staticmethod
    def __update_memory(agent_memory, response, observation):
        agent_memory.save_context(
            {"input": response},
            {"output": "\n返回结果:\n" + str(observation)}
        )

    @staticmethod
    def __chinese_friendly(string) -> str:
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{') and line.endswith('}'):
                try:
                    lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
                except:
                    pass
        return '\n'.join(lines)
    
search_stock_tool = StructuredTool.from_function(
    func=search_stock,
    name="查询股票基本信息",
    description="根据输入的股票代码或名称查询股票的基本信息",
)

finish_placeholder = StructuredTool.from_function(
    func=lambda: None,
    name="FINISH",
    description="用于表示任务完成的占位符工具"
)

tools = [search_stock_tool, finish_placeholder]
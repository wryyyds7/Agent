from typing import Callable

from langchain.agents import AgentState
# from django.contrib.staticfiles.management.commands.collectstatic import Command
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from streamlit.runtime import RuntimeState

from utils.logger_handler import logger_agent
from utils.prompt_loader import load_report_prompts, load_system_prompts


@wrap_tool_call
def monitor_tool(
        # 请求的数据封装,函数的参数
        request: ToolCallRequest,
        # 执行的函数本身
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command: # 工具执行的监控
    logger_agent.info(f"[tool monitor]工具调用开始: {request.tool_call['name']}")
    logger_agent.info(f"[tool monitor]工具调用参数: {request.tool_call['args']}")
    try:
        result =  handler(request)
        logger_agent.info(f"[tool monitor]工具调用结束并成功: {request.tool_call['name']}")
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context['report'] = True #设置标记

        return result
    except Exception as e:
        logger_agent.error(f"[tool monitor]工具调用失败: {request.tool_call['name']}\n原因为：{str(e)}", exc_info=True)
        raise e

@before_model
def log_before_mode(
        state: AgentState,      # 整个Agent智能体中的状态信息
        runtime: Runtime,       # 记录了整个执行过程中的上下文信息
):      # 在模型执行前输出日志
    logger_agent.info(f"[log_before_mode]将调佣模型，带有消息{len(state['messages'])}条")
    # logger_agent.info(f"[log_before_mode]当前使用的prompt: {state.prompt.name}")
    logger_agent.debug(f"[log_before_mode]当前使用的内容为:{type(state['messages'][-1]).__name__}| {state['messages'][-1].content.strip()}")

    return None


def report_tool_call():
    pass

@dynamic_prompt  # 每一次在生成提示词前，调用此函数
def report_prompt_switch(request: ModelRequest):     # 动态切换提示词""", runtime: RuntimeState"""
    is_report = request.runtime.context.get('report', False)        # 如果键不存在，则返回False
    if is_report:       # 是报告生成场景，返回报告生成提示词内容
        return load_report_prompts()
    return load_system_prompts()
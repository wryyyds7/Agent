from utils.config_handler import prompts_conf
from utils.path_tools import get_abs_path
from utils.logger_handler import logger_agent

def load_system_prompts():
    try:
        system_prompts_path = get_abs_path(prompts_conf["main_prompt_path"])
    except Exception as e:
        logger_agent.error("[load_system_prompts]加载系统配置项错误: main_prompt_path未配置}")
        raise e

    try:
        return open(system_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger_agent.error(f"[load_system_prompts]解析系统提示词错误: {system_prompts_path}\n{str(e)}")
        raise e

def load_rag_prompts():
    try:
        rag_prompts_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except Exception as e:
        logger_agent.error("[load_rag_prompts]加载配置项错误: rag_summarize_prompt_path未配置}")
        raise e

    try:
        return open(rag_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger_agent.error(f"[load_rag_prompts]解析RAG总结提示词错误: {rag_prompts_path}\n{str(e)}")
        raise e

def load_report_prompts():
    try:
        report_prompts_path = get_abs_path(prompts_conf["report_prompt_path"])
    except Exception as e:
        logger_agent.error("[load_report_prompts]加载配置项错误: report_prompt_path未配置}")
        raise e

    try:
        return open(report_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger_agent.error(f"[load_report_prompts]解析报告生成提示词错误: {report_prompts_path}\n{str(e)}")
        raise e
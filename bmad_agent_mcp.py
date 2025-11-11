#!/usr/bin/env python3
"""
BMAD Agent FastMCP Service

基于 .bmad-core 的智能体调用服务，支持：
- 智能体管理和调用
- 工作流程执行
- 任务管理
- 模板处理
- 状态跟踪
"""

import asyncio
import json
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import re

from fastmcp import FastMCP
from utils import BMADUtils, format_scan_report
from llm_client import initialize_llm_client, get_llm_client

# 初始化 FastMCP 应用
mcp = FastMCP("BMAD Agent Service")

# 全局配置
# Build absolute path to .bmad-core to ensure it's found regardless of CWD
SCRIPT_DIR = Path(__file__).resolve().parent
BMAD_CORE_PATH = SCRIPT_DIR / ".bmad-core"
CONFIG_FILE = BMAD_CORE_PATH / "core-config.yaml"

# LLM 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # DeepSeek API Key（外部 API 模式使用）
USE_BUILTIN_LLM = os.getenv("USE_BUILTIN_LLM", "true").lower() == "true"  # 默认使用内置 LLM

# 初始化 LLM 客户端
if USE_BUILTIN_LLM:
    initialize_llm_client()  # 内置 LLM 模式，不需要 API Key
else:
    initialize_llm_client(DEEPSEEK_API_KEY)  # 外部 API 模式

@dataclass
class AgentInfo:
    """智能体信息"""
    id: str
    name: str
    title: str
    icon: str
    description: str  # 添加描述字段
    when_to_use: str
    role: str
    style: str
    identity: str
    focus: str
    dependencies: Dict[str, List[str]]

@dataclass
class WorkflowInfo:
    """工作流程信息"""
    id: str
    name: str
    description: str
    type: str
    project_types: List[str]
    sequence: List[Dict[str, Any]]

@dataclass
class TaskInfo:
    """任务信息"""
    name: str
    description: str
    agent: Optional[str]
    dependencies: List[str]
    outputs: List[str]

class BMADCore:
    """BMAD 核心管理器 - 优化版本，支持缓存和懒加载"""
    
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.workflows: Dict[str, WorkflowInfo] = {}
        self.tasks: Dict[str, TaskInfo] = {}
        self.templates: Dict[str, str] = {}
        self.current_agent: Optional[str] = None
        self.current_workflow: Optional[str] = None
        self.workflow_state: Dict[str, Any] = {}
        
        # Performance optimization: cache for parsed files
        self._agent_cache: Dict[str, tuple[float, AgentInfo]] = {}
        self._workflow_cache: Dict[str, tuple[float, WorkflowInfo]] = {}
        self._templates_loaded = False
        self._tasks_loaded = False
        
        self.load_core_config()
        self.discover_agents()
        self.discover_workflows()
        # Lazy load tasks and templates only when needed
    
    def load_core_config(self):
        """加载核心配置"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}
    
    def discover_agents(self):
        """发现所有智能体 - 优化版本，使用缓存"""
        agents_dir = BMAD_CORE_PATH / "agents"
        if not agents_dir.exists():
            return
        
        for agent_file in agents_dir.glob("*.md"):
            agent_id = agent_file.stem
            
            # Check cache first
            mtime = agent_file.stat().st_mtime
            if agent_id in self._agent_cache:
                cached_mtime, cached_info = self._agent_cache[agent_id]
                if cached_mtime == mtime:
                    self.agents[agent_id] = cached_info
                    continue
            
            # Parse and cache
            agent_info = self.parse_agent_file(agent_file)
            if agent_info:
                self.agents[agent_id] = agent_info
                self._agent_cache[agent_id] = (mtime, agent_info)
    
    def parse_agent_file(self, file_path: Path) -> Optional[AgentInfo]:
        """解析智能体文件 - 优化版本"""
        try:
            # Read file once
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 YAML 配置 - 使用更高效的正则表达式
            yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
            if not yaml_match:
                return None
            
            yaml_content = yaml_match.group(1)
            config = yaml.safe_load(yaml_content)
            
            # Quick validation
            if not isinstance(config, dict):
                return None
            
            agent_config = config.get('agent', {})
            if not agent_config:
                return None
            
            persona_config = config.get('persona', {})
            dependencies = config.get('dependencies', {})
            
            return AgentInfo(
                id=agent_config.get('id', file_path.stem),
                name=agent_config.get('name', ''),
                title=agent_config.get('title', ''),
                icon=agent_config.get('icon', '🤖'),
                description=agent_config.get('description', agent_config.get('title', '')),
                when_to_use=agent_config.get('whenToUse', ''),
                role=persona_config.get('role', ''),
                style=persona_config.get('style', ''),
                identity=persona_config.get('identity', ''),
                focus=persona_config.get('focus', ''),
                dependencies=dependencies
            )
        except (IOError, yaml.YAMLError) as e:
            # Specific error types for I/O and YAML parsing
            return None
        except Exception:
            # Catch-all for other errors
            return None
    
    def discover_workflows(self):
        """发现所有工作流程 - 优化版本，使用缓存"""
        workflows_dir = BMAD_CORE_PATH / "workflows"
        if not workflows_dir.exists():
            return
        
        for workflow_file in workflows_dir.glob("*.yaml"):
            workflow_id = workflow_file.stem
            
            # Check cache first
            mtime = workflow_file.stat().st_mtime
            if workflow_id in self._workflow_cache:
                cached_mtime, cached_info = self._workflow_cache[workflow_id]
                if cached_mtime == mtime:
                    self.workflows[workflow_id] = cached_info
                    continue
            
            # Parse and cache
            workflow_info = self.parse_workflow_file(workflow_file)
            if workflow_info:
                self.workflows[workflow_info.id] = workflow_info
                self._workflow_cache[workflow_id] = (mtime, workflow_info)
    
    def parse_workflow_file(self, file_path: Path) -> Optional[WorkflowInfo]:
        """解析工作流程文件 - 优化版本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Quick validation
            if not isinstance(config, dict):
                return None
            
            workflow_config = config.get('workflow', {})
            if not workflow_config:
                return None
            
            return WorkflowInfo(
                id=workflow_config.get('id', file_path.stem),
                name=workflow_config.get('name', ''),
                description=workflow_config.get('description', ''),
                type=workflow_config.get('type', ''),
                project_types=workflow_config.get('project_types', []),
                sequence=workflow_config.get('sequence', [])
            )
        except (IOError, yaml.YAMLError):
            # Specific error types for I/O and YAML parsing
            return None
        except Exception:
            # Catch-all for other errors
            return None
    
    def discover_tasks(self):
        """发现所有任务 - 懒加载优化"""
        if self._tasks_loaded:
            return
        
        tasks_dir = BMAD_CORE_PATH / "tasks"
        if not tasks_dir.exists():
            self._tasks_loaded = True
            return
        
        for task_file in tasks_dir.glob("*.md"):
            task_name = task_file.stem
            # 简化的任务信息，实际应该解析 markdown 文件
            self.tasks[task_name] = TaskInfo(
                name=task_name,
                description=f"Task: {task_name}",
                agent=None,
                dependencies=[],
                outputs=[]
            )
        
        self._tasks_loaded = True
    
    def discover_templates(self):
        """发现所有模板 - 懒加载优化"""
        if self._templates_loaded:
            return
        
        templates_dir = BMAD_CORE_PATH / "templates"
        if not templates_dir.exists():
            self._templates_loaded = True
            return
        
        for template_file in templates_dir.glob("*.md"):
            template_name = template_file.stem
            with open(template_file, 'r', encoding='utf-8') as f:
                self.templates[template_name] = f.read()
        
        self._templates_loaded = True
    
    def get_task(self, task_name: str) -> Optional[TaskInfo]:
        """获取任务信息，触发懒加载"""
        if not self._tasks_loaded:
            self.discover_tasks()
        return self.tasks.get(task_name)
    
    def get_all_tasks(self) -> Dict[str, TaskInfo]:
        """获取所有任务，触发懒加载"""
        if not self._tasks_loaded:
            self.discover_tasks()
        return self.tasks
    
    def get_template(self, template_name: str) -> Optional[str]:
        """获取模板，触发懒加载"""
        if not self._templates_loaded:
            self.discover_templates()
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, str]:
        """获取所有模板，触发懒加载"""
        if not self._templates_loaded:
            self.discover_templates()
        return self.templates

# 全局 BMAD 核心实例
bmad_core = BMADCore()

# 全局 LLM 客户端实例
llm_client = get_llm_client()

# 创建不使用装饰器的核心函数
def _list_agents_core() -> Dict[str, Any]:
    """核心 list_agents 函数（不使用装饰器）"""
    try:
        agents_list = []
        for agent_id, agent in bmad_core.agents.items():
            agents_list.append({
                "id": agent.id,
                "name": agent.name,
                "title": agent.title,
                "icon": agent.icon,
                "description": agent.description,
                "when_to_use": agent.when_to_use,
                "role": agent.role,
                "focus": agent.focus
            })

        return {
            "success": True,
            "agents": agents_list,
            "count": len(agents_list),
            "current_agent": bmad_core.current_agent,
            "message": f"发现 {len(agents_list)} 个智能体"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agents": [],
            "count": 0,
            "current_agent": None
        }

@mcp.tool()
def list_agents() -> Dict[str, Any]:
    """
    列出所有可用的 BMAD 智能体

    Returns:
        包含所有智能体信息的字典
    """
    return _list_agents_core()

@mcp.tool()
def get_agent_details(agent_id: str) -> Dict[str, Any]:
    """
    获取特定智能体的详细信息
    
    Args:
        agent_id: 智能体ID
        
    Returns:
        智能体的详细信息
    """
    if agent_id not in bmad_core.agents:
        return {"error": f"Agent '{agent_id}' not found"}
    
    agent = bmad_core.agents[agent_id]
    return asdict(agent)

@mcp.tool()
def activate_agent(agent_id: str) -> Dict[str, Any]:
    """
    激活指定的智能体
    
    Args:
        agent_id: 要激活的智能体ID
        
    Returns:
        激活结果和智能体信息
    """
    if agent_id not in bmad_core.agents:
        return {"error": f"Agent '{agent_id}' not found"}
    
    bmad_core.current_agent = agent_id
    agent = bmad_core.agents[agent_id]
    
    return {
        "success": True,
        "message": f"Activated agent: {agent.title} {agent.icon}",
        "agent": {
            "id": agent.id,
            "name": agent.name,
            "title": agent.title,
            "icon": agent.icon,
            "role": agent.role,
            "focus": agent.focus
        }
    }

@mcp.tool()
def list_workflows() -> Dict[str, Any]:
    """
    列出所有可用的工作流程
    
    Returns:
        包含所有工作流程信息的字典
    """
    return {
        "workflows": {
            workflow_id: {
                "name": workflow.name,
                "description": workflow.description,
                "type": workflow.type,
                "project_types": workflow.project_types
            }
            for workflow_id, workflow in bmad_core.workflows.items()
        },
        "current_workflow": bmad_core.current_workflow
    }

@mcp.tool()
def get_workflow_details(workflow_id: str) -> Dict[str, Any]:
    """
    获取特定工作流程的详细信息
    
    Args:
        workflow_id: 工作流程ID
        
    Returns:
        工作流程的详细信息
    """
    if workflow_id not in bmad_core.workflows:
        return {"error": f"Workflow '{workflow_id}' not found"}
    
    workflow = bmad_core.workflows[workflow_id]
    return asdict(workflow)

@mcp.tool()
def start_workflow(workflow_id: str, project_type: Optional[str] = None) -> Dict[str, Any]:
    """
    启动指定的工作流程

    Args:
        workflow_id: 工作流程ID
        project_type: 项目类型（可选）

    Returns:
        工作流程启动结果
    """
    if workflow_id not in bmad_core.workflows:
        return {"error": f"Workflow '{workflow_id}' not found"}

    workflow = bmad_core.workflows[workflow_id]

    # 检查项目类型是否匹配
    if project_type and project_type not in workflow.project_types:
        return {
            "error": f"Project type '{project_type}' not supported by workflow '{workflow_id}'",
            "supported_types": workflow.project_types
        }

    # 初始化工作流程状态
    bmad_core.current_workflow = workflow_id
    bmad_core.workflow_state = {
        "workflow_id": workflow_id,
        "project_type": project_type,
        "current_step": 0,
        "completed_steps": [],
        "created_artifacts": [],
        "started_at": datetime.now().isoformat(),
        "status": "active"
    }

    # 获取第一个步骤
    first_step = workflow.sequence[0] if workflow.sequence else None

    return {
        "success": True,
        "message": f"Started workflow: {workflow.name}",
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "total_steps": len(workflow.sequence)
        },
        "next_step": first_step,
        "state": bmad_core.workflow_state
    }

@mcp.tool()
def get_workflow_status() -> Dict[str, Any]:
    """
    获取当前工作流程的状态

    Returns:
        当前工作流程状态信息
    """
    if not bmad_core.current_workflow:
        return {"message": "No active workflow"}

    workflow = bmad_core.workflows[bmad_core.current_workflow]
    state = bmad_core.workflow_state

    current_step_index = state.get("current_step", 0)
    total_steps = len(workflow.sequence)
    progress = (current_step_index / total_steps * 100) if total_steps > 0 else 0

    current_step = None
    if current_step_index < total_steps:
        current_step = workflow.sequence[current_step_index]

    return {
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description
        },
        "progress": {
            "current_step": current_step_index,
            "total_steps": total_steps,
            "percentage": round(progress, 2),
            "completed_steps": state.get("completed_steps", []),
            "created_artifacts": state.get("created_artifacts", [])
        },
        "current_step": current_step,
        "status": state.get("status", "unknown"),
        "started_at": state.get("started_at")
    }

@mcp.tool()
def advance_workflow_step(artifacts_created: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    推进工作流程到下一步

    Args:
        artifacts_created: 在当前步骤中创建的文档/产物列表

    Returns:
        工作流程推进结果
    """
    if not bmad_core.current_workflow:
        return {"error": "No active workflow"}

    workflow = bmad_core.workflows[bmad_core.current_workflow]
    state = bmad_core.workflow_state

    current_step_index = state.get("current_step", 0)

    if current_step_index >= len(workflow.sequence):
        return {"error": "Workflow already completed"}

    # 记录完成的步骤
    completed_step = workflow.sequence[current_step_index]
    state["completed_steps"].append({
        "step_index": current_step_index,
        "step": completed_step,
        "completed_at": datetime.now().isoformat(),
        "artifacts": artifacts_created or []
    })

    # 添加创建的产物
    if artifacts_created:
        state["created_artifacts"].extend(artifacts_created)

    # 推进到下一步
    state["current_step"] = current_step_index + 1

    # 检查是否完成
    if state["current_step"] >= len(workflow.sequence):
        state["status"] = "completed"
        state["completed_at"] = datetime.now().isoformat()
        next_step = None
        message = f"Workflow '{workflow.name}' completed successfully!"
    else:
        next_step = workflow.sequence[state["current_step"]]
        message = f"Advanced to step {state['current_step'] + 1} of {len(workflow.sequence)}"

    return {
        "success": True,
        "message": message,
        "completed_step": completed_step,
        "next_step": next_step,
        "progress": {
            "current_step": state["current_step"],
            "total_steps": len(workflow.sequence),
            "percentage": round((state["current_step"] / len(workflow.sequence)) * 100, 2)
        },
        "status": state["status"]
    }

@mcp.tool()
def list_tasks(agent_id: Optional[str] = None) -> Dict[str, Any]:
    """
    列出可用的任务

    Args:
        agent_id: 可选的智能体ID，用于过滤特定智能体的任务

    Returns:
        任务列表
    """
    # Use lazy loading
    tasks = bmad_core.get_all_tasks()

    if agent_id:
        if agent_id not in bmad_core.agents:
            return {"error": f"Agent '{agent_id}' not found"}

        agent = bmad_core.agents[agent_id]
        agent_tasks = {}

        # 获取智能体相关的任务
        for task_type, task_list in agent.dependencies.items():
            if task_type == "tasks":
                for task_name in task_list:
                    if task_name in tasks:
                        agent_tasks[task_name] = asdict(tasks[task_name])

        return {
            "agent": agent_id,
            "tasks": agent_tasks
        }

    return {
        "tasks": {name: asdict(task) for name, task in tasks.items()}
    }

@mcp.tool()
def execute_task(task_name: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    执行指定的任务

    Args:
        task_name: 任务名称
        context: 任务执行上下文

    Returns:
        任务执行结果
    """
    # Use lazy loading
    task = bmad_core.get_task(task_name)
    if not task:
        return {"error": f"Task '{task_name}' not found"}

    # 检查是否有激活的智能体
    if not bmad_core.current_agent:
        return {"error": "No agent activated. Please activate an agent first."}

    # 模拟任务执行
    result = {
        "success": True,
        "message": f"Executed task '{task_name}' with agent '{bmad_core.current_agent}'",
        "task": asdict(task),
        "agent": bmad_core.current_agent,
        "context": context or {},
        "executed_at": datetime.now().isoformat()
    }

    # 如果有活动的工作流程，记录任务执行
    if bmad_core.current_workflow:
        if "task_executions" not in bmad_core.workflow_state:
            bmad_core.workflow_state["task_executions"] = []

        bmad_core.workflow_state["task_executions"].append({
            "task_name": task_name,
            "agent": bmad_core.current_agent,
            "executed_at": datetime.now().isoformat(),
            "context": context
        })

    return result

@mcp.tool()
def call_agent_with_llm(agent_id: str, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    使用 LLM 调用智能体执行任务

    Args:
        agent_id: 智能体ID
        task: 要执行的任务描述
        context: 任务上下文信息

    Returns:
        智能体执行结果
    """
    try:
        # 检查智能体是否存在
        if agent_id not in bmad_core.agents:
            return {
                "success": False,
                "error": f"智能体 '{agent_id}' 不存在",
                "available_agents": list(bmad_core.agents.keys())
            }

        agent = bmad_core.agents[agent_id]

        # 构建角色提示
        role_prompt = f"""你现在是 {agent.name}（{agent.title}）。

🎭 角色身份：{agent.identity}

🎯 专业领域：{agent.focus}

💼 工作风格：{agent.style}

📋 核心职责：{agent.role}

🔧 使用场景：{agent.when_to_use}

请以这个角色的身份，用专业的态度和方式来处理用户的任务。保持角色的专业性和一致性。"""

        # 获取当前 LLM 模式
        current_mode = "builtin_llm" if llm_client.use_builtin_llm else "external_api"

        if current_mode == "builtin_llm":
            # 内置 LLM 模式：返回角色提示让 Cursor 的 LLM 使用
            return {
                "success": True,
                "agent_id": agent_id,
                "agent_name": agent.name,
                "agent_title": agent.title,
                "task": task,
                "role_prompt": role_prompt,
                "context": context or {},
                "mode": "builtin_llm",
                "mode_description": "Cursor 内置 LLM",
                "message": f"已激活 {agent.name}，请以此角色身份处理任务",
                "executed_at": datetime.now().isoformat()
            }
        else:
            # 外部 API 模式：调用 DeepSeek API
            try:
                # 获取 LLM 客户端
                llm_client_instance = get_llm_client()
                if not llm_client_instance:
                    return {"error": "LLM 客户端未初始化"}

                # 获取智能体配置
                agent_config = {
                    "title": agent.title,
                    "role": agent.role,
                    "style": agent.style,
                    "identity": agent.identity,
                    "focus": agent.focus
                }

                # 调用 LLM
                result = llm_client_instance.call_agent(agent_id, agent_config, task, context)

                # 添加模式信息和时间戳
                result["mode"] = "external_api"
                result["mode_description"] = "DeepSeek API"
                result["executed_at"] = datetime.now().isoformat()

                return result

            except Exception as api_error:
                return {
                    "success": False,
                    "agent_id": agent_id,
                    "task": task,
                    "error": f"DeepSeek API 调用失败: {str(api_error)}",
                    "suggestion": "可以尝试切换到内置 LLM 模式：switch_llm_mode('builtin')",
                    "mode": "external_api"
                }

    except Exception as e:
        return {
            "success": False,
            "agent_id": agent_id,
            "task": task,
            "error": f"调用智能体失败: {str(e)}"
        }

@mcp.tool()
def analyze_requirements_with_llm(requirements: str, project_type: str = "web-app") -> Dict[str, Any]:
    """
    使用 LLM 分析项目需求

    Args:
        requirements: 项目需求描述
        project_type: 项目类型

    Returns:
        需求分析结果
    """
    try:
        # 获取 LLM 客户端
        llm_client = get_llm_client()
        if not llm_client:
            return {"error": "LLM 客户端未初始化"}

        # 调用需求分析
        result = llm_client.analyze_requirements(requirements, project_type)

        # 添加时间戳
        result["analyzed_at"] = datetime.now().isoformat()

        return result

    except Exception as e:
        return {
            "success": False,
            "requirements": requirements,
            "project_type": project_type,
            "error": f"需求分析失败: {str(e)}"
        }

@mcp.tool()
def list_templates() -> Dict[str, Any]:
    """
    列出所有可用的模板

    Returns:
        模板列表
    """
    # Use lazy loading
    templates = bmad_core.get_all_templates()
    return {
        "templates": list(templates.keys()),
        "count": len(templates)
    }

@mcp.tool()
def get_template(template_name: str) -> Dict[str, Any]:
    """
    获取指定模板的内容

    Args:
        template_name: 模板名称

    Returns:
        模板内容
    """
    # Use lazy loading
    template_content = bmad_core.get_template(template_name)
    if not template_content:
        return {"error": f"Template '{template_name}' not found"}

    return {
        "template_name": template_name,
        "content": template_content
    }

@mcp.tool()
def get_system_status() -> Dict[str, Any]:
    """
    获取 BMAD 系统状态

    Returns:
        系统状态信息
    """
    # 获取当前 LLM 模式
    current_mode = "builtin_llm" if llm_client.use_builtin_llm else "external_api"

    return {
        "bmad_core_path": str(BMAD_CORE_PATH),
        "config_loaded": bool(bmad_core.config),
        "agents_count": len(bmad_core.agents),
        "workflows_count": len(bmad_core.workflows),
        "tasks_count": len(bmad_core.get_all_tasks()),
        "templates_count": len(bmad_core.get_all_templates()),
        "current_agent": bmad_core.current_agent,
        "current_workflow": bmad_core.current_workflow,
        "workflow_active": bool(bmad_core.current_workflow),
        "system_time": datetime.now().isoformat(),
        "llm_mode": current_mode,
        "llm_mode_description": "Cursor 内置 LLM" if current_mode == "builtin_llm" else "DeepSeek API",
        "llm_client_ready": llm_client is not None,
        "lazy_loading": {
            "tasks_loaded": bmad_core._tasks_loaded,
            "templates_loaded": bmad_core._templates_loaded
        }
    }

@mcp.tool()
def switch_llm_mode(mode: str) -> Dict[str, Any]:
    """
    切换 LLM 模式

    Args:
        mode: LLM 模式，可选值：'builtin' (内置LLM) 或 'external' (外部API)

    Returns:
        切换结果信息
    """
    try:
        if mode.lower() in ['builtin', 'builtin_llm', 'internal', 'cursor']:
            # 切换到内置 LLM 模式
            os.environ["USE_BUILTIN_LLM"] = "true"

            # 重新初始化 LLM 客户端
            # 注意：这里只是设置环境变量，实际的客户端会在下次调用时重新初始化

            return {
                "success": True,
                "mode": "builtin_llm",
                "description": "Cursor 内置 LLM",
                "message": "已切换到 Cursor 内置 LLM 模式",
                "features": [
                    "✅ 使用 Cursor IDE 内置的 LLM",
                    "✅ 无需外部 API 调用",
                    "✅ 响应更快，无网络延迟",
                    "✅ 无 API 费用"
                ]
            }

        elif mode.lower() in ['external', 'external_api', 'api', 'deepseek']:
            # 切换到外部 API 模式
            os.environ["USE_BUILTIN_LLM"] = "false"

            # 重新初始化 LLM 客户端
            # 注意：这里只是设置环境变量，实际的客户端会在下次调用时重新初始化

            return {
                "success": True,
                "mode": "external_api",
                "description": "DeepSeek API",
                "message": "已切换到 DeepSeek API 模式",
                "features": [
                    "✅ 使用 DeepSeek API",
                    "✅ 专门的 LLM 模型",
                    "✅ 更强的推理能力",
                    "⚠️  需要网络连接和 API Key"
                ],
                "note": "请确保已设置 DEEPSEEK_API_KEY 环境变量"
            }

        else:
            return {
                "success": False,
                "error": f"无效的模式: {mode}",
                "valid_modes": [
                    "builtin - Cursor 内置 LLM",
                    "external - DeepSeek API"
                ]
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"切换模式失败: {str(e)}",
            "current_mode": "builtin_llm" if llm_client.use_builtin_llm else "external_api"
        }

@mcp.tool()
def get_llm_mode_info() -> Dict[str, Any]:
    """
    获取 LLM 模式详细信息

    Returns:
        LLM 模式信息
    """
    current_mode = "builtin_llm" if llm_client.use_builtin_llm else "external_api"

    mode_info = {
        "current_mode": current_mode,
        "current_description": "Cursor 内置 LLM" if current_mode == "builtin_llm" else "DeepSeek API",
        "available_modes": {
            "builtin_llm": {
                "name": "Cursor 内置 LLM",
                "description": "使用 Cursor IDE 内置的 LLM",
                "advantages": [
                    "无需外部 API 调用",
                    "响应更快，无网络延迟",
                    "无 API 费用",
                    "隐私保护更好"
                ],
                "usage": "switch_llm_mode('builtin')"
            },
            "external_api": {
                "name": "DeepSeek API",
                "description": "使用 DeepSeek 外部 API",
                "advantages": [
                    "专门的 LLM 模型",
                    "更强的推理能力",
                    "支持更复杂的任务",
                    "模型更新更频繁"
                ],
                "requirements": [
                    "需要网络连接",
                    "需要 DEEPSEEK_API_KEY"
                ],
                "usage": "switch_llm_mode('external')"
            }
        }
    }

    # 检查 DeepSeek API Key
    if os.getenv("DEEPSEEK_API_KEY"):
        mode_info["deepseek_api_key_status"] = "已设置"
    else:
        mode_info["deepseek_api_key_status"] = "未设置"
        mode_info["deepseek_setup_note"] = "要使用 DeepSeek API，请设置环境变量 DEEPSEEK_API_KEY"

    return mode_info

@mcp.tool()
def scan_bmad_core() -> Dict[str, Any]:
    """
    扫描 .bmad-core 目录并验证文件

    Returns:
        扫描结果和验证报告
    """
    scan_result = BMADUtils.scan_bmad_core(BMAD_CORE_PATH)
    report = format_scan_report(scan_result)

    return {
        "scan_result": scan_result,
        "report": report
    }

@mcp.tool()
def validate_agent(agent_id: str) -> Dict[str, Any]:
    """
    验证特定智能体文件

    Args:
        agent_id: 智能体ID

    Returns:
        验证结果
    """
    agent_file = BMAD_CORE_PATH / "agents" / f"{agent_id}.md"

    if not agent_file.exists():
        return {"error": f"Agent file '{agent_id}.md' not found"}

    return BMADUtils.validate_agent_file(agent_file)

@mcp.tool()
def validate_workflow(workflow_id: str) -> Dict[str, Any]:
    """
    验证特定工作流程文件

    Args:
        workflow_id: 工作流程ID

    Returns:
        验证结果
    """
    workflow_file = BMAD_CORE_PATH / "workflows" / f"{workflow_id}.yaml"

    if not workflow_file.exists():
        return {"error": f"Workflow file '{workflow_id}.yaml' not found"}

    return BMADUtils.validate_workflow_file(workflow_file)

@mcp.tool()
def export_workflow_state(output_file: str) -> Dict[str, Any]:
    """
    导出当前工作流程状态到文件

    Args:
        output_file: 输出文件路径

    Returns:
        导出结果
    """
    if not bmad_core.current_workflow:
        return {"error": "No active workflow to export"}

    output_path = Path(output_file)
    success = BMADUtils.export_workflow_state(bmad_core.workflow_state, output_path)

    if success:
        return {
            "success": True,
            "message": f"Workflow state exported to {output_file}",
            "file_path": str(output_path.absolute())
        }
    else:
        return {"error": f"Failed to export workflow state to {output_file}"}

@mcp.tool()
def import_workflow_state(input_file: str) -> Dict[str, Any]:
    """
    从文件导入工作流程状态

    Args:
        input_file: 输入文件路径

    Returns:
        导入结果
    """
    input_path = Path(input_file)

    if not input_path.exists():
        return {"error": f"Input file '{input_file}' not found"}

    state = BMADUtils.import_workflow_state(input_path)

    if state:
        bmad_core.workflow_state = state
        bmad_core.current_workflow = state.get("workflow_id")

        return {
            "success": True,
            "message": f"Workflow state imported from {input_file}",
            "workflow_id": bmad_core.current_workflow,
            "state": state
        }
    else:
        return {"error": f"Failed to import workflow state from {input_file}"}

@mcp.tool()
def generate_workflow_report() -> Dict[str, Any]:
    """
    生成当前工作流程的执行报告

    Returns:
        工作流程报告
    """
    if not bmad_core.current_workflow:
        return {"error": "No active workflow"}

    report = BMADUtils.generate_workflow_report(bmad_core.workflow_state)

    return {
        "workflow_id": bmad_core.current_workflow,
        "report": report,
        "state": bmad_core.workflow_state
    }

@mcp.tool()
def reset_workflow() -> Dict[str, Any]:
    """
    重置当前工作流程状态

    Returns:
        重置结果
    """
    if not bmad_core.current_workflow:
        return {"message": "No active workflow to reset"}

    old_workflow = bmad_core.current_workflow
    bmad_core.current_workflow = None
    bmad_core.workflow_state = {}

    return {
        "success": True,
        "message": f"Reset workflow '{old_workflow}'",
        "previous_workflow": old_workflow
    }

@mcp.tool()
def get_agent_tasks(agent_id: str) -> Dict[str, Any]:
    """
    获取特定智能体的所有相关任务和能力

    Args:
        agent_id: 智能体ID

    Returns:
        智能体的任务和能力信息
    """
    if agent_id not in bmad_core.agents:
        return {"error": f"Agent '{agent_id}' not found"}

    agent = bmad_core.agents[agent_id]

    # 获取智能体相关的任务 - 使用懒加载
    all_tasks = bmad_core.get_all_tasks()
    agent_tasks = {}
    for task_type, task_list in agent.dependencies.items():
        if task_type == "tasks":
            for task_name in task_list:
                if task_name in all_tasks:
                    agent_tasks[task_name] = asdict(all_tasks[task_name])

    # 获取智能体相关的模板 - 使用懒加载
    all_templates = bmad_core.get_all_templates()
    agent_templates = {}
    for task_type, task_list in agent.dependencies.items():
        if task_type == "templates":
            for template_name in task_list:
                if template_name in all_templates:
                    agent_templates[template_name] = len(all_templates[template_name])

    return {
        "agent": asdict(agent),
        "tasks": agent_tasks,
        "templates": agent_templates,
        "dependencies": agent.dependencies
    }

if __name__ == "__main__":
    mcp.run()

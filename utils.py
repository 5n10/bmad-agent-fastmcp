#!/usr/bin/env python3
"""
BMAD Agent FastMCP Service 工具函数

提供各种辅助功能和工具
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class BMADUtils:
    """BMAD 工具类"""
    
    @staticmethod
    def validate_agent_file(file_path: Path) -> Dict[str, Any]:
        """验证智能体文件格式 - 优化版本"""
        result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "agent_info": None
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含 YAML 配置
            import re
            yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
            if not yaml_match:
                result["errors"].append("未找到 YAML 配置块")
                return result
            
            # 解析 YAML
            yaml_content = yaml_match.group(1)
            config = yaml.safe_load(yaml_content)
            
            # Quick type check
            if not isinstance(config, dict):
                result["errors"].append("YAML 配置不是有效的字典")
                return result
            
            # 验证必需字段
            required_fields = {
                "agent": ["id", "name", "title"],
                "persona": ["role"]
            }
            
            for section, fields in required_fields.items():
                if section not in config:
                    result["errors"].append(f"缺少 {section} 配置节")
                    continue
                
                section_data = config[section]
                if not isinstance(section_data, dict):
                    result["errors"].append(f"{section} 配置节不是有效的字典")
                    continue
                
                for field in fields:
                    if field not in section_data:
                        result["errors"].append(f"缺少 {section}.{field} 字段")
            
            if not result["errors"]:
                result["valid"] = True
                result["agent_info"] = config
            
        except yaml.YAMLError as e:
            result["errors"].append(f"YAML 解析错误: {str(e)}")
        except IOError as e:
            result["errors"].append(f"文件读取错误: {str(e)}")
        except Exception as e:
            result["errors"].append(f"未知错误: {str(e)}")
        
        return result
    
    @staticmethod
    def validate_workflow_file(file_path: Path) -> Dict[str, Any]:
        """验证工作流程文件格式 - 优化版本"""
        result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "workflow_info": None
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Quick type check
            if not isinstance(config, dict):
                result["errors"].append("配置不是有效的字典")
                return result
            
            # 验证必需字段
            if "workflow" not in config:
                result["errors"].append("缺少 workflow 配置节")
                return result
            
            workflow = config["workflow"]
            if not isinstance(workflow, dict):
                result["errors"].append("workflow 配置节不是有效的字典")
                return result
            
            required_fields = ["id", "name", "description"]
            
            for field in required_fields:
                if field not in workflow:
                    result["errors"].append(f"缺少 workflow.{field} 字段")
            
            # 验证序列
            if "sequence" in workflow:
                if not isinstance(workflow["sequence"], list):
                    result["errors"].append("workflow.sequence 必须是列表")
                elif len(workflow["sequence"]) == 0:
                    result["warnings"].append("工作流程序列为空")
            else:
                result["warnings"].append("缺少 workflow.sequence 字段")
            
            if not result["errors"]:
                result["valid"] = True
                result["workflow_info"] = config
            
        except yaml.YAMLError as e:
            result["errors"].append(f"YAML 解析错误: {str(e)}")
        except IOError as e:
            result["errors"].append(f"文件读取错误: {str(e)}")
        except Exception as e:
            result["errors"].append(f"未知错误: {str(e)}")
        
        return result
    
    @staticmethod
    def export_workflow_state(workflow_state: Dict[str, Any], output_file: Path):
        """导出工作流程状态到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(workflow_state, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"导出工作流程状态失败: {e}")
            return False
    
    @staticmethod
    def import_workflow_state(input_file: Path) -> Optional[Dict[str, Any]]:
        """从文件导入工作流程状态"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"导入工作流程状态失败: {e}")
            return None
    
    @staticmethod
    def generate_workflow_report(workflow_state: Dict[str, Any]) -> str:
        """生成工作流程报告"""
        if not workflow_state:
            return "无工作流程状态数据"
        
        report = []
        report.append("# 工作流程执行报告")
        report.append("")
        
        # 基本信息
        report.append("## 基本信息")
        report.append(f"- 工作流程ID: {workflow_state.get('workflow_id', 'N/A')}")
        report.append(f"- 项目类型: {workflow_state.get('project_type', 'N/A')}")
        report.append(f"- 开始时间: {workflow_state.get('started_at', 'N/A')}")
        report.append(f"- 状态: {workflow_state.get('status', 'N/A')}")
        
        if workflow_state.get('completed_at'):
            report.append(f"- 完成时间: {workflow_state['completed_at']}")
        
        report.append("")
        
        # 进度信息
        current_step = workflow_state.get('current_step', 0)
        completed_steps = workflow_state.get('completed_steps', [])
        
        report.append("## 进度信息")
        report.append(f"- 当前步骤: {current_step}")
        report.append(f"- 已完成步骤: {len(completed_steps)}")
        report.append("")
        
        # 已完成步骤详情
        if completed_steps:
            report.append("## 已完成步骤")
            for i, step in enumerate(completed_steps, 1):
                report.append(f"### 步骤 {i}")
                report.append(f"- 完成时间: {step.get('completed_at', 'N/A')}")
                
                if step.get('artifacts'):
                    report.append("- 创建的产物:")
                    for artifact in step['artifacts']:
                        report.append(f"  - {artifact}")
                
                report.append("")
        
        # 创建的产物
        artifacts = workflow_state.get('created_artifacts', [])
        if artifacts:
            report.append("## 创建的产物")
            for artifact in artifacts:
                report.append(f"- {artifact}")
            report.append("")
        
        # 任务执行历史
        task_executions = workflow_state.get('task_executions', [])
        if task_executions:
            report.append("## 任务执行历史")
            for i, execution in enumerate(task_executions, 1):
                report.append(f"### 任务 {i}: {execution.get('task_name', 'N/A')}")
                report.append(f"- 执行智能体: {execution.get('agent', 'N/A')}")
                report.append(f"- 执行时间: {execution.get('executed_at', 'N/A')}")
                
                if execution.get('context'):
                    report.append("- 上下文:")
                    for key, value in execution['context'].items():
                        report.append(f"  - {key}: {value}")
                
                report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def scan_bmad_core(bmad_path: Path) -> Dict[str, Any]:
        """扫描 .bmad-core 目录并生成报告 - 优化版本"""
        result = {
            "path": str(bmad_path),
            "exists": bmad_path.exists(),
            "agents": {"count": 0, "files": [], "valid": [], "invalid": []},
            "workflows": {"count": 0, "files": [], "valid": [], "invalid": []},
            "tasks": {"count": 0, "files": []},
            "templates": {"count": 0, "files": []},
            "other_files": []
        }
        
        if not bmad_path.exists():
            return result
        
        # 扫描智能体 - 优化：先收集所有文件，然后批量处理
        agents_dir = bmad_path / "agents"
        if agents_dir.exists():
            agent_files = list(agents_dir.glob("*.md"))
            result["agents"]["count"] = len(agent_files)
            result["agents"]["files"] = [f.name for f in agent_files]
            
            # Batch validation
            for agent_file in agent_files:
                validation = BMADUtils.validate_agent_file(agent_file)
                if validation["valid"]:
                    result["agents"]["valid"].append(agent_file.name)
                else:
                    result["agents"]["invalid"].append({
                        "file": agent_file.name,
                        "errors": validation["errors"]
                    })
        
        # 扫描工作流程 - 优化：先收集所有文件，然后批量处理
        workflows_dir = bmad_path / "workflows"
        if workflows_dir.exists():
            workflow_files = list(workflows_dir.glob("*.yaml"))
            result["workflows"]["count"] = len(workflow_files)
            result["workflows"]["files"] = [f.name for f in workflow_files]
            
            # Batch validation
            for workflow_file in workflow_files:
                validation = BMADUtils.validate_workflow_file(workflow_file)
                if validation["valid"]:
                    result["workflows"]["valid"].append(workflow_file.name)
                else:
                    result["workflows"]["invalid"].append({
                        "file": workflow_file.name,
                        "errors": validation["errors"]
                    })
        
        # 扫描任务 - 优化：只收集文件名，不读取内容
        tasks_dir = bmad_path / "tasks"
        if tasks_dir.exists():
            task_files = list(tasks_dir.glob("*.md"))
            result["tasks"]["count"] = len(task_files)
            result["tasks"]["files"] = [f.name for f in task_files]
        
        # 扫描模板 - 优化：只收集文件名，不读取内容
        templates_dir = bmad_path / "templates"
        if templates_dir.exists():
            template_files = list(templates_dir.glob("*.md"))
            result["templates"]["count"] = len(template_files)
            result["templates"]["files"] = [f.name for f in template_files]
        
        return result

def format_scan_report(scan_result: Dict[str, Any]) -> str:
    """格式化扫描报告"""
    report = []
    report.append("# BMAD Core 扫描报告")
    report.append("")
    report.append(f"扫描路径: {scan_result['path']}")
    report.append(f"目录存在: {'✅' if scan_result['exists'] else '❌'}")
    report.append("")
    
    if not scan_result['exists']:
        report.append("❌ .bmad-core 目录不存在")
        return "\n".join(report)
    
    # 智能体报告
    agents = scan_result['agents']
    report.append(f"## 🤖 智能体 ({agents['count']} 个)")
    report.append(f"- 有效: {len(agents['valid'])}")
    report.append(f"- 无效: {len(agents['invalid'])}")
    
    if agents['invalid']:
        report.append("\n### 无效的智能体文件:")
        for invalid in agents['invalid']:
            report.append(f"- {invalid['file']}")
            for error in invalid['errors']:
                report.append(f"  - ❌ {error}")
    
    report.append("")
    
    # 工作流程报告
    workflows = scan_result['workflows']
    report.append(f"## 🔄 工作流程 ({workflows['count']} 个)")
    report.append(f"- 有效: {len(workflows['valid'])}")
    report.append(f"- 无效: {len(workflows['invalid'])}")
    
    if workflows['invalid']:
        report.append("\n### 无效的工作流程文件:")
        for invalid in workflows['invalid']:
            report.append(f"- {invalid['file']}")
            for error in invalid['errors']:
                report.append(f"  - ❌ {error}")
    
    report.append("")
    
    # 任务和模板报告
    report.append(f"## 📋 任务 ({scan_result['tasks']['count']} 个)")
    report.append(f"## 📄 模板 ({scan_result['templates']['count']} 个)")
    
    return "\n".join(report)
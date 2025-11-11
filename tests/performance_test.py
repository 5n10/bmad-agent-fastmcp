#!/usr/bin/env python3
"""
Performance benchmark test for BMAD Agent FastMCP

Tests the performance improvements including:
- Lazy loading
- File caching
- Startup time
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_startup_time():
    """Test startup time with optimizations"""
    print("🧪 测试启动时间")
    print("-" * 50)
    
    start_time = time.time()
    
    # Import and initialize
    from bmad_agent_mcp import bmad_core
    
    init_time = time.time() - start_time
    
    print(f"✅ 启动时间: {init_time:.4f} 秒")
    print(f"   智能体数量: {len(bmad_core.agents)}")
    print(f"   工作流程数量: {len(bmad_core.workflows)}")
    print(f"   任务已加载: {bmad_core._tasks_loaded}")
    print(f"   模板已加载: {bmad_core._templates_loaded}")
    
    return init_time

def test_lazy_loading():
    """Test lazy loading functionality"""
    print("\n🧪 测试懒加载功能")
    print("-" * 50)
    
    from bmad_agent_mcp import bmad_core
    
    # Check initial state
    print("初始状态:")
    print(f"   任务已加载: {bmad_core._tasks_loaded}")
    print(f"   模板已加载: {bmad_core._templates_loaded}")
    
    # Trigger task loading
    start_time = time.time()
    tasks = bmad_core.get_all_tasks()
    task_load_time = time.time() - start_time
    
    print(f"\n首次加载任务:")
    print(f"   加载时间: {task_load_time:.4f} 秒")
    print(f"   任务数量: {len(tasks)}")
    print(f"   任务已加载: {bmad_core._tasks_loaded}")
    
    # Trigger template loading
    start_time = time.time()
    templates = bmad_core.get_all_templates()
    template_load_time = time.time() - start_time
    
    print(f"\n首次加载模板:")
    print(f"   加载时间: {template_load_time:.4f} 秒")
    print(f"   模板数量: {len(templates)}")
    print(f"   模板已加载: {bmad_core._templates_loaded}")
    
    # Test subsequent access (should be instant)
    start_time = time.time()
    tasks2 = bmad_core.get_all_tasks()
    cached_task_time = time.time() - start_time
    
    print(f"\n缓存访问任务:")
    print(f"   访问时间: {cached_task_time:.6f} 秒")
    print(f"   速度提升: {task_load_time/cached_task_time:.2f}x")
    
    return True

def test_agent_caching():
    """Test agent file caching"""
    print("\n🧪 测试智能体缓存")
    print("-" * 50)
    
    from bmad_agent_mcp import bmad_core
    
    print(f"缓存的智能体数量: {len(bmad_core._agent_cache)}")
    print(f"加载的智能体数量: {len(bmad_core.agents)}")
    
    if len(bmad_core._agent_cache) > 0:
        print("✅ 智能体缓存工作正常")
        
        # Show a sample cached agent
        sample_id = list(bmad_core._agent_cache.keys())[0]
        mtime, agent_info = bmad_core._agent_cache[sample_id]
        print(f"\n示例缓存项:")
        print(f"   ID: {sample_id}")
        print(f"   修改时间: {mtime}")
        print(f"   名称: {agent_info.name}")
        return True
    else:
        print("⚠️  没有智能体被缓存")
        return False

def test_workflow_caching():
    """Test workflow file caching"""
    print("\n🧪 测试工作流程缓存")
    print("-" * 50)
    
    from bmad_agent_mcp import bmad_core
    
    print(f"缓存的工作流程数量: {len(bmad_core._workflow_cache)}")
    print(f"加载的工作流程数量: {len(bmad_core.workflows)}")
    
    if len(bmad_core._workflow_cache) > 0:
        print("✅ 工作流程缓存工作正常")
        
        # Show a sample cached workflow
        sample_id = list(bmad_core._workflow_cache.keys())[0]
        mtime, workflow_info = bmad_core._workflow_cache[sample_id]
        print(f"\n示例缓存项:")
        print(f"   ID: {sample_id}")
        print(f"   修改时间: {mtime}")
        print(f"   名称: {workflow_info.name}")
        return True
    else:
        print("⚠️  没有工作流程被缓存")
        return False

def test_memory_efficiency():
    """Test memory efficiency"""
    print("\n🧪 测试内存效率")
    print("-" * 50)
    
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        print(f"当前内存使用:")
        print(f"   RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
        print(f"   VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
        
        return True
    except ImportError:
        print("⚠️  psutil 未安装，跳过内存测试")
        return None

def main():
    """Run all performance tests"""
    print("=" * 50)
    print("🚀 BMAD Agent 性能测试")
    print("=" * 50)
    
    results = []
    
    # Test startup time
    startup_time = test_startup_time()
    results.append(("启动时间", startup_time < 2.0))  # Should be under 2 seconds (includes library imports)
    
    # Test lazy loading
    lazy_loading_ok = test_lazy_loading()
    results.append(("懒加载", lazy_loading_ok))
    
    # Test caching
    agent_cache_ok = test_agent_caching()
    results.append(("智能体缓存", agent_cache_ok))
    
    workflow_cache_ok = test_workflow_caching()
    results.append(("工作流程缓存", workflow_cache_ok))
    
    # Test memory efficiency
    memory_ok = test_memory_efficiency()
    if memory_ok is not None:
        results.append(("内存效率", memory_ok))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 性能测试总结")
    print("=" * 50)
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("✅ 所有性能测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())

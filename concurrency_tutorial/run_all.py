"""
主运行脚本
提供交互式菜单来运行各个示例
"""

import sys
import subprocess
import time


def print_banner():
    """打印欢迎横幅"""
    print("\n" + "="*70)
    print(" "*15 + "🚀 Python并发编程学习教程 🚀")
    print("="*70)
    print("\n欢迎！本教程将帮助你理解进程、线程和协程。")
    print("\n学习目标:")
    print("  ✓ 理解为什么需要并发")
    print("  ✓ 掌握进程、线程、协程的区别")
    print("  ✓ 学会在实际场景中应用")
    print("  ✓ 了解常见陷阱和最佳实践")


def print_menu():
    """打印菜单"""
    print("\n" + "="*70)
    print("请选择要运行的示例:")
    print("="*70)
    print("\n基础教程:")
    print("  1. 进程 (Process) 基础示例")
    print("  2. 线程 (Thread) 基础示例")
    print("  3. 协程 (Coroutine) 基础示例")
    print("\n对比分析:")
    print("  4. 性能对比 - CPU密集 vs I/O密集")
    print("  5. 真实场景应用示例")
    print("\n进阶内容:")
    print("  6. 常见陷阱和最佳实践")
    print("\n其他选项:")
    print("  7. 运行所有示例（全部演示）")
    print("  8. 快速演示（精简版）")
    print("  0. 退出")
    print("="*70)


def run_script(script_name, description):
    """运行指定的Python脚本"""
    print("\n" + "="*70)
    print(f"▶️  正在运行: {description}")
    print("="*70)
    print(f"脚本: {script_name}")
    print("-"*70)
    
    try:
        # 运行脚本
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n" + "-"*70)
            print("✅ 运行完成")
        else:
            print("\n" + "-"*70)
            print("❌ 运行出错")
            
    except FileNotFoundError:
        print(f"\n❌ 错误: 找不到文件 {script_name}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print("="*70)


def run_quick_demo():
    """运行快速演示版本"""
    print("\n" + "="*70)
    print("🚀 快速演示模式")
    print("="*70)
    print("\n这是一个精简的演示，展示核心概念...")
    print("-"*70)
    
    # 简单的演示代码
    import threading
    import multiprocessing as mp
    import asyncio
    
    print("\n1️⃣  线程示例:")
    print("-"*70)
    
    def thread_worker(name):
        print(f"   线程 {name} 正在工作...")
        time.sleep(0.5)
        print(f"   线程 {name} 完成")
    
    threads = [threading.Thread(target=thread_worker, args=(f"T{i}",)) for i in range(3)]
    start = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"   耗时: {time.time()-start:.2f}秒")
    
    print("\n2️⃣  进程示例:")
    print("-"*70)
    
    def process_worker(name):
        print(f"   进程 {name} 正在工作...")
        time.sleep(0.5)
        print(f"   进程 {name} 完成")
    
    processes = [mp.Process(target=process_worker, args=(f"P{i}",)) for i in range(3)]
    start = time.time()
    for p in processes: p.start()
    for p in processes: p.join()
    print(f"   耗时: {time.time()-start:.2f}秒")
    
    print("\n3️⃣  协程示例:")
    print("-"*70)
    
    async def coroutine_worker(name):
        print(f"   协程 {name} 正在工作...")
        await asyncio.sleep(0.5)
        print(f"   协程 {name} 完成")
    
    async def run_coroutines():
        start = time.time()
        await asyncio.gather(*[coroutine_worker(f"C{i}") for i in range(3)])
        print(f"   耗时: {time.time()-start:.2f}秒")
    
    asyncio.run(run_coroutines())
    
    print("\n" + "="*70)
    print("💡 观察:")
    print("   - 所有方式都能实现并发")
    print("   - 线程和进程创建有开销")
    print("   - 协程最轻量，适合高并发")
    print("="*70)


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*70)
    print("🎯 运行所有示例")
    print("="*70)
    print("\n⚠️  这将运行所有示例，可能需要几分钟时间。")
    
    confirm = input("\n确定要继续吗? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消。")
        return
    
    examples = [
        ("01_process_basic.py", "进程基础"),
        ("02_thread_basic.py", "线程基础"),
        ("03_coroutine_basic.py", "协程基础"),
        ("04_comparison.py", "性能对比"),
        ("05_real_world_examples.py", "真实场景"),
        ("06_pitfalls_and_best_practices.py", "陷阱和最佳实践"),
    ]
    
    total = len(examples)
    for i, (script, desc) in enumerate(examples, 1):
        print(f"\n进度: [{i}/{total}]")
        run_script(script, desc)
        
        if i < total:
            print("\n⏳ 3秒后继续下一个示例...")
            time.sleep(3)
    
    print("\n" + "="*70)
    print("🎉 所有示例运行完成！")
    print("="*70)


def show_tips():
    """显示学习提示"""
    print("\n" + "="*70)
    print("💡 学习提示")
    print("="*70)
    print("""
建议的学习顺序:
  1. 先阅读 README.md 了解理论
  2. 按顺序运行示例 1 → 2 → 3
  3. 运行示例 4 看性能对比
  4. 运行示例 5 了解实际应用
  5. 最后学习示例 6 的最佳实践

遇到问题?
  - 查看 QUICKSTART.md
  - 检查是否安装了依赖: pip install -r requirements.txt
  - 确保 Python 版本 >= 3.7

动手实践:
  - 修改示例中的参数
  - 尝试编写自己的示例
  - 观察性能变化
    """)


def main():
    """主函数"""
    print_banner()
    show_tips()
    
    while True:
        print_menu()
        
        try:
            choice = input("\n请输入选项 (0-8): ").strip()
            
            if choice == '0':
                print("\n👋 感谢使用！祝学习愉快！")
                break
                
            elif choice == '1':
                run_script("01_process_basic.py", "进程基础示例")
                
            elif choice == '2':
                run_script("02_thread_basic.py", "线程基础示例")
                
            elif choice == '3':
                run_script("03_coroutine_basic.py", "协程基础示例")
                
            elif choice == '4':
                run_script("04_comparison.py", "性能对比")
                
            elif choice == '5':
                run_script("05_real_world_examples.py", "真实场景应用")
                
            elif choice == '6':
                run_script("06_pitfalls_and_best_practices.py", "陷阱和最佳实践")
                
            elif choice == '7':
                run_all_examples()
                
            elif choice == '8':
                run_quick_demo()
                
            else:
                print("\n❌ 无效的选项，请重新输入。")
                
            # 询问是否继续
            if choice in ['1', '2', '3', '4', '5', '6']:
                input("\n按回车键返回菜单...")
                
        except KeyboardInterrupt:
            print("\n\n👋 检测到中断，退出程序。")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    main()


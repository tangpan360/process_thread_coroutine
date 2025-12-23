"""
常见陷阱和最佳实践
展示并发编程中容易犯的错误以及如何避免
"""

import threading
import multiprocessing as mp
import time
import asyncio
from queue import Queue


print("="*60)
print("常见陷阱和最佳实践")
print("="*60)


# ===== 陷阱1: 竞态条件 (Race Condition) =====
print("\n" + "="*60)
print("陷阱1: 竞态条件")
print("="*60)

counter = 0

def increment_unsafe():
    """不安全的递增（有竞态条件）"""
    global counter
    for _ in range(100000):
        counter += 1

print("\n❌ 错误示例：不使用锁")
counter = 0
threads = [threading.Thread(target=increment_unsafe) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(f"预期: 200000, 实际: {counter}")

# 正确的做法
counter = 0
counter_lock = threading.Lock()

def increment_safe():
    """安全的递增（使用锁）"""
    global counter
    for _ in range(100000):
        with counter_lock:
            counter += 1

print("\n✅ 正确示例：使用锁")
counter = 0
threads = [threading.Thread(target=increment_safe) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(f"预期: 200000, 实际: {counter}")

print("\n💡 最佳实践:")
print("   - 访问共享变量时必须加锁")
print("   - 使用 with 语句自动管理锁")
print("   - 尽量减小锁的范围")


# ===== 陷阱2: 死锁 (Deadlock) =====
print("\n" + "="*60)
print("陷阱2: 死锁")
print("="*60)

lock1 = threading.Lock()
lock2 = threading.Lock()

def task_a_bad():
    """容易造成死锁"""
    with lock1:
        print("  任务A获得锁1")
        time.sleep(0.1)
        with lock2:
            print("  任务A获得锁2")

def task_b_bad():
    """容易造成死锁"""
    with lock2:
        print("  任务B获得锁2")
        time.sleep(0.1)
        with lock1:
            print("  任务B获得锁1")

print("\n❌ 错误示例：可能死锁")
print("（为了演示，我们不实际运行，否则程序会卡住）")
print("task_a_bad: 获取 lock1 → 等待 lock2")
print("task_b_bad: 获取 lock2 → 等待 lock1")
print("结果: 两个任务互相等待，死锁！")

# 正确的做法：统一锁的顺序
def task_a_good():
    """按顺序获取锁"""
    with lock1:
        with lock2:
            print("  任务A完成")

def task_b_good():
    """按顺序获取锁"""
    with lock1:
        with lock2:
            print("  任务B完成")

print("\n✅ 正确示例：统一锁的顺序")
t1 = threading.Thread(target=task_a_good)
t2 = threading.Thread(target=task_b_good)
t1.start(); t2.start()
t1.join(); t2.join()

print("\n💡 最佳实践:")
print("   - 所有线程按相同顺序获取锁")
print("   - 避免嵌套锁")
print("   - 使用超时机制")
print("   - 考虑使用 threading.RLock (可重入锁)")


# ===== 陷阱3: GIL的误解 =====
print("\n" + "="*60)
print("陷阱3: 对Python GIL的误解")
print("="*60)

def cpu_task():
    """CPU密集型任务"""
    total = 0
    for i in range(5000000):
        total += i
    return total

print("\n❌ 错误认知：多线程总能提升性能")
print("测试CPU密集型任务...")

# 单线程
start = time.time()
result = cpu_task()
serial_time = time.time() - start
print(f"单线程: {serial_time:.2f} 秒")

# 多线程（受GIL限制）
from concurrent.futures import ThreadPoolExecutor
start = time.time()
with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(lambda x: cpu_task(), range(2)))
thread_time = time.time() - start
print(f"多线程: {thread_time:.2f} 秒")

print(f"\n加速比: {serial_time/thread_time:.2f}x (应该接近1，甚至更慢！)")

print("\n✅ 正确认知:")
print("   - Python的GIL导致同一时间只有一个线程执行Python代码")
print("   - 多线程适合I/O密集型，不适合CPU密集型")
print("   - CPU密集型应该使用多进程")

print("\n💡 最佳实践:")
print("   - CPU密集型 → multiprocessing")
print("   - I/O密集型 → threading 或 asyncio")
print("   - 使用 Cython 或 NumPy 等可以释放GIL")


# ===== 陷阱4: 忘记join() =====
print("\n" + "="*60)
print("陷阱4: 忘记等待线程/进程")
print("="*60)

print("\n❌ 错误示例：忘记join()")
print("（为了演示，我们展示但不实际运行）")
print("""
def worker():
    time.sleep(1)
    print("工作完成")

t = threading.Thread(target=worker)
t.start()
# 忘记 t.join()
print("主程序结束")
# 主程序可能在worker完成前就退出了！
""")

print("\n✅ 正确示例：使用join()")
def worker():
    time.sleep(0.5)
    print("  工作完成")

t = threading.Thread(target=worker)
t.start()
t.join()  # 等待线程完成
print("主程序结束")

print("\n💡 最佳实践:")
print("   - 总是join()你创建的线程/进程")
print("   - 或者使用上下文管理器（with）")
print("   - 或者使用 daemon 线程（但要谨慎）")


# ===== 陷阱5: 协程中使用阻塞调用 =====
print("\n" + "="*60)
print("陷阱5: 协程中使用阻塞调用")
print("="*60)

async def bad_coroutine():
    """错误：在协程中使用阻塞调用"""
    print("  开始任务")
    time.sleep(1)  # ❌ 阻塞调用！会阻塞整个事件循环
    print("  任务完成")

async def good_coroutine():
    """正确：使用异步调用"""
    print("  开始任务")
    await asyncio.sleep(1)  # ✅ 异步调用
    print("  任务完成")

print("\n❌ 错误示例：阻塞调用")
async def demo_bad():
    start = time.time()
    await asyncio.gather(bad_coroutine(), bad_coroutine())
    print(f"  耗时: {time.time() - start:.2f} 秒 (应该是2秒，串行执行！)")

asyncio.run(demo_bad())

print("\n✅ 正确示例：异步调用")
async def demo_good():
    start = time.time()
    await asyncio.gather(good_coroutine(), good_coroutine())
    print(f"  耗时: {time.time() - start:.2f} 秒 (应该是1秒，并发执行！)")

asyncio.run(demo_good())

print("\n💡 最佳实践:")
print("   - 在 async 函数中使用 await 而不是阻塞调用")
print("   - 使用 asyncio 兼容的库（aiohttp、aiofiles等）")
print("   - 如果必须调用阻塞函数，使用 run_in_executor")


# ===== 陷阱6: 共享状态的问题 =====
print("\n" + "="*60)
print("陷阱6: 多进程共享状态")
print("="*60)

# 错误的做法
global_list = []

def worker_bad(value):
    """尝试修改全局列表（不会生效）"""
    global_list.append(value)

print("\n❌ 错误示例：尝试共享普通变量")
processes = [mp.Process(target=worker_bad, args=(i,)) for i in range(3)]
for p in processes: p.start()
for p in processes: p.join()
print(f"全局列表: {global_list}")
print("（列表是空的！每个进程有自己的副本）")

# 正确的做法
def worker_good(shared_list, value):
    """使用共享数据结构"""
    shared_list.append(value)

print("\n✅ 正确示例：使用Manager")
manager = mp.Manager()
shared_list = manager.list()
processes = [mp.Process(target=worker_good, args=(shared_list, i)) for i in range(3)]
for p in processes: p.start()
for p in processes: p.join()
print(f"共享列表: {list(shared_list)}")

print("\n💡 最佳实践:")
print("   - 进程间不能直接共享普通变量")
print("   - 使用 multiprocessing.Manager")
print("   - 使用 multiprocessing.Value 或 Array")
print("   - 或者通过 Queue/Pipe 传递数据")


# ===== 陷阱7: 异常处理 =====
print("\n" + "="*60)
print("陷阱7: 子线程/进程中的异常")
print("="*60)

def worker_with_error():
    """会抛出异常的worker"""
    time.sleep(0.1)
    raise ValueError("出错了！")

print("\n❌ 错误示例：异常被吞掉")
t = threading.Thread(target=worker_with_error)
t.start()
t.join()
print("主线程继续执行，但看不到异常")

print("\n✅ 正确示例：使用线程池捕获异常")
from concurrent.futures import ThreadPoolExecutor

def worker_with_error_2():
    raise ValueError("出错了！")

with ThreadPoolExecutor() as executor:
    future = executor.submit(worker_with_error_2)
    try:
        result = future.result()
    except ValueError as e:
        print(f"捕获到异常: {e}")

print("\n💡 最佳实践:")
print("   - 使用 concurrent.futures 的 Future 对象")
print("   - 在 worker 内部捕获并记录异常")
print("   - 使用队列传递异常信息")


# ===== 陷阱8: 资源泄漏 =====
print("\n" + "="*60)
print("陷阱8: 忘记释放资源")
print("="*60)

print("\n❌ 错误示例：忘记关闭线程池")
print("""
executor = ThreadPoolExecutor(max_workers=5)
executor.submit(task)
# 忘记关闭！线程一直存在
""")

print("\n✅ 正确示例：使用上下文管理器")
print("""
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(task)
# 自动关闭和清理
""")

print("\n💡 最佳实践:")
print("   - 使用 with 语句管理资源")
print("   - 确保调用 executor.shutdown()")
print("   - 使用 try-finally 确保清理")


# ===== 最佳实践总结 =====
print("\n" + "="*60)
print("最佳实践总结")
print("="*60)

print("""
1. 线程安全
   ✓ 访问共享变量必须加锁
   ✓ 使用 threading.Lock 或 threading.RLock
   ✓ 用 with 语句管理锁

2. 避免死锁
   ✓ 统一锁的获取顺序
   ✓ 避免嵌套锁
   ✓ 使用超时机制

3. 选择合适的并发模型
   ✓ CPU密集 → 多进程
   ✓ I/O密集 → 多线程或协程
   ✓ 高并发 → 协程

4. 异常处理
   ✓ 使用 concurrent.futures 捕获异常
   ✓ 在 worker 中捕获并记录
   ✓ 不要忽略子任务的错误

5. 资源管理
   ✓ 使用上下文管理器（with）
   ✓ 确保 join() 所有线程/进程
   ✓ 正确关闭线程池/进程池

6. 进程间通信
   ✓ 使用 Queue、Pipe 或 Manager
   ✓ 不要尝试共享普通变量
   ✓ 考虑序列化开销

7. 协程注意事项
   ✓ 使用 await 而不是阻塞调用
   ✓ 使用异步库（aiohttp等）
   ✓ 正确处理异步上下文管理器

8. 性能考虑
   ✓ 不要创建过多线程/进程
   ✓ 使用线程池/进程池
   ✓ 测量和优化瓶颈

9. 调试技巧
   ✓ 使用日志而非 print
   ✓ 记录进程/线程ID
   ✓ 使用专门的调试工具

10. 测试
    ✓ 编写并发安全的测试
    ✓ 测试边界情况
    ✓ 使用 threading.Barrier 同步测试
""")

print("\n" + "="*60)
print("记住：并发编程是困难的，但掌握这些原则会让你少走弯路！")
print("="*60)


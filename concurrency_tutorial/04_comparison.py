"""
性能对比示例
对比进程、线程、协程在不同场景下的性能表现
"""

import time
import multiprocessing as mp
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ===== 场景1: CPU密集型任务 =====
def cpu_bound_task(n):
    """CPU密集型任务：计算质数"""
    count = 0
    for i in range(2, n):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


def test_cpu_bound_serial():
    """串行执行"""
    print("\n[串行] 单线程执行:")
    start = time.time()
    
    results = []
    for _ in range(4):
        results.append(cpu_bound_task(10000))
    
    duration = time.time() - start
    print(f"  结果: {results}")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def test_cpu_bound_process():
    """多进程执行"""
    print("\n[多进程] 利用多核:")
    start = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, [10000] * 4))
    
    duration = time.time() - start
    print(f"  结果: {results}")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def test_cpu_bound_thread():
    """多线程执行（受GIL限制）"""
    print("\n[多线程] 受GIL限制:")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, [10000] * 4))
    
    duration = time.time() - start
    print(f"  结果: {results}")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


async def cpu_bound_task_async(n):
    """协程版本（仍然是阻塞的）"""
    return cpu_bound_task(n)


async def test_cpu_bound_coroutine():
    """协程执行（不适合CPU密集型）"""
    print("\n[协程] 无法并行:")
    start = time.time()
    
    tasks = [cpu_bound_task_async(10000) for _ in range(4)]
    results = await asyncio.gather(*tasks)
    
    duration = time.time() - start
    print(f"  结果: {results}")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def compare_cpu_bound():
    """对比CPU密集型任务"""
    print("="*60)
    print("场景1: CPU密集型任务（计算质数）")
    print("="*60)
    print("任务: 4个独立的计算任务，每个计算10000以内的质数")
    
    # 串行
    serial_time = test_cpu_bound_serial()
    
    # 多进程
    process_time = test_cpu_bound_process()
    
    # 多线程
    thread_time = test_cpu_bound_thread()
    
    # 协程
    coroutine_time = asyncio.run(test_cpu_bound_coroutine())
    
    # 总结
    print("\n" + "="*60)
    print("CPU密集型任务总结:")
    print("="*60)
    print(f"串行:     {serial_time:.2f} 秒 (基准)")
    print(f"多进程:   {process_time:.2f} 秒 (加速 {serial_time/process_time:.2f}x) ✅ 最优")
    print(f"多线程:   {thread_time:.2f} 秒 (加速 {serial_time/thread_time:.2f}x) ❌ GIL限制")
    print(f"协程:     {coroutine_time:.2f} 秒 (加速 {serial_time/coroutine_time:.2f}x) ❌ 无并行")
    print("\n结论: CPU密集型任务应该使用多进程！")


# ===== 场景2: I/O密集型任务 =====
def io_bound_task(task_id):
    """I/O密集型任务：模拟网络请求"""
    time.sleep(1)  # 模拟I/O等待
    return f"Task-{task_id}"


def test_io_bound_serial():
    """串行执行"""
    print("\n[串行] 依次执行:")
    start = time.time()
    
    results = []
    for i in range(10):
        results.append(io_bound_task(i))
    
    duration = time.time() - start
    print(f"  完成: {len(results)} 个任务")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def test_io_bound_process():
    """多进程执行"""
    print("\n[多进程] 并行执行:")
    start = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_bound_task, range(10)))
    
    duration = time.time() - start
    print(f"  完成: {len(results)} 个任务")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def test_io_bound_thread():
    """多线程执行"""
    print("\n[多线程] 并发执行:")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(io_bound_task, range(10)))
    
    duration = time.time() - start
    print(f"  完成: {len(results)} 个任务")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


async def io_bound_task_async(task_id):
    """异步I/O任务"""
    await asyncio.sleep(1)  # 异步睡眠
    return f"Task-{task_id}"


async def test_io_bound_coroutine():
    """协程执行"""
    print("\n[协程] 异步执行:")
    start = time.time()
    
    tasks = [io_bound_task_async(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    duration = time.time() - start
    print(f"  完成: {len(results)} 个任务")
    print(f"  耗时: {duration:.2f} 秒")
    return duration


def compare_io_bound():
    """对比I/O密集型任务"""
    print("\n" + "="*60)
    print("场景2: I/O密集型任务（模拟网络请求）")
    print("="*60)
    print("任务: 10个网络请求，每个耗时1秒")
    
    # 串行
    serial_time = test_io_bound_serial()
    
    # 多进程
    process_time = test_io_bound_process()
    
    # 多线程
    thread_time = test_io_bound_thread()
    
    # 协程
    coroutine_time = asyncio.run(test_io_bound_coroutine())
    
    # 总结
    print("\n" + "="*60)
    print("I/O密集型任务总结:")
    print("="*60)
    print(f"串行:     {serial_time:.2f} 秒 (基准)")
    print(f"多进程:   {process_time:.2f} 秒 (加速 {serial_time/process_time:.2f}x) ⚠️  开销大")
    print(f"多线程:   {thread_time:.2f} 秒 (加速 {serial_time/thread_time:.2f}x) ✅ 很好")
    print(f"协程:     {coroutine_time:.2f} 秒 (加速 {serial_time/coroutine_time:.2f}x) ✅ 最优")
    print("\n结论: I/O密集型任务，协程和多线程都很好，协程更轻量！")


# ===== 场景3: 高并发场景 =====
def compare_high_concurrency():
    """对比高并发场景"""
    print("\n" + "="*60)
    print("场景3: 高并发场景（1000个轻量任务）")
    print("="*60)
    
    # 多线程（可能遇到资源限制）
    print("\n[多线程] 1000个线程:")
    try:
        start = time.time()
        with ThreadPoolExecutor(max_workers=1000) as executor:
            results = list(executor.map(lambda x: time.sleep(0.1), range(1000)))
        thread_time = time.time() - start
        print(f"  耗时: {thread_time:.2f} 秒")
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        thread_time = float('inf')
    
    # 协程（轻松处理）
    async def light_task(i):
        await asyncio.sleep(0.1)
    
    async def run_coroutines():
        start = time.time()
        await asyncio.gather(*[light_task(i) for i in range(1000)])
        return time.time() - start
    
    print("\n[协程] 1000个协程:")
    coroutine_time = asyncio.run(run_coroutines())
    print(f"  耗时: {coroutine_time:.2f} 秒")
    
    # 总结
    print("\n" + "="*60)
    print("高并发场景总结:")
    print("="*60)
    if thread_time != float('inf'):
        print(f"多线程:   {thread_time:.2f} 秒")
    else:
        print(f"多线程:   失败（资源限制）")
    print(f"协程:     {coroutine_time:.2f} 秒 ✅ 最优")
    print("\n结论: 超高并发场景，协程是唯一选择！")


# ===== 场景4: 资源占用对比 =====
def compare_resource_usage():
    """对比资源占用"""
    print("\n" + "="*60)
    print("场景4: 资源占用对比")
    print("="*60)
    
    print("\n理论对比:")
    print("┌─────────┬────────────┬────────────┬──────────┐")
    print("│  类型   │  创建时间  │  内存占用  │ 数量上限 │")
    print("├─────────┼────────────┼────────────┼──────────┤")
    print("│  进程   │   ~100ms   │   ~10MB    │  ~100    │")
    print("│  线程   │    ~1ms    │   ~1MB     │ ~1000    │")
    print("│  协程   │   <0.1ms   │   ~1KB     │ ~100000  │")
    print("└─────────┴────────────┴────────────┴──────────┘")
    
    # 实际测试创建时间
    print("\n实际测试 - 创建100个:")
    
    # 进程
    start = time.time()
    processes = [mp.Process(target=lambda: None) for _ in range(100)]
    process_create_time = time.time() - start
    print(f"创建100个进程: {process_create_time:.3f} 秒")
    
    # 线程
    start = time.time()
    threads = [threading.Thread(target=lambda: None) for _ in range(100)]
    thread_create_time = time.time() - start
    print(f"创建100个线程: {thread_create_time:.3f} 秒")
    
    # 协程
    async def create_coroutines():
        start = time.time()
        async def dummy(): pass
        coroutines = [dummy() for _ in range(100)]
        await asyncio.gather(*coroutines)
        return time.time() - start
    
    coroutine_create_time = asyncio.run(create_coroutines())
    print(f"创建100个协程: {coroutine_create_time:.3f} 秒")
    
    print(f"\n协程比线程快: {thread_create_time / coroutine_create_time:.1f}x")
    print(f"协程比进程快: {process_create_time / coroutine_create_time:.1f}x")


# ===== 主函数 =====
def main():
    print("="*60)
    print("进程 vs 线程 vs 协程 - 性能对比")
    print("="*60)
    
    # 场景1: CPU密集型
    compare_cpu_bound()
    
    # 场景2: I/O密集型
    compare_io_bound()
    
    # 场景3: 高并发
    compare_high_concurrency()
    
    # 场景4: 资源占用
    compare_resource_usage()
    
    # 最终建议
    print("\n" + "="*60)
    print("最终建议")
    print("="*60)
    print("""
    ┌─────────────────┬───────────────────────────────┐
    │   任务类型      │          最佳选择             │
    ├─────────────────┼───────────────────────────────┤
    │ CPU密集型       │ 多进程 (充分利用多核)         │
    │ I/O密集型       │ 协程 > 多线程                 │
    │ 高并发I/O       │ 协程 (唯一选择)               │
    │ 需要隔离        │ 多进程 (独立内存空间)         │
    │ 简单后台任务    │ 多线程 (简单易用)             │
    └─────────────────┴───────────────────────────────┘
    
    记住:
    1. 进程 = 重量级，隔离性强，能并行，适合CPU密集
    2. 线程 = 中量级，共享内存，适合I/O密集
    3. 协程 = 轻量级，高并发，适合异步I/O
    """)


if __name__ == "__main__":
    mp.freeze_support()
    main()


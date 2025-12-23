"""
协程基础示例
演示：async/await、异步I/O、并发执行、异步生成器
"""

import asyncio
import time
import aiohttp
import aiofiles


# ===== 示例1: 基本的协程 =====
async def say_hello(name, delay):
    """异步函数：打印问候语"""
    print(f"[协程 {name}] 开始")
    await asyncio.sleep(delay)  # 异步睡眠，不阻塞其他协程
    print(f"[协程 {name}] Hello after {delay} seconds!")
    return f"{name} 完成"


async def example_basic_coroutine():
    """示例1: 基本协程"""
    print("\n" + "="*60)
    print("示例1: 基本协程创建和执行")
    print("="*60)
    
    # 方式1: 依次等待（串行）
    print("\n[方式1] 串行执行:")
    start = time.time()
    result1 = await say_hello("协程A", 1)
    result2 = await say_hello("协程B", 1)
    result3 = await say_hello("协程C", 1)
    print(f"耗时: {time.time() - start:.2f} 秒")
    
    # 方式2: 并发执行（推荐）
    print("\n[方式2] 并发执行:")
    start = time.time()
    results = await asyncio.gather(
        say_hello("协程X", 1),
        say_hello("协程Y", 1),
        say_hello("协程Z", 1)
    )
    print(f"结果: {results}")
    print(f"耗时: {time.time() - start:.2f} 秒")


# ===== 示例2: 异步HTTP请求 =====
async def fetch_url(session, url):
    """异步获取URL内容"""
    print(f"  开始请求: {url}")
    try:
        async with session.get(url, timeout=5) as response:
            data = await response.text()
            print(f"  完成请求: {url} (状态码: {response.status}, 大小: {len(data)} 字节)")
            return {
                'url': url,
                'status': response.status,
                'size': len(data)
            }
    except Exception as e:
        print(f"  请求失败: {url} - {e}")
        return {'url': url, 'error': str(e)}


async def example_async_http():
    """示例2: 异步HTTP请求"""
    print("\n" + "="*60)
    print("示例2: 异步HTTP请求")
    print("="*60)
    
    urls = [
        'http://httpbin.org/delay/1',
        'http://httpbin.org/delay/2',
        'http://httpbin.org/delay/1',
        'http://httpbin.org/uuid',
        'http://httpbin.org/user-agent',
    ]
    
    print(f"\n需要请求 {len(urls)} 个URL\n")
    
    start = time.time()
    
    # 创建一个HTTP会话
    async with aiohttp.ClientSession() as session:
        # 并发执行所有请求
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    end = time.time()
    
    print(f"\n所有请求完成!")
    print(f"总耗时: {end - start:.2f} 秒")
    print(f"如果串行执行大约需要: 6+ 秒")


# ===== 示例3: 异步文件I/O =====
async def write_file_async(filename, content):
    """异步写入文件"""
    print(f"  开始写入: {filename}")
    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
        await f.write(content)
    print(f"  完成写入: {filename}")


async def read_file_async(filename):
    """异步读取文件"""
    print(f"  开始读取: {filename}")
    async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
        content = await f.read()
    print(f"  完成读取: {filename} (大小: {len(content)} 字节)")
    return content


async def example_async_file():
    """示例3: 异步文件I/O"""
    print("\n" + "="*60)
    print("示例3: 异步文件I/O")
    print("="*60)
    
    # 创建多个文件
    files = [
        ('test_file_1.txt', '这是文件1的内容\n' * 100),
        ('test_file_2.txt', '这是文件2的内容\n' * 100),
        ('test_file_3.txt', '这是文件3的内容\n' * 100),
    ]
    
    print("\n[写入文件]")
    start = time.time()
    
    write_tasks = [write_file_async(name, content) for name, content in files]
    await asyncio.gather(*write_tasks)
    
    print(f"写入耗时: {time.time() - start:.2f} 秒")
    
    print("\n[读取文件]")
    start = time.time()
    
    read_tasks = [read_file_async(name) for name, _ in files]
    contents = await asyncio.gather(*read_tasks)
    
    print(f"读取耗时: {time.time() - start:.2f} 秒")
    
    # 清理文件
    import os
    for name, _ in files:
        try:
            os.remove(name)
        except:
            pass


# ===== 示例4: 异步生成器 =====
async def async_range(start, end, delay):
    """异步生成器"""
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i


async def example_async_generator():
    """示例4: 异步生成器"""
    print("\n" + "="*60)
    print("示例4: 异步生成器")
    print("="*60)
    
    print("\n逐个生成数字（每个延迟0.5秒）:")
    async for num in async_range(1, 6, 0.5):
        print(f"  生成: {num}")


# ===== 示例5: 协程超时控制 =====
async def long_running_task(task_id, duration):
    """一个长时间运行的任务"""
    print(f"  [任务 {task_id}] 开始，预计耗时 {duration} 秒")
    await asyncio.sleep(duration)
    print(f"  [任务 {task_id}] 完成")
    return f"任务 {task_id} 的结果"


async def example_timeout():
    """示例5: 超时控制"""
    print("\n" + "="*60)
    print("示例5: 协程超时控制")
    print("="*60)
    
    # 任务1: 正常完成
    print("\n[测试1] 任务在超时前完成:")
    try:
        result = await asyncio.wait_for(long_running_task(1, 2), timeout=3)
        print(f"  ✅ 成功: {result}")
    except asyncio.TimeoutError:
        print(f"  ❌ 超时")
    
    # 任务2: 超时
    print("\n[测试2] 任务超时:")
    try:
        result = await asyncio.wait_for(long_running_task(2, 5), timeout=2)
        print(f"  ✅ 成功: {result}")
    except asyncio.TimeoutError:
        print(f"  ❌ 超时！任务被取消")


# ===== 示例6: 任务取消 =====
async def cancellable_task(name):
    """可取消的任务"""
    try:
        print(f"  [{name}] 开始执行")
        for i in range(10):
            print(f"  [{name}] 步骤 {i+1}/10")
            await asyncio.sleep(0.5)
        print(f"  [{name}] 完成")
        return f"{name} 的结果"
    except asyncio.CancelledError:
        print(f"  [{name}] 被取消")
        raise  # 重新抛出，让调用者知道任务被取消了


async def example_task_cancellation():
    """示例6: 任务取消"""
    print("\n" + "="*60)
    print("示例6: 任务取消")
    print("="*60)
    
    # 创建任务
    task = asyncio.create_task(cancellable_task("任务A"))
    
    # 让任务运行一会儿
    await asyncio.sleep(2)
    
    # 取消任务
    print("\n主程序: 取消任务")
    task.cancel()
    
    # 等待任务完成（会抛出CancelledError）
    try:
        result = await task
        print(f"结果: {result}")
    except asyncio.CancelledError:
        print("主程序: 任务已被取消")


# ===== 示例7: 异步上下文管理器 =====
class AsyncResource:
    """异步资源"""
    
    async def __aenter__(self):
        print("  🔓 获取资源")
        await asyncio.sleep(0.5)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("  🔒 释放资源")
        await asyncio.sleep(0.5)
    
    async def use(self):
        print("  ⚙️  使用资源")
        await asyncio.sleep(1)


async def example_async_context_manager():
    """示例7: 异步上下文管理器"""
    print("\n" + "="*60)
    print("示例7: 异步上下文管理器")
    print("="*60)
    
    async with AsyncResource() as resource:
        await resource.use()
    
    print("资源已正确释放")


# ===== 示例8: 事件循环控制 =====
async def background_task():
    """后台任务"""
    for i in range(5):
        print(f"  后台任务运行中... ({i+1}/5)")
        await asyncio.sleep(1)


async def example_event_loop():
    """示例8: 事件循环"""
    print("\n" + "="*60)
    print("示例8: 事件循环和后台任务")
    print("="*60)
    
    # 创建后台任务
    task = asyncio.create_task(background_task())
    
    # 主任务
    print("主任务: 执行其他工作")
    await asyncio.sleep(2.5)
    print("主任务: 完成")
    
    # 等待后台任务
    await task
    print("所有任务完成")


# ===== 示例9: 多个协程的不同等待方式 =====
async def task_with_result(task_id, duration):
    """带结果的任务"""
    await asyncio.sleep(duration)
    return f"任务{task_id}完成"


async def example_waiting_strategies():
    """示例9: 不同的等待策略"""
    print("\n" + "="*60)
    print("示例9: 不同的等待策略")
    print("="*60)
    
    # 策略1: gather - 等待所有任务完成
    print("\n[策略1] gather - 等待所有:")
    start = time.time()
    results = await asyncio.gather(
        task_with_result(1, 1),
        task_with_result(2, 2),
        task_with_result(3, 1.5)
    )
    print(f"  结果: {results}")
    print(f"  耗时: {time.time() - start:.2f} 秒")
    
    # 策略2: wait with FIRST_COMPLETED - 等待第一个完成
    print("\n[策略2] wait FIRST_COMPLETED - 等待第一个:")
    start = time.time()
    tasks = [
        asyncio.create_task(task_with_result(4, 2)),
        asyncio.create_task(task_with_result(5, 1)),
        asyncio.create_task(task_with_result(6, 3))
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    for task in done:
        print(f"  完成: {task.result()}")
    print(f"  还有 {len(pending)} 个任务在运行")
    print(f"  耗时: {time.time() - start:.2f} 秒")
    
    # 取消剩余任务
    for task in pending:
        task.cancel()


# ===== 主函数 =====
async def main():
    print("="*60)
    print("协程 (Coroutine) 学习示例")
    print("="*60)
    print("\n关键概念:")
    print("1. 协程是用户态的轻量级线程")
    print("2. 通过 async/await 语法实现")
    print("3. 协程在事件循环中调度")
    print("4. 遇到 await 时主动让出CPU")
    print("5. 适合高并发I/O密集型任务")
    print("6. 单线程执行，无需考虑线程安全")
    
    # 运行所有示例
    await example_basic_coroutine()
    
    # HTTP示例需要网络，可能失败
    try:
        await example_async_http()
    except Exception as e:
        print(f"\n⚠️  HTTP示例跳过（需要网络连接）: {e}")
    
    await example_async_file()
    await example_async_generator()
    await example_timeout()
    await example_task_cancellation()
    await example_async_context_manager()
    await example_event_loop()
    await example_waiting_strategies()
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)
    print("\n✨ 协程的优势:")
    print("   - 极高的并发能力（可以轻松处理数万个并发）")
    print("   - 极低的内存占用")
    print("   - 代码简洁（用同步的方式写异步代码）")
    print("\n⚠️  协程的限制:")
    print("   - 不能利用多核（单线程）")
    print("   - 需要库支持（asyncio生态）")
    print("   - 不适合CPU密集型任务")


if __name__ == "__main__":
    # 运行主协程
    asyncio.run(main())


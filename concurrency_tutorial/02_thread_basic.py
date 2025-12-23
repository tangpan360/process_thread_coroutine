"""
线程基础示例
演示：线程创建、线程同步、线程池、线程安全
"""

import threading
import time
import queue


# ===== 示例1: 基本的线程创建 =====
def worker_function(name, sleep_time):
    """工作函数：模拟一个耗时任务"""
    thread_id = threading.get_ident()
    print(f"[线程 {name}] 开始执行 (Thread ID: {thread_id})")
    time.sleep(sleep_time)
    print(f"[线程 {name}] 执行完成")


def example_basic_thread():
    """示例1: 创建和使用线程"""
    print("\n" + "="*60)
    print("示例1: 基本线程创建")
    print("="*60)
    
    print(f"主线程 ID: {threading.get_ident()}")
    
    # 创建多个线程
    threads = []
    for i in range(3):
        t = threading.Thread(
            target=worker_function,
            args=(f"Worker-{i}", 1)
        )
        threads.append(t)
        t.start()  # 启动线程
        print(f"启动了线程 {t.name}")
    
    # 等待所有线程完成
    for t in threads:
        t.join()  # 阻塞，直到线程结束
    
    print("所有线程执行完毕")


# ===== 示例2: 线程同步 - Lock =====
# 全局计数器（共享资源）
counter = 0
counter_lock = threading.Lock()


def increment_counter_unsafe(name, count):
    """不安全的计数器增加（会有竞态条件）"""
    global counter
    for i in range(count):
        temp = counter
        time.sleep(0.0001)  # 模拟一些处理时间
        counter = temp + 1


def increment_counter_safe(name, count):
    """安全的计数器增加（使用锁）"""
    global counter
    for i in range(count):
        with counter_lock:  # 自动加锁和解锁
            temp = counter
            time.sleep(0.0001)
            counter = temp + 1


def example_thread_lock():
    """示例2: 线程同步 - Lock"""
    print("\n" + "="*60)
    print("示例2: 线程同步 - Lock")
    print("="*60)
    
    # 不安全的版本
    print("\n[测试1] 不使用锁（不安全）:")
    global counter
    counter = 0
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=increment_counter_unsafe, args=(f"Thread-{i}", 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"  预期结果: 500")
    print(f"  实际结果: {counter}")
    print(f"  {'❌ 错误！有数据竞争' if counter != 500 else '✅ 正确'}")
    
    # 安全的版本
    print("\n[测试2] 使用锁（安全）:")
    counter = 0
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=increment_counter_safe, args=(f"Thread-{i}", 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"  预期结果: 500")
    print(f"  实际结果: {counter}")
    print(f"  {'✅ 正确！锁保证了线程安全' if counter == 500 else '❌ 错误'}")


# ===== 示例3: 生产者-消费者模式 =====
def producer_thread(q, items):
    """生产者线程"""
    thread_id = threading.get_ident()
    print(f"[生产者 Thread: {thread_id}] 开始生产")
    for item in items:
        print(f"  生产: {item}")
        q.put(item)
        time.sleep(0.3)
    print("[生产者] 完成")


def consumer_thread(q, name):
    """消费者线程"""
    thread_id = threading.get_ident()
    print(f"[消费者-{name} Thread: {thread_id}] 开始消费")
    while True:
        try:
            # 设置超时，避免无限等待
            item = q.get(timeout=2)
            print(f"  消费者-{name} 消费: {item}")
            time.sleep(0.5)
            q.task_done()
        except queue.Empty:
            break
    print(f"[消费者-{name}] 完成")


def example_producer_consumer():
    """示例3: 生产者-消费者模式"""
    print("\n" + "="*60)
    print("示例3: 生产者-消费者模式")
    print("="*60)
    
    # 创建队列
    q = queue.Queue()
    
    items = ['任务1', '任务2', '任务3', '任务4', '任务5']
    
    # 创建生产者线程
    producer = threading.Thread(target=producer_thread, args=(q, items))
    
    # 创建消费者线程
    consumer1 = threading.Thread(target=consumer_thread, args=(q, "A"))
    consumer2 = threading.Thread(target=consumer_thread, args=(q, "B"))
    
    # 启动所有线程
    producer.start()
    consumer1.start()
    consumer2.start()
    
    # 等待完成
    producer.join()
    q.join()  # 等待队列中的所有任务完成
    
    print("生产者-消费者模式完成")


# ===== 示例4: 线程池 =====
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(file_id):
    """模拟下载文件（I/O密集型任务）"""
    print(f"  [线程 {threading.get_ident()}] 开始下载文件 {file_id}")
    time.sleep(1)  # 模拟网络延迟
    print(f"  [线程 {threading.get_ident()}] 完成下载文件 {file_id}")
    return f"file_{file_id}.dat"


def example_thread_pool():
    """示例4: 使用线程池"""
    print("\n" + "="*60)
    print("示例4: 线程池")
    print("="*60)
    
    file_ids = list(range(1, 11))
    
    print(f"需要下载 {len(file_ids)} 个文件")
    
    # 方法1: map() - 按顺序返回结果
    print("\n[方法1] 使用 map():")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(download_file, file_ids)
        downloaded = list(results)
    
    end_time = time.time()
    print(f"下载完成: {downloaded}")
    print(f"耗时: {end_time - start_time:.2f} 秒")
    
    # 方法2: submit() - 更灵活，可以获取每个任务的Future对象
    print("\n[方法2] 使用 submit():")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(download_file, fid) for fid in file_ids]
        
        # as_completed按完成顺序返回结果
        for future in as_completed(futures):
            result = future.result()
            print(f"  完成: {result}")
    
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f} 秒")


# ===== 示例5: 信号量 Semaphore =====
# 模拟资源池（如数据库连接池）
semaphore = threading.Semaphore(3)  # 最多3个线程同时访问


def access_limited_resource(worker_id):
    """访问受限资源"""
    print(f"[工作线程-{worker_id}] 等待访问资源...")
    with semaphore:
        print(f"[工作线程-{worker_id}] ✅ 获得资源，开始工作")
        time.sleep(2)  # 模拟使用资源
        print(f"[工作线程-{worker_id}] 释放资源")


def example_semaphore():
    """示例5: 信号量限制并发"""
    print("\n" + "="*60)
    print("示例5: 信号量 (Semaphore)")
    print("="*60)
    print("模拟场景: 数据库连接池只有3个连接，5个线程竞争\n")
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=access_limited_resource, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("\n所有线程完成")


# ===== 示例6: 事件 Event =====
event = threading.Event()


def waiter(name):
    """等待事件的线程"""
    print(f"[{name}] 等待信号...")
    event.wait()  # 阻塞，直到事件被设置
    print(f"[{name}] 收到信号，开始执行！")


def setter():
    """设置事件的线程"""
    print("[触发器] 3秒后发送信号...")
    time.sleep(3)
    print("[触发器] 发送信号！")
    event.set()  # 设置事件，唤醒所有等待的线程


def example_event():
    """示例6: 事件同步"""
    print("\n" + "="*60)
    print("示例6: 事件 (Event)")
    print("="*60)
    
    # 创建等待线程
    waiters = []
    for i in range(3):
        t = threading.Thread(target=waiter, args=(f"等待者-{i}",))
        waiters.append(t)
        t.start()
    
    # 创建触发线程
    trigger = threading.Thread(target=setter)
    trigger.start()
    
    # 等待完成
    for t in waiters:
        t.join()
    trigger.join()
    
    print("事件同步完成")


# ===== 示例7: 线程本地存储 =====
thread_local_data = threading.local()


def process_data(data):
    """每个线程处理自己的数据"""
    # 每个线程有自己独立的thread_local_data.value
    thread_local_data.value = data
    thread_id = threading.get_ident()
    print(f"[线程 {thread_id}] 存储数据: {data}")
    time.sleep(1)
    print(f"[线程 {thread_id}] 读取数据: {thread_local_data.value}")


def example_thread_local():
    """示例7: 线程本地存储"""
    print("\n" + "="*60)
    print("示例7: 线程本地存储 (Thread Local)")
    print("="*60)
    print("每个线程有自己独立的存储空间\n")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=process_data, args=(f"数据-{i}",))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("\n线程本地存储示例完成")


# ===== 主函数 =====
def main():
    print("="*60)
    print("线程 (Thread) 学习示例")
    print("="*60)
    print("\n关键概念:")
    print("1. 线程是CPU调度的基本单位")
    print("2. 同一进程内的线程共享内存空间")
    print("3. 线程间通信简单，但需要注意线程安全")
    print("4. Python的GIL限制了多线程的并行能力")
    print("5. 适合I/O密集型任务")
    
    # 运行所有示例
    example_basic_thread()
    example_thread_lock()
    example_producer_consumer()
    example_thread_pool()
    example_semaphore()
    example_event()
    example_thread_local()
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)
    print("\n⚠️  注意: Python的GIL（全局解释器锁）限制:")
    print("   - 同一时间只有一个线程执行Python字节码")
    print("   - 对于CPU密集型任务，多线程不会提升性能")
    print("   - 对于I/O密集型任务，多线程很有效")


if __name__ == "__main__":
    main()


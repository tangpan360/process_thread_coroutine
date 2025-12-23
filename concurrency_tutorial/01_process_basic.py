"""
进程基础示例
演示：进程创建、进程间通信、进程池
"""

import multiprocessing as mp
import time
import os


# ===== 示例1: 基本的进程创建 =====
def worker_function(name, sleep_time):
    """工作函数：模拟一个耗时任务"""
    print(f"[进程 {name}] 开始执行 (PID: {os.getpid()})")
    time.sleep(sleep_time)
    print(f"[进程 {name}] 执行完成")
    return f"{name} 的结果"


def example_basic_process():
    """示例1: 创建和使用进程"""
    print("\n" + "="*60)
    print("示例1: 基本进程创建")
    print("="*60)
    
    print(f"主进程 PID: {os.getpid()}")
    
    # 创建多个进程
    processes = []
    for i in range(3):
        p = mp.Process(
            target=worker_function,
            args=(f"Worker-{i}", 2)
        )
        processes.append(p)
        p.start()  # 启动进程
        print(f"启动了进程 {p.name} (PID: {p.pid})")
    
    # 等待所有进程完成
    for p in processes:
        p.join()  # 阻塞，直到进程结束
    
    print("所有进程执行完毕")


# ===== 示例2: 进程间通信 - Queue =====
def producer(queue, items):
    """生产者：向队列中放入数据"""
    print(f"[生产者 PID: {os.getpid()}] 开始生产")
    for item in items:
        print(f"  生产: {item}")
        queue.put(item)
        time.sleep(0.5)
    queue.put(None)  # 发送结束信号
    print("[生产者] 完成")


def consumer(queue, name):
    """消费者：从队列中取出数据"""
    print(f"[消费者-{name} PID: {os.getpid()}] 开始消费")
    while True:
        item = queue.get()
        if item is None:
            queue.put(None)  # 传递结束信号给其他消费者
            break
        print(f"  消费者-{name} 消费: {item}")
        time.sleep(0.8)
    print(f"[消费者-{name}] 完成")


def example_queue_communication():
    """示例2: 使用Queue进行进程间通信"""
    print("\n" + "="*60)
    print("示例2: 进程间通信 - Queue")
    print("="*60)
    
    # 创建一个队列
    queue = mp.Queue()
    
    # 生产数据
    items = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']
    
    # 创建生产者进程
    prod = mp.Process(target=producer, args=(queue, items))
    
    # 创建消费者进程
    cons1 = mp.Process(target=consumer, args=(queue, "A"))
    cons2 = mp.Process(target=consumer, args=(queue, "B"))
    
    # 启动所有进程
    prod.start()
    cons1.start()
    cons2.start()
    
    # 等待完成
    prod.join()
    cons1.join()
    cons2.join()
    
    print("生产者-消费者模式完成")


# ===== 示例3: 进程间通信 - Pipe =====
def sender(conn, messages):
    """发送者：通过管道发送消息"""
    print(f"[发送者 PID: {os.getpid()}] 开始发送")
    for msg in messages:
        print(f"  发送: {msg}")
        conn.send(msg)
        time.sleep(0.5)
    conn.send("END")
    conn.close()


def receiver(conn):
    """接收者：通过管道接收消息"""
    print(f"[接收者 PID: {os.getpid()}] 开始接收")
    while True:
        msg = conn.recv()
        if msg == "END":
            break
        print(f"  接收: {msg}")
    conn.close()
    print("[接收者] 完成")


def example_pipe_communication():
    """示例3: 使用Pipe进行进程间通信"""
    print("\n" + "="*60)
    print("示例3: 进程间通信 - Pipe")
    print("="*60)
    
    # 创建一个双向管道
    parent_conn, child_conn = mp.Pipe()
    
    messages = ["Hello", "World", "From", "Process"]
    
    # 创建进程
    p1 = mp.Process(target=sender, args=(parent_conn, messages))
    p2 = mp.Process(target=receiver, args=(child_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("管道通信完成")


# ===== 示例4: 进程池 =====
def compute_square(n):
    """计算平方（模拟CPU密集型任务）"""
    print(f"  [PID: {os.getpid()}] 计算 {n}^2")
    time.sleep(0.5)  # 模拟计算时间
    return n * n


def example_process_pool():
    """示例4: 使用进程池处理任务"""
    print("\n" + "="*60)
    print("示例4: 进程池")
    print("="*60)
    
    numbers = list(range(1, 11))
    
    # 创建进程池（默认使用CPU核心数）
    cpu_count = mp.cpu_count()
    print(f"CPU核心数: {cpu_count}")
    print(f"创建 {cpu_count} 个进程的进程池")
    
    start_time = time.time()
    
    with mp.Pool(processes=cpu_count) as pool:
        # 并行计算
        results = pool.map(compute_square, numbers)
    
    end_time = time.time()
    
    print(f"\n结果: {results}")
    print(f"耗时: {end_time - start_time:.2f} 秒")


# ===== 示例5: 共享内存 =====
def increment_shared_value(shared_val, lock, name):
    """增加共享变量的值"""
    for _ in range(5):
        with lock:  # 加锁，防止竞态条件
            current = shared_val.value
            print(f"  [进程-{name}] 读取: {current}")
            time.sleep(0.1)
            shared_val.value = current + 1
            print(f"  [进程-{name}] 写入: {shared_val.value}")


def example_shared_memory():
    """示例5: 共享内存和锁"""
    print("\n" + "="*60)
    print("示例5: 共享内存和进程同步")
    print("="*60)
    
    # 创建共享值
    shared_value = mp.Value('i', 0)  # 'i' 表示整数
    lock = mp.Lock()
    
    # 创建两个进程
    p1 = mp.Process(target=increment_shared_value, args=(shared_value, lock, "A"))
    p2 = mp.Process(target=increment_shared_value, args=(shared_value, lock, "B"))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print(f"\n最终值: {shared_value.value}")
    print("（如果没有锁，最终值可能小于10，因为会有竞态条件）")


# ===== 主函数 =====
def main():
    print("="*60)
    print("进程 (Process) 学习示例")
    print("="*60)
    print("\n关键概念:")
    print("1. 进程是操作系统分配资源的基本单位")
    print("2. 每个进程有独立的内存空间")
    print("3. 进程间通信需要特殊机制（Queue、Pipe、共享内存等）")
    print("4. 进程创建和切换开销较大")
    print("5. 适合CPU密集型任务，可以利用多核")
    
    # 运行所有示例
    example_basic_process()
    example_queue_communication()
    example_pipe_communication()
    example_process_pool()
    example_shared_memory()
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)


if __name__ == "__main__":
    # Windows上需要这个保护
    mp.freeze_support()
    main()


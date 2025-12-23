"""
真实场景示例
展示进程、线程、协程在实际应用中的使用
"""

import time
import asyncio
import multiprocessing as mp
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import hashlib
import json
from pathlib import Path


# ===== 场景1: Web爬虫 (协程最优) =====
async def fetch_page_async(url, session_id):
    """异步爬取网页（模拟）"""
    # 模拟网络延迟
    await asyncio.sleep(0.5)
    
    # 模拟数据处理
    content = f"Content from {url}"
    data = {
        'url': url,
        'title': f'Page {url.split("/")[-1]}',
        'content_length': len(content),
        'timestamp': time.time()
    }
    
    return data


async def web_scraper_coroutine(urls):
    """协程版爬虫：高并发"""
    print("\n[协程爬虫] 开始爬取 {} 个网页...".format(len(urls)))
    start = time.time()
    
    # 并发爬取所有页面
    tasks = [fetch_page_async(url, i) for i, url in enumerate(urls)]
    results = await asyncio.gather(*tasks)
    
    duration = time.time() - start
    print(f"[协程爬虫] 完成！爬取 {len(results)} 个页面")
    print(f"[协程爬虫] 耗时: {duration:.2f} 秒")
    print(f"[协程爬虫] 平均速度: {len(results)/duration:.1f} 页/秒")
    
    return results, duration


def fetch_page_sync(url):
    """同步爬取网页（模拟）"""
    time.sleep(0.5)
    content = f"Content from {url}"
    return {
        'url': url,
        'title': f'Page {url.split("/")[-1]}',
        'content_length': len(content),
        'timestamp': time.time()
    }


def web_scraper_thread(urls):
    """多线程版爬虫"""
    print("\n[多线程爬虫] 开始爬取 {} 个网页...".format(len(urls)))
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_page_sync, urls))
    
    duration = time.time() - start
    print(f"[多线程爬虫] 完成！爬取 {len(results)} 个页面")
    print(f"[多线程爬虫] 耗时: {duration:.2f} 秒")
    print(f"[多线程爬虫] 平均速度: {len(results)/duration:.1f} 页/秒")
    
    return results, duration


def compare_web_scraping():
    """对比Web爬虫"""
    print("="*60)
    print("场景1: Web爬虫 (100个URL)")
    print("="*60)
    
    # 生成测试URL
    urls = [f"https://example.com/page/{i}" for i in range(100)]
    
    # 协程版本
    coro_results, coro_time = asyncio.run(web_scraper_coroutine(urls))
    
    # 多线程版本
    thread_results, thread_time = web_scraper_thread(urls)
    
    # 对比
    print("\n" + "="*60)
    print("Web爬虫总结:")
    print("="*60)
    print(f"协程:     {coro_time:.2f} 秒 ✅ 推荐")
    print(f"多线程:   {thread_time:.2f} 秒")
    print(f"性能提升: {thread_time/coro_time:.2f}x")
    print("\n原因:")
    print("- 爬虫是典型的I/O密集型任务")
    print("- 协程可以处理成千上万的并发连接")
    print("- 内存占用小，切换开销低")


# ===== 场景2: 图像处理 (多进程最优) =====
def process_image(image_id):
    """CPU密集型：处理图像（模拟）"""
    # 模拟复杂的图像处理算法
    result = 0
    for i in range(1000000):
        result += hashlib.md5(f"{image_id}_{i}".encode()).digest()[0]
    
    return {
        'image_id': image_id,
        'processed': True,
        'checksum': result % 1000
    }


def image_processor_process(image_ids):
    """多进程版图像处理"""
    print("\n[多进程处理] 开始处理 {} 张图片...".format(len(image_ids)))
    start = time.time()
    
    cpu_count = mp.cpu_count()
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        results = list(executor.map(process_image, image_ids))
    
    duration = time.time() - start
    print(f"[多进程处理] 完成！处理 {len(results)} 张图片")
    print(f"[多进程处理] 耗时: {duration:.2f} 秒")
    print(f"[多进程处理] 使用 {cpu_count} 个进程")
    
    return results, duration


def image_processor_thread(image_ids):
    """多线程版图像处理"""
    print("\n[多线程处理] 开始处理 {} 张图片...".format(len(image_ids)))
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_image, image_ids))
    
    duration = time.time() - start
    print(f"[多线程处理] 完成！处理 {len(results)} 张图片")
    print(f"[多线程处理] 耗时: {duration:.2f} 秒")
    
    return results, duration


def compare_image_processing():
    """对比图像处理"""
    print("\n" + "="*60)
    print("场景2: 图像处理 (8张图片)")
    print("="*60)
    
    image_ids = list(range(1, 9))
    
    # 多进程版本
    process_results, process_time = image_processor_process(image_ids)
    
    # 多线程版本（受GIL限制）
    thread_results, thread_time = image_processor_thread(image_ids)
    
    # 对比
    print("\n" + "="*60)
    print("图像处理总结:")
    print("="*60)
    print(f"多进程:   {process_time:.2f} 秒 ✅ 推荐（充分利用多核）")
    print(f"多线程:   {thread_time:.2f} 秒 ❌ 受GIL限制")
    print(f"性能提升: {thread_time/process_time:.2f}x")
    print("\n原因:")
    print("- 图像处理是典型的CPU密集型任务")
    print("- 多进程可以真正并行计算")
    print("- 多线程受GIL限制，无法并行")


# ===== 场景3: 数据库批量操作 (多线程合适) =====
class MockDatabase:
    """模拟数据库"""
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
    
    def insert(self, key, value):
        """插入数据（模拟I/O）"""
        time.sleep(0.1)  # 模拟网络延迟
        with self.lock:
            self.data[key] = value
        return True
    
    def batch_insert(self, items):
        """批量插入"""
        for key, value in items:
            self.insert(key, value)


db = MockDatabase()


def insert_batch(batch_id, records):
    """插入一批记录"""
    for record_id in records:
        key = f"batch_{batch_id}_record_{record_id}"
        value = {'id': record_id, 'data': f"Data {record_id}"}
        db.insert(key, value)
    return len(records)


def database_operations_serial(batches):
    """串行数据库操作"""
    print("\n[串行操作] 开始插入数据...")
    start = time.time()
    
    for batch_id, records in enumerate(batches):
        insert_batch(batch_id, records)
    
    duration = time.time() - start
    total_records = sum(len(b) for b in batches)
    print(f"[串行操作] 完成！插入 {total_records} 条记录")
    print(f"[串行操作] 耗时: {duration:.2f} 秒")
    
    return duration


def database_operations_thread(batches):
    """多线程数据库操作"""
    print("\n[多线程操作] 开始插入数据...")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(insert_batch, i, records) 
                   for i, records in enumerate(batches)]
        results = [f.result() for f in futures]
    
    duration = time.time() - start
    total_records = sum(results)
    print(f"[多线程操作] 完成！插入 {total_records} 条记录")
    print(f"[多线程操作] 耗时: {duration:.2f} 秒")
    
    return duration


def compare_database_operations():
    """对比数据库操作"""
    print("\n" + "="*60)
    print("场景3: 数据库批量操作 (50条记录)")
    print("="*60)
    
    # 准备数据：5批，每批10条记录
    batches = [list(range(i*10, (i+1)*10)) for i in range(5)]
    
    # 串行操作
    serial_time = database_operations_serial(batches)
    
    # 重置数据库
    db.data.clear()
    
    # 多线程操作
    thread_time = database_operations_thread(batches)
    
    # 对比
    print("\n" + "="*60)
    print("数据库操作总结:")
    print("="*60)
    print(f"串行:     {serial_time:.2f} 秒")
    print(f"多线程:   {thread_time:.2f} 秒 ✅ 推荐")
    print(f"性能提升: {serial_time/thread_time:.2f}x")
    print("\n原因:")
    print("- 数据库操作是I/O密集型")
    print("- 多线程可以充分利用等待时间")
    print("- 实现简单，易于维护")


# ===== 场景4: 文件批量处理 (混合使用) =====
def process_file(file_path):
    """处理单个文件"""
    # 模拟读取
    time.sleep(0.05)
    content = f"Content of {file_path}"
    
    # 模拟处理（CPU密集）
    result = 0
    for i in range(100000):
        result += hash(f"{content}_{i}") % 1000
    
    # 模拟写入
    time.sleep(0.05)
    
    return {
        'file': file_path,
        'size': len(content),
        'processed': result
    }


def file_processor_hybrid(files):
    """混合方案：进程池 + 线程池"""
    print("\n[混合方案] 使用进程池处理文件...")
    start = time.time()
    
    # 使用进程池处理CPU密集的部分
    cpu_count = min(mp.cpu_count(), 4)
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        results = list(executor.map(process_file, files))
    
    duration = time.time() - start
    print(f"[混合方案] 完成！处理 {len(results)} 个文件")
    print(f"[混合方案] 耗时: {duration:.2f} 秒")
    
    return results, duration


def compare_file_processing():
    """对比文件处理"""
    print("\n" + "="*60)
    print("场景4: 文件批量处理 (16个文件)")
    print("="*60)
    
    files = [f"file_{i}.txt" for i in range(16)]
    
    results, duration = file_processor_hybrid(files)
    
    print("\n" + "="*60)
    print("文件处理总结:")
    print("="*60)
    print(f"混合方案: {duration:.2f} 秒")
    print("\n方案:")
    print("- 使用多进程处理CPU密集部分")
    print("- 每个进程内部可以用线程处理I/O")
    print("- 充分利用系统资源")


# ===== 场景5: 实时数据处理管道 =====
def data_pipeline_example():
    """数据处理管道：生产者-处理者-消费者"""
    print("\n" + "="*60)
    print("场景5: 实时数据处理管道")
    print("="*60)
    
    # 使用队列连接各个阶段
    raw_queue = mp.Queue(maxsize=10)
    processed_queue = mp.Queue(maxsize=10)
    
    def producer(queue):
        """生产原始数据"""
        print("[生产者] 开始生产数据...")
        for i in range(20):
            data = {'id': i, 'value': i * 100}
            queue.put(data)
            time.sleep(0.1)
        queue.put(None)  # 结束信号
        print("[生产者] 完成")
    
    def processor(in_queue, out_queue):
        """处理数据（CPU密集）"""
        print("[处理者] 开始处理数据...")
        count = 0
        while True:
            data = in_queue.get()
            if data is None:
                out_queue.put(None)
                break
            
            # 模拟CPU密集处理
            processed = {
                'id': data['id'],
                'result': sum(i for i in range(data['value']))
            }
            out_queue.put(processed)
            count += 1
        
        print(f"[处理者] 完成，处理了 {count} 条数据")
    
    def consumer(queue):
        """消费处理后的数据"""
        print("[消费者] 开始消费数据...")
        count = 0
        while True:
            data = queue.get()
            if data is None:
                break
            # 模拟存储
            time.sleep(0.05)
            count += 1
        
        print(f"[消费者] 完成，消费了 {count} 条数据")
    
    # 创建进程
    prod = mp.Process(target=producer, args=(raw_queue,))
    proc = mp.Process(target=processor, args=(raw_queue, processed_queue))
    cons = mp.Process(target=consumer, args=(processed_queue,))
    
    print("\n启动管道...")
    start = time.time()
    
    prod.start()
    proc.start()
    cons.start()
    
    prod.join()
    proc.join()
    cons.join()
    
    duration = time.time() - start
    
    print(f"\n管道完成！总耗时: {duration:.2f} 秒")
    print("\n架构:")
    print("生产者(进程) → 队列 → 处理者(进程) → 队列 → 消费者(进程)")
    print("优点: 各阶段独立，可以充分利用多核，解耦合")


# ===== 主函数 =====
def main():
    print("="*60)
    print("真实场景示例")
    print("="*60)
    
    # 场景1: Web爬虫
    compare_web_scraping()
    
    # 场景2: 图像处理
    compare_image_processing()
    
    # 场景3: 数据库操作
    compare_database_operations()
    
    # 场景4: 文件处理
    compare_file_processing()
    
    # 场景5: 数据管道
    data_pipeline_example()
    
    # 总结
    print("\n" + "="*60)
    print("实战总结")
    print("="*60)
    print("""
    应用场景选择指南:
    
    1. Web服务器/API服务
       → 协程 (asyncio + aiohttp)
       → 高并发，低延迟
    
    2. 数据分析/科学计算
       → 多进程 (multiprocessing)
       → 充分利用CPU
    
    3. 数据库批量操作
       → 多线程 (ThreadPoolExecutor)
       → I/O密集，实现简单
    
    4. 视频/图像处理
       → 多进程 (ProcessPoolExecutor)
       → CPU密集，需要并行
    
    5. 实时数据处理
       → 多进程 + 队列
       → 流水线架构
    
    6. Web爬虫
       → 协程 (asyncio + aiohttp)
       → 海量并发连接
    
    混合使用:
    - 进程处理CPU密集任务
    - 线程处理I/O密集任务
    - 协程处理高并发I/O
    """)


if __name__ == "__main__":
    mp.freeze_support()
    main()


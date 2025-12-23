# 快速开始指南

## 环境准备

### 1. Python版本要求
- Python 3.7 或更高版本（推荐 Python 3.9+）
- 协程示例需要 Python 3.7+ 的 async/await 支持

### 2. 安装依赖

```bash
# 进入项目目录
cd concurrency_tutorial

# 安装依赖
pip install -r requirements.txt

# 或者使用国内镜像加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 学习路径

### 📚 第一步：阅读理论

阅读 `README.md`，理解：
- 为什么需要并发？
- 进程、线程、协程的区别
- 各自的优缺点和适用场景

### 🔧 第二步：运行基础示例

按顺序运行以下示例，理解基本概念：

```bash
# 1. 进程基础
python 01_process_basic.py

# 2. 线程基础
python 02_thread_basic.py

# 3. 协程基础
python 03_coroutine_basic.py
```

**预期输出**: 每个脚本会运行多个示例，展示各种用法和技巧。

### ⚡第三步：性能对比

运行性能对比脚本，直观感受三者的差异：

```bash
python 04_comparison.py
```

**你会看到**:
- CPU密集型任务：多进程最快
- I/O密集型任务：协程和多线程都很好
- 高并发场景：协程完胜
- 资源占用对比

### 🌍 第四步：真实场景

运行真实场景示例，了解实际应用：

```bash
python 05_real_world_examples.py
```

**涵盖场景**:
- Web爬虫
- 图像处理
- 数据库操作
- 文件处理
- 数据处理管道

---

## 常见问题

### Q1: 运行时出现 "ModuleNotFoundError: No module named 'aiohttp'"

**解决**: 确保已安装依赖
```bash
pip install aiohttp aiofiles
```

### Q2: Windows上进程示例运行异常

**解决**: 确保代码中有 `if __name__ == "__main__":` 保护，这是Windows上多进程的要求。

所有示例都已经包含了这个保护。

### Q3: 协程示例中的HTTP请求失败

**原因**: 需要网络连接访问 httpbin.org

**解决**: 
- 确保网络连接正常
- 或者跳过HTTP示例（代码中已有异常处理）

### Q4: 进程数量限制

**问题**: 创建太多进程可能失败

**原因**: 操作系统对进程数量有限制

**解决**: 使用进程池，控制并发数量

### Q5: Python多线程不能加速CPU密集型任务

**原因**: 这是Python的GIL（全局解释器锁）限制

**不是bug**: 这是设计决策，运行 `04_comparison.py` 可以看到对比

**解决**: CPU密集型任务使用多进程

---

## 自己动手实践

### 练习1: 修改参数

尝试修改示例中的参数，观察变化：
- 改变任务数量
- 改变工作线程/进程数
- 改变睡眠/计算时间

### 练习2: 编写自己的示例

基于学到的知识，实现以下场景：

1. **批量下载器**
   - 从URL列表下载文件
   - 使用协程实现高并发

2. **日志分析器**
   - 读取多个大型日志文件
   - 使用多进程并行处理

3. **数据转换工具**
   - 从CSV读取数据
   - 转换并写入数据库
   - 使用多线程

### 练习3: 性能调优

尝试回答：
- 对于1000个网络请求，最优的并发数是多少？
- 对于图像处理，进程数设置为CPU核心数+1会更快吗？
- 如何避免线程的竞态条件？

---

## 进阶学习

### 推荐阅读

1. **官方文档**
   - [multiprocessing文档](https://docs.python.org/3/library/multiprocessing.html)
   - [threading文档](https://docs.python.org/3/library/threading.html)
   - [asyncio文档](https://docs.python.org/3/library/asyncio.html)

2. **书籍推荐**
   - 《Python并行编程手册》
   - 《流畅的Python》第17-21章

3. **实战项目**
   - FastAPI (异步Web框架)
   - Celery (分布式任务队列)
   - Ray (分布式计算框架)

### 高级主题

- 分布式计算（跨机器）
- 无锁数据结构
- 协程在框架中的应用
- 性能剖析和调优

---

## 调试技巧

### 1. 打印进程/线程ID

```python
import os
import threading

print(f"进程ID: {os.getpid()}")
print(f"线程ID: {threading.get_ident()}")
```

### 2. 使用日志而非print

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(process)d:%(thread)d] %(message)s'
)
```

### 3. 使用调试器

```bash
# 使用pdb调试
python -m pdb your_script.py
```

---

## 性能测量

### 使用time模块

```python
import time

start = time.time()
# 你的代码
duration = time.time() - start
print(f"耗时: {duration:.2f} 秒")
```

### 使用timeit模块

```python
import timeit

time_taken = timeit.timeit(
    'your_function()',
    number=100,
    globals=globals()
)
```

### 使用psutil监控资源

```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"CPU使用率: {process.cpu_percent()}%")
print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

---

## 获取帮助

如果遇到问题：

1. 检查 `README.md` 中的概念说明
2. 查看代码注释
3. 运行简化版本的代码
4. 搜索错误信息
5. 查阅官方文档

---

## 下一步

完成这个教程后，你应该：

✅ 理解进程、线程、协程的区别  
✅ 知道在什么场景使用什么技术  
✅ 能够编写基本的并发程序  
✅ 了解常见的陷阱和最佳实践  

**继续学习**:
- 尝试在你的实际项目中应用
- 学习异步Web框架（如FastAPI、aiohttp）
- 探索分布式计算（如Dask、Ray）

祝学习愉快！🚀


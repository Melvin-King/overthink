from git import Repo
import os
import json
import pandas as pd

# 克隆 LCB 仓库到本地
repo_url = "https://github.com/LiveCodeBench/LiveCodeBench.git"
local_dir = "./LiveCodeBench"

if not os.path.exists(local_dir):
    Repo.clone_from(repo_url, local_dir)
    print("LiveCodeBench is downloaded！")
else:
    print("LiveCodeBench already exists！")

# load data（假设数据存储在 prompts/few_shot_examples/generation/*.json）
data_dir = "./LiveCodeBench/lcb_runner/prompts/few_shot_examples/generation"
problems = []

for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        with open(os.path.join(data_dir, filename), 'r') as f:
            problem_data = json.load(f)
            # 假设 JSON 文件结构包含问题描述、示例输入输出和隐藏测试用例
            problems.append({
                "problem_id": problem_data.get("id", filename.split('.')[0]),
                "prompt": problem_data.get("prompt", ""),
                "example_io": problem_data.get("examples", []),  # 示例输入输出
                "hidden_test_cases": problem_data.get("test_cases", []),  # 隐藏测试用例
                "reference_code": problem_data.get("reference_code", "")  # 可选参考代码
            })

# 如果 prompts 目录没有数据，尝试从 benchmarks 目录加载（可能需要调整）
if not problems:
    benchmark_dir = "./LiveCodeBench/benchmarks"
    for py_file in os.listdir(benchmark_dir):
        if py_file.endswith(".py") and py_file != "__init__.py":
            # 假设 benchmarks 中的 Python 文件可能生成或包含数据
            # 这里需要根据具体逻辑调用这些脚本（例如通过 import 或运行）
            print(f"可能需要运行 {py_file} 来生成数据")

# 转换为 DataFrame
if problems:
    df = pd.DataFrame(problems)
    print(f"加载了 {len(df)} 个问题")
else:
    print("未找到数据文件，请检查目录结构或运行相关脚本生成数据")

# 保存 DataFrame 以便后续使用
if 'df' in locals():
    df.to_csv("./data/lcb_problems.csv", index=False)
import pytest
import os

print("开始运行")

pytest.main()

# 执行命令
os.system(f"allure generate -c -o report  temps")

print("运行结束")
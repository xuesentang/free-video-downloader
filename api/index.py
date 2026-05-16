import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# 导入 FastAPI 应用
from main import app

# 导出 app 供 Vercel 使用

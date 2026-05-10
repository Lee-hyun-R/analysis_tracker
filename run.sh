#!/bin/bash

# 国考资料分析练习追踪系统启动脚本

echo "正在启动国考资料分析练习追踪系统..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 启动应用
echo "启动应用..."
echo "应用将在 http://localhost:8080 运行"
echo "按 Ctrl+C 停止应用"
python app.py
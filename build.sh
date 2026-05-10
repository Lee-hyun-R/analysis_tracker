#!/bin/bash

# 国考行测练习追踪系统打包脚本

echo "=========================================="
echo "  国考行测练习追踪系统 - 打包工具"
echo "=========================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 清理旧的构建文件
echo "清理旧文件..."
rm -rf build dist

# 开始打包
echo "开始打包..."
pyinstaller build.spec

# 检查打包结果
if [ -f "dist/国考行测练习追踪" ] || [ -f "dist/国考行测练习追踪.exe" ]; then
    echo ""
    echo "=========================================="
    echo "  打包成功！"
    echo "  生成文件: dist/国考行测练习追踪"
    echo ""
    echo "  使用说明:"
    echo "  1. 将 dist 目录下的文件复制给同学"
    echo "  2. 双击运行即可启动"
    echo "  3. 数据会保存在 exe 同级的 data 目录"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "  打包失败，请检查错误信息"
    echo "=========================================="
fi
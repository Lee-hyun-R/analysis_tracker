import os
import sys
import webbrowser
import threading
import time

def get_base_path():
    """获取基础路径，兼容 PyInstaller 打包"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_data_path():
    """获取数据存储路径，exe 同级目录"""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'data')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    # 设置基础路径
    base_path = get_base_path()
    data_path = get_data_path()
    
    # 确保数据目录存在
    os.makedirs(data_path, exist_ok=True)
    
    # 设置环境变量
    os.environ['BASE_PATH'] = base_path
    os.environ['DATA_PATH'] = data_path
    
    # 切换到基础目录
    os.chdir(base_path)
    
    # 导入 Flask 应用
    from app import app, DATA_DIR
    
    # 修改数据目录为 exe 同级目录
    import app as app_module
    app_module.DATA_DIR = data_path
    
    # 在新线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("=" * 50)
    print("  国考行测练习追踪系统")
    print("  正在启动，请稍候...")
    print("  浏览器将自动打开")
    print("  按 Ctrl+C 停止程序")
    print("=" * 50)
    
    # 启动 Flask
    app.run(host='127.0.0.1', port=8080, debug=False)
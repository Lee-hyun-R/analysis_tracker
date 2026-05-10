# 国考行测练习追踪

一个用于记录和分析国家公务员考试（国考）行测练习成绩的工具。

## 功能特点

- 📊 六大板块分项记录：资料分析、言语理解、判断推理、数量关系、常识判断、政治理论
- 📝 套题模拟考试记录
- 📈 成绩趋势图表分析
- 📋 Markdown 复盘总结支持
- 🔄 数据导入导出
- 🖥️ 支持打包为独立桌面应用

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装运行

```bash
# 克隆项目
git clone https://github.com/你的用户名/analysis_tracker.git
cd analysis_tracker

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

访问 http://localhost:8080 或者 http://192.168.0.130:8080即可使用。

### 打包为桌面应用

```bash
./build.sh
```

打包完成后，在 `dist/` 目录下生成可执行文件。

## 数据存储

所有数据以 JSON 格式存储在 `data/` 目录：

- `{module}_records.json` - 各板块练习记录
- `mock_records.json` - 套题记录
- `{module}_reviews.json` - 各板块复盘总结
- `mock_reviews.json` - 套题复盘总结

首次运行时 `data/` 目录会自动创建。

## 技术栈

- **后端**: Python + Flask
- **前端**: HTML + Tailwind CSS + Chart.js
- **Markdown**: Marked.js
- **打包**: PyInstaller

## 项目结构

```
analysis_tracker/
├── app.py              # Flask 后端
├── main.py             # PyInstaller 入口
├── requirements.txt    # Python 依赖
├── build.sh            # 打包脚本
├── run.sh              # 启动脚本
├── templates/
│   └── index.html      # 单页应用
├── static/             # 静态资源
└── data/               # 数据目录（自动创建）
```

## License

MIT

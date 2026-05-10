import json
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 支持 PyInstaller 打包
def get_data_dir():
    """获取数据目录，支持打包后的路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的 exe 运行
        return os.path.join(os.path.dirname(sys.executable), 'data')
    return os.environ.get('DATA_PATH', 'data')

DATA_DIR = get_data_dir()

# 板块配置
MODULES = {
    'ziliao': {'name': '资料分析', 'total': 20, 'icon': 'chart-bar'},
    'yanyu': {'name': '言语理解', 'total': 30, 'icon': 'chat'},
    'panduan': {'name': '判断推理', 'total': 35, 'icon': 'check-circle'},
    'shuliang': {'name': '数量关系', 'total': 15, 'icon': 'calculator'},
    'changshi': {'name': '常识判断', 'total': 15, 'icon': 'book-open'},
    'zhengzhi': {'name': '政治理论', 'total': 20, 'icon': 'academic-cap'}
}

def get_data_file(module):
    return os.path.join(DATA_DIR, f'{module}_records.json')

def get_mock_file():
    return os.path.join(DATA_DIR, 'mock_records.json')

def get_review_file(module):
    return os.path.join(DATA_DIR, f'{module}_reviews.json')

def get_mock_review_file():
    return os.path.join(DATA_DIR, 'mock_reviews.json')

def load_data(module):
    filepath = get_data_file(module)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(module, records):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_data_file(module)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_mock_data():
    filepath = get_mock_file()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_mock_data(records):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_mock_file()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_reviews(module):
    filepath = get_review_file(module)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_reviews(module, reviews):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_review_file(module)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def load_mock_reviews():
    filepath = get_mock_review_file()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_mock_reviews(reviews):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_mock_review_file()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/modules', methods=['GET'])
def get_modules():
    return jsonify(MODULES)

# 单板块记录 API
@app.route('/api/<module>/records', methods=['GET'])
def get_module_records(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    records = load_data(module)
    return jsonify(records)

@app.route('/api/<module>/records', methods=['POST'])
def add_module_record(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    records = load_data(module)
    
    new_record = {
        'id': len(records) + 1,
        'practice_number': len(records) + 1,
        'correct_count': data.get('correct_count', 0),
        'total_count': MODULES[module]['total'],
        'time_minutes': data.get('time_minutes', 0),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'notes': data.get('notes', '')
    }
    
    records.append(new_record)
    save_data(module, records)
    return jsonify(new_record), 201

@app.route('/api/<module>/records/<int:record_id>', methods=['PUT'])
def update_module_record(module, record_id):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    records = load_data(module)
    
    for record in records:
        if record['id'] == record_id:
            record.update(data)
            save_data(module, records)
            return jsonify(record)
    
    return jsonify({'error': 'Record not found'}), 404

@app.route('/api/<module>/records/<int:record_id>', methods=['DELETE'])
def delete_module_record(module, record_id):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    records = load_data(module)
    records = [r for r in records if r['id'] != record_id]
    
    for i, record in enumerate(records):
        record['id'] = i + 1
        record['practice_number'] = i + 1
    
    save_data(module, records)
    return jsonify({'message': 'Record deleted'})

@app.route('/api/<module>/records/clear', methods=['DELETE'])
def clear_module_records(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    save_data(module, [])
    return jsonify({'message': f'{MODULES[module]["name"]} records cleared'})

@app.route('/api/<module>/records/import', methods=['POST'])
def import_module_records(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    records = load_data(module)
    
    imported = data.get('records', [])
    for record in imported:
        record['id'] = len(records) + 1
        record['practice_number'] = len(records) + 1
        record['total_count'] = record.get('total_count', MODULES[module]['total'])
        records.append(record)
    
    save_data(module, records)
    return jsonify({'message': f'Imported {len(imported)} records'})

@app.route('/api/<module>/records/export', methods=['GET'])
def export_module_records(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    records = load_data(module)
    return jsonify(records)

# 套题记录 API
@app.route('/api/mock/records', methods=['GET'])
def get_mock_records():
    records = load_mock_data()
    return jsonify(records)

@app.route('/api/mock/records', methods=['POST'])
def add_mock_record():
    data = request.get_json()
    records = load_mock_data()
    
    # 计算各板块正确率
    modules_data = data.get('modules', {})
    total_correct = sum(m.get('correct_count', 0) for m in modules_data.values())
    total_questions = sum(MODULES.get(k, {}).get('total', 0) for k in modules_data.keys())
    
    new_record = {
        'id': len(records) + 1,
        'mock_number': len(records) + 1,
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'time_minutes': data.get('time_minutes', 0),
        'modules': modules_data,
        'total_correct': total_correct,
        'total_questions': total_questions,
        'accuracy': round(total_correct / total_questions * 100, 1) if total_questions > 0 else 0,
        'notes': data.get('notes', '')
    }
    
    records.append(new_record)
    save_mock_data(records)
    return jsonify(new_record), 201

@app.route('/api/mock/records/<int:record_id>', methods=['DELETE'])
def delete_mock_record(record_id):
    records = load_mock_data()
    records = [r for r in records if r['id'] != record_id]
    
    for i, record in enumerate(records):
        record['id'] = i + 1
        record['mock_number'] = i + 1
    
    save_mock_data(records)
    return jsonify({'message': 'Record deleted'})

@app.route('/api/mock/records/clear', methods=['DELETE'])
def clear_mock_records():
    save_mock_data([])
    return jsonify({'message': 'Mock records cleared'})

# 单板块复盘 API
@app.route('/api/<module>/reviews', methods=['GET'])
def get_module_reviews(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    reviews = load_reviews(module)
    return jsonify(reviews)

@app.route('/api/<module>/reviews', methods=['POST'])
def add_module_review(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    reviews = load_reviews(module)
    
    new_review = {
        'id': len(reviews) + 1,
        'content': data.get('content', ''),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'practice_number': data.get('practice_number', len(reviews) + 1),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    reviews.append(new_review)
    save_reviews(module, reviews)
    return jsonify(new_review), 201

@app.route('/api/<module>/reviews/<int:review_id>', methods=['PUT'])
def update_module_review(module, review_id):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    reviews = load_reviews(module)
    
    for review in reviews:
        if review['id'] == review_id:
            review['content'] = data.get('content', review['content'])
            review['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_reviews(module, reviews)
            return jsonify(review)
    
    return jsonify({'error': 'Review not found'}), 404

@app.route('/api/<module>/reviews/<int:review_id>', methods=['DELETE'])
def delete_module_review(module, review_id):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    reviews = load_reviews(module)
    reviews = [r for r in reviews if r['id'] != review_id]
    
    for i, review in enumerate(reviews):
        review['id'] = i + 1
    
    save_reviews(module, reviews)
    return jsonify({'message': 'Review deleted'})

@app.route('/api/<module>/reviews/clear', methods=['DELETE'])
def clear_module_reviews(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    save_reviews(module, [])
    return jsonify({'message': f'{MODULES[module]["name"]} reviews cleared'})

# 套题复盘 API
@app.route('/api/mock/reviews', methods=['GET'])
def get_mock_reviews_list():
    reviews = load_mock_reviews()
    return jsonify(reviews)

@app.route('/api/mock/reviews', methods=['POST'])
def add_mock_review():
    data = request.get_json()
    reviews = load_mock_reviews()
    
    new_review = {
        'id': len(reviews) + 1,
        'content': data.get('content', ''),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'mock_number': data.get('mock_number', len(reviews) + 1),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    reviews.append(new_review)
    save_mock_reviews(reviews)
    return jsonify(new_review), 201

@app.route('/api/mock/reviews/<int:review_id>', methods=['PUT'])
def update_mock_review(review_id):
    data = request.get_json()
    reviews = load_mock_reviews()
    
    for review in reviews:
        if review['id'] == review_id:
            review['content'] = data.get('content', review['content'])
            review['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_mock_reviews(reviews)
            return jsonify(review)
    
    return jsonify({'error': 'Review not found'}), 404

@app.route('/api/mock/reviews/<int:review_id>', methods=['DELETE'])
def delete_mock_review(review_id):
    reviews = load_mock_reviews()
    reviews = [r for r in reviews if r['id'] != review_id]
    
    for i, review in enumerate(reviews):
        review['id'] = i + 1
    
    save_mock_reviews(reviews)
    return jsonify({'message': 'Review deleted'})

@app.route('/api/mock/reviews/clear', methods=['DELETE'])
def clear_mock_reviews():
    save_mock_reviews([])
    return jsonify({'message': 'Mock reviews cleared'})

# 合并复盘 API
@app.route('/api/reviews/combined', methods=['GET'])
def get_combined_reviews():
    all_reviews = []
    
    for module, config in MODULES.items():
        reviews = load_reviews(module)
        for review in reviews:
            all_reviews.append({
                'module': module,
                'module_name': config['name'],
                'type': 'module',
                'id': review['id'],
                'content': review['content'],
                'date': review['date'],
                'practice_number': review.get('practice_number', review['id']),
                'created_at': review.get('created_at', '')
            })
    
    mock_reviews = load_mock_reviews()
    for review in mock_reviews:
        all_reviews.append({
            'module': 'mock',
            'module_name': '套题记录',
            'type': 'mock',
            'id': review['id'],
            'content': review['content'],
            'date': review['date'],
            'mock_number': review.get('mock_number', review['id']),
            'created_at': review.get('created_at', '')
        })
    
    all_reviews.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(all_reviews)

# 统计 API
@app.route('/api/<module>/stats', methods=['GET'])
def get_module_stats(module):
    if module not in MODULES:
        return jsonify({'error': 'Module not found'}), 404
    
    records = load_data(module)
    
    if not records:
        return jsonify({
            'total_practice': 0,
            'avg_correct': 0,
            'avg_time': 0,
            'avg_accuracy': 0,
            'best_correct': 0,
            'trend': '-'
        })
    
    total = len(records)
    avg_correct = sum(r['correct_count'] for r in records) / total
    avg_time = sum(r['time_minutes'] for r in records) / total
    total_count = MODULES[module]['total']
    avg_accuracy = (avg_correct / total_count) * 100
    best_correct = max(r['correct_count'] for r in records)
    
    trend = '-'
    if total >= 2:
        last = records[-1]['correct_count']
        prev = records[-2]['correct_count']
        diff = last - prev
        trend = f'↑{diff}' if diff > 0 else f'↓{abs(diff)}' if diff < 0 else '→'
    
    return jsonify({
        'total_practice': total,
        'avg_correct': round(avg_correct, 1),
        'avg_time': round(avg_time, 1),
        'avg_accuracy': round(avg_accuracy, 1),
        'best_correct': best_correct,
        'trend': trend
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from datetime import datetime
import sqlite3
import os
import zipfile
import tempfile
import shutil
import base64
import time
import pandas as pd
from docx import Document
import PyPDF2

st.set_page_config(
    page_title="图像处理实验室 - 融思政平台",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化实验室CSS
st.markdown("""
<style>
:root {
    --primary-red: #dc2626;
    --dark-red: #b91c1c;
    --light-red: #fef2f2;
    --accent-red: #ef4444;
    --gold: #f59e0b;
    --beige-light: #fefaf0;
    --beige-medium: #fdf6e3;
    --beige-dark: #faf0d9;
}

/* 整体页面背景 - 米色渐变 */
.stApp {
    background: linear-gradient(135deg, #fefaf0 0%, #fdf6e3 50%, #faf0d9 100%);
}

.lab-header {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    color: white;
    padding: 40px 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(220, 38, 38, 0.3);
    border: 3px solid #f59e0b;
}

.lab-title {
    font-size: 2.5rem;
    margin-bottom: 10px;
    font-weight: bold;
}

.ideology-card {
    background: linear-gradient(135deg, #fef2f2, #fff);
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #dc2626;
    margin: 20px 0;
    box-shadow: 0 6px 12px rgba(220, 38, 38, 0.15);
}

.info-card {
    background: linear-gradient(135deg, #fef2f2, #ffecec);
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #dc2626;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(220, 38, 38, 0.1);
}

.image-container {
    border: 3px solid #dc2626;
    border-radius: 12px;
    padding: 15px;
    background: white;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}



 /* 现代化按钮 - 红白渐变悬浮效果 */
.stButton button {
    background: linear-gradient(135deg, #ffffff, #fef2f2);
    color: #dc2626;
    border: 2px solid #dc2626;
    padding: 14px 28px;
    border-radius: 50px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2);
    transition: all 0.3s ease;
    font-size: 1rem;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
}
    
.stButton button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(220, 38, 38, 0.1), transparent);
    transition: left 0.6s;
}
    
 .stButton button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4);
    border-color: #dc2626;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    /* 特殊按钮样式 - 金色边框 */
.stButton button.gold-btn {
    border: 2px solid #d4af37;
    color: #d4af37;
    background: linear-gradient(135deg, #fffdf6, #fefaf0);
}
    
.stButton button.gold-btn:hover {
    background: linear-gradient(135deg, #d4af37, #b8941f);
    color: white;
    border-color: #d4af37;
}
    
/* 整体页面内容区域 */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background: linear-gradient(135deg, #fefaf0 0%, #fdf6e3 50%, #faf0d9 100%);
}





/* 侧边栏样式 - 米色渐变 */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #fdf6e3 0%, #faf0d9 50%, #f5e6c8 100%) !important;
}

.file-item {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.file-item:hover {
    background: #e9ecef;
}

/* 文件预览样式 */
.file-preview {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e9ecef;
}

.preview-content {
    max-height: 400px;
    overflow: auto;
}

/* 提交成功特效 */
.success-animation {
    animation: successPulse 2s ease-in-out;
    text-align: center;
    padding: 30px;
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border-radius: 15px;
    border: 3px solid #10b981;
    margin: 20px 0;
}

@keyframes successPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* 分数徽章 */
.score-badge {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 12px 24px;
    border-radius: 25px;
    font-weight: bold;
    font-size: 1.3rem;
    text-align: center;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    display: inline-block;
}

/* 提交记录卡片 */
.submission-card {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.submission-card:hover {
    border-color: #dc2626;
    box-shadow: 0 6px 12px rgba(220, 38, 38, 0.2);
    transform: translateY(-2px);
}

/* 状态徽章 */
.status-badge {
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: bold;
    display: inline-block;
}

.status-pending {
    background: #fef3c7;
    color: #d97706;
    border: 1px solid #f59e0b;
}

.status-graded {
    background: #d1fae5;
    color: #059669;
    border: 1px solid #10b981;
}

.status-returned {
    background: #fee2e2;
    color: #dc2626;
    border: 1px solid #ef4444;
}

/* 统计卡片 */
.stats-card {
    background: linear-gradient(135deg, #fef2f2, #fff);
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #dc2626;
    text-align: center;
    margin: 10px;
}

.stats-number {
    font-size: 2rem;
    font-weight: bold;
    color: #dc2626;
    margin: 10px 0;
}

.stats-label {
    font-size: 0.9rem;
    color: #666;
}

/* 烟花特效容器 */
.fireworks-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
}

/* 教师评分卡片 */
.grading-card {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #0ea5e9;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(14, 165, 233, 0.2);
}

/* 提交特效 */
.submission-success {
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    border-radius: 20px;
    border: 4px solid #22c55e;
    margin: 20px 0;
    animation: celebrate 2s ease-in-out;
}

@keyframes celebrate {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.05); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}

.confetti {
    position: fixed;
    width: 10px;
    height: 10px;
    background: #ff0000;
    opacity: 0.7;
    animation: fall linear forwards;
}

@keyframes fall {
    to {
        transform: translateY(100vh) rotate(360deg);
        opacity: 0;
    }
}
</style>
""", unsafe_allow_html=True)

# 创建上传文件存储目录
UPLOAD_DIR = "experiment_submissions"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 数据库函数 - 修复版本
def init_experiment_db():
    """初始化实验提交数据库"""
    conn = sqlite3.connect('image_processing_platform.db')
    c = conn.cursor()
    
    # 检查表是否存在
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experiment_submissions'")
    table_exists = c.fetchone()
    
    if table_exists:
        # 表已存在，检查所有必需的列
        c.execute("PRAGMA table_info(experiment_submissions)")
        columns = [column[1] for column in c.fetchall()]
        
        required_columns = {
            'can_view_score': 'BOOLEAN DEFAULT 0',
            'file_names': 'TEXT DEFAULT ""',
            'resubmission_count': 'INTEGER DEFAULT 0'
        }
        
        for col_name, col_type in required_columns.items():
            if col_name not in columns:
                try:
                    c.execute(f'ALTER TABLE experiment_submissions ADD COLUMN {col_name} {col_type}')
                    st.success(f"已添加缺失的列: {col_name}")
                except Exception as e:
                    st.error(f"添加列 {col_name} 失败: {str(e)}")
    else:
        # 创建新表
        c.execute('''
            CREATE TABLE experiment_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_username TEXT NOT NULL,
                experiment_number INTEGER NOT NULL,
                experiment_title TEXT NOT NULL,
                submission_content TEXT NOT NULL,
                submission_time TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                teacher_feedback TEXT DEFAULT '',
                score INTEGER DEFAULT 0,
                can_view_score BOOLEAN DEFAULT 0,
                resubmission_count INTEGER DEFAULT 0,
                file_names TEXT DEFAULT ''
            )
        ''')
        st.success("创建实验提交表成功")
    
    conn.commit()
    conn.close()

def save_uploaded_files(uploaded_files, submission_id, student_username):
    """保存上传的文件"""
    saved_files = []
    if uploaded_files:
        submission_dir = os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}")
        if not os.path.exists(submission_dir):
            os.makedirs(submission_dir)
        
        for uploaded_file in uploaded_files:
            file_path = os.path.join(submission_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_files.append(uploaded_file.name)
    
    return saved_files

def get_submission_files(submission_id, student_username):
    """获取提交的文件列表"""
    submission_dir = os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}")
    if os.path.exists(submission_dir):
        return os.listdir(submission_dir)
    return []

def get_file_path(submission_id, student_username, filename):
    """获取文件路径"""
    return os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}", filename)

def create_zip_file(submission_id, student_username):
    """创建包含所有提交文件的ZIP包"""
    submission_dir = os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}")
    if os.path.exists(submission_dir):
        zip_path = os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(submission_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, submission_dir))
        return zip_path
    return None

def submit_experiment(student_username, experiment_number, experiment_title, submission_content, uploaded_files):
    """提交实验"""
    try:
        conn = sqlite3.connect('image_processing_platform.db')
        c = conn.cursor()
        submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 先插入提交记录
        c.execute('''
            INSERT INTO experiment_submissions 
            (student_username, experiment_number, experiment_title, submission_content, submission_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_username, experiment_number, experiment_title, submission_content, submission_time))
        
        submission_id = c.lastrowid
        
        # 保存上传的文件
        saved_files = save_uploaded_files(uploaded_files, submission_id, student_username)
        
        # 更新文件名字段
        c.execute('''
            UPDATE experiment_submissions 
            SET file_names = ? 
            WHERE id = ?
        ''', (','.join(saved_files), submission_id))
        
        conn.commit()
        conn.close()
        return True, "实验提交成功！", submission_id
    except Exception as e:
        return False, f"提交失败：{str(e)}", None

def get_student_experiments(student_username):
    """获取学生的实验提交记录"""
    try:
        conn = sqlite3.connect('image_processing_platform.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM experiment_submissions 
            WHERE student_username = ? 
            ORDER BY submission_time DESC
        ''', (student_username,))
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        st.error(f"获取学生实验记录失败: {str(e)}")
        return []

def get_all_experiments():
    """获取所有学生的实验提交（教师端使用）"""
    try:
        conn = sqlite3.connect('image_processing_platform.db')
        c = conn.cursor()
        c.execute('''
            SELECT es.*, u.role 
            FROM experiment_submissions es
            JOIN users u ON es.student_username = u.username
            ORDER BY es.submission_time DESC
        ''')
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        st.error(f"获取所有实验记录失败: {str(e)}")
        return []

def update_experiment_score(submission_id, score, feedback, can_view_score, status):
    """更新实验评分和反馈"""
    try:
        conn = sqlite3.connect('image_processing_platform.db')
        c = conn.cursor()
        c.execute('''
            UPDATE experiment_submissions 
            SET score = ?, teacher_feedback = ?, can_view_score = ?, status = ?
            WHERE id = ?
        ''', (score, feedback, can_view_score, status, submission_id))
        conn.commit()
        conn.close()
        return True, "评分更新成功！"
    except Exception as e:
        return False, f"更新失败：{str(e)}"

def withdraw_experiment(submission_id, student_username):
    """撤回实验提交"""
    try:
        conn = sqlite3.connect('image_processing_platform.db')
        c = conn.cursor()
        c.execute('''
            DELETE FROM experiment_submissions 
            WHERE id = ? AND student_username = ? AND status = 'pending'
        ''', (submission_id, student_username))
        
        # 删除对应的文件
        submission_dir = os.path.join(UPLOAD_DIR, f"{student_username}_{submission_id}")
        if os.path.exists(submission_dir):
            shutil.rmtree(submission_dir)
        
        conn.commit()
        conn.close()
        return True, "实验提交已撤回！"
    except Exception as e:
        return False, "撤回失败：只能撤回待批改状态的提交"

def get_experiment_title(number):
    titles = {
        1: "图像增强技术实践",
        2: "边缘检测算法比较",
        3: "图像滤波处理实验",
        4: "图像锐化技术应用",
        5: "采样与量化分析",
        6: "彩色图像分割实践",
        7: "综合图像处理项目",
        8: "创新应用开发"
    }
    return titles.get(number, f"实验{number}")

def get_experiment_description(number):
    descriptions = {
        1: "使用不同的图像增强技术处理图像，分析比较效果",
        2: "实现并比较多种边缘检测算法的性能",
        3: "应用中值滤波、均值滤波等技术进行图像去噪",
        4: "使用拉普拉斯算子等方法进行图像锐化",
        5: "分析不同采样率和量化等级对图像质量的影响",
        6: "实现基于RGB和HSI颜色空间的图像分割",
        7: "综合运用多种图像处理技术完成实际项目",
        8: "开发具有创新性的图像处理应用"
    }
    return descriptions.get(number, "完成指定的图像处理实验")

def read_pdf_file(file_path):
    """读取PDF文件内容"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"读取PDF文件时出错: {str(e)}"

def read_docx_file(file_path):
    """读取DOCX文件内容"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"读取DOCX文件时出错: {str(e)}"

def preview_file_content(file_path, filename):
    """预览文件内容"""
    try:
        file_ext = filename.lower().split('.')[-1]
        
        # 图像文件预览
        if file_ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            image = Image.open(file_path)
            st.image(image, caption=filename, use_container_width=True)
        
        # 文本文件预览
        elif file_ext in ['txt', 'py', 'java', 'cpp', 'c', 'h', 'html', 'css', 'js', 'md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            st.code(content, language=file_ext if file_ext in ['py', 'java', 'cpp', 'c', 'html', 'css', 'js'] else None)
        
        # PDF文件预览
        elif file_ext == 'pdf':
            st.markdown(f"**📄 PDF文件预览: {filename}**")
            
            # 显示PDF基本信息
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    st.info(f"📊 PDF信息: 共 {num_pages} 页")
                    
                    # 显示PDF内容
                    st.markdown("**📖 内容预览:**")
                    pdf_text = read_pdf_file(file_path)
                    if pdf_text.strip():
                        with st.expander("查看PDF文本内容", expanded=False):
                            st.text_area("PDF内容", pdf_text, height=300, key=f"pdf_{filename}")
                    else:
                        st.warning("无法提取PDF文本内容，可能为扫描版PDF")
                    
                    # 提供PDF页面预览
                    st.markdown("**🖼️ 页面预览:**")
                    col1, col2, col3 = st.columns(3)
                    
                    # 显示前3页的预览
                    for i, page_num in enumerate(range(min(3, num_pages))):
                        with col1 if i == 0 else col2 if i == 1 else col3:
                            # 这里可以添加PDF页面转图像的功能
                            # 目前先显示页面信息
                            st.markdown(f"**第 {page_num + 1} 页**")
                            st.info(f"页面 {page_num + 1}/{num_pages}")
                            
            except Exception as e:
                st.error(f"处理PDF文件时出错: {str(e)}")
            
            # 提供PDF下载
            with open(file_path, "rb") as f:
                pdf_data = f.read()
                st.download_button(
                    label="📥 下载PDF文件",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"download_pdf_{filename}",
                    use_container_width=True
                )
        
        # DOC/DOCX文件预览
        elif file_ext in ['doc', 'docx']:
            st.markdown(f"**📝 Word文档预览: {filename}**")
            
            try:
                if file_ext == 'docx':
                    # 读取DOCX文件内容
                    doc_text = read_docx_file(file_path)
                    
                    if doc_text.strip():
                        st.markdown("**📖 文档内容:**")
                        st.text_area("文档内容", doc_text, height=400, key=f"docx_{filename}")
                    else:
                        st.warning("文档内容为空或无法读取")
                        
                    # 显示文档统计信息
                    word_count = len(doc_text.split())
                    line_count = len(doc_text.split('\n'))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("字数统计", f"{word_count} 字")
                    with col2:
                        st.metric("行数统计", f"{line_count} 行")
                        
                else:
                    st.info("📋 .doc格式文件需要特殊处理，建议转换为.docx格式以获得更好的预览效果")
                    
            except Exception as e:
                st.error(f"处理Word文档时出错: {str(e)}")
            
            # 提供下载
            with open(file_path, "rb") as f:
                doc_data = f.read()
                st.download_button(
                    label="📥 下载Word文档",
                    data=doc_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if file_ext == 'docx' else "application/msword",
                    key=f"download_doc_{filename}",
                    use_container_width=True
                )
        
        # 不支持预览的文件类型
        else:
            st.info(f"📄 文件类型 '{file_ext}' 不支持在线预览，请下载查看")
            
    except Exception as e:
        st.error(f"预览文件时出错: {str(e)}")

# 初始化数据库
init_experiment_db()

# 其他图像处理函数保持不变...
def create_sample_image():
    """创建示例图像"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    # 添加渐变背景
    for i in range(400):
        for j in range(600):
            img[i, j] = [255 - i//3, 255 - j//4, 255]
    
    # 添加文字
    cv2.putText(img, "数字图像处理实验室", (100, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (220, 38, 38), 3)
    cv2.putText(img, "融思政平台示例图像", (150, 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)
    cv2.putText(img, "践行工匠精神 · 培养科学素养", (120, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (220, 38, 38), 2)
    return img

def apply_edge_detection(image, operator):
    """应用边缘检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    if operator == "Sobel":
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        processed = cv2.magnitude(sobelx, sobely)
    elif operator == "Canny":
        processed = cv2.Canny(gray, 50, 150)
    else:  # Laplacian
        processed = cv2.Laplacian(gray, cv2.CV_64F)
    
    return cv2.normalize(processed, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def apply_filter(image, filter_type, kernel_size):
    """应用滤波器"""
    if filter_type == "中值滤波":
        return cv2.medianBlur(image, kernel_size)
    else:  # 均值滤波
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        return cv2.filter2D(image, -1, kernel)

def provide_download_button(image, filename, button_text):
    """提供下载按钮"""
    try:
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        image_pil = Image.fromarray(image)
        buffered = io.BytesIO()
        image_pil.save(buffered, format="JPEG", quality=95)
        
        st.download_button(
            label=button_text,
            data=buffered.getvalue(),
            file_name=filename,
            mime="image/jpeg",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"下载功能出错: {str(e)}")

def apply_operator(image, operator):
    """应用微分算子"""
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if operator == "Sobel (一阶)":
        # Sobel算子
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        processed = cv2.magnitude(sobelx, sobely).astype(np.uint8)

    elif operator == "Prewitt (一阶)":
        # Prewitt算子
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        prewittx = cv2.filter2D(gray.astype(np.float32), -1, kernelx)
        prewitty = cv2.filter2D(gray.astype(np.float32), -1, kernely)
        processed = cv2.magnitude(prewittx, prewitty).astype(np.uint8)

    elif operator == "Roberts (一阶)":
        # Roberts算子
        kernelx = np.array([[1, 0], [0, -1]])
        kernely = np.array([[0, 1], [-1, 0]])
        robertsx = cv2.filter2D(gray.astype(np.float32), -1, kernelx)
        robertsy = cv2.filter2D(gray.astype(np.float32), -1, kernely)
        processed = cv2.magnitude(robertsx, robertsy).astype(np.uint8)

    elif operator == "Laplacian (二阶)":
        # Laplacian算子
        processed = cv2.Laplacian(gray, cv2.CV_64F).astype(np.uint8)

    # 将处理后的图像转换回BGR格式以便显示
    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

    return processed

def apply_piecewise_linear_transformation(image, a, b, c, d):
    """应用分段线性变换"""
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 将图像归一化到[0, 1]
    gray_normalized = gray.astype(np.float32) / 255.0

    # 分段线性变换
    transformed = np.zeros_like(gray_normalized)
    transformed[gray_normalized < a] = gray_normalized[gray_normalized < a] * (b / a)
    transformed[(gray_normalized >= a) & (gray_normalized < c)] = gray_normalized[(gray_normalized >= a) & (
            gray_normalized < c)] * ((d - b) / (c - a)) + b
    transformed[gray_normalized >= c] = gray_normalized[gray_normalized >= c] * ((1 - d) / (1 - c)) + d

    # 将图像恢复到[0, 255]
    transformed = (transformed * 255).astype(np.uint8)

    # 将变换后的图像转换回BGR格式以便显示
    transformed = cv2.cvtColor(transformed, cv2.COLOR_GRAY2BGR)

    return transformed

def apply_sampling(image, sample_ratio):
    """应用图像采样"""
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 获取原始图像尺寸
    height, width = gray.shape

    # 计算采样后的图像尺寸
    sampled_height = height // sample_ratio
    sampled_width = width // sample_ratio

    # 采样后的图像
    sampled = cv2.resize(gray, (sampled_width, sampled_height), interpolation=cv2.INTER_NEAREST)

    # 将采样后的图像转换回BGR格式以便显示
    sampled = cv2.cvtColor(sampled, cv2.COLOR_GRAY2BGR)

    return sampled

def apply_quantization(image, quantization_level):
    """应用图像量化"""
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 量化
    quantized = np.uint8(np.floor(gray / (256 / quantization_level)) * (256 / quantization_level))

    # 将量化后的图像转换回BGR格式以便显示
    quantized = cv2.cvtColor(quantized, cv2.COLOR_GRAY2BGR)

    return quantized

def apply_rgb_segmentation(image, lower_thresh, upper_thresh):
    """应用RGB分割"""
    # 创建一个掩码，其中满足阈值条件的像素为白色，其余为黑色
    lower = np.array([lower_thresh, lower_thresh, lower_thresh])
    upper = np.array([upper_thresh, upper_thresh, upper_thresh])
    mask = cv2.inRange(image, lower, upper)

    # 应用掩码到原始图像
    segmented = cv2.bitwise_and(image, image, mask=mask)

    return segmented

# 渲染侧边栏
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; 
                    padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;
                    box-shadow: 0 6px 12px rgba(220, 38, 38, 0.3); border: 2px solid #f59e0b;'>
            <h3 style='margin: 0;'>🔬 图像处理实验室</h3>
            <p style='margin: 10px 0 0 0;'>技术报国 · 创新发展 · 思政引领</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 快速导航
        st.markdown("### 🧭 快速导航")
        
        # 修复导航按钮 - 使用正确的页面路径
        if st.button("🏠 返回首页", use_container_width=True):
            st.switch_page("main.py")
        if st.button("🔬 图像处理实验室", use_container_width=True):
            st.switch_page("pages/1_🔬_图像处理实验室.py")
        if st.button("📚 学习资源中心", use_container_width=True):
            st.switch_page("pages/2_📚_学习资源中心.py")
        if st.button("📝 我的思政足迹", use_container_width=True):
            st.switch_page("pages/3_📝_我的思政足迹.py")
        if st.button("🏆 成果展示", use_container_width=True):
            st.switch_page("pages/4_🏆_成果展示.py")
        
        # 思政学习进度
        st.markdown("### 📚 思政学习进度")
        
        ideology_progress = [
            {"name": "工匠精神", "icon": "🔧", "progress": 85},
            {"name": "科学态度", "icon": "🔬", "progress": 78},
            {"name": "创新意识", "icon": "💡", "progress": 82},
            {"name": "责任担当", "icon": "⚖️", "progress": 88}
        ]
        
        for item in ideology_progress:
            st.markdown(f"**{item['icon']} {item['name']}**")
            st.progress(item['progress'] / 100)
        
        st.markdown("---")
        
        # 思政理论学习
        st.markdown("### 🎯 思政理论学习")
        theory_topics = [
            "图像处理中的工匠精神",
            "科技创新与国家发展",
            "技术伦理与社会责任",
            "科学家精神传承"
        ]
        
        for topic in theory_topics:
            if st.button(f"📖 {topic}", key=f"theory_{topic}", use_container_width=True):
                st.info(f"开始学习：{topic}")
        
        st.markdown("---")
        
        # 实验指南
        st.markdown("""
        <div class='info-card'>
            <h4>📚 实验指南</h4>
            <ol style='padding-left: 20px;'>
                <li>选择实验模块</li>
                <li>上传图像文件</li>
                <li>调整处理参数</li>
                <li>查看实时效果</li>
                <li>记录学习感悟</li>
            </ol>
            <p><strong>支持格式：</strong> JPG, PNG, JPEG, PDF, DOC, DOCX</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 思政教育提示
        st.markdown("""
        <div class='ideology-card'>
            <h5>💡 思政教育提示</h5>
            <p style='font-size: 0.9rem;'>在技术学习中培养：</p>
            <ul style='padding-left: 15px; font-size: 0.85rem;'>
                <li>🎯 精益求精的工匠精神</li>
                <li>🔬 实事求是的科学态度</li>
                <li>💡 创新发展的时代担当</li>
                <li>🇨🇳 科技报国的家国情怀</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 快速开始示例
        if st.button("查看示例图像", use_container_width=True):
            sample_image = create_sample_image()
            st.image(sample_image, caption="示例图像", use_container_width=True)
        
        # 系统信息
        st.markdown("---")
        st.markdown("**📊 系统信息**")
        st.text(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.text("状态: 🟢 正常运行")
        st.text("版本: v2.1.0")

# 实验室头部
st.markdown("""
<div class='lab-header'>
    <h1 class='lab-title'>🔬 数字图像处理实验室</h1>
    <p style='font-size: 1.3rem; opacity: 0.95;'>融合现代化图像处理实践平台 · 践行工匠精神 · 培养科学素养</p>
</div>
""", unsafe_allow_html=True)

# 渲染侧边栏
render_sidebar()

# 创建选项卡
tab_names = [
    "🔬 图像增强", 
    "📐 边缘检测", 
    "🔄 线性变换", 
    "✨ 图像锐化",
    "📊 采样与量化",
    "🎨 彩色图像分割",
    "📝 实验提交"  # 所有用户都可以看到实验提交选项卡
]

tabs = st.tabs(tab_names)

# 图像增强选项卡（保持不变）
with tabs[0]:
    st.markdown("### 🔬 图像增强处理")
    
    # 思政教育卡片
    st.markdown("""
    <div class='ideology-card'>
        <h4>🎯 思政关联：精益求精的工匠精神</h4>
        <p style='text-align: left;'>
        <strong>图像增强技术</strong>体现了<strong style='color: #dc2626;'>精益求精</strong>的工匠精神，
        通过不断优化细节，追求更高质量的图像效果，这正体现了社会主义核心价值观中的<strong style='color: #dc2626;'>敬业</strong>精神。
        在技术学习中，我们要发扬这种一丝不苟、追求卓越的精神品质。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📤 选择图像文件", 
        type=["jpg", "jpeg", "png"], 
        key="enhancement_upload"
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image = np.array(image)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, caption="原始图像", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='info-card'>
                    <h5>📊 图像信息</h5>
                    <p><strong>尺寸：</strong>{image.shape[1]} × {image.shape[0]}</p>
                    <p><strong>通道：</strong>{image.shape[2] if len(image.shape) > 2 else 1}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 处理选项
            operator = st.selectbox(
                "选择微分算子",
                ("Sobel (一阶)", "Prewitt (一阶)", "Roberts (一阶)", "Laplacian (二阶)"),
                key="selectbox_enhancement"
            )
            
            if st.button("处理图像", key="button_enhancement", use_container_width=True):
                with st.spinner("处理中..."):
                    processed_image = apply_operator(image, operator)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption="原始图像", use_container_width=True)
                with col2:
                    st.image(processed_image, caption=f"使用{operator}处理后的图像", use_container_width=True)
                
                provide_download_button(processed_image, f"enhanced_{operator}.jpg", "下载处理结果")
                    
        except Exception as e:
            st.error(f"处理失败：{str(e)}")
    else:
        st.info("请上传图像文件开始处理")

# 其他图像处理选项卡保持不变...

# 实验提交选项卡 - 所有用户都可以访问
with tabs[6]:
    st.markdown("### 📝 实验提交中心")
    
    # 根据用户角色显示不同的内容
    if st.session_state.get('role') == 'student':
        # 学生端：实验提交界面
        st.markdown("#### 🎓 学生实验提交")
        
        # 实验选择
        experiment_number = st.selectbox(
            "选择实验",
            options=[1, 2, 3, 4, 5, 6, 7, 8],
            format_func=lambda x: f"实验{x}: {get_experiment_title(x)}"
        )
        
        experiment_title = get_experiment_title(experiment_number)
        
        st.markdown(f"### {experiment_title}")
        st.markdown(get_experiment_description(experiment_number))
        
        # 提交内容
        submission_content = st.text_area(
            "实验报告内容",
            placeholder="请详细描述您的实验过程、结果分析、遇到的问题及解决方案...",
            height=300
        )
        
        # 文件上传
        uploaded_files = st.file_uploader(
            "上传实验文件（代码、结果图像、报告文档等）",
            type=['py', 'jpg', 'png', 'zip', 'pdf', 'doc', 'docx', 'txt', 'cpp', 'c', 'java'],
            accept_multiple_files=True,
            help="支持多种文件格式：代码文件(.py, .java, .cpp, .c)、图像文件(.jpg, .png)、文档(.pdf, .doc, .docx)、压缩包(.zip)等"
        )
        
        # 显示已选择的文件
        if uploaded_files:
            st.markdown("**已选择的文件:**")
            for file in uploaded_files:
                st.markdown(f"""
                <div class='file-item'>
                    <span>📎 {file.name}</span>
                    <span style='color: #666; font-size: 0.9rem;'>{file.size / 1024:.1f} KB</span>
                </div>
                """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 提交实验", use_container_width=True):
                if submission_content.strip():
                    # 确保用户已登录
                    if 'username' not in st.session_state:
                        st.session_state.username = "demo_student"
                    
                    success, message, submission_id = submit_experiment(
                        st.session_state.username,
                        experiment_number,
                        experiment_title,
                        submission_content,
                        uploaded_files
                    )
                    if success:
                        # 显示提交成功特效
                        st.markdown(f"""
                        <div class='submission-success'>
                            <h1 style='color: #16a34a; margin-bottom: 20px;'>🎉 提交成功！</h1>
                            <p style='font-size: 1.5rem; margin-bottom: 20px;'>您的实验报告已成功提交</p>
                            <div style='background: white; padding: 20px; border-radius: 15px; display: inline-block; margin-bottom: 20px;'>
                                <p style='margin: 0; font-weight: bold; font-size: 1.2rem;'>提交ID: <span style='color: #dc2626;'>{submission_id}</span></p>
                            </div>
                            <p style='font-size: 1.1rem;'>请等待老师批阅，您可以在下方查看提交记录</p>
                            <div style='font-size: 2rem; margin-top: 20px;'>
                                🎊 🎈 🎉 ✨ 🎇
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 多重特效
                        st.balloons()
                        st.snow()
                        
                        # 添加成功提示
                        st.success("✅ 实验提交成功！")
                        
                        # 自动显示提交记录
                        st.session_state.show_my_submissions = True
                        
                        # 添加延迟刷新
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("请填写实验报告内容")
        
        with col2:
            if st.button("🔄 查看我的提交", use_container_width=True):
                st.session_state.show_my_submissions = True
        
        # 显示我的提交记录
        if st.session_state.get('show_my_submissions', False):
            st.markdown("---")
            st.markdown("### 📋 我的实验提交记录")
            
            # 确保用户已登录
            if 'username' not in st.session_state:
                st.session_state.username = "demo_student"
            
            submissions = get_student_experiments(st.session_state.username)
            
            if submissions:
                # 统计信息
                total_submissions = len(submissions)
                graded_submissions = len([s for s in submissions if s[6] == 'graded'])
                pending_submissions = len([s for s in submissions if s[6] == 'pending'])
                average_score = sum([s[8] for s in submissions if s[6] == 'graded']) / graded_submissions if graded_submissions > 0 else 0
                
                # 显示统计卡片
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown("""
                    <div class='stats-card'>
                        <div>📊 总提交</div>
                        <div class='stats-number'>{}</div>
                        <div class='stats-label'>实验总数</div>
                    </div>
                    """.format(total_submissions), unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                    <div class='stats-card'>
                        <div>✅ 已批改</div>
                        <div class='stats-number'>{}</div>
                        <div class='stats-label'>完成评分</div>
                    </div>
                    """.format(graded_submissions), unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                    <div class='stats-card'>
                        <div>⏳ 待批改</div>
                        <div class='stats-number'>{}</div>
                        <div class='stats-label'>等待评分</div>
                    </div>
                    """.format(pending_submissions), unsafe_allow_html=True)
                with col4:
                    st.markdown("""
                    <div class='stats-card'>
                        <div>🎯 平均分</div>
                        <div class='stats-number'>{:.1f}</div>
                        <div class='stats-label'>当前成绩</div>
                    </div>
                    """.format(average_score), unsafe_allow_html=True)
                
                # 显示详细提交记录
                st.markdown("### 详细提交记录")
                for sub in submissions:
                    status_info = {
                        'pending': ('⏳ 待批改', 'status-pending'),
                        'graded': ('✅ 已评分', 'status-graded'),
                        'returned': ('🔙 已退回', 'status-returned')
                    }.get(sub[6], ('⚪ 未知', ''))
                    
                    with st.expander(f"{status_info[0]} - 实验{sub[2]}: {sub[3]} - {sub[5]}", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("**📝 提交内容:**")
                            st.text_area("内容", sub[4], height=150, key=f"content_{sub[0]}", disabled=True)
                            
                            # 显示提交的文件 - 添加预览功能
                            if len(sub) > 10 and sub[10]:  # file_names字段
                                file_list = sub[10].split(',') if sub[10] else []
                                if file_list:
                                    st.markdown("**📎 提交的文件:**")
                                    for filename in file_list:
                                        if filename.strip():
                                            file_path = get_file_path(sub[0], st.session_state.username, filename.strip())
                                            if os.path.exists(file_path):
                                                # 文件预览区域
                                                st.markdown(f'<div class="file-preview">', unsafe_allow_html=True)
                                                st.markdown(f'<div class="preview-header"><strong>📄 {filename}</strong></div>', unsafe_allow_html=True)
                                                
                                                # 预览内容
                                                preview_file_content(file_path, filename)
                                                
                                                # 下载按钮
                                                with open(file_path, "rb") as file:
                                                    file_data = file.read()
                                                    st.download_button(
                                                        label=f"📥 下载 {filename}",
                                                        data=file_data,
                                                        file_name=filename,
                                                        mime="application/octet-stream",
                                                        key=f"download_{sub[0]}_{filename}",
                                                        use_container_width=True
                                                    )
                                                st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # 提供打包下载
                                    zip_path = create_zip_file(sub[0], st.session_state.username)
                                    if zip_path and os.path.exists(zip_path):
                                        with open(zip_path, "rb") as zip_file:
                                            zip_data = zip_file.read()
                                            st.download_button(
                                                label="📦 下载所有文件(ZIP)",
                                                data=zip_data,
                                                file_name=f"实验{sub[2]}_提交文件.zip",
                                                mime="application/zip",
                                                key=f"zip_{sub[0]}",
                                                use_container_width=True
                                            )
                            
                            # 显示分数和反馈（如果已评分且允许查看）
                            if sub[6] == 'graded' and sub[9]:  # 已评分且允许查看
                                st.markdown(f"""
                                <div class='score-badge'>
                                    🎯 得分: {sub[8]}/100
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if sub[7]:  # 教师反馈
                                    st.markdown("**💬 教师反馈:**")
                                    st.info(sub[7])
                        
                        with col2:
                            st.markdown(f"**📊 状态:**")
                            st.markdown(f"<span class='{status_info[1]} status-badge'>{status_info[0]}</span>", unsafe_allow_html=True)
                            st.markdown(f"**🕒 提交时间:** {sub[5]}")
                            st.markdown(f"**🔢 提交ID:** `{sub[0]}`")
                            
                            if sub[6] == 'pending':
                                if st.button("撤回", key=f"withdraw_{sub[0]}", use_container_width=True):
                                    success, msg = withdraw_experiment(sub[0], st.session_state.username)
                                    if success:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
            else:
                st.info("暂无提交记录，请先提交实验报告")
    
    elif st.session_state.get('role') == 'teacher':
        # 教师端：实验管理界面
        st.markdown("#### 👨‍🏫 教师实验管理")
        
        # 获取所有学生的实验提交
        all_submissions = get_all_experiments()
        
        if all_submissions:
            # 教师端统计信息
            total_submissions = len(all_submissions)
            pending_submissions = len([s for s in all_submissions if s[6] == 'pending'])
            graded_submissions = len([s for s in all_submissions if s[6] == 'graded'])
            average_score = sum([s[8] for s in all_submissions if s[6] == 'graded']) / graded_submissions if graded_submissions > 0 else 0
            
            # 显示统计卡片
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                <div class='stats-card'>
                    <div>📊 总提交</div>
                    <div class='stats-number'>{}</div>
                    <div class='stats-label'>所有实验</div>
                </div>
                """.format(total_submissions), unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class='stats-card'>
                    <div>⏳ 待批改</div>
                    <div class='stats-number'>{}</div>
                    <div class='stats-label'>等待评分</div>
                </div>
                """.format(pending_submissions), unsafe_allow_html=True)
            with col3:
                st.markdown("""
                <div class='stats-card'>
                    <div>✅ 已批改</div>
                    <div class='stats-number'>{}</div>
                    <div class='stats-label'>完成评分</div>
                </div>
                """.format(graded_submissions), unsafe_allow_html=True)
            with col4:
                st.markdown("""
                <div class='stats-card'>
                    <div>🎯 平均分</div>
                    <div class='stats-number'>{:.1f}</div>
                    <div class='stats-label'>班级平均</div>
                </div>
                """.format(average_score), unsafe_allow_html=True)
            
            # 按状态筛选
            st.markdown("### 🔍 筛选提交")
            filter_status = st.selectbox(
                "筛选状态",
                ["全部", "待批改", "已评分", "已退回"]
            )
            
            filtered_submissions = all_submissions
            if filter_status == "待批改":
                filtered_submissions = [s for s in all_submissions if s[6] == 'pending']
            elif filter_status == "已评分":
                filtered_submissions = [s for s in all_submissions if s[6] == 'graded']
            elif filter_status == "已退回":
                filtered_submissions = [s for s in all_submissions if s[6] == 'returned']
            
            st.markdown(f"**找到 {len(filtered_submissions)} 个提交**")
            
            # 显示提交列表
            for sub in filtered_submissions:
                status_info = {
                    'pending': ('⏳ 待批改', 'status-pending'),
                    'graded': ('✅ 已评分', 'status-graded'),
                    'returned': ('🔙 已退回', 'status-returned')
                }.get(sub[6], ('⚪ 未知', ''))
                
                with st.expander(f"{sub[1]} - 实验{sub[2]}: {sub[3]} - {status_info[0]} - {sub[5]}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("**👤 学生:**")
                        st.info(f"**{sub[1]}**")
                        
                        st.markdown("**📝 提交内容:**")
                        st.text_area("内容", sub[4], height=150, key=f"teacher_content_{sub[0]}", disabled=True)
                        
                        # 显示提交的文件
                        if len(sub) > 10 and sub[10]:
                            file_list = sub[10].split(',') if sub[10] else []
                            if file_list:
                                st.markdown("**📎 提交的文件:**")
                                for filename in file_list:
                                    if filename.strip():
                                        file_path = get_file_path(sub[0], sub[1], filename.strip())
                                        if os.path.exists(file_path):
                                            # 文件预览区域
                                            st.markdown(f'<div class="file-preview">', unsafe_allow_html=True)
                                            st.markdown(f'<div class="preview-header"><strong>📄 {filename}</strong></div>', unsafe_allow_html=True)
                                            
                                            # 预览内容
                                            preview_file_content(file_path, filename)
                                            
                                            # 下载按钮
                                            with open(file_path, "rb") as file:
                                                file_data = file.read()
                                                st.download_button(
                                                    label=f"📥 下载 {filename}",
                                                    data=file_data,
                                                    file_name=filename,
                                                    mime="application/octet-stream",
                                                    key=f"teacher_download_{sub[0]}_{filename}",
                                                    use_container_width=True
                                                )
                                            st.markdown('</div>', unsafe_allow_html=True)
                                
                                # 提供打包下载
                                zip_path = create_zip_file(sub[0], sub[1])
                                if zip_path and os.path.exists(zip_path):
                                    with open(zip_path, "rb") as zip_file:
                                        zip_data = zip_file.read()
                                        st.download_button(
                                            label="📦 下载所有文件(ZIP)",
                                            data=zip_data,
                                            file_name=f"{sub[1]}_实验{sub[2]}_提交文件.zip",
                                            mime="application/zip",
                                            key=f"teacher_zip_{sub[0]}",
                                            use_container_width=True
                                        )
                        
                        # 显示现有评分和反馈
                        if sub[6] == 'graded':
                            st.markdown(f"""
                            <div class='score-badge'>
                                🎯 当前得分: {sub[8]}/100
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if sub[7]:
                                st.markdown("**💬 当前反馈:**")
                                st.info(sub[7])
                    
                    with col2:
                        st.markdown(f"**📊 状态:**")
                        st.markdown(f"<span class='{status_info[1]} status-badge'>{status_info[0]}</span>", unsafe_allow_html=True)
                        st.markdown(f"**🕒 提交时间:** {sub[5]}")
                        st.markdown(f"**🔢 提交ID:** `{sub[0]}`")
                        
                        # 评分和反馈表单
                        st.markdown("---")
                        st.markdown("**📝 评分与反馈**")
                        
                        with st.form(key=f"grade_form_{sub[0]}"):
                            score = st.slider("评分", 0, 100, sub[8] if sub[8] else 60, key=f"score_{sub[0]}")
                            feedback = st.text_area("教师反馈", sub[7] if sub[7] else "", 
                                                  placeholder="请输入对学生的反馈意见...", 
                                                  key=f"feedback_{sub[0]}")
                            can_view_score = st.checkbox("允许学生查看分数", value=bool(sub[9]), key=f"view_{sub[0]}")
                            status = st.selectbox("状态", 
                                                ["pending", "graded", "returned"], 
                                                index=["pending", "graded", "returned"].index(sub[6]) if sub[6] in ["pending", "graded", "returned"] else 0,
                                                key=f"status_{sub[0]}")
                            
                            submitted = st.form_submit_button("💾 保存评分", use_container_width=True)
                            if submitted:
                                success, message = update_experiment_score(sub[0], score, feedback, can_view_score, status)
                                if success:
                                    st.success("✅ " + message)
                                    st.rerun()
                                else:
                                    st.error("❌ " + message)
        else:
            st.info("暂无学生提交的实验报告")
    
    else:
        # 未登录用户提示
        st.warning("请先登录以访问实验提交功能")

# 底部思政总结
st.markdown("---")
st.markdown("""
<div class='ideology-card'>
    <h3>🌟 思政学习总结</h3>
    <p style='text-align: center; font-size: 1.1rem;'>
    通过图像处理实验，我们不仅学习技术知识，更重要的是培养<strong style='color: #dc2626;'>工匠精神、科学态度、创新意识和责任担当</strong>，
    将个人成长与国家发展紧密结合，为实现科技强国目标贡献力量。
    </p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="思政成果展示", 
    page_icon="🏆", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化米色思政主题CSS
def apply_modern_css():
    st.markdown("""
    <style>
    /* 现代化米色主题变量 */
    :root {
        --primary-red: #dc2626;
        --dark-red: #b91c1c;
        --accent-red: #ef4444;
        --beige-light: #fefaf0;
        --beige-medium: #fdf6e3;
        --beige-dark: #faf0d9;
        --gold: #d4af37;
        --light-gold: #fef3c7;
        --dark-text: #1f2937;
        --light-text: #6b7280;
        --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        --hover-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
    }
    
    /* 整体页面背景 - 米色渐变 */
    .stApp {
        background: linear-gradient(135deg, #fefaf0 0%, #fdf6e3 50%, #faf0d9 100%);
    }
    
    /* 现代化头部 */
    .modern-header {
        background: linear-gradient(135deg, var(--primary-red) 0%, var(--dark-red) 100%);
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 24px;
        margin: 20px 0 40px 0;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        font-size: 2.5rem;
        margin-bottom: 15px;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        background: linear-gradient(135deg, #fff, #fef3c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .achievement-card {
        background: linear-gradient(135deg, #fff, var(--beige-light));
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid var(--primary-red);
        margin: 20px 0;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
    }
    
    .achievement-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--hover-shadow);
    }
    
    .project-card {
        background: linear-gradient(135deg, #fff, var(--beige-light));
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--hover-shadow);
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, var(--primary-red), var(--accent-red));
    }
    
    .ideology-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary-red), var(--accent-red));
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    
    .ideology-badge.blue {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    }
    
    .ideology-badge.green {
        background: linear-gradient(135deg, #10b981, #047857);
    }
    
    .ideology-badge.yellow {
        background: linear-gradient(135deg, #f59e0b, #d97706);
    }
    
    .ideology-badge.purple {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    }
    
    .section-title {
        color: var(--primary-red);
        font-size: 2rem;
        margin: 30px 0 20px 0;
        border-bottom: 3px solid #e5e7eb;
        padding-bottom: 10px;
        font-weight: 700;
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
    
    .css-1d391kg {
        background: linear-gradient(135deg, #fdf6e3 0%, #faf0d9 50%, #f5e6c8 100%) !important;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 渲染侧边栏
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; 
            padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;
            box-shadow: 0 6px 12px rgba(220, 38, 38, 0.3);'>
            <h3>🏆 思政成果展示</h3>
            <p style='margin: 10px 0 0 0; font-size: 1rem;'>技术报国 · 思想引领 · 创新发展</p>
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
            {"name": "工匠精神", "icon": "🔧", "progress": 90},
            {"name": "家国情怀", "icon": "🇨🇳", "progress": 85},
            {"name": "科学态度", "icon": "🔬", "progress": 78},
            {"name": "创新意识", "icon": "💡", "progress": 82},
            {"name": "责任担当", "icon": "⚖️", "progress": 88},
            {"name": "团队合作", "icon": "🤝", "progress": 80}
        ]
        
        for item in ideology_progress:
            st.markdown(f"**{item['icon']} {item['name']}**")
            st.progress(item['progress'] / 100)
        
        st.markdown("---")
        
        # 思政理论学习
        st.markdown("### 🎯 思政理论学习")
        theory_topics = [
            "新时代工匠精神的内涵与实践",
            "科技创新与国家发展战略",
            "社会主义核心价值观与技术伦理",
            "科学家精神与家国情怀",
            "数字时代的责任与担当"
        ]
        
        for topic in theory_topics:
            if st.button(f"📖 {topic}", key=f"theory_{topic}", use_container_width=True):
                st.info(f"开始学习：{topic}")
        
        st.markdown("---")
        
        
        # 思政学习提醒
        st.markdown("---")
        st.markdown("### 💫 思政学习提醒")
        st.success("""
        🎯 **本周思政重点：**
        - 学习科学家精神
        - 践行工匠精神
        - 培养家国情怀
        - 强化责任担当
        """)

# 生成优秀作品数据（基于事实的优秀成果）
def generate_projects_data():
    projects = [
        {
            "title": "智能图像增强系统",
            "author": "李天龙、陈曦、王语嫣（团队）",
            "tech_highlight": "基于进化算法的CNN自适应图像增强技术",
            "ideology": ["工匠精神", "创新意识"],
            "description": "团队在魏培阳、甘建红老师指导下，优化CNN模型架构，结合进化算法实现复杂场景下的图像去噪、超分辨率重建，解决传统算法细节丢失问题，每一个参数调整都历经上百次测试，体现了精益求精的技术追求和算法创新突破。",
            "achievement": "第17届中国大学生计算机设计大赛全国二等奖",
            "impact": "可应用于气象雷达图像、安防监控画面优化，已为2家气象观测站提供数据处理支持，提升图像分析准确率25%",
            "date": "2024-08-11"
        },
        {
            "title": "细胞智绘—基于超分辨的AI细胞图像分析系统",
            "author": "吴欣遥、刘馨宇、赵彬宇（团队）",
            "tech_highlight": "超分辨成像+神经元细胞精准定位算法",
            "ideology": ["科学态度", "责任担当"],
            "description": "在杨昊、周航老师指导下，针对脑神经元细胞标注难题，研发超分辨图像分析技术，通过算法拉开紧密接触的细胞间距，实现精准定位标注，减少科研人员手动标注工作量，体现了用技术解决医学研究痛点的责任担当和严谨科学态度。",
            "achievement": "第17届中国大学生计算机设计大赛全国三等奖",
            "impact": "已辅助脑科学研究团队提升数据处理效率40%，降低科研资源消耗30%，为神经科学研究提供技术支撑",
            "date": "2024-08-20"
        },
        {
            "title": "传承“徽”煌数学—传统文化数字图像处理平台",
            "author": "王佳艺、王欣钰（团队）",
            "tech_highlight": "PS图像处理+Illustrator矢量绘图融合技术",
            "ideology": ["文化自信", "传承创新"],
            "description": "团队在范晶、刘雪峰老师指导下，运用专业图像处理工具，将刘徽数学思想与徽派文化元素通过图像可视化呈现，每一处视觉细节都经过反复雕琢，实现艺术与技术的完美融合，体现了对传统文化的传承与数字技术创新的结合。",
            "achievement": "第17届中国大学生计算机设计大赛全国三等奖",
            "impact": "已应用于3所中学传统文化教学，帮助学生通过视觉化方式理解古代数学成就，覆盖师生2000余人",
            "date": "2024-08-20"
        },
        {
            "title": "工业零件缺陷智能检测系统",
            "author": "张宇恒、李佳琦、陈思远（团队）",
            "tech_highlight": "轻量化YOLOv8+实时图像分割检测技术",
            "ideology": ["实践创新", "责任担当"],
            "description": "在周骏教授指导下，针对制造业零件检测需求，优化YOLOv8算法实现轻量化部署，精准识别金属表面裂纹、注塑件瑕疵，检测准确率达99.2%，团队扎根企业车间收集真实数据，体现了面向实际需求的创新思维和解决工业痛点的责任担当。",
            "achievement": "2023年全国大学生“软件杯”程序设计大赛全国一等奖",
            "impact": "已在2家汽车零部件企业试点应用，检测效率提升6倍，降低产品不良率15%，助力制造业高质量发展",
            "date": "2023-07-15"
        },
        {
            "title": "低照度医疗影像实时增强系统",
            "author": "赵铭宇、孙晓雯、周子昂（团队）",
            "tech_highlight": "时空域联合降噪+自适应亮度调节算法",
            "ideology": ["精益求精", "人文关怀"],
            "description": "团队在周骏教授指导下，聚焦医疗影像低照度问题，研发时空域联合增强技术，在抑制噪声的同时保留病灶细节，实时处理帧率达30fps，反复优化算法以适配不同医疗设备，体现了对技术性能的极致追求和关爱患者的人文关怀。",
            "achievement": "2022年全国大学生“软件杯”程序设计大赛全国二等奖",
            "impact": "已接入1家基层医院放射科，提升低剂量CT影像清晰度，帮助医生减少漏诊率8%",
            "date": "2022-08-05"
        },
        {
            "title": "文物数字化修复与展示系统",
            "author": "林雨桐、郑浩然、徐静怡（团队）",
            "tech_highlight": "点云配准优化+纹理映射修复技术",
            "ideology": ["文化传承", "创新意识"],
            "description": "在范晶老师指导下，通过高清图像采集、点云配准算法优化，实现破损文物的数字化重建与虚拟修复，还原徽派古建筑木雕细节，团队多次实地采集文物数据，结合数字技术让文化遗产“活起来”，体现了传承文化的责任与技术创新的意识。",
            "achievement": "第17届中国大学生计算机设计大赛省级一等奖",
            "impact": "已为1家地方博物馆提供3件文物数字化服务，助力文化遗产永久保存与线上展示，累计线上访问量超5万人次",
            "date": "2024-07-10"
        },
        {
            "title": "基于Gabor-pix2pix的灰度图像智能彩色化系统",
            "author": "马宇辰、刘思彤、张昊（团队）",
            "tech_highlight": "Gabor滤波器纹理提取+改进型pix2pix生成对抗网络",
            "ideology": ["创新意识", "科学态度"],
            "description": "团队在西安科技大学李洪安教授指导下，针对传统图像彩色化存在的颜色越界、边界模糊问题，提出融合Gabor滤波器与pix2pix模型的解决方案：先通过Gabor滤波器提取6尺度4方向纹理特征（最优参数为7×7尺度、0°方向），再改进pix2pix生成器网络深度并引入LSGAN最小二乘损失函数，解决大规模数据集训练不稳定问题。经summer风景数据集测试，彩色化结果误着色区域减少35%，细节还原度提升40%，体现对技术痛点的创新突破与严谨的科学验证态度。",
            "achievement": "2024年全国大学生人工智能创新大赛省级一等奖",
            "impact": "已应用于历史黑白照片修复、遥感图像增强场景，为2家博物馆提供老照片数字化服务，帮助还原历史场景色彩信息",
            "date": "2024-09-28"
        },
        {
            "title": "Pillow+OpenCV电商产品图批量处理系统",
            "author": "陈雨薇、周子墨、吴浩宇（团队）",
            "tech_highlight": "多平台自适应裁剪算法+半透明水印嵌入技术",
            "ideology": ["实践创新", "工匠精神"],
            "description": "团队在高校王磊老师指导下，基于Pillow与OpenCV开发电商图像自动化处理工具：支持批量调整尺寸（默认800×800像素）、按平台比例裁剪（Instagram 1:1/4:5、Twitter 16:9）、嵌入半透明品牌水印（字体自适应图像尺寸），并通过高斯滤波优化色彩质量。工具解决传统人工处理效率低、格式不统一问题，单批次处理100张图像仅需3分钟，参数设置历经20余次迭代优化，体现面向产业需求的实践创新与精益求精的技术追求。",
            "achievement": "2024年全国大学生计算机应用能力大赛国家级三等奖",
            "impact": "已服务3家中小电商企业，产品图处理效率提升90%，统一化图像使店铺点击率平均增长18%",
            "date": "2024-10-15"
        }
    ]
    return projects

# 生成统计数据
def generate_stats_data():
    stats = {
        'ideology_distribution': {
            '工匠精神': 35,
            '家国情怀': 28,
            '创新意识': 22,
            '责任担当': 25,
            '科学态度': 20,
            '团队合作': 18
        },
        'project_types': {
            '技术创新类': 45,
            '社会服务类': 30,
            '文化传承类': 15,
            '国家战略类': 10
        }
    }
    return stats

def main():
    # 应用CSS样式
    apply_modern_css()
    
    # 页面标题
    st.markdown("""
    <div class='modern-header'>
        <h1>🏆 思政成果展示</h1>
        <p class='subtitle'>技术赋能 · 思想引领 · 创新驱动 · 服务国家</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 渲染侧边栏
    render_sidebar()
    
    # 总体统计
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 优秀作品", "156个", "+28个")
    with col2:
        st.metric("🏅 获得奖项", "86项", "+15项")
    with col3:
        st.metric("💡 技术创新", "245项", "+42项")
    with col4:
        st.metric("🌟 思政融合", "100%", "深度融合")
    
    # 使用标签页组织内容
    tab1, tab2, tab3 = st.tabs(["🎨 优秀作品", "📊 成果分析", "💡 作品征集"])
    
    with tab1:
        st.markdown('<div class="section-title">🎨 优秀作品展示</div>', unsafe_allow_html=True)
        
        projects = generate_projects_data()
        
        # 筛选选项
        col1, col2 = st.columns(2)
        with col1:
            filter_ideology = st.multiselect(
                "筛选思政元素",
                ["工匠精神", "家国情怀", "创新意识", "责任担当", "科学态度", "团队合作", "文化自信", "追求卓越"],
                default=[]
            )
        
        # 显示项目
        filtered_projects = projects
        if filter_ideology:
            filtered_projects = [p for p in projects if any(ideology in p['ideology'] for ideology in filter_ideology)]
        
        # 两列布局显示项目
        cols = st.columns(2)
        for i, project in enumerate(filtered_projects):
            with cols[i % 2]:
                ideology_badges = " ".join([f'<span class="ideology-badge">{ideology}</span>' for ideology in project['ideology']])
                
                st.markdown(f"""
                <div class='project-card'>
                    <h3>🎯 {project['title']}</h3>
                    <p><strong>👤 作者：</strong>{project['author']}</p>
                    <p><strong>💻 技术亮点：</strong>{project['tech_highlight']}</p>
                    <p><strong>🇨🇳 思政元素：</strong>{ideology_badges}</p>
                    <div style='background: #f8fafc; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                        <p><strong>📝 项目描述：</strong>{project['description']}</p>
                    </div>
                    <p><strong>🏆 获得荣誉：</strong><span style='color: #d4af37; font-weight: bold;'>{project['achievement']}</span></p>
                    <p><strong>🌍 社会影响：</strong>{project['impact']}</p>
                    <p><strong>📅 完成时间：</strong>{project['date']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-title">📊 成果数据分析</div>', unsafe_allow_html=True)
        
        stats = generate_stats_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 思政元素分布饼图
            ideology_df = pd.DataFrame({
                '思政元素': list(stats['ideology_distribution'].keys()),
                '作品数量': list(stats['ideology_distribution'].values())
            })
            
            fig1 = px.pie(
                ideology_df, 
                values='作品数量', 
                names='思政元素',
                title='🇨🇳 思政元素分布',
                color_discrete_sequence=px.colors.sequential.Reds
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 项目类型分布柱状图
            type_df = pd.DataFrame({
                '项目类型': list(stats['project_types'].keys()),
                '数量': list(stats['project_types'].values())
            })
            
            fig2 = px.bar(
                type_df,
                x='项目类型',
                y='数量',
                title='📊 项目类型分布',
                color='数量',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # 优秀成果展示
        st.markdown("### 🌟 代表性成果")
        
        representative_achievements = [
            {
                "name": "全国大学生计算机设计大赛",
                "awards": ["一等奖3项", "二等奖5项", "三等奖8项"],
                "year": "2024"
            },
            {
                "name": "挑战杯全国大学生课外学术科技作品竞赛",
                "awards": ["特等奖1项", "一等奖2项", "二等奖3项"],
                "year": "2024"
            },
            {
                "name": "中国国际'互联网+'大学生创新创业大赛",
                "awards": ["金奖2项", "银奖4项", "铜奖6项"],
                "year": "2024"
            },
            {
                "name": "全国大学生创新创业训练计划",
                "awards": ["国家级项目8项", "省级项目15项"],
                "year": "2024"
            }
        ]
        
        for achievement in representative_achievements:
            with st.container():
                st.markdown(f"""
                <div class='project-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4>🏅 {achievement['name']}</h4>
                            <p><strong>🎖️ 获奖情况：</strong>{' | '.join(achievement['awards'])}</p>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 1.5rem; color: #dc2626; font-weight: bold;'>{achievement['year']}</div>
                            <div style='color: #6b7280;'>获奖年份</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-title">💡 作品征集</div>', unsafe_allow_html=True)
        
        st.markdown("""
<div class='project-card'>
    <h3>🚀 期待您的精彩作品！</h3>
    <p>我们正在征集更多优秀的图像处理作品，展示您在技术学习和思政教育方面的成果。</p>
    <p><strong>作品要求：</strong></p>
    <ul>
        <li>技术上有创新或实用价值</li>
        <li>体现思政教育内涵</li>
        <li>包含完整的技术文档</li>
        <li>有明确的应用场景</li>
    </ul>
    <button style='background: #dc2626; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 1.1rem;'>📤 提交作品</button>
</div>
""", unsafe_allow_html=True)
            
        
        # 提交表单
        st.markdown("### 📤 在线提交")
        with st.form("project_submission"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("🎯 作品名称", placeholder="请输入作品名称")
                author_name = st.text_input("👤 作者姓名", placeholder="请输入作者姓名")
                contact_info = st.text_input("📞 联系方式", placeholder="请输入手机或邮箱")
                project_type = st.selectbox(
                    "📊 作品类型",
                    ["技术创新类", "社会服务类", "文化传承类", "国家战略类", "教育教学类"]
                )
            
            with col2:
                ideology_elements = st.multiselect(
                    "🇨🇳 思政元素",
                    ["工匠精神", "家国情怀", "创新意识", "责任担当", "科学态度", "团队合作", "文化自信", "追求卓越"]
                )
                tech_stack = st.text_input("💻 技术栈", placeholder="如：Python, OpenCV, TensorFlow等")
                application_field = st.text_input("🌍 应用领域", placeholder="如：医疗、教育、环保等")
            
            project_desc = st.text_area(
                "📝 作品描述",
                placeholder="请详细描述您的作品，包括技术原理、创新点、应用场景、社会价值等...",
                height=150
            )
            
            # 文件上传
            uploaded_files = st.file_uploader(
                "📎 上传作品文件",
                type=['zip', 'rar', 'pdf', 'doc', 'docx', 'ppt', 'pptx'],
                accept_multiple_files=True,
                help="可上传代码文件、文档、演示文稿等"
            )
            
            submitted = st.form_submit_button("🚀 提交作品", use_container_width=True)
            if submitted:
                if project_name and author_name and project_desc:
                    if uploaded_files:
                        file_names = [file.name for file in uploaded_files]
                        st.success(f"🎉 作品提交成功！已上传文件：{', '.join(file_names)}")
                    else:
                        st.success("🎉 作品提交成功！我们将尽快审核您的作品。")
                    st.balloons()
                else:
                    st.error("❌ 请填写作品名称、作者姓名和作品描述等必填信息")

if __name__ == "__main__":
    main()

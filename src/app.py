import streamlit as st
import pandas as pd 
import numpy as np 
from load_data import load_and_process_data, create_nutrient_constraints, load_all_menus, load_sample_file
from evaluation_function import calculate_harmony_matrix, get_top_n_harmony_pairs
from utils import diet_to_dataframe, count_menu_changes
from spea2_optimizer import SPEA2Optimizer
from Diet_class import NutrientConstraints

# Set page config
st.set_page_config(page_title="요양원 식단 최적화 프로그램", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #FAFAFA !important;
        color: black !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 15px 0 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 10px !important;
        border-radius: 8px !important;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .stButton:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    }
    .div[data-testid="element-container"]:has(button:contains("↻")) button {
        background-color: transparent !important;
        border: none !important;
        color: #2d2736 !important;
        padding: 0.rem !important;
        font-weight: bold;
    }
    .button[key="optimize_button"] {
        width: 100% !important;
        background-color: #FF6B88 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 15px 0 !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        align-items: center;
    }
    .menu-item {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .menu-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    }
    .menu-item strong {
        color: #2d2736;
        font-weight: 500;
    }
    .emoji-rank {
    font-size: 1em;
    margin-right: 5px;
    color: #2d2736;
    font-weight: bold;
    }
    .algorithm-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    .algorithm-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #2196F3;
        margin-bottom: 10px;
    }
    .metrics-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        flex: 1;
    }
    [data-testid="stSidebar"] {
            background-color: #e6f4ea;
            box-shadow: 2px 0px 5px rgba(0,0,0,0.1);
            border-radius: 0 10px 10px 0;}
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {color: #4a6d42;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    name = 'sarang'
    diet_db_path = f'../data/sarang_DB/processed_DB/DIET_{name}.xlsx'
    menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
    ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'
    
    diet_db = load_and_process_data(diet_db_path, menu_db_path, ingre_db_path)
    nutrient_constraints = create_nutrient_constraints()
    harmony_matrix, menus, menu_counts, _ = calculate_harmony_matrix(diet_db)
    all_menus = load_all_menus(menu_db_path, ingre_db_path)
    
    return diet_db, nutrient_constraints, harmony_matrix, menus, menu_counts, all_menus

diet_db, default_constraints, harmony_matrix, menus, menu_counts, all_menus = load_data()
default_min_values = default_constraints.min_values
default_max_values = default_constraints.max_values
default_weights = default_constraints.weights
user_min_values, user_max_values, user_weights = {}, {}, {}

def calculate_improvements(initial_fitness, optimized_fitness):
    improvements = []
    for init, opt in zip(initial_fitness, optimized_fitness):
        if init != 0:
            imp = (opt - init) / abs(init) * 100
        else:
            imp = float('inf') if opt > 0 else (0 if opt == 0 else float('-inf'))
        improvements.append(imp)
    return improvements

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'reupload' not in st.session_state:
    st.session_state.reupload = False

# Initialize session state for tracking optimization progress
if 'optimization_running' not in st.session_state:
    st.session_state.optimization_running = False
if 'optimization_complete' not in st.session_state:
    st.session_state.optimization_complete = False
if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = {}
if 'current_algorithm' not in st.session_state:
    st.session_state.current_algorithm = None
if 'total_algorithms' not in st.session_state:
    st.session_state.total_algorithms = 0
if 'progress' not in st.session_state:
    st.session_state.progress = 0

def handle_reupload():
    st.session_state.file_uploaded = False
    st.session_state.reupload = True
    st.session_state.optimization_running = False
    st.session_state.optimization_complete = False
    st.session_state.optimization_results = {}

# 최적화 파라미터 고정
generations = 100
population_size = 50

# 사이드바: 식단 제공 현황
with st.sidebar:
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.image("../assets/logo.png", width=180, use_column_width=True)
    st.markdown("---")
    
    st.subheader('🍽️ 가장 많이 나온 메뉴 조합')
    top_5_pairs = get_top_n_harmony_pairs(harmony_matrix, menus, 5)
    for i, (menu1, menu2, frequency) in enumerate(top_5_pairs, 1):
        emoji_rank = ['①', '②', '③', '④', '⑤'][i-1]
        st.markdown(f"""
        <div class="menu-item" style="font-size: 0.85em;">
            <span class="emoji-rank">{emoji_rank}</span>
            <strong>{menu1}</strong> - <strong>{menu2}</strong>: {frequency}회
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader('🍲 가장 많이 나온 메뉴')
    top_5_menus = menu_counts.most_common(5)
    for i, (menu, occurrences) in enumerate(top_5_menus, 1):
        emoji_rank = ['①', '②', '③', '④', '⑤'][i-1]
        st.markdown(f"""
        <div class="menu-item" style="font-size: 0.85em;">
            <span class="emoji-rank">{emoji_rank}</span>
            <strong>{menu}</strong>: {occurrences}회
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔧 영양소 제한 설정")
    st.markdown('<p style="font-size: 0.9em; color: #666;">슬라이더를 조정하여 각 영양소의 최소값, 최대값, 가중치를 설정하세요.</p>', unsafe_allow_html=True)

    nutrients = list(default_min_values.keys())
    num_nutrients = len(nutrients)

        
    tabs = st.tabs(list(default_min_values.keys()))

    for i, nutrient in enumerate(default_min_values.keys()):
        with tabs[i]:
            st.markdown(f"### {nutrient} 설정")
            
            min_range = 0
            max_range = default_max_values[nutrient] * 2
            
            user_min_values[nutrient] = st.slider(
                "최소값",
                min_value=min_range,
                max_value=max_range,
                value=default_min_values[nutrient],
                step=10,
                help=f"{nutrient}의 일일 최소 권장량을 설정합니다."
            )
            
            user_max_values[nutrient] = st.slider(
                "최대값",
                min_value=user_min_values[nutrient],
                max_value=max_range,
                value=default_max_values[nutrient],
                step=10,
                help=f"{nutrient}의 일일 최대 권장량을 설정합니다."
            )
            
            user_weights[nutrient] = st.slider(
                "가중치",
                min_value=0.1,
                max_value=5.0,
                value=default_weights[nutrient],
                step=0.1,
                help="해당 영양소의 중요도를 설정합니다. 높을수록 최적화 시 더 중요하게 고려됩니다."
            )

        nutrient_constraints = NutrientConstraints(min_values=user_min_values, 
                                        max_values=user_max_values, 
                                        weights=user_weights)
        
    # 설정 저장 버튼
    if st.button("설정 저장", type="primary"):
        nutrient_constraints = NutrientConstraints(
            min_values=user_min_values, 
            max_values=user_max_values, 
            weights=user_weights
        )
        st.success("영양소 제한 설정이 저장되었습니다!")

# Streamlit 앱 시작
st.title('식단 최적화 프로그램')
st.markdown("---")

if not st.session_state.file_uploaded:
    st.subheader('📂 초기 식단 업로드')
    uploaded_file = st.file_uploader("", type="xlsx")
    
    if uploaded_file is not None:
        st.session_state.file_uploaded = True
        st.session_state.uploaded_file = uploaded_file
        st.experimental_rerun()
else:
    uploaded_file = st.session_state.uploaded_file

    col1, col2 = st.columns([15, 1])
    with col1:
        st.subheader('👀 초기 식단')
    with col2:
        st.button("↻", key="reupload_button", on_click=handle_reupload, help="다른 식단 파일을 업로드합니다", type="secondary")

    name = 'sarang'
    menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
    ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'

    weekly_diet = load_and_process_data(uploaded_file, menu_db_path, ingre_db_path)
    
    # SPEA2 옵티마이저 초기화
    optimizer = SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix)
    initial_fitness = optimizer.fitness(diet_db, weekly_diet)
    
    st.dataframe(diet_to_dataframe(weekly_diet, "Initial Diet"), use_container_width=True)
    
    # 초기 비용 계산
    initial_cost = sum(sum(ingredient.price for menu in meal.menus for ingredient in menu.ingredients) for meal in weekly_diet.meals)
    # 영양성분 계산
    days = len(weekly_diet.meals) // 3
    st.subheader("🔎 초기 식단 일일 평균 영양성분")
    
    nutrients_data = []
    for nutrient in nutrient_constraints.min_values.keys():
        total = sum(sum(menu.nutrients[nutrient] for menu in meal.menus) for meal in weekly_diet.meals)
        daily_avg = total / days
        min_val = nutrient_constraints.min_values[nutrient]
        max_val = nutrient_constraints.max_values[nutrient]
        
        # 권장범위 내 여부 확인
        status = "✅" if min_val <= daily_avg <= max_val else "⚠️"
        
        nutrients_data.append({
            "영양소": nutrient,
            "일일평균": f"{daily_avg:.1f}",
            "권장범위": f"{min_val} ~ {max_val}",
            "상태": status
        })
    
    st.table(pd.DataFrame(nutrients_data))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">💰 식단 총 비용</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{:,.0f}원</p>
        </div>
        """.format(initial_cost), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">👏🏻 조화 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{:.2f}점</p>
        </div>
        """.format(initial_fitness[2]), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">💡 다양성 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{:.2f}점</p>
        </div>
        """.format(initial_fitness[3]), unsafe_allow_html=True)
    
# 최적화 실행 버튼
st.markdown("""
    <style>
    .optimize-container .stButton>button {
        background-color: #ff4b4b !important; /* 강조된 빨간색 */
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        border-radius: 12px !important;
        border: 2px solid #ff1a1a !important;
        transition: all 0.3s ease-in-out;
    }
    .optimize-container .stButton>button:hover {
        background-color: #cc0000 !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="optimize-container">', unsafe_allow_html=True)
    st.markdown("---")
    start_button = st.button("🚀 식단 최적화 시작", key="optimize_button")
    st.markdown("</div>", unsafe_allow_html=True)

if start_button:
    if uploaded_file is None:
        st.error("초기 식단 파일을 먼저 업로드해주세요.")
    else:
        st.session_state.optimization_running = True
        st.session_state.optimization_complete = False
        st.session_state.optimization_results = {}
        st.session_state.total_algorithms = 1
        st.session_state.progress = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()

# 최적화 진행 중 표시
if st.session_state.optimization_running and not st.session_state.optimization_complete:
    progress_bar = st.progress(st.session_state.progress)
    status_text = st.empty()
    
    # SPEA2 알고리즘만 초기화
    optimizer = SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix)
    algorithm_name = 'SPEA2'
    
    # 최적화 실행
    st.session_state.current_algorithm = algorithm_name
    st.session_state.progress = 0.5
    progress_bar.progress(st.session_state.progress)
    status_text.text(f"최적화 진행 중...")
    
    pareto_front = optimizer.optimize(diet_db, weekly_diet, generations)
    
    # 개선된 식단 선별
    improved_diets = []
    for optimized_diet in pareto_front:
        optimized_fitness = optimizer.fitness(diet_db, optimized_diet)
        improvements = calculate_improvements(initial_fitness, optimized_fitness)
        if sum(1 for imp in improvements if imp > 0) >= 3:
            improved_diets.append((optimized_diet, optimized_fitness, improvements))
    
    improved_diets = improved_diets[:5]
    st.session_state.optimization_results[algorithm_name] = improved_diets
    
    st.session_state.progress = 1.0
    progress_bar.progress(st.session_state.progress)
       
    st.session_state.optimization_running = False
    st.session_state.optimization_complete = True
    status_text.text("최적화 완료!")
    st.experimental_rerun()

# 최적화 결과 표시
if st.session_state.optimization_complete:
    st.subheader('🏆 최적화 결과')
    
    # SPEA2 알고리즘 결과만 표시
    algorithm = 'SPEA2'
    improved_diets = st.session_state.optimization_results.get(algorithm, [])
    
    if improved_diets:
        diet_tabs = st.tabs([f"제안 식단 {i+1}" for i in range(len(improved_diets))])
        
        for j, (diet_tab, (optimized_diet, optimized_fitness, improvements)) in enumerate(zip(diet_tabs, improved_diets)):
            with diet_tab:
                st.dataframe(diet_to_dataframe(optimized_diet, f"{algorithm} - 제안 식단 {j+1}"), use_container_width=True)
                
                # 총 비용 계산
                optimized_cost = sum(sum(ingredient.price for menu in meal.menus for ingredient in menu.ingredients) for meal in optimized_diet.meals)
                initial_cost = sum(sum(ingredient.price for menu in meal.menus for ingredient in menu.ingredients) for meal in weekly_diet.meals)
                cost_change = ((optimized_cost - initial_cost) / initial_cost) * 100 if initial_cost > 0 else 0
                
                # 영양성분 계산
                days = len(optimized_diet.meals) // 3
                st.subheader("📊 일일 평균 영양성분")
                
                nutrients_data = []
                for nutrient in nutrient_constraints.min_values.keys():
                    total = sum(sum(menu.nutrients[nutrient] for menu in meal.menus) for meal in optimized_diet.meals)
                    daily_avg = total / days
                    min_val = nutrient_constraints.min_values[nutrient]
                    max_val = nutrient_constraints.max_values[nutrient]
                    
                    # 권장범위 내 여부 확인
                    status = "✅" if min_val <= daily_avg <= max_val else "⚠️"
                    
                    nutrients_data.append({
                        "영양소": nutrient,
                        "일일평균": f"{daily_avg:.1f}",
                        "권장범위": f"{min_val} ~ {max_val}",
                        "상태": status
                    })
                
                st.table(pd.DataFrame(nutrients_data))
                
                # 새로운 디자인으로 점수 표시
                col1, col2, col3 = st.columns(3)               

                with col1:
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                        <h3 style="margin: 0; color: #404040; font-size: 18px;">💰 식단 총 비용</h3>
                        <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_cost:,.0f}원 <span style="color: {'red' if cost_change > 0 else 'green'};">({cost_change:+.2f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                        <h3 style="margin: 0; color: #404040; font-size: 18px;">👏🏻 조화 점수</h3>
                        <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[2]:.2f} <span style="color: {'green' if improvements[2] > 0 else 'red'};">({improvements[2]:+.2f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                        <h3 style="margin: 0; color: #404040; font-size: 18px;">💡 다양성 점수</h3>
                        <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[3]:.2f} <span style="color: {'green' if improvements[3] > 0 else 'red'};">({improvements[3]:+.2f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                menu_changes = count_menu_changes(weekly_diet, optimized_diet)
                st.markdown('---')
                st.markdown('#### 📈 카테고리별 메뉴 변경 비율')
                cols = st.columns(4)
                for i, (category, counts) in enumerate(menu_changes.items()):
                    percentage = (counts['changed'] / counts['total']) * 100 if counts['total'] > 0 else 0
                    
                    if percentage > 50:
                        color = "#FF7043"
                    elif percentage > 25:
                        color = "#FFB74D"
                    else:
                        color = "#81C784"
                    
                    bar_width = percentage
                    
                    cols[i % 4].markdown(f"""
                    <div style="margin-bottom: 15px; padding: 12px; border-radius: 8px; background-color: #F5F5F5; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                        <div style="font-weight: bold; margin-bottom: 5px; font-size: 15px;">{category}</div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>{counts['changed']}/{counts['total']}</span>
                            <span style="font-weight: bold;">{percentage:.1f}%</span>
                        </div>
                        <div style="background-color: #E0E0E0; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background-color: {color}; width: {bar_width}%; height: 100%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("3가지 이상 개선된 식단을 찾지 못했습니다. 다른 초기 식단으로 시도해보세요.")

    # 다시 실행 버튼
    if st.button('🔄 새로운 최적화 실행'):
        st.session_state.optimization_running = False
        st.session_state.optimization_complete = False
        st.session_state.optimization_results = {}
        st.experimental_rerun()

st.markdown("---")
st.caption("© 2025 사랑과 선행 요양원 식단 최적화 프로그램. All rights reserved.")
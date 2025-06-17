import streamlit as st
import pandas as pd 
import os
from load_data import load_and_process_data, create_nutrient_constraints, load_all_menus
from evaluation_function import calculate_harmony_matrix, get_top_n_harmony_pairs, validate_weekly_constraints, validate_weekly_constraints_detailed
from spea2_optimizer import SPEA2Optimizer
from Diet_class import NutrientConstraints
import time
from datetime import datetime
from utils import diet_to_dataframe, count_menu_changes

import os
from pathlib import Path

def debug_file_paths():
    """파일 위치 디버깅 정보 출력"""
    current_dir = Path.cwd()
    print(f"현재 작업 디렉토리: {current_dir}")
    
    # 기존 경로들 확인
    paths_to_check = [
        '../data/sarang_DB/processed_DB/DIET_jeongseong.xlsx',
        './data/sarang_DB/processed_DB/DIET_jeongseong.xlsx', 
        'data/sarang_DB/processed_DB/DIET_jeongseong.xlsx',
        'DIET_jeongseong.xlsx'
    ]
    
    print("\n=== 경로 존재 확인 ===")
    for path in paths_to_check:
        exists = os.path.exists(path)
        print(f"{'✓' if exists else '✗'} {path}")
    
    # 프로젝트 구조 출력 (최대 3레벨)
    print("\n=== 프로젝트 구조 ===")
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(str(current_dir), '').count(os.sep)
        if level > 2:  # 3레벨까지만
            continue
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        
        # Excel 파일만 표시
        excel_files = [f for f in files if f.endswith('.xlsx')]
        for file in excel_files:
            print(f"{indent}  📄 {file}")
    
    # 필요한 파일들 검색
    print("\n=== 필요한 파일 검색 ===")
    target_files = ['DIET_jeongseong.xlsx', 'Menu_ingredient_nutrient_jeongseong.xlsx', 'Ingredient_Price_jeongseong.xlsx']
    
    for target in target_files:
        found = list(current_dir.glob(f"**/{target}"))
        if found:
            print(f"✓ {target}: {found[0]}")
        else:
            print(f"✗ {target}: 찾을 수 없음")


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

USERS = {
    "SR01": "test01",
    "SR02": "test02",
    "SR03": "test03",
    "SR04": "test04",
    "SR05": "test05",
    "SR06": "test06",
    "SR07": "test07",
    "SR08": "test08",
    "SR09": "test09",
    "SR010": "test10",
    "SR011": "test11",
    "SR012": "test12",
    "SR013": "test13",
}

# Session state 초기화
if 'weekly_diet' not in st.session_state:
    st.session_state.weekly_diet = None
if 'initial_fitness' not in st.session_state:
    st.session_state.initial_fitness = None
if 'initial_cost' not in st.session_state:
    st.session_state.initial_cost = None
if 'nutrients_data' not in st.session_state:
    st.session_state.nutrients_data = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'optimization_complete' not in st.session_state:
    st.session_state.optimization_complete = False
if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = {}
if 'optimization_start_time' not in st.session_state:
    st.session_state.optimization_start_time = None
if 'optimization_end_time' not in st.session_state:
    st.session_state.optimization_end_time = None
if 'optimization_duration' not in st.session_state:
    st.session_state.optimization_duration = None

# 사용되는 함수 처리
def login_page():
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-title {
            text-align: center;
            color: #2d2736;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:        
        st.markdown('<h2 class="login-title">🔐 시스템 로그인</h2>', unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("사용자명", placeholder="부여받은 아이디를 입력하세요")
            password = st.text_input("비밀번호", type="password", placeholder="부여받은 비밀번호를 입력하세요")
            submit_button = st.form_submit_button("로그인", use_container_width=True)
            if submit_button:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("로그인 성공!")
                    st.experimental_rerun()
                else:
                    st.error("사용자명 또는 비밀번호가 올바르지 않습니다.")
        st.markdown('</div>', unsafe_allow_html=True)
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()
@st.cache_data
def load_data():
    debug_file_paths()

    name = 'jeongseong'
    diet_db_path = f'../data/sarang_DB/processed_DB/DIET_{name}.xlsx'
    menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
    ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'

    print(f"\n=== 시도할 경로 ===")
    print(f"Diet DB: {diet_db_path}")
    print(f"Menu DB: {menu_db_path}") 
    print(f"Ingredient DB: {ingre_db_path}")

    try:
        from load_data import load_and_process_data, create_nutrient_constraints, load_all_menus
        from evaluation_function import calculate_harmony_matrix
        
        diet_db = load_and_process_data(diet_db_path, menu_db_path, ingre_db_path)
        nutrient_constraints = create_nutrient_constraints()
        harmony_matrix, menus, menu_counts, _ = calculate_harmony_matrix(diet_db)
        all_menus = load_all_menus(menu_db_path, ingre_db_path)
        
        return diet_db, nutrient_constraints, harmony_matrix, menus, menu_counts, all_menus
        
    except FileNotFoundError as e:
        print(f"\n❌ 파일 없음: {e}")
        print("위의 디버깅 정보를 확인하여 올바른 경로로 수정하세요.")
        return None, None, None, None, None, None

    diet_db = load_and_process_data(diet_db_path, menu_db_path, ingre_db_path)
    nutrient_constraints = create_nutrient_constraints()
    harmony_matrix, menus, menu_counts, _ = calculate_harmony_matrix(diet_db)
    all_menus = load_all_menus(menu_db_path, ingre_db_path)
    
    return diet_db, nutrient_constraints, harmony_matrix, menus, menu_counts, all_menus
def calculate_improvements(initial_fitness, optimized_fitness):
    improvements = []
    for init, opt in zip(initial_fitness, optimized_fitness):
        if init != 0:
            imp = (opt - init) / abs(init) * 100
        else:
            imp = float('inf') if opt > 0 else (0 if opt == 0 else float('-inf'))
        improvements.append(imp)
    return improvements
def handle_reupload():
    st.session_state.file_uploaded = False
    st.session_state.optimization_complete = False
    st.session_state.optimization_results = {}
    st.session_state.weekly_diet = None
    st.session_state.initial_fitness = None
    st.session_state.initial_cost = None
    st.session_state.nutrients_data = None
    st.session_state.optimization_start_time = None
    st.session_state.optimization_end_time = None
    st.session_state.optimization_duration = None

# 로그인
if not st.session_state.logged_in:
    login_page()
    st.stop()
col1, col2, col3 = st.columns([3, 5, 1])
with col1:
    st.markdown(f'<p style="font-size: 20px; font-weight: normal; margin-top: 4px;">🙋‍♀️ {st.session_state.username}님 환영합니다!</p>', unsafe_allow_html=True)
with col3:
    if st.button("로그아웃", key="logout_btn"):
        logout()

# 사용되는 데이터 불러오기
diet_db, default_constraints, harmony_matrix, menus, menu_counts, all_menus = load_data()

# 사이드바
with st.sidebar:
    col1, col2, col3 = st.columns([1, 5, 1])
    '''with col2:
        st.image("../assets/logo.png", width=180, use_column_width=True)'''

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
    user_min_values = {}
    user_max_values = {}
    user_weights = {}
    tabs = st.tabs(list(default_constraints.min_values.keys()))
    for i, nutrient in enumerate(default_constraints.min_values.keys()):
        with tabs[i]:
            st.markdown(f"### {nutrient} 설정")
            min_range = 0.0
            max_range = float(default_constraints.max_values[nutrient] * 2)
            default_min = float(default_constraints.min_values[nutrient])
            default_max = float(default_constraints.max_values[nutrient])
            default_weight = float(default_constraints.weights[nutrient])
            
            user_min_values[nutrient] = st.slider(
                "최소값",
                min_value=min_range,
                max_value=max_range,
                value=default_min,
                step=10.0,
                help=f"{nutrient}의 일일 최소 권장량을 설정합니다."
            )
            
            user_max_values[nutrient] = st.slider(
                "최대값",
                min_value=user_min_values[nutrient],
                max_value=max_range,
                value=default_max,
                step=10.0,
                help=f"{nutrient}의 일일 최대 권장량을 설정합니다."
            )
            
            user_weights[nutrient] = st.slider(
                "가중치",
                min_value=0.1,
                max_value=5.0,
                value=default_weight,
                step=0.1,
                help="해당 영양소의 중요도를 설정합니다. 높을수록 최적화 시 더 중요하게 고려됩니다."
            )
    nutrient_constraints = NutrientConstraints(
        min_values=user_min_values, 
        max_values=user_max_values, 
        weights=user_weights
    )

# 메인 앱
st.markdown("---")
st.title('식단 최적화 프로그램')
optimizer = SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix)
st.markdown("---")

# 파일 업로드
if not st.session_state.file_uploaded:
    st.subheader('📂 초기 식단 업로드')
    uploaded_file = st.file_uploader("초기 식단 파일을 업로드하세요", type="xlsx", label_visibility="collapsed")
    
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

    # 초기 식단 분석 및 캐시 저장
    if st.session_state.weekly_diet is None:
        name = 'jeongseong'
        menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
        ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'
        st.session_state.weekly_diet = load_and_process_data(uploaded_file, menu_db_path, ingre_db_path)
    
        st.session_state.initial_fitness = optimizer.fitness(diet_db, st.session_state.weekly_diet)
        
        # 초기 식단 분석 (serving_ratio 반영)
        st.session_state.initial_cost = sum(menu.get_adjusted_price() for meal in st.session_state.weekly_diet.meals for menu in meal.menus)
        days = len(st.session_state.weekly_diet.meals) // 3
    
        nutrients_data = []
        for nutrient in nutrient_constraints.min_values.keys():
            total = sum(sum(menu.get_adjusted_nutrients()[nutrient] for menu in meal.menus) for meal in st.session_state.weekly_diet.meals)
            daily_avg = total / days
            min_val = nutrient_constraints.min_values[nutrient]
            max_val = nutrient_constraints.max_values[nutrient]
            
            status = "✅" if min_val <= daily_avg <= max_val else "⚠️"
            
            nutrients_data.append({
                "영양소": nutrient,
                "일일평균": f"{daily_avg:.1f}",
                "권장범위": f"{min_val} ~ {max_val}",
                "상태": status
            })
        
        st.session_state.nutrients_data = nutrients_data

    # 캐시된 데이터 사용하여 초기 식단 분석 결과 재표시
    weekly_diet = st.session_state.weekly_diet
    initial_fitness = st.session_state.initial_fitness
    initial_cost = st.session_state.initial_cost

    st.dataframe(diet_to_dataframe(weekly_diet, "Initial Diet"), use_container_width=True)
    st.subheader("🔎 초기 식단 일일 평균 영양성분")
    st.table(pd.DataFrame(st.session_state.nutrients_data))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">🥗 영양 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{initial_fitness[0]:.2f}점</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">💰 비용 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{initial_fitness[1]:.2f}점</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">👏🏻 조화 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{initial_fitness[2]:.2f}점</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
            <h3 style="margin: 0; color: #404040; font-size: 18px;">💡 다양성 점수</h3>
            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{initial_fitness[3]:.2f}점</p>
        </div>
        """, unsafe_allow_html=True)

    # 최적화 시작 
    st.markdown("---")
    if st.button("🚀 식단 최적화 시작", key="optimize_button"):
        # 시작 시간 기록
        st.session_state.optimization_start_time = datetime.now()
        start_time_for_duration = time.time()

        with st.spinner('SPEA2 알고리즘 최적화 진행 중...'):
            pareto_front = optimizer.optimize(diet_db, weekly_diet, 10)
            # 완료 시간 기록
            st.session_state.optimization_end_time = datetime.now()
            optimization_duration = time.time() - start_time_for_duration
            st.session_state.optimization_duration = optimization_duration

            # 개선된 식단 찾기
            constraint_satisfied_diets = []
            constraint_violated_diets = []

            for optimized_diet in pareto_front:
                optimized_fitness = optimizer.fitness(diet_db, optimized_diet)
                improvements = calculate_improvements(initial_fitness, optimized_fitness)
                improved_count = sum(1 for imp in improvements if imp > 0)
                
                if improved_count >= 3:
                    is_valid = validate_weekly_constraints(optimized_diet, nutrient_constraints)
                    diet_info = (optimized_diet, optimized_fitness, improvements)
                    
                    if is_valid:
                        constraint_satisfied_diets.append(diet_info)
                    else:
                        constraint_violated_diets.append(diet_info)
            
            improved_diets = constraint_satisfied_diets[:5]
            if len(improved_diets) < 5:
                needed = 5 - len(improved_diets)
                improved_diets.extend(constraint_violated_diets[:needed])
            
            st.session_state.optimization_results = improved_diets
            st.session_state.optimization_complete = True

    # 최적화 결과 표시
    if st.session_state.optimization_complete and st.session_state.optimization_results:
        st.subheader('🏆 SPEA2 최적화 결과')
        improved_diets = st.session_state.optimization_results
        if improved_diets:
            diet_tabs = st.tabs([f"제안 식단 {i+1}" for i in range(len(improved_diets))])
            
            for j, (diet_tab, (optimized_diet, optimized_fitness, improvements)) in enumerate(zip(diet_tabs, improved_diets)):
                with diet_tab:
                    st.dataframe(diet_to_dataframe(optimized_diet, f"SPEA2 - 제안 식단 {j+1}"), use_container_width=True)
                    
                    # 영양성분 분석
                    days = len(optimized_diet.meals) // 3
                    st.subheader("📊 일일 평균 영양성분")
                    nutrients_data = []
                    for nutrient in nutrient_constraints.min_values.keys():
                        total = sum(sum(menu.get_adjusted_nutrients()[nutrient] for menu in meal.menus) for meal in optimized_diet.meals)
                        daily_avg = total / days
                        min_val = nutrient_constraints.min_values[nutrient]
                        max_val = nutrient_constraints.max_values[nutrient]
                        
                        status = "✅" if min_val <= daily_avg <= max_val else "⚠️"
                        
                        nutrients_data.append({
                            "영양소": nutrient,
                            "일일평균": f"{daily_avg:.1f}",
                            "권장범위": f"{min_val} ~ {max_val}",
                            "상태": status
                        })
                    st.table(pd.DataFrame(nutrients_data))
                    
                    # 비용 계산 (serving_ratio 반영)
                    optimized_cost = sum(menu.get_adjusted_price() for meal in optimized_diet.meals for menu in meal.menus)
                    cost_change = ((optimized_cost - initial_cost) / initial_cost) * 100 if initial_cost > 0 else 0
                    
                    # 개선율 표시
                    col1, col2, col3, col4 = st.columns(4)                    
                    improvement_colors = ['green' if imp > 0 else 'red' for imp in improvements]
                    with col1:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                            <h3 style="margin: 0; color: #404040; font-size: 18px;">🥗 영양 점수</h3>
                            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[0]:.2f} <span style="color: {improvement_colors[0]};">({improvements[0]:+.2f}%)</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                            <h3 style="margin: 0; color: #404040; font-size: 18px;">💰 비용 점수</h3>
                            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[1]:.2f} <span style="color: {improvement_colors[1]};">({improvements[1]:+.2f}%)</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                            <h3 style="margin: 0; color: #404040; font-size: 18px;">👏🏻 조화 점수</h3>
                            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[2]:.2f} <span style="color: {improvement_colors[2]};">({improvements[2]:+.2f}%)</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                        <div style="padding: 10px; border-radius: 10px; background-color: #FAFAFA;">
                            <h3 style="margin: 0; color: #404040; font-size: 18px;">💡 다양성 점수</h3>
                            <p style="font-size: 20px; font-weight: bold; margin: 0px 0 0 0;">{optimized_fitness[3]:.2f} <span style="color: {improvement_colors[3]};">({improvements[3]:+.2f}%)</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown(f"**총 식재료 비용**: {optimized_cost:,.0f}원 ({cost_change:+.2f}%)")
                    
                    # 메뉴 변경률 표시
                    menu_changes = count_menu_changes(weekly_diet, optimized_diet)
                    st.markdown('---')
                    st.markdown('#### 📈 카테고리별 메뉴 변경 비율')
                    cols = st.columns(5)
                    for i, (category, counts) in enumerate(menu_changes.items()):
                        percentage = (counts['changed'] / counts['total']) * 100 if counts['total'] > 0 else 0
                        if percentage > 50:
                            color = "#FF7043"
                        elif percentage > 25:
                            color = "#FFB74D"
                        else:
                            color = "#81C784"
                        bar_width = percentage
                        cols[i % 5].markdown(f"""
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
                    
            if (hasattr(st.session_state, 'optimization_start_time') and 
                hasattr(st.session_state, 'optimization_end_time') and 
                hasattr(st.session_state, 'optimization_duration') and
                st.session_state.optimization_start_time is not None and
                st.session_state.optimization_end_time is not None and
                st.session_state.optimization_duration is not None):
                
                st.markdown("---")
                st.subheader("📋 최적화 요약 정보")
                
                all_improvements = [improvements for _, _, improvements in improved_diets]
                avg_improvements = [sum(imp[i] for imp in all_improvements) / len(all_improvements) for i in range(4)]
                
                all_change_rates = []
                for diet, _, _ in improved_diets:
                    menu_changes = count_menu_changes(weekly_diet, diet)
                    total_menus = sum(counts['total'] for counts in menu_changes.values())
                    total_changed = sum(counts['changed'] for counts in menu_changes.values())
                    change_rate = (total_changed / total_menus * 100) if total_menus > 0 else 0
                    all_change_rates.append(change_rate)
                overall_change_rate = sum(all_change_rates) / len(all_change_rates) if all_change_rates else 0
                
                summary_data = {
                    "사용자": [st.session_state.username],
                    "시작시간": [st.session_state.optimization_start_time.strftime("%Y-%m-%d %H:%M:%S")],
                    "완료시간": [st.session_state.optimization_end_time.strftime("%Y-%m-%d %H:%M:%S")],
                    "소요시간(초)": [f"{st.session_state.optimization_duration:.1f}초"],
                    "개선율": [f"영양 점수: {avg_improvements[0]:+.2f}% | 비용 점수: {avg_improvements[1]:+.2f}% | 조화 점수: {avg_improvements[2]:+.2f}% | 다양성 점수: {avg_improvements[3]:+.2f}%"]}
                
                summary_df = pd.DataFrame(summary_data).set_index("사용자")
                st.markdown("""
                <style>
                .summary-table {
                    border-radius: 10px;
                }
                </style>
                """, unsafe_allow_html=True)
                st.markdown('<div class="summary-table">', unsafe_allow_html=True)
                st.dataframe(summary_df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("최적화 시간 정보가 누락되었습니다.")

        else:
            st.warning("3가지 이상 개선된 식단을 찾지 못했습니다. 다른 초기 식단으로 시도해보세요.")

        if st.button('🔄 새로운 최적화 실행'):
            st.session_state.optimization_complete = False
            st.session_state.optimization_results = {}
            st.experimental_rerun()

st.markdown("---")
st.caption("© 2025 사랑과 선행 요양원 식단 최적화 프로그램. All rights reserved.")

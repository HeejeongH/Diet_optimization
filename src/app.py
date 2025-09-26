import streamlit as st
import pandas as pd
import os
import tempfile
from load_data import load_and_process_data, create_nutrient_constraints, load_all_menus
from evaluation_function import calculate_harmony_matrix, get_top_n_harmony_pairs, validate_weekly_constraints, validate_weekly_constraints_detailed, calculate_actual_cost
from spea2_optimizer import SPEA2Optimizer
from Diet_class import NutrientConstraints, set_servings, get_servings
from diet_converter import convert_diet_format
from food_mapper import apply_food_mapping
import time
from datetime import datetime
from utils import diet_to_dataframe, count_menu_changes
import random

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
    name = 'jeongseong'
    diet_db_path = f'../data/sarang_DB/processed_DB/DIET_{name}.xlsx'
    menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
    ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'

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
    # 업로드 파일 관련 상태 초기화
    if 'uploaded_file' in st.session_state:
        del st.session_state.uploaded_file
    if 'random_diet' in st.session_state:
        del st.session_state.random_diet

def generate_random_weekly_diet():
    """랜덤 주간 식단 생성"""
    diet_db_path = '../data/sarang_DB/processed_DB/DIET_jeongseong.xlsx'
    df = pd.read_excel(diet_db_path)

    unique_days = df['Day'].unique()
    selected_days = random.sample(list(unique_days), 7)
    selected_days.sort()

    selected_meals = df[df['Day'].isin(selected_days)].copy()

    day_mapping = {day: i+1 for i, day in enumerate(selected_days)}
    selected_meals['Day'] = selected_meals['Day'].map(day_mapping)

    meal_order = {'Breakfast': 1, 'Lunch': 2, 'Dinner': 3}
    selected_meals['sort_order'] = selected_meals['MealType'].map(meal_order)
    selected_meals = selected_meals.sort_values(['Day', 'sort_order'])
    selected_meals = selected_meals.drop('sort_order', axis=1)

    return selected_meals

def process_mapped_diet_data(file_path):
    """
    매핑된 식단 데이터를 시스템에서 사용할 수 있는 표준 형태로 변환
    """
    try:
        df = pd.read_excel(file_path)

        # 매핑된 파일인지 확인 (Mapped_Menus 컬럼 존재)
        if 'Mapped_Menus' in df.columns:
            # Mapped_Menus를 Menus로 변경하여 표준 형태로 만들기
            standard_df = df[['Day', 'MealType', 'Mapped_Menus']].copy()
            standard_df.rename(columns={'Mapped_Menus': 'Menus'}, inplace=True)

            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='_standard.xlsx') as tmp_file:
                standard_file_path = tmp_file.name

            standard_df.to_excel(standard_file_path, index=False)
            return standard_file_path
        else:
            # 이미 표준 형태인 경우 그대로 반환
            return file_path

    except Exception as e:
        st.error(f"❌ 매핑된 데이터 처리 중 오류 발생: {str(e)}")
        return file_path

def detect_and_convert_diet_format(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            temp_input_path = tmp_file.name

        df = pd.read_excel(temp_input_path)

        # Weekly_diet_ex.xlsx 형태인지 확인 (Day, MealType, Menus 컬럼 존재)
        expected_columns = ['Day', 'MealType', 'Menus']
        if all(col in df.columns for col in expected_columns):
            st.success("✅ 올바른 형태의 식단 파일입니다.")

            # 매핑 과정 적용
            mapping_file_path = 'food_mapping.csv'

            with tempfile.NamedTemporaryFile(delete=False, suffix='_mapped.xlsx') as tmp_mapped:
                temp_mapped_path = tmp_mapped.name

            try:
                apply_food_mapping(temp_input_path, mapping_file_path, temp_mapped_path)

                # 원본 임시 파일 삭제
                os.unlink(temp_input_path)

                st.success("✅ 음식 매핑이 완료되었습니다.")

                # 매핑된 데이터를 표준 형태로 변환
                final_path = process_mapped_diet_data(temp_mapped_path)

                # 매핑 파일 삭제 (표준 형태로 변환된 파일 사용)
                if final_path != temp_mapped_path:
                    os.unlink(temp_mapped_path)

                return final_path

            except Exception as e:
                st.warning(f"⚠️ 음식 매핑 중 오류 발생: {str(e)}")
                return temp_input_path

        # 식단표 예시.xlsx 형태인지 확인 (주간 식단표 형태)
        if '주간 식단표' in df.columns or len(df.columns) >= 7:

            with tempfile.NamedTemporaryFile(delete=False, suffix='_converted.xlsx') as tmp_converted:
                temp_output_path = tmp_converted.name

            # 형태 변환
            convert_diet_format(temp_input_path, temp_output_path)

            # 원본 임시 파일 삭제
            os.unlink(temp_input_path)

            st.success("✅ 파일 형태 변환이 완료되었습니다.")

            # 매핑 과정 적용
            mapping_file_path = 'food_mapping.csv'

            with tempfile.NamedTemporaryFile(delete=False, suffix='_mapped.xlsx') as tmp_mapped:
                temp_mapped_path = tmp_mapped.name

            try:
                apply_food_mapping(temp_output_path, mapping_file_path, temp_mapped_path)

                # 변환된 임시 파일 삭제
                os.unlink(temp_output_path)

                st.success("✅ 음식 매핑이 완료되었습니다.")

                # 매핑된 데이터를 표준 형태로 변환
                final_path = process_mapped_diet_data(temp_mapped_path)

                # 매핑 파일 삭제 (표준 형태로 변환된 파일 사용)
                if final_path != temp_mapped_path:
                    os.unlink(temp_mapped_path)

                return final_path

            except Exception as e:
                st.warning(f"⚠️ 음식 매핑 중 오류 발생: {str(e)}")
                return temp_output_path
        else:
            st.error("❌ 지원되지 않는 파일 형태입니다. Weekly Diet 형태나 주간 식단표 형태의 파일을 업로드해주세요.")
            os.unlink(temp_input_path)
            return None

    except Exception as e:
        st.error(f"❌ 파일 처리 중 오류가 발생했습니다: {str(e)}")
        if 'temp_input_path' in locals():
            os.unlink(temp_input_path)
        return None

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
    st.subheader("🍽️ 서빙 설정")
    servings = st.number_input(
        "서빙 인원수",
        min_value=1,
        max_value=200,
        value=55,
        step=1,
        help="식단을 준비할 인원수를 설정합니다. 비용 계산에 반영됩니다."
    )
    set_servings(servings)
    
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

# 파일 업로드 또는 랜덤 생성
if not st.session_state.file_uploaded:
    st.subheader('📂 초기 식단 설정')
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("초기 식단 파일을 업로드하세요", type="xlsx")
    with col2:
        if st.button("🎲 랜덤 식단 생성", use_container_width=True):
            st.session_state.file_uploaded = True
            st.session_state.uploaded_file = None
            st.session_state.random_diet = True
            st.experimental_rerun()
    
    if uploaded_file is not None:
        st.session_state.file_uploaded = True
        st.session_state.uploaded_file = uploaded_file
        st.session_state.random_diet = False
        st.experimental_rerun()
else:
    col1, col2 = st.columns([15, 1])
    with col1:
        if hasattr(st.session_state, 'random_diet') and st.session_state.random_diet:
            st.subheader('🎲 랜덤 생성된 초기 식단')
        else:
            st.subheader('👀 업로드된 초기 식단')
    with col2:
        st.button("↻", key="reupload_button", on_click=handle_reupload, help="다른 식단을 설정합니다", type="secondary")

    # 초기 식단 분석 및 캐시 저장
    if st.session_state.weekly_diet is None:
        name = 'jeongseong'
        menu_db_path = f'../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
        ingre_db_path = f'../data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'
        
        if hasattr(st.session_state, 'random_diet') and st.session_state.random_diet:
            # 랜덤 식단 생성
            random_diet_df = generate_random_weekly_diet()
            # 임시 파일로 저장 후 로드
            temp_file = "temp_random_diet.xlsx"
            random_diet_df.to_excel(temp_file, index=False)
            st.session_state.weekly_diet = load_and_process_data(temp_file, menu_db_path, ingre_db_path)
            os.remove(temp_file)  # 임시 파일 삭제
        else:
            # 업로드된 파일 사용 (자동 변환 포함)
            uploaded_file = st.session_state.uploaded_file

            # 파일 형태 감지 및 변환
            converted_file_path = detect_and_convert_diet_format(uploaded_file)

            if converted_file_path:
                try:
                    # 변환된 파일 내용 확인 (디버깅용)
                    debug_df = pd.read_excel(converted_file_path)

                    # 표준 출력을 캡쳐하여 누락 메뉴 확인
                    import io
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = captured_output = io.StringIO()

                    try:
                        st.session_state.weekly_diet = load_and_process_data(converted_file_path, menu_db_path, ingre_db_path)
                    finally:
                        sys.stdout = old_stdout

                    # 캡쳐된 출력에서 매핑 및 누락 메뉴 정보 표시
                    captured_text = captured_output.getvalue()
                    if "Menu mappings" in captured_text:
                        mapping_lines = [line for line in captured_text.split('\n') if "Menu mappings" in line]

                    if "Missing menus" in captured_text:
                        missing_lines = [line for line in captured_text.split('\n') if "Missing menus" in line]
                        st.warning(f"⚠️ 데이터베이스에서 찾을 수 없어 제외된 메뉴들:\n" + "\n".join(missing_lines[:10]))

                    # 로드된 데이터 확인 (디버깅용)
                    if st.session_state.weekly_diet and st.session_state.weekly_diet.meals:
                        first_meal_menus = [menu.name for menu in st.session_state.weekly_diet.meals[0].menus]

                    # 임시 파일 정리
                    os.unlink(converted_file_path)
                except Exception as e:
                    st.error(f"❌ 식단 데이터 로드 중 오류가 발생했습니다: {str(e)}")
                    if os.path.exists(converted_file_path):
                        os.unlink(converted_file_path)
                    st.stop()
            else:
                st.error("❌ 파일을 처리할 수 없습니다. 다른 파일을 업로드해주세요.")
                st.stop()
    
        st.session_state.initial_fitness = optimizer.fitness(diet_db, st.session_state.weekly_diet)
        
        # 초기 식단 비용 계산 (serving_ratio와 실제 구매 비용 반영)
        current_servings = get_servings()
        st.session_state.initial_cost = calculate_actual_cost(st.session_state.weekly_diet, current_servings)
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
    
    # 서빙 정보 표시
    st.info(f"현재 설정: **{get_servings()}인분**으로 계산됨 (사이드바에서 변경 가능)")
    
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
    
    st.markdown(f"**총 식재료 비용**: {initial_cost:,.0f}원")

    # 최적화 시작 
    st.markdown("---")
    
    # 세대수 설정
    generations = st.slider("최적화 세대수 설정", min_value=50, max_value=500, value=200, step=50, 
                           help="세대수가 높을수록 더 좋은 결과를 얻을 수 있지만 시간이 더 오래 걸립니다.")
    
    if st.button("🚀 SPEA2 식단 최적화 시작", key="optimize_button"):
        # 시작 시간 기록
        st.session_state.optimization_start_time = datetime.now()
        start_time_for_duration = time.time()

        with st.spinner(f'SPEA2 알고리즘 최적화 진행 중... ({generations}세대)'):
            pareto_front = optimizer.optimize(diet_db, weekly_diet, generations)
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
                    
                    # 비용 계산 (실제 구매 비용으로 계산)
                    current_servings = get_servings()
                    optimized_cost = calculate_actual_cost(optimized_diet, current_servings)
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
                    
                    # 제약조건 만족 여부 표시
                    is_valid, violations = validate_weekly_constraints_detailed(optimized_diet, nutrient_constraints)
                    if is_valid:
                        st.success("✅ 모든 영양소 제약조건을 만족합니다!")
                    else:
                        st.warning(f"⚠️ 제약조건 위반: {', '.join(violations)}")
                    
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
                    
                    # 서빙 비율 정보
                    avg_serving_ratio = sum(menu.serving_ratio for meal in optimized_diet.meals for menu in meal.menus) / sum(len(meal.menus) for meal in optimized_diet.meals)
                    st.markdown(f"**평균 서빙 비율**: {avg_serving_ratio:.2f}")
                    
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
                    "알고리즘": ["SPEA2"],
                    "세대수": [generations],
                    "시작시간": [st.session_state.optimization_start_time.strftime("%Y-%m-%d %H:%M:%S")],
                    "완료시간": [st.session_state.optimization_end_time.strftime("%Y-%m-%d %H:%M:%S")],
                    "소요시간(초)": [f"{st.session_state.optimization_duration:.1f}초"],
                    "개선된 해 개수": [len(improved_diets)],
                    "평균 개선율": [f"영양: {avg_improvements[0]:+.1f}% | 비용: {avg_improvements[1]:+.1f}% | 조화: {avg_improvements[2]:+.1f}% | 다양성: {avg_improvements[3]:+.1f}%"],
                    "평균 메뉴 변경률": [f"{overall_change_rate:.1f}%"]
                }
                
                summary_df = pd.DataFrame(summary_data).set_index("사용자")
                st.dataframe(summary_df, use_container_width=True)
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

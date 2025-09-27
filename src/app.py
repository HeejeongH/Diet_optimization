import streamlit as st
import pandas as pd
import io
import sys
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
import io
from datetime import datetime
import os
from github import Github, Auth
import base64

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
    diet_db_path = f'./data/sarang_DB/processed_DB/DIET_{name}.xlsx'
    menu_db_path = f'./data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
    ingre_db_path = f'./data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'

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
    if 'uploaded_file' in st.session_state:
        del st.session_state.uploaded_file
    if 'random_diet' in st.session_state:
        del st.session_state.random_diet

def generate_random_weekly_diet():
    diet_db_path = './data/sarang_DB/processed_DB/DIET_jeongseong.xlsx'
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
    try:
        df = pd.read_excel(file_path)

        if 'Mapped_Menus' in df.columns:
            standard_df = df[['Day', 'MealType', 'Mapped_Menus']].copy()
            standard_df.rename(columns={'Mapped_Menus': 'Menus'}, inplace=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix='_standard.xlsx') as tmp_file:
                standard_file_path = tmp_file.name

            standard_df.to_excel(standard_file_path, index=False)
            return standard_file_path
        else:
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

        expected_columns = ['Day', 'MealType', 'Menus']
        if all(col in df.columns for col in expected_columns):
            mapping_file_path = './src/food_mapping.csv'

            with tempfile.NamedTemporaryFile(delete=False, suffix='_mapped.xlsx') as tmp_mapped:
                temp_mapped_path = tmp_mapped.name

            apply_food_mapping(temp_input_path, mapping_file_path, temp_mapped_path)
            os.unlink(temp_input_path)

            final_path = process_mapped_diet_data(temp_mapped_path)
            if final_path != temp_mapped_path:
                os.unlink(temp_mapped_path)

            return final_path

        if '주간 식단표' in df.columns or len(df.columns) >= 7:

            with tempfile.NamedTemporaryFile(delete=False, suffix='_converted.xlsx') as tmp_converted:
                temp_output_path = tmp_converted.name

            convert_diet_format(temp_input_path, temp_output_path)
            os.unlink(temp_input_path)

            mapping_file_path = './src/food_mapping.csv'

            with tempfile.NamedTemporaryFile(delete=False, suffix='_mapped.xlsx') as tmp_mapped:
                temp_mapped_path = tmp_mapped.name

            apply_food_mapping(temp_output_path, mapping_file_path, temp_mapped_path)
            os.unlink(temp_output_path)
            final_path = process_mapped_diet_data(temp_mapped_path)
            if final_path != temp_mapped_path:
                os.unlink(temp_mapped_path)
            return final_path

        else:
            st.error("❌ 지원되지 않는 파일 형태입니다. Weekly Diet 형태나 주간 식단표 형태의 파일을 업로드해주세요.")
            os.unlink(temp_input_path)
            return None

    except Exception as e:
        st.error(f"❌ 파일 처리 중 오류가 발생했습니다: {str(e)}")
        if 'temp_input_path' in locals():
            os.unlink(temp_input_path)
        return None

def create_weekly_diet_table(weekly_diet, title="주간 식단표", return_menu_counts=False):
    from datetime import datetime, timedelta

    days_data = {}
    meal_types = ['Breakfast', 'Lunch', 'Dinner']
    korean_meals = ['아침', '점심', '저녁']

    for day in range(1, 8):
        days_data[day] = {meal: [] for meal in meal_types}

    for i, meal in enumerate(weekly_diet.meals):
        day = (i // 3) + 1
        meal_type = meal_types[i % 3]

        if day <= 7:  # 7일까지만
            menu_names = [menu.name for menu in meal.menus]
            days_data[day][meal_type] = menu_names

    max_menus = {}
    for meal_type in meal_types:
        max_count = 0
        for day in range(1, 8):
            count = len(days_data[day][meal_type])
            if count > max_count:
                max_count = count
        max_menus[meal_type] = max_count

    today = datetime.now().date()
    weekdays = []
    for i in range(7):
        date = today + timedelta(days=i)
        weekdays.append(date)

    table_data = []

    header_row = ['구분'] + weekdays
    table_data.append(header_row)

    for meal_idx, (meal_type, korean_meal) in enumerate(zip(meal_types, korean_meals)):
        max_menu_count = max_menus[meal_type]

        for menu_idx in range(max_menu_count):
            if menu_idx == 0:
                row = [korean_meal]
            else:
                row = ['']

            for day in range(1, 8):
                menus = days_data[day][meal_type]
                if menu_idx < len(menus):
                    row.append(menus[menu_idx])
                else:
                    row.append('')

            table_data.append(row)

    if return_menu_counts:
        return pd.DataFrame(table_data), max_menus
    else:
        return pd.DataFrame(table_data)

def upload_to_github(file_buffer, filename, github_token=None, repo_name="diet-optimization-results"):
    if not github_token:
        github_token = st.secrets.get("GITHUB_TOKEN")

    if not github_token:
        return {
            'success': False,
            'error': 'GitHub 토큰이 설정되지 않았습니다. config/github_token.txt 파일을 생성하거나 Streamlit secrets에 GITHUB_TOKEN을 설정해주세요.'
        }

    try:
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        file_content = base64.b64encode(file_buffer.getvalue()).decode()

        today = datetime.now().strftime("%Y-%m-%d")
        file_path = f"results/{today}/{filename}"

        try:
            existing_file = repo.get_contents(file_path)
            repo.update_file(
                file_path,
                f"Update {filename}",
                file_content,
                existing_file.sha
            )
        except:
            repo.create_file(
                file_path,
                f"Add {filename}",
                file_content
            )

        return {
            'success': True,
            'repo_url': repo.html_url,
            'file_path': file_path
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'GitHub 업로드 실패: {str(e)}'
        }


def export_results_to_excel():
    if not st.session_state.optimization_complete or not st.session_state.optimization_results:
        return None

    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:

        # 스타일 정의
        header_font = Font(bold=True, size=12, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_alignment = Alignment(horizontal='center', vertical='center')

        # 1. 요약 정보 시트
        improved_diets = st.session_state.optimization_results
        all_improvements = [improvements for _, _, improvements in improved_diets]
        avg_improvements = [sum(imp[i] for imp in all_improvements) / len(all_improvements) for i in range(4)]

        all_change_rates = []
        for diet, _, _ in improved_diets:
            menu_changes = count_menu_changes(st.session_state.weekly_diet, diet)
            total_menus = sum(counts['total'] for counts in menu_changes.values())
            total_changed = sum(counts['changed'] for counts in menu_changes.values())
            change_rate = (total_changed / total_menus * 100) if total_menus > 0 else 0
            all_change_rates.append(change_rate)
        overall_change_rate = sum(all_change_rates) / len(all_change_rates) if all_change_rates else 0

        summary_data = {
            "항목": ["사용자", "알고리즘", "세대수", "시작시간", "완료시간", "소요시간", "개선된 해 개수", "평균 영양 개선율(%)", "평균 비용 개선율(%)", "평균 조화 개선율(%)", "평균 다양성 개선율(%)", "평균 메뉴 변경률(%)"],
            "값": [
                st.session_state.username,
                "SPEA2",
                getattr(st.session_state, 'generations', 'N/A'),
                st.session_state.optimization_start_time.strftime("%Y-%m-%d %H:%M:%S") if st.session_state.optimization_start_time else 'N/A',
                st.session_state.optimization_end_time.strftime("%Y-%m-%d %H:%M:%S") if st.session_state.optimization_end_time else 'N/A',
                f"{st.session_state.optimization_duration:.1f}초" if st.session_state.optimization_duration else 'N/A',
                len(improved_diets),
                f"{avg_improvements[0]:.2f}" if len(avg_improvements) > 0 else 'N/A',
                f"{avg_improvements[1]:.2f}" if len(avg_improvements) > 1 else 'N/A',
                f"{avg_improvements[2]:.2f}" if len(avg_improvements) > 2 else 'N/A',
                f"{avg_improvements[3]:.2f}" if len(avg_improvements) > 3 else 'N/A',
                f"{overall_change_rate:.1f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='📊 최적화 요약', index=False)

        ws_summary = writer.sheets['📊 최적화 요약']
        ws_summary.column_dimensions['A'].width = 20
        ws_summary.column_dimensions['B'].width = 25

        for cell in ws_summary[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment
            cell.border = border

        for row in ws_summary.iter_rows(min_row=2, max_row=ws_summary.max_row):
            for cell in row:
                cell.border = border
                cell.alignment = center_alignment

        # 2. 각 제안 식단 시트
        def style_table(ws, start_row, table_length, max_col=8):
            end_row = start_row + table_length + 1
            
            # 헤더 스타일링
            for col_idx in range(1, max_col + 1):
                cell = ws.cell(row=start_row, column=col_idx)
                cell.font = Font(bold=True, size=12, color="FFFFFF")
                cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = border
            
            # 데이터 행 스타일링
            for row_idx in range(start_row + 1, end_row):
                for col_idx in range(1, max_col + 1):
                    cell = ws.cell(row=row_idx, column=col_idx)
                    cell.border = border
                    cell.alignment = Alignment(horizontal='center', vertical='center')

        start_row = 1
        initial_nutrients_start = 22
        initial_cost_start = 30
        initial_perform_start = 36

        for j, (optimized_diet, optimized_fitness, improvements) in enumerate(improved_diets):
            days = len(optimized_diet.meals) // 3
            current_servings = get_servings()
            optimized_cost = calculate_actual_cost(optimized_diet, current_servings)
            initial_cost = st.session_state.initial_cost
            cost_change = initial_cost - optimized_cost
            menu_changes = count_menu_changes(st.session_state.weekly_diet, optimized_diet)

            start_row = 1
            sheet_name = f'💡 제안식단 {j+1}'

            ## 1. 식단 섹션
            weekly_diet_table, max_menus_info = create_weekly_diet_table(optimized_diet, f"제안 식단 {j+1}", return_menu_counts=True)

            weekly_diet_table.to_excel(writer, 
                                       sheet_name=sheet_name, 
                                       startrow = start_row, 
                                       index=False, 
                                       header=False)

            ws = writer.sheets[sheet_name]
            ws[f'A{start_row}'] = f"🍽️ 최적화된 주간 식단표 - 제안 식단 {j+1}"
            ws[f'A{start_row}'].font = Font(bold=True, size=14, color="2F5597")

            ## 2. 영양성분 섹션
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
            nutrients_df = pd.DataFrame(nutrients_data)

            nutrients_df.to_excel(writer, 
                                  sheet_name=sheet_name, 
                                  startrow=initial_nutrients_start, 
                                  index=False)

            ws[f'A{initial_nutrients_start}'] = "🍎 영양성분 분석"
            ws[f'A{initial_nutrients_start}'].font = Font(bold=True, size=14, color="2F5597")

            ## 3. 비용 정보 섹션
            cost_data = {
                "항목": ["총 식재료 비용", "1인당 비용", "1끼당 비용"],
                "금액": [
                    f"{optimized_cost:,.0f}원",
                    f"{optimized_cost/current_servings:,.0f}원" if current_servings > 0 else "N/A",
                    f"{optimized_cost/(current_servings*21):,.0f}원" if current_servings > 0 else "N/A"
                ]
            }
            cost_df = pd.DataFrame(cost_data)

            cost_df.to_excel(writer, 
                             sheet_name=sheet_name, 
                             startrow=initial_cost_start, 
                             index=False)
            
            ws[f'A{initial_cost_start}'] = "💰 총 식재료 비용 정보"
            ws[f'A{initial_cost_start}'].font = Font(bold=True, size=14, color="2F5597")

            ## 4. 성능 지표 비교 섹션 (마지막)
            performance_data = {
                "지표": ["영양 점수", "비용 점수", "조화 점수", "다양성 점수", "총 식재료 비용(원)"],
                "초기값": [
                    f"{st.session_state.initial_fitness[0]:.2f}",
                    f"{st.session_state.initial_fitness[1]:.2f}",
                    f"{st.session_state.initial_fitness[2]:.2f}",
                    f"{st.session_state.initial_fitness[3]:.2f}",
                    f"{initial_cost:,.0f}",
                ],
                "최적화값": [
                    f"{optimized_fitness[0]:.2f}",
                    f"{optimized_fitness[1]:.2f}",
                    f"{optimized_fitness[2]:.2f}",
                    f"{optimized_fitness[3]:.2f}",
                    f"{optimized_cost:,.0f}",
                ],
                "개선율(%)": [
                    f"{improvements[0]:.2f}",
                    f"{improvements[1]:.2f}",
                    f"{improvements[2]:.2f}",
                    f"{improvements[3]:.2f}",
                    f"{cost_change:,.0f}원",
                ]
            }
            performance_df = pd.DataFrame(performance_data)

            performance_df.to_excel(writer, 
                                    sheet_name=sheet_name, 
                                    startrow=initial_perform_start, 
                                    index=False)

            ws[f'A{initial_perform_start}'] = "📈 기존 식단과의 성능 비교"
            ws[f'A{initial_perform_start}'].font = Font(bold=True, size=14, color="2F5597")

            ## 열 너비 조정
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 25)
                ws.column_dimensions[column].width = adjusted_width

            ## 식단표 스타일링 및 셀 병합
            ws.merge_cells('A1:E1')
            ws.merge_cells(f'A{initial_nutrients_start}:D{initial_nutrients_start}')
            ws.merge_cells(f'A{initial_cost_start}:B{initial_cost_start}')
            ws.merge_cells(f'A{initial_perform_start}:D{initial_perform_start}')

            diet_start_row = 3
            current_row = diet_start_row

            meal_types = ['Breakfast', 'Lunch', 'Dinner']
            korean_meals = ['아침', '점심', '저녁']

            _, initial_max_menus = create_weekly_diet_table(st.session_state.weekly_diet, "초기 식단", return_menu_counts=True)

            for i, meal_type in enumerate(meal_types):
                korean_meal = korean_meals[i]
                max_menu_count = initial_max_menus[meal_type]

                if max_menu_count > 1:
                    start_row = current_row
                    end_row = current_row + max_menu_count - 1
                    ws.merge_cells(f'A{start_row}:A{end_row}')

                    merged_cell = ws[f'A{start_row}']
                    merged_cell.value = korean_meal
                    merged_cell.font = Font(bold=True, size=11)
                    merged_cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
                    merged_cell.alignment = Alignment(horizontal='center', vertical='center')
                    merged_cell.border = border
                else:
                    cell = ws[f'A{current_row}']
                    cell.font = Font(bold=True, size=11)
                    cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.border = border

                current_row += max_menu_count

            ## 식단 표 스타일링
            style_table(ws, 2, len(weekly_diet_table)-1, 8)  # 식단 표
            style_table(ws, initial_nutrients_start + 1, len(nutrients_df), 4)  # 영양 표
            style_table(ws, initial_cost_start + 1, len(cost_df), 2)  # 가격 표
            style_table(ws, initial_perform_start + 1, len(performance_df), 4) 

    buffer.seek(0)
    return buffer

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
        st.image("./assets/logo.png", width=180, use_column_width=True)

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

    if st.session_state.weekly_diet is None:
        name = 'jeongseong'
        menu_db_path = f'./data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
        ingre_db_path = f'./data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'
        
        if hasattr(st.session_state, 'random_diet') and st.session_state.random_diet:
            random_diet_df = generate_random_weekly_diet()
            temp_file = "temp_random_diet.xlsx"
            random_diet_df.to_excel(temp_file, index=False)
            st.session_state.weekly_diet = load_and_process_data(temp_file, menu_db_path, ingre_db_path)
            os.remove(temp_file)
        else:
            uploaded_file = st.session_state.uploaded_file
            converted_file_path = detect_and_convert_diet_format(uploaded_file)

            if converted_file_path:
                try:
                    debug_df = pd.read_excel(converted_file_path)
                    old_stdout = sys.stdout
                    sys.stdout = captured_output = io.StringIO()

                    try:
                        st.session_state.weekly_diet = load_and_process_data(converted_file_path, menu_db_path, ingre_db_path)
                    finally:
                        sys.stdout = old_stdout

                    captured_text = captured_output.getvalue()
                    if "Menu mappings" in captured_text:
                        mapping_lines = [line for line in captured_text.split('\n') if "Menu mappings" in line]

                    if "Missing menus" in captured_text:
                        missing_lines = [line for line in captured_text.split('\n') if "Missing menus" in line]
                        st.warning(f"⚠️ 데이터베이스에서 찾을 수 없어 제외된 메뉴들:\n" + "\n".join(missing_lines[:10]))

                    if st.session_state.weekly_diet and st.session_state.weekly_diet.meals:
                        first_meal_menus = [menu.name for menu in st.session_state.weekly_diet.meals[0].menus]

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
        
        # 초기 식단 비용 계산
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

    # 초기 식단 분석 결과 표시
    weekly_diet = st.session_state.weekly_diet
    initial_fitness = st.session_state.initial_fitness
    initial_cost = st.session_state.initial_cost

    st.dataframe(diet_to_dataframe(weekly_diet, "Initial Diet"), use_container_width=True)
    st.subheader("🔎 초기 식단 일일 평균 영양성분")
    st.table(pd.DataFrame(st.session_state.nutrients_data))
    
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

    st.markdown("---")
    
    generations = st.slider("최적화 세대수 설정", min_value=50, max_value=500, value=200, step=50, 
                           help="세대수가 높을수록 더 좋은 결과를 얻을 수 있지만 시간이 더 오래 걸립니다.")
    
    if st.button("🚀 SPEA2 식단 최적화 시작", key="optimize_button"):
        st.session_state.generations = generations
        
        st.session_state.optimization_start_time = datetime.now()
        start_time_for_duration = time.time()

        with st.spinner(f'SPEA2 알고리즘 최적화 진행 중... ({generations}세대)'):
            pareto_front = optimizer.optimize(diet_db, weekly_diet, generations)
            st.session_state.optimization_end_time = datetime.now()
            optimization_duration = time.time() - start_time_for_duration
            st.session_state.optimization_duration = optimization_duration

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
            # 각 식단의 총 개선율 계산 (4개 지표의 평균)
            total_improvements = []
            for _, _, improvements in improved_diets:
                total_improvement = sum(improvements) / len(improvements)
                total_improvements.append(total_improvement)

            # 가장 높은 개선율을 가진 식단의 인덱스 찾기
            best_diet_index = total_improvements.index(max(total_improvements))

            # 탭 이름에 별 추가
            tab_names = []
            for i in range(len(improved_diets)):
                if i == best_diet_index:
                    tab_names.append(f"⭐ 제안 식단 {i+1}")
                else:
                    tab_names.append(f"제안 식단 {i+1}")

            diet_tabs = st.tabs(tab_names)
            
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
                    cost_change = initial_cost - optimized_cost
                    
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
                    
                    st.markdown(f"**총 식재료 비용**: {optimized_cost:,.0f}원 ({cost_change:,.0f}원)")                    
                    is_valid, violations = validate_weekly_constraints_detailed(optimized_diet, nutrient_constraints)
                    
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
                
                st.markdown("---")
                excel_buffer = export_results_to_excel()
                if excel_buffer:
                    filename = f"식단최적화결과_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                    col1, col2, col3 = st.columns([1, 1, 1])

                    with col1:
                        st.download_button(
                            label="📥 엑셀 다운로드",
                            data=excel_buffer,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

                    with col2:
                        if st.button("파일 업로드", use_container_width=True):
                            with st.spinner('파일 업로드 중...'):
                                excel_buffer.seek(0)
                                result = upload_to_github(excel_buffer, filename)

                                if result and result.get('success'):
                                    st.success("✅ 파일 업로드 완료!")
                                    if result.get('repo_url'):
                                        st.info(f"📂 업로드된 위치: {result['repo_url']}")
                                else:
                                    error_msg = result.get('error', '알 수 없는 오류가 발생했습니다.') if result else '업로드 결과를 받을 수 없습니다.'
                                    st.error(f"❌ 파일 업로드 실패: {error_msg}")

                                    if 'GitHub 토큰' in error_msg:
                                        st.info("💡 Streamlit Cloud 앱 설정의 Secrets 탭에서 GITHUB_TOKEN을 설정해주세요.")
                                        st.code("GITHUB_TOKEN = \"your_token_here\"")
                                    elif 'Repository not found' in error_msg or '404' in error_msg:
                                        st.info("💡 'diet-optimization-results' 저장소를 먼저 생성해주세요.")
                                    elif 'Bad credentials' in error_msg or '401' in error_msg:
                                        st.info("💡 GitHub 토큰이 유효하지 않습니다. 새로운 토큰을 생성해주세요.")

                                    with st.expander("🔧 문제 해결 방법"):
                                        st.markdown("""
                                        **1. GitHub Personal Access Token 생성:**
                                        - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
                                        - 'Generate new token' 클릭
                                        - 권한: `repo` (전체 저장소 액세스) 체크

                                        **2. Streamlit Cloud에서 설정:**
                                        - 앱 설정 → Secrets 탭
                                        - `GITHUB_TOKEN = "생성한_토큰"` 추가

                                        **3. 저장소 생성:**
                                        - GitHub에서 'diet-optimization-results' 저장소 생성
                                        """)

                    with col3:
                        st.empty()
            else:
                st.info("최적화 시간 정보가 누락되었습니다.")

        else:
            st.warning("3가지 이상 개선된 식단을 찾지 못했습니다. 다른 초기 식단으로 시도해보세요.")

        if st.button('🔄 새로운 최적화 실행'):
            st.session_state.optimization_complete = False
            st.session_state.optimization_results = {}
            st.experimental_rerun()

st.markdown("---")
st.caption("© 2025 요양원 식단 최적화 프로그램. All rights reserved.")

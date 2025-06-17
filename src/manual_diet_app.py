import streamlit as st
import pandas as pd
import numpy as np
from load_data import load_all_menus, create_nutrient_constraints
from Diet_class import Menu, Meal, Diet
from evaluation_function import validate_weekly_constraints_detailed
import plotly.express as px
import plotly.graph_objects as go

class ManualDietDesigner:
    def __init__(self, name):
        self.menu_db_path = f'./data/sarang_DB/processed_DB/Menu_ingredient_nutrient_{name}.xlsx'
        self.ingre_db_path = f'./data/sarang_DB/processed_DB/Ingredient_Price_{name}.xlsx'
        self.diet_db_path = f'./data/sarang_DB/processed_DB/DIET_{name}.xlsx'
        
    @st.cache_data
    def load_menus(_self):
        return load_all_menus(_self.menu_db_path, _self.ingre_db_path)
    
    @st.cache_data
    def get_nutrient_constraints(_self):
        return create_nutrient_constraints()

def initialize_session_state():
    meal_structure = ['밥', '국', '주찬', '부찬1', '부찬2', '김치']
    
    if 'diet_table' not in st.session_state:
        st.session_state.diet_table = {}
        for day in range(1, 8):
            for meal in ['아침', '점심', '저녁']:
                for category in meal_structure:
                    st.session_state.diet_table[f"{day}_{meal}_{category}"] = None
    
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False

def create_diet_from_table():
    meals = []
    meal_type_mapping = {'아침': 'Breakfast', '점심': 'Lunch', '저녁': 'Dinner'}
    meal_structure = ['밥', '국', '주찬', '부찬1', '부찬2', '김치']
    
    for day in range(1, 8):
        for meal_kr in ['아침', '점심', '저녁']:
            meal_menus = []
            
            for category in meal_structure:
                key = f"{day}_{meal_kr}_{category}"
                selected_menu = st.session_state.diet_table.get(key)
                if selected_menu:
                    meal_menus.append(selected_menu)
            
            meal_type_en = meal_type_mapping[meal_kr]
            meals.append(Meal(meal_menus, str(day), meal_type_en))
    
    return Diet(meals)

def calculate_daily_totals():
    daily_nutrients = {}
    daily_costs = {}
    meal_structure = ['밥', '국', '주찬', '부찬1', '부찬2', '김치']
    
    for day in range(1, 8):
        nutrients = {'에너지(kcal)': 0, '탄수화물(g)': 0, '단백질(g)': 0, '지방(g)': 0, '식이섬유(g)': 0}
        cost = 0
        
        for meal in ['아침', '점심', '저녁']:
            for category in meal_structure:
                key = f"{day}_{meal}_{category}"
                menu = st.session_state.diet_table.get(key)
                
                if menu:
                    adjusted_nutrients = menu.get_adjusted_nutrients()
                    for nutrient, amount in adjusted_nutrients.items():
                        nutrients[nutrient] += amount
                    cost += menu.get_adjusted_price()
        
        daily_nutrients[day] = nutrients
        daily_costs[day] = cost
    
    return daily_nutrients, daily_costs

def get_category_menus(all_menus, category):
    category_mapping = {'밥': ['밥'],'국': ['국'],'주찬': ['주찬'],'부찬1': ['부찬'],'부찬2': ['부찬'],'김치': ['김치']}
    target_categories = category_mapping.get(category, [])
    return [menu for menu in all_menus if menu.category in target_categories]

def main():
    st.set_page_config(page_title="식단 설계", layout="wide")
    st.title("🍽️ 일주일치 식단표 설계")
    
    name = 'jeongseong'
    designer = ManualDietDesigner(name)
    all_menus = designer.load_menus()
    nutrient_constraints = designer.get_nutrient_constraints()
    
    initialize_session_state()
    
    # 상단 컨트롤 패널
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col2:
            if st.button("🗑️ 전체 초기화", use_container_width=True):
                st.session_state.diet_table = {}
                initialize_session_state()
                st.experimental_rerun()
        
        with col3:
            if st.button("📊 영양 분석", use_container_width=True):
                st.session_state.show_analysis = True
        
        with col4:
            if st.button("💾 저장", use_container_width=True):
                st.success("식단이 저장되었습니다!")
    
    # 메인 식단표
    st.header("📅 한식 주간 식단표")
    
    meal_structure = ['밥', '국', '주찬', '부찬1', '부찬2', '김치']
    meal_emojis = {'밥': '🍚', '국': '🍲', '주찬': '🥩', '부찬1': '🥗', '부찬2': '🥬', '김치': '🥬'}
    
    # 식단표 헤더
    header_cols = st.columns([1, 1] + [1.5]*7)
    header_cols[0].write("**끼니**")
    header_cols[1].write("**구성**")
    for i, day in enumerate(['월', '화', '수', '목', '금', '토', '일'], 2):
        header_cols[i].write(f"**Day {i-1} ({day})**")
    
    # 각 끼니별 행
    for meal_kr in ['아침', '점심', '저녁']:
        meal_emoji = {'아침': '🌅', '점심': '🌞', '저녁': '🌙'}
        
        for cat_idx, category in enumerate(meal_structure):
            row_cols = st.columns([1, 1] + [1.5]*7)
            
            if cat_idx == 0:
                row_cols[0].markdown(f"**{meal_emoji[meal_kr]}<br>{meal_kr}**", unsafe_allow_html=True)
            else:
                row_cols[0].write("")
            
            # 카테고리 라벨
            row_cols[1].write(f"**{meal_emojis[category]} {category}**")
            
            # 각 날짜별 메뉴 선택
            for day in range(1, 8):
                with row_cols[day + 1]:
                    key = f"{day}_{meal_kr}_{category}"
                    
                    # 해당 카테고리의 메뉴 목록 가져오기
                    category_menus = get_category_menus(all_menus, category)
                    
                    # 메뉴 옵션 생성 (기본 가격 표시)
                    menu_options = ["선택안함"] + [
                        f"{menu.name} ({sum(ing.price for ing in menu.ingredients):.0f}원)" 
                        for menu in category_menus
                    ]
                    
                    # 현재 선택된 메뉴와 서빙 비율
                    current_menu = st.session_state.diet_table.get(key)
                    current_index = 0
                    if current_menu:
                        for i, menu in enumerate(category_menus):
                            if menu.name == current_menu.name:
                                current_index = i + 1
                                break
                    
                    # 메뉴 선택 드롭다운
                    selected_index = st.selectbox(
                        label=f"{category}",
                        options=range(len(menu_options)),
                        format_func=lambda x: menu_options[x],
                        index=current_index,
                        key=f"select_{key}",
                        label_visibility="collapsed"
                    )
                    
                    # 메뉴가 선택된 경우
                    if selected_index > 0:
                        selected_menu = category_menus[selected_index - 1]
                        
                        # 기존 서빙 비율 유지 또는 기본값
                        current_ratio = current_menu.serving_ratio if current_menu and current_menu.name == selected_menu.name else 1.0
                        
                        # 서빙 비율 슬라이더
                        serving_ratio = st.slider("배율", 0.6, 1.0, current_ratio, 0.1,
                            key=f"ratio_{key}", label_visibility="collapsed"
                        )
                        
                        # 메뉴 객체 생성/업데이트
                        new_menu = Menu(selected_menu.name, selected_menu.nutrients, selected_menu.ingredients, selected_menu.category, serving_ratio)
                        st.session_state.diet_table[key] = new_menu
                        
                        # 조정된 영양 정보 표시
                        adjusted_nutrients = new_menu.get_adjusted_nutrients()
                        adjusted_price = new_menu.get_adjusted_price()
                        energy = adjusted_nutrients.get('에너지(kcal)', 0)
                        protein = adjusted_nutrients.get('단백질(g)', 0)
                        
                        st.caption(f"⚡ {energy:.0f}kcal | 💰 {adjusted_price:.0f}원")
                        
                    else:
                        # 선택안함인 경우 메뉴 제거
                        st.session_state.diet_table[key] = None
    
    # 일별 영양소 현황
    st.header("📊 일별 영양소 현황")
    daily_nutrients, daily_costs = calculate_daily_totals()
    
    summary_data = []
    for day in range(1, 8):
        nutrients = daily_nutrients[day]
        cost = daily_costs[day]
        
        # 완성도 계산 (6개 구성 중 몇 개 완성되었는지)
        completed_items = 0
        for meal in ['아침', '점심', '저녁']:
            for category in meal_structure:
                key = f"{day}_{meal}_{category}"
                if st.session_state.diet_table.get(key):
                    completed_items += 1
        
        completion_rate = (completed_items / 18) * 100  # 18 = 3끼 × 6구성
        
        # 제약조건 체크
        violations = []
        for nutrient, amount in nutrients.items():
            min_val = nutrient_constraints.min_values[nutrient]
            max_val = nutrient_constraints.max_values[nutrient]
            if amount < min_val or amount > max_val:
                violations.append(nutrient)
        
        summary_data.append({
            'Day': f'Day {day}',
            '완성도': f"{completion_rate:.1f}%",
            '에너지': f"{nutrients['에너지(kcal)']:.0f}",
            '단백질': f"{nutrients['단백질(g)']:.1f}",
            '탄수화물': f"{nutrients['탄수화물(g)']:.1f}",
            '지방': f"{nutrients['지방(g)']:.1f}",
            '비용': f"{cost:,.0f}원",
            '상태': "✅" if not violations else f"❌({len(violations)})"
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # 영양 분석 모달
    if st.session_state.show_analysis:
        st.header("📊 영양 분석 결과")
        
        current_diet = create_diet_from_table()
        is_valid, violations = validate_weekly_constraints_detailed(current_diet, nutrient_constraints)
        
        if is_valid:
            st.success("✅ 모든 영양소 범위 만족")
        else:
            st.error("❌ 영양소 범위 위반")
            for violation in violations:
                st.write(f"• {violation}")
        
if __name__ == "__main__":
    main()
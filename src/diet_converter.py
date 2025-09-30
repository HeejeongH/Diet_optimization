import pandas as pd
from datetime import datetime

def convert_diet_format(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path)
    result_data = []

    date_row = df.iloc[1]
    dates = [i for i in range(1, len(date_row)) if pd.notna(date_row.iloc[i]) and isinstance(date_row.iloc[i], datetime)]

    # 첫 번째 열에서 식사 시간 행 찾기
    first_col = df.iloc[:, 0].astype(str)
    breakfast_start = first_col[first_col.str.contains('아침', na=False)].index[0]
    lunch_start = first_col[first_col.str.contains('점심', na=False)].index[0]
    dinner_start = first_col[first_col.str.contains('저녁', na=False)].index[0]
    
    # 저녁 끝: 두 번째 열에서 저녁 시작 이후 첫 NaN
    dinner_end = dinner_start
    for i in range(dinner_start + 1, len(df)):
        if pd.isna(df.iloc[i, 1]):
            dinner_end = i - 1
            break
    else:
        dinner_end = len(df) - 1

    meal_sections = {
        'Breakfast': {'start': breakfast_start, 'end': lunch_start - 1},
        'Lunch': {'start': lunch_start, 'end': dinner_start - 1},
        'Dinner': {'start': dinner_start, 'end': dinner_end}
    }

    for day_idx, col_idx in enumerate(dates, 1):
        for meal_type, section in meal_sections.items():
            menus = []
            for row_idx in range(section['start'], section['end'] + 1):
                menu_item = df.iloc[row_idx, col_idx]
                if pd.notna(menu_item) and str(menu_item).strip():
                    menu_cleaned = str(menu_item).split('/')[0].strip()
                    menus.append(menu_cleaned)

            result_data.append({
                'Day': day_idx,
                'MealType': meal_type,
                'Menus': ', '.join(menus)
            })
    
    result_df = pd.DataFrame(result_data)
    result_df.to_excel(output_file_path, index=False)
    print(f"변환 완료: {output_file_path}")
    
    return result_df


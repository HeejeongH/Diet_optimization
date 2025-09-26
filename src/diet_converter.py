import pandas as pd
from datetime import datetime

def convert_diet_format(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path)
    result_data = []

    date_row = df.iloc[1]
    dates = []
    for col_idx in range(1, len(date_row)):
        if pd.notna(date_row.iloc[col_idx]) and isinstance(date_row.iloc[col_idx], datetime):
            dates.append(col_idx)

    meal_sections = {
        'Breakfast': {'start': 2, 'end': 7},  # 아침 (행 2-7)
        'Lunch': {'start': 9, 'end': 14},     # 점심 (행 9-14)
        'Dinner': {'start': 15, 'end': 20}    # 저녁 (행 15-20)
    }

    for day_idx, col_idx in enumerate(dates, 1):
        for meal_type, section in meal_sections.items():
            print(meal_type)
            menus = []
            for row_idx in range(section['start'], section['end'] + 1):
                menu_item = df.iloc[row_idx, col_idx]
                if pd.notna(menu_item) and str(menu_item).strip():
                    menu_cleaned = str(menu_item).split('/')[0].strip()
                    print(menu_cleaned)
                    menus.append(menu_cleaned)

            result_data.append({
                'Day': day_idx,
                'MealType': meal_type,
                'Menus': ', '.join(menus)
            })
    result_df = pd.DataFrame(result_data)

    result_df.to_excel(output_file_path, index=False)

    print(f"변환 완료: {input_file_path} -> {output_file_path}")
    print(f"생성된 데이터:")
    print(result_df)

    return result_df


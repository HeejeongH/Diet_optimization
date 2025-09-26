import pandas as pd

def apply_food_mapping(diet_file_path, mapping_file_path, output_file_path):
    """
    식단 데이터에 음식 매핑을 적용하여 시스템이 인식할 수 있는 형태로 변환

    Args:
        diet_file_path: 변환된 식단 데이터 파일 경로
        mapping_file_path: 음식 매핑 파일 경로
        output_file_path: 매핑 적용된 최종 출력 파일 경로

    Returns:
        DataFrame: 매핑이 적용된 식단 데이터
    """

    # 데이터 로드
    diet_df = pd.read_excel(diet_file_path)
    mapping_df = pd.read_csv(mapping_file_path)

    # 매핑 딕셔너리 생성
    mapping_dict = dict(zip(mapping_df['pre_food'], mapping_df['post_food']))

    print(f"로드된 식단 데이터: {len(diet_df)}개 식사")
    print(f"로드된 매핑 데이터: {len(mapping_dict)}개 매핑")

    # 매핑 적용
    mapped_data = []
    mapping_stats = {'total_items': 0, 'mapped_items': 0, 'unmapped_items': 0}
    unmapped_items = set()

    for _, row in diet_df.iterrows():
        day = row['Day']
        meal_type = row['MealType']
        menus = row['Menus']

        # 메뉴 항목들을 분리하고 매핑 적용
        menu_items = [item.strip() for item in str(menus).split(',')]
        mapped_menu_items = []

        for item in menu_items:
            mapping_stats['total_items'] += 1

            if item in mapping_dict:
                mapped_item = mapping_dict[item]
                mapped_menu_items.append(mapped_item)
                mapping_stats['mapped_items'] += 1
                print(f"매핑: '{item}' -> '{mapped_item}'")
            else:
                # 매핑되지 않은 항목은 원본 그대로 유지
                mapped_menu_items.append(item)
                mapping_stats['unmapped_items'] += 1
                unmapped_items.add(item)
                print(f"매핑 불가: '{item}' (원본 유지)")

        # 매핑된 메뉴들을 하나의 문자열로 결합
        mapped_menus = ', '.join(mapped_menu_items)

        mapped_data.append({
            'Day': day,
            'MealType': meal_type,
            'Original_Menus': menus,
            'Mapped_Menus': mapped_menus
        })

    # 결과 DataFrame 생성
    result_df = pd.DataFrame(mapped_data)

    # 결과 저장
    result_df.to_excel(output_file_path, index=False)

    # 통계 출력
    print(f"\n=== 매핑 통계 ===")
    print(f"전체 메뉴 항목: {mapping_stats['total_items']}개")
    print(f"매핑된 항목: {mapping_stats['mapped_items']}개")
    print(f"매핑되지 않은 항목: {mapping_stats['unmapped_items']}개")

    if unmapped_items:
        print(f"\n매핑되지 않은 항목들:")
        for item in sorted(unmapped_items):
            print(f"- {item}")

    print(f"\n매핑 결과가 저장되었습니다: {output_file_path}")
    print(f"생성된 데이터:")
    print(result_df.head())

    return result_df

if __name__ == "__main__":
    # 테스트 실행
    diet_file = "../data/Converted_Weekly_diet.xlsx"
    mapping_file = "food_mapping.csv"
    output_file = "../data/Mapped_Weekly_diet.xlsx"

    result = apply_food_mapping(diet_file, mapping_file, output_file)
"""
CSV 프로세서 병합 테스트 - id_supply 컬럼 없이도 동작 확인
"""
import pandas as pd
import pytest

from app.etl.csv_processor import CSVDataProcessor


def test_merge_demand_supply_without_id_supply():
    """id_supply 컬럼이 없어도 병합이 수행되는지 테스트"""
    processor = CSVDataProcessor()
    
    # 수요 데이터 (CSV 데이터 시뮬레이션)
    demand_df = pd.DataFrame(
        {
            "region_code": ["11", "11", "21", "21"],
            "facility_type": ["pool", "gym", "pool", "gym"],
            "demand_percentage": [50, 70, 60, 80],
        }
    )
    
    # 공급 데이터 (API 데이터 시뮬레이션 - id_supply 없음)
    supply_df = pd.DataFrame(
        {
            "region_code": ["11", "11", "11", "21"],
            "facility_type": ["pool", "pool", "gym", "pool"],
            # id_supply 컬럼이 없음!
        }
    )
    
    # 병합 실행
    result = processor.merge_demand_supply_data(demand_df, supply_df)
    
    # 서울(11) 수영장 검증
    pool_row = result[(result["region_code"] == "11") & (result["facility_type"] == "pool")].iloc[0]
    assert pool_row["supply_count"] == 2  # 2개 시설
    assert pool_row["demand_supply_ratio"] == pytest.approx(50 / (2 + 1) * 100)
    
    # 서울(11) 체육관 검증
    gym_row = result[(result["region_code"] == "11") & (result["facility_type"] == "gym")].iloc[0]
    assert gym_row["supply_count"] == 1  # 1개 시설
    assert gym_row["demand_supply_ratio"] == pytest.approx(70 / (1 + 1) * 100)
    
    # 부산(21) 수영장 검증
    busan_pool = result[(result["region_code"] == "21") & (result["facility_type"] == "pool")].iloc[0]
    assert busan_pool["supply_count"] == 1  # 1개 시설
    assert busan_pool["demand_supply_ratio"] == pytest.approx(60 / (1 + 1) * 100)
    
    # 부산(21) 체육관 검증 (공급 없음)
    busan_gym = result[(result["region_code"] == "21") & (result["facility_type"] == "gym")].iloc[0]
    assert busan_gym["supply_count"] == 0  # 시설 없음
    assert busan_gym["demand_supply_ratio"] == pytest.approx(80 / (0 + 1) * 100)


def test_merge_with_id_supply_column():
    """id_supply 컬럼이 있어도 정상 동작하는지 테스트"""
    processor = CSVDataProcessor()
    
    demand_df = pd.DataFrame(
        {
            "region_code": ["11"],
            "facility_type": ["pool"],
            "demand_percentage": [50],
        }
    )
    
    # id_supply 컬럼이 있는 경우
    supply_df = pd.DataFrame(
        {
            "region_code": ["11", "11"],
            "facility_type": ["pool", "pool"],
            "id_supply": [1, 2],  # id_supply 컬럼 존재
        }
    )
    
    result = processor.merge_demand_supply_data(demand_df, supply_df)
    
    assert len(result) == 2  # 공급 데이터 2개 행
    assert result["supply_count"].iloc[0] == 2
    assert "id_supply" in result.columns  # 원본 컬럼 유지


def test_merge_empty_supply():
    """공급 데이터가 비어있을 때 처리"""
    processor = CSVDataProcessor()
    
    demand_df = pd.DataFrame(
        {
            "region_code": ["11"],
            "facility_type": ["pool"],
            "demand_percentage": [100],
        }
    )
    
    # 빈 공급 데이터
    supply_df = pd.DataFrame(columns=["region_code", "facility_type"])
    
    result = processor.merge_demand_supply_data(demand_df, supply_df)
    
    assert len(result) == 1
    assert result["supply_count"].iloc[0] == 0
    assert result["demand_supply_ratio"].iloc[0] == 100 / 1 * 100  # 공급 0일 때
    assert result["is_imbalanced"].iloc[0] == True  # 공급 없으면 불균형


def test_imbalance_detection():
    """불균형 지역 감지 테스트"""
    processor = CSVDataProcessor()
    
    demand_df = pd.DataFrame(
        {
            "region_code": ["11", "21", "31"],
            "facility_type": ["pool", "pool", "pool"],
            "demand_percentage": [30, 100, 200],
        }
    )
    
    supply_df = pd.DataFrame(
        {
            "region_code": ["11", "11", "11", "11", "21"],  # 11: 4개, 21: 1개, 31: 0개
            "facility_type": ["pool", "pool", "pool", "pool", "pool"],
        }
    )
    
    result = processor.merge_demand_supply_data(demand_df, supply_df)
    
    # 지역별 불균형 상태 확인
    seoul = result[result["region_code"] == "11"].iloc[0]
    busan = result[result["region_code"] == "21"].iloc[0]
    daegu = result[result["region_code"] == "31"].iloc[0]
    
    # 서울: 수요 30%, 공급 4개 → 비율 = 30/(4+1)*100 = 6 → 균형
    assert seoul["supply_count"] == 4
    assert seoul["is_imbalanced"] == False
    
    # 부산: 수요 100%, 공급 1개 → 비율 = 100/(1+1)*100 = 50 → 균형  
    assert busan["supply_count"] == 1
    assert busan["is_imbalanced"] == False
    
    # 대구: 수요 200%, 공급 0개 → 비율 = 200/(0+1)*100 = 200 → 불균형
    assert daegu["supply_count"] == 0
    assert daegu["is_imbalanced"] == True


if __name__ == "__main__":
    # 직접 실행 시 모든 테스트 수행
    test_merge_demand_supply_without_id_supply()
    print("✓ id_supply 없이 병합 테스트 통과")
    
    test_merge_with_id_supply_column()
    print("✓ id_supply 있을 때 병합 테스트 통과")
    
    test_merge_empty_supply()
    print("✓ 빈 공급 데이터 처리 테스트 통과")
    
    test_imbalance_detection()
    print("✓ 불균형 감지 테스트 통과")
    
    print("\n✅ 모든 테스트 통과!")
"""
공공데이터 API 클라이언트 테스트 스크립트
API 키 없이도 기본 동작을 테스트할 수 있도록 구성
"""
import asyncio
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_facilities_client():
    """체육시설 API 클라이언트 테스트"""
    try:
        from app.services.facilities_api_client import FacilitiesAPIClient
        from app.core.config import settings
        
        if not settings.DATA_GO_KR_API_KEY or settings.DATA_GO_KR_API_KEY == "your_api_key_here":
            logger.warning("API 키가 설정되지 않았습니다. 모의 데이터로 테스트합니다.")
            return {
                "status": "mock",
                "message": "API 키 없음 - 모의 데이터 사용",
                "mock_data": {
                    "total_facilities": 2847,
                    "by_type": {
                        "수영장": 234,
                        "체육관": 456,
                        "축구장": 789,
                        "테니스장": 345
                    }
                }
            }
        
        client = FacilitiesAPIClient()
        
        # 서울시 수영장 조회 테스트
        logger.info("서울시 수영장 데이터 조회 중...")
        result = await client.get_facilities_list(
            city_name="서울특별시",
            facility_type="수영장",
            num_of_rows=5
        )
        
        logger.info(f"조회 성공: {len(result.get('response', {}).get('body', {}).get('items', {}).get('item', []))}개")
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"체육시설 API 테스트 실패: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


async def test_fund_client():
    """기금 API 클라이언트 테스트"""
    try:
        from app.services.fund_api_client import FundAPIClient
        from app.core.config import settings
        
        if not settings.DATA_GO_KR_API_KEY or settings.DATA_GO_KR_API_KEY == "your_api_key_here":
            logger.warning("API 키가 설정되지 않았습니다. 모의 데이터로 테스트합니다.")
            return {
                "status": "mock",
                "message": "API 키 없음 - 모의 데이터 사용",
                "mock_data": {
                    "total_budget": 4500000000000,  # 4.5조원
                    "by_sport": {
                        "축구": 320000000000,
                        "야구": 280000000000,
                        "수영": 150000000000
                    }
                }
            }
        
        client = FundAPIClient()
        
        # 2023년 데이터 조회 테스트
        logger.info("2023년 기금 지원실적 조회 중...")
        result = await client.get_fund_support_list(
            year=2023,
            num_of_rows=5
        )
        
        logger.info(f"조회 성공")
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"기금 API 테스트 실패: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


async def test_performance_client():
    """성과금 API 클라이언트 테스트"""
    try:
        from app.services.performance_api_client import PerformanceAPIClient
        from app.core.config import settings
        
        if not settings.DATA_GO_KR_API_KEY or settings.DATA_GO_KR_API_KEY == "your_api_key_here":
            logger.warning("API 키가 설정되지 않았습니다. 모의 데이터로 테스트합니다.")
            return {
                "status": "mock",
                "message": "API 키 없음 - 모의 데이터 사용",
                "mock_data": {
                    "top_sports": [
                        {"sport": "양궁", "medals": {"금": 5, "은": 3, "동": 2}},
                        {"sport": "태권도", "medals": {"금": 4, "은": 2, "동": 3}},
                        {"sport": "펜싱", "medals": {"금": 3, "은": 4, "동": 2}}
                    ]
                }
            }
        
        client = PerformanceAPIClient()
        
        # 2023년 데이터 조회 테스트
        logger.info("2023년 성과금 지급 데이터 조회 중...")
        result = await client.get_performance_rewards(
            year=2023,
            num_of_rows=5
        )
        
        logger.info(f"조회 성공")
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"성과금 API 테스트 실패: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


async def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("공공데이터 API 클라이언트 테스트")
    print("=" * 60)
    
    # 1. 체육시설 API 테스트
    print("\n[1] 전국공공체육시설 API 테스트")
    print("-" * 40)
    facilities_result = await test_facilities_client()
    print(f"결과: {facilities_result['status']}")
    if facilities_result['status'] == 'mock':
        print(f"모의 데이터: 총 {facilities_result['mock_data']['total_facilities']}개 시설")
    
    # 2. 기금 API 테스트
    print("\n[2] 국민체육진흥기금 API 테스트")
    print("-" * 40)
    fund_result = await test_fund_client()
    print(f"결과: {fund_result['status']}")
    if fund_result['status'] == 'mock':
        print(f"모의 데이터: 총 예산 {fund_result['mock_data']['total_budget']:,}원")
    
    # 3. 성과금 API 테스트
    print("\n[3] 경기력향상성과금 API 테스트")
    print("-" * 40)
    performance_result = await test_performance_client()
    print(f"결과: {performance_result['status']}")
    if performance_result['status'] == 'mock':
        print(f"모의 데이터: 상위 {len(performance_result['mock_data']['top_sports'])}개 종목")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
    
    # 요약
    print("\n[테스트 요약]")
    print("-" * 40)
    
    if all(r['status'] == 'mock' for r in [facilities_result, fund_result, performance_result]):
        print("⚠️  모든 API가 모의 데이터를 사용 중입니다.")
        print("실제 데이터를 사용하려면:")
        print("1. 공공데이터포털(data.go.kr)에서 API 키 발급")
        print("2. backend/.env 파일에 DATA_GO_KR_API_KEY 설정")
    elif all(r['status'] == 'success' for r in [facilities_result, fund_result, performance_result]):
        print("✅ 모든 API 테스트 성공!")
    else:
        print("⚠️  일부 API 테스트 실패. 로그를 확인하세요.")


if __name__ == "__main__":
    # Python 경로 설정
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # 테스트 실행
    asyncio.run(main())
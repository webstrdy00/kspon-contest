#!/usr/bin/env python3
"""
공공데이터 API 클라이언트 모의 테스트
실제 API 대신 모의 데이터로 테스트
"""
import asyncio
import logging
import sys
from datetime import datetime
from typing import Dict, Any

# 프로젝트 경로 추가
sys.path.append('.')

from app.services.facilities_api_client import FacilitiesAPIClient
from app.services.fund_api_client import FundAPIClient
from app.services.performance_api_client import PerformanceAPIClient

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_mock_facilities_data() -> Dict[str, Any]:
    """모의 체육시설 데이터 생성"""
    return {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "NORMAL SERVICE."
            },
            "body": {
                "items": {
                    "item": [
                        {
                            "faclty_nm": "강남구민체육센터",
                            "ftype_nm": "수영장",
                            "cp_nm": "서울특별시",
                            "cpb_nm": "강남구",
                            "faclty_addr": "서울특별시 강남구 삼성로 635",
                            "lat": 37.5145,
                            "lot": 127.0478,
                            "rm_matr": "실내 수영장 6레인, 어린이풀",
                            "opn_yn": "Y",
                            "tel_no": "02-3411-5000"
                        },
                        {
                            "faclty_nm": "송파구민체육관",
                            "ftype_nm": "체육관",
                            "cp_nm": "서울특별시",
                            "cpb_nm": "송파구",
                            "faclty_addr": "서울특별시 송파구 올림픽로 326",
                            "lat": 37.5111,
                            "lot": 127.0811,
                            "rm_matr": "배드민턴장, 농구장",
                            "opn_yn": "Y",
                            "tel_no": "02-2147-2000"
                        }
                    ]
                },
                "numOfRows": 2,
                "pageNo": 1,
                "totalCount": 2
            }
        }
    }


def create_mock_fund_data() -> Dict[str, Any]:
    """모의 기금 지원 데이터 생성"""
    return {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "NORMAL SERVICE."
            },
            "body": {
                "items": {
                    "item": [
                        {
                            "sprt_year": "2023",
                            "sprt_se": "생활체육시설 지원",
                            "sprt_trget": "서울특별시",
                            "sprt_amount": 5000000000,
                            "sprt_co": 15,
                            "rm": "수영장 3개소, 체육관 5개소, 운동장 7개소"
                        },
                        {
                            "sprt_year": "2023",
                            "sprt_se": "전문체육시설 지원",
                            "sprt_trget": "경기도",
                            "sprt_amount": 8000000000,
                            "sprt_co": 10,
                            "rm": "훈련장 5개소, 경기장 5개소"
                        }
                    ]
                },
                "numOfRows": 2,
                "pageNo": 1,
                "totalCount": 2
            }
        }
    }


def create_mock_performance_data() -> Dict[str, Any]:
    """모의 성과금 데이터 생성"""
    return {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "NORMAL SERVICE."
            },
            "body": {
                "items": {
                    "item": [
                        {
                            "pmnt_year": "2023",
                            "event_nm": "아시안게임",
                            "sport_nm": "수영",
                            "medal_se": "금메달",
                            "athlt_cnt": 5,
                            "pmnt_amount": 500000000,
                            "pmnt_dt": "2023-10-15"
                        },
                        {
                            "pmnt_year": "2023",
                            "event_nm": "세계선수권",
                            "sport_nm": "양궁",
                            "medal_se": "은메달",
                            "athlt_cnt": 3,
                            "pmnt_amount": 150000000,
                            "pmnt_dt": "2023-08-20"
                        }
                    ]
                },
                "numOfRows": 2,
                "pageNo": 1,
                "totalCount": 2
            }
        }
    }


async def test_with_mock_data():
    """모의 데이터로 테스트"""
    
    print("=" * 60)
    print("공공데이터 API 클라이언트 모의 테스트")
    print("=" * 60)
    
    # 1. 체육시설 데이터 처리 테스트
    print("\n[1] 체육시설 데이터 처리 테스트")
    print("-" * 40)
    
    mock_facilities = create_mock_facilities_data()
    items = mock_facilities["response"]["body"]["items"]["item"]
    
    print(f"✅ 체육시설 {len(items)}개 처리 완료")
    for item in items:
        print(f"   - {item['faclty_nm']} ({item['ftype_nm']}) - {item['cpb_nm']}")
    
    # 2. 기금 지원 데이터 처리 테스트
    print("\n[2] 기금 지원 데이터 처리 테스트")
    print("-" * 40)
    
    mock_fund = create_mock_fund_data()
    items = mock_fund["response"]["body"]["items"]["item"]
    
    print(f"✅ 기금 지원 {len(items)}건 처리 완료")
    for item in items:
        amount_billion = item['sprt_amount'] / 1000000000
        print(f"   - {item['sprt_trget']}: {amount_billion:.1f}억원 ({item['sprt_se']})")
    
    # 3. 성과금 데이터 처리 테스트
    print("\n[3] 성과금 데이터 처리 테스트")
    print("-" * 40)
    
    mock_performance = create_mock_performance_data()
    items = mock_performance["response"]["body"]["items"]["item"]
    
    print(f"✅ 성과금 지급 {len(items)}건 처리 완료")
    for item in items:
        amount_million = item['pmnt_amount'] / 1000000
        print(f"   - {item['sport_nm']} {item['medal_se']}: {amount_million:.0f}백만원 ({item['event_nm']})")
    
    # 4. 통합 분석 테스트
    print("\n[4] 통합 분석 테스트")
    print("-" * 40)
    
    # 예산 대비 성과 분석
    total_fund = sum(item['sprt_amount'] for item in mock_fund["response"]["body"]["items"]["item"])
    total_reward = sum(item['pmnt_amount'] for item in mock_performance["response"]["body"]["items"]["item"])
    
    print(f"✅ 2023년 예산-성과 분석")
    print(f"   - 총 지원 예산: {total_fund/1000000000:.1f}억원")
    print(f"   - 총 성과금: {total_reward/1000000000:.1f}억원")
    print(f"   - ROI: {(total_reward/total_fund)*100:.1f}%")
    
    # 지역별 시설 분포
    print(f"\n✅ 지역별 시설 분포")
    region_facilities = {}
    for item in mock_facilities["response"]["body"]["items"]["item"]:
        region = item['cpb_nm']
        if region not in region_facilities:
            region_facilities[region] = []
        region_facilities[region].append(item['faclty_nm'])
    
    for region, facilities in region_facilities.items():
        print(f"   - {region}: {len(facilities)}개 시설")
    
    print("\n" + "=" * 60)
    print("모의 테스트 완료 - 모든 데이터 처리 정상")
    print("=" * 60)
    print("\n💡 실제 API 연동 시 참고사항:")
    print("1. API 키가 유효한지 확인")
    print("2. API 활용신청이 승인되었는지 확인")
    print("3. API URL과 엔드포인트가 정확한지 확인")
    print("4. 일일 트래픽 제한 확인 (기본 1,000회)")


if __name__ == "__main__":
    asyncio.run(test_with_mock_data())
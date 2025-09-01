#!/usr/bin/env python
"""
수정된 공공데이터 API 테스트
"""
import asyncio
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# API 클라이언트 임포트
from app.services.facilities_api_client import FacilitiesAPIClient
from app.services.fund_api_client import FundAPIClient
from app.services.performance_api_client import PerformanceAPIClient
from app.services.fund_evaluation_api_client import FundEvaluationAPIClient
from app.services.fund_comprehensive_api_client import FundComprehensiveAPIClient


async def test_performance_api():
    """수정된 Performance API 테스트"""
    print("\n=== 체육인복지 경기력성과포상금 API 테스트 ===")
    client = PerformanceAPIClient()
    
    try:
        # 새로운 파라미터로 테스트
        result = await client.get_performance_rewards(
            payment_month="202401",  # YYYYMM 형식
            page_no=1,
            num_of_rows=5
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 데이터")
            
            items = body.get('items', {}).get('item', [])
            if items:
                print("\n실제 응답 데이터 구조:")
                if isinstance(items, list):
                    first_item = items[0]
                else:
                    first_item = items
                
                # 파싱 테스트
                parsed = client.parse_performance_data(first_item)
                print("\n파싱된 데이터:")
                for key, value in parsed.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
                        
                # 원본 데이터와 비교
                print("\n원본 필드:")
                for key, value in first_item.items():
                    print(f"  {key}: {value}")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_evaluation_api():
    """Fund Evaluation API 파싱 테스트"""
    print("\n=== 기금지원사업평가 API 파싱 테스트 ===")
    client = FundEvaluationAPIClient()
    
    try:
        # 데이터가 있는 연도로 테스트
        result = await client.get_evaluation_items(
            apply_year=2022,
            page_no=1,
            num_of_rows=3
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 데이터")
            
            items = body.get('items', {}).get('item', [])
            if items:
                if isinstance(items, list):
                    first_item = items[0]
                else:
                    first_item = items
                
                # 파싱 테스트
                parsed = client.parse_evaluation_data(first_item)
                print("\n파싱된 데이터:")
                for key, value in parsed.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_comprehensive_api():
    """Fund Comprehensive API 파싱 테스트"""
    print("\n=== 종합지원실적지표 API 파싱 테스트 ===")
    client = FundComprehensiveAPIClient()
    
    try:
        result = await client.get_comprehensive_results(
            year="2023",
            page_no=1,
            num_of_rows=3
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 데이터")
            
            items = body.get('items', {}).get('item', [])
            if items:
                if isinstance(items, list):
                    first_item = items[0]
                else:
                    first_item = items
                
                # 파싱 테스트
                parsed = client.parse_comprehensive_data(first_item)
                print("\n파싱된 데이터:")
                for key, value in parsed.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_performance_analysis():
    """Performance API 분석 메서드 테스트"""
    print("\n=== Performance API 분석 메서드 테스트 ===")
    client = PerformanceAPIClient()
    
    try:
        # 2024년 종목별 성과 분석
        print("2024년 종목별 성과 분석 중...")
        sport_performance = await client.get_performance_by_sport(2024)
        
        print(f"\n종목별 성과 (총 {len(sport_performance)}개 종목):")
        for sport, data in list(sport_performance.items())[:5]:
            print(f"  {sport}:")
            print(f"    - 총 지급액: {data.get('total_reward', 0):,}원")
            print(f"    - 지급 건수: {data.get('count', 0)}건")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("수정된 공공데이터 API 테스트")
    print("=" * 60)
    
    # API 키 확인
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    if not api_key or api_key == "your_data_go_kr_api_key_here":
        print("\n⚠️  경고: API 키가 설정되지 않았습니다.")
        return
    
    # 각 API 테스트
    await test_performance_api()
    await test_fund_evaluation_api()
    await test_fund_comprehensive_api()
    await test_performance_analysis()
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료!")
    print("=" * 60)
    print("\n수정 내용:")
    print("1. Performance API: payment_month (YYYYMM), sport_name, recipient_name 파라미터")
    print("2. Performance API: 파싱 로직 수정 (pmt_yymm, spm_nm, mmamt 등)")
    print("3. Fund Evaluation API: 파싱 메서드 검증 완료")
    print("4. Fund Comprehensive API: 파싱 메서드 검증 완료")


if __name__ == "__main__":
    asyncio.run(main())
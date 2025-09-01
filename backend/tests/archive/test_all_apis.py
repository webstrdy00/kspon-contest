#!/usr/bin/env python
"""
모든 공공데이터 API 테스트 스크립트
2025-08-31 업데이트 버전
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


async def test_facilities_api():
    """전국체육시설 API 테스트"""
    print("\n=== 전국체육시설 API 테스트 ===")
    print("URL: https://apis.data.go.kr/B551014/SRVC_API_SFMS_FACI")
    print("엔드포인트: TODZ_API_SFMS_FACI")
    
    try:
        client = FacilitiesAPIClient()
        
        # 서울특별시 체육시설 조회
        result = await client.get_facilities_list(
            city_name="서울특별시",
            page_no=1,
            num_of_rows=10
        )
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 시설 조회 가능")
            items = result.get('body', {}).get('items', {})
            if items and isinstance(items, dict):
                item = items.get('item', [])
                if item:
                    first_item = item[0] if isinstance(item, list) else item
                    print(f"   첫 번째 시설: {first_item.get('faci_nm', 'N/A')}")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_api():
    """국민체육진흥기금 지원 정보 API 테스트"""
    print("\n=== 국민체육진흥기금 지원 정보 API 테스트 ===")
    print("URL: https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_OBJ_ORG_API")
    
    try:
        client = FundAPIClient()
        
        # 기금지원실적 조회
        print("\n1. 기금지원실적 조회 (todz_api_fun_dvdc_erp_api_i)")
        result = await client.get_fund_support_list(year=2023)
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 데이터")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
        # 수행기관정보 조회
        print("\n2. 수행기관정보 조회 (todz_api_fun_obj_org_api_i)")
        result = await client.get_organization_info()
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 기관")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_performance_api():
    """체육인복지 경기력성과포상금 API 테스트"""
    print("\n=== 체육인복지 경기력성과포상금 API 테스트 ===")
    print("URL: https://apis.data.go.kr/B551014/SRVC_TODZ_USFUN_PIRPEN_NON_DSPSN")
    print("엔드포인트: TODZ_USFUN_PIRPEN_NON_DSPSN")
    
    try:
        client = PerformanceAPIClient()
        
        # 2024년 데이터 조회
        result = await client.get_performance_rewards(year=2024)
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 데이터")
            items = result.get('body', {}).get('items', {})
            if items and isinstance(items, dict):
                item = items.get('item', [])
                if item:
                    first_item = item[0] if isinstance(item, list) else item
                    print(f"   첫 번째 종목: {first_item.get('spm_nm', 'N/A')}")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_evaluation_api():
    """국민체육진흥기금 기금지원사업평가 API 테스트"""
    print("\n=== 국민체육진흥기금 기금지원사업평가 API 테스트 ===")
    print("URL: https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_FLDESTM_QSTN_API")
    print("엔드포인트: todz_api_fun_qstn_api_i")
    
    try:
        client = FundEvaluationAPIClient()
        
        # 2023년 평가 데이터 조회
        result = await client.get_evaluation_items(year="2023")
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 평가항목")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_comprehensive_api():
    """국민체육진흥기금 종합지원실적지표 API 테스트"""
    print("\n=== 국민체육진흥기금 종합지원실적지표 API 테스트 ===")
    print("URL: https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_INSTT_BSNS_RSLT_API")
    print("엔드포인트: todz_api_fun_instt_api_i")
    
    try:
        client = FundComprehensiveAPIClient()
        
        # 2023년 종합실적 조회
        result = await client.get_comprehensive_results(year="2023")
        
        if result.get('header', {}).get('resultCode') == '00':
            print(f"✅ 성공: {result.get('body', {}).get('totalCount', 0)}개 실적 데이터")
        else:
            print(f"❌ 실패: {result.get('header', {}).get('resultMsg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def main():
    """메인 함수"""
    print("=" * 60)
    print("공공데이터 API 테스트 시작")
    print("=" * 60)
    
    # API 키 확인
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    if not api_key or api_key == "your_data_go_kr_api_key_here":
        print("\n⚠️  경고: DATA_GO_KR_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 실제 API 키를 설정해주세요.")
        print("   https://www.data.go.kr 에서 발급받을 수 있습니다.")
        return
    
    print(f"\nAPI 키: {api_key[:10]}..." if len(api_key) > 10 else api_key)
    
    # 각 API 테스트
    await test_facilities_api()
    await test_fund_api()
    await test_performance_api()
    await test_fund_evaluation_api()
    await test_fund_comprehensive_api()
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
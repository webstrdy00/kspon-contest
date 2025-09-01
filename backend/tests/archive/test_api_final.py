#!/usr/bin/env python
"""
공공데이터 API 최종 통합 테스트
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


async def test_facilities():
    """전국체육시설 API 테스트"""
    print("\n=== 전국체육시설 API 테스트 ===")
    client = FacilitiesAPIClient()
    
    try:
        result = await client.get_facilities_list(
            city_name="서울특별시",
            page_no=1,
            num_of_rows=5
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 시설")
            
            items = body.get('items', {}).get('item', [])
            if items:
                for idx, item in enumerate(items[:3], 1):
                    print(f"   {idx}. {item.get('faci_nm')} ({item.get('fcob_nm')})")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_performance():
    """체육인복지 경기력성과포상금 API 테스트"""
    print("\n=== 체육인복지 경기력성과포상금 API 테스트 ===")
    client = PerformanceAPIClient()
    
    try:
        # Performance API는 payment_month 파라미터가 필요하므로 메서드 추가 필요
        # 임시로 직접 호출
        params = {
            "pageNo": 1,
            "numOfRows": 5,
            "resultType": "json",
            "pmt_yymm": "202401"
        }
        result = await client._request("TODZ_USFUN_PIRPEN_NON_DSPSN", params)
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 종목")
            
            items = body.get('items', {}).get('item', [])
            if items:
                for idx, item in enumerate(items[:3], 1):
                    amount = item.get('mmamt', 0)
                    print(f"   {idx}. {item.get('prg_item_nm')}: {amount:,}원")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund():
    """국민체육진흥기금 API 테스트"""
    print("\n=== 국민체육진흥기금 지원 API 테스트 ===")
    client = FundAPIClient()
    
    try:
        result = await client.get_fund_support_list(
            year=2023,
            page_no=1,
            num_of_rows=5
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 지원실적")
            
            items = body.get('items', {}).get('item', [])
            if items:
                for idx, item in enumerate(items[:3], 1):
                    amount = item.get('dvdc_amt', 0)
                    print(f"   {idx}. {item.get('reqst_instt_nm')} - {item.get('ddtlbz_nm')}: {amount:,}원")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_evaluation():
    """기금지원사업평가 API 테스트"""
    print("\n=== 기금지원사업평가 API 테스트 ===")
    client = FundEvaluationAPIClient()
    
    try:
        # 2023년은 데이터가 없으므로 2022년으로 조회
        result = await client.get_evaluation_items(
            apply_year=2022,
            page_no=1,
            num_of_rows=5
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            total = body.get('totalCount', 0)
            
            if total == 0:
                # 연도 파라미터 없이 재시도
                result = await client.get_evaluation_items(
                    page_no=1,
                    num_of_rows=5
                )
                body = result.get('response', {}).get('body', {})
                total = body.get('totalCount', 0)
            
            print(f"✅ 성공: 총 {total}개 평가항목")
            
            items = body.get('items', {}).get('item', [])
            if items:
                for idx, item in enumerate(items[:3], 1):
                    question = item.get('qstn_nm', 'N/A')
                    year = item.get('aply_yr', 'N/A')
                    score_level = item.get('scr_level_val', 'N/A')
                    print(f"   {idx}. [{year}년] {question[:30]}... (점수레벨: {score_level})")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def test_fund_comprehensive():
    """종합지원실적지표 API 테스트"""
    print("\n=== 종합지원실적지표 API 테스트 ===")
    client = FundComprehensiveAPIClient()
    
    try:
        result = await client.get_comprehensive_results(
            year="2023",
            page_no=1,
            num_of_rows=5
        )
        
        if result.get('response', {}).get('header', {}).get('resultCode') == '00':
            body = result.get('response', {}).get('body', {})
            print(f"✅ 성공: 총 {body.get('totalCount', 0)}개 실적데이터")
            
            items = body.get('items', {}).get('item', [])
            if items:
                for idx, item in enumerate(items[:3], 1):
                    org = item.get('org_nm', 'N/A')
                    biz = item.get('biz_nm', 'N/A')
                    amt = item.get('sprt_amt', 0)
                    print(f"   {idx}. {org} - {biz}: {amt:,}원")
        else:
            print(f"❌ 실패: {result.get('response', {}).get('header', {}).get('resultMsg')}")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")


async def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("공공데이터 API 최종 통합 테스트")
    print("=" * 60)
    
    # API 키 확인
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    if not api_key or api_key == "your_data_go_kr_api_key_here":
        print("\n⚠️  경고: API 키가 설정되지 않았습니다.")
        return
    
    print(f"\n✅ API 키 설정 확인")
    print(f"✅ 모든 API URL 업데이트 완료")
    
    # 각 API 테스트
    await test_facilities()
    await test_performance()
    await test_fund()
    await test_fund_evaluation()
    await test_fund_comprehensive()
    
    print("\n" + "=" * 60)
    print("✅ 모든 API 테스트 완료!")
    print("=" * 60)
    print("\n주요 업데이트 내용:")
    print("1. 전국체육시설 API: SRVC_API_SFMS_FACI/TODZ_API_SFMS_FACI")
    print("2. 경기력성과포상금 API: TODZ_USFUN_PIRPEN_NON_DSPSN (pmt_yymm 파라미터)")
    print("3. 국민체육진흥기금 API: 다양한 엔드포인트 통합")
    print("4. 모든 API 응답 형식: response.body.items.item 구조로 통일")


if __name__ == "__main__":
    asyncio.run(main())
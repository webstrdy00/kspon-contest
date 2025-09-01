#!/usr/bin/env python
"""
공공데이터 API 클라이언트 통합 테스트
모든 API 클라이언트의 기능을 테스트
"""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
import pytest

# 환경변수 로드
load_dotenv()

# API 클라이언트 임포트
from app.services.facilities_api_client import FacilitiesAPIClient
from app.services.fund_api_client import FundAPIClient
from app.services.performance_api_client import PerformanceAPIClient
from app.services.fund_evaluation_api_client import FundEvaluationAPIClient
from app.services.fund_comprehensive_api_client import FundComprehensiveAPIClient


class TestFacilitiesAPI:
    """전국체육시설 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_facilities_list(self):
        """시설 목록 조회 테스트"""
        client = FacilitiesAPIClient()
        
        result = await client.get_facilities_list(
            city_name="서울특별시",
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'
        body = result.get('response', {}).get('body', {})
        assert 'totalCount' in body
        assert 'items' in body
        
        items = body.get('items', {}).get('item', [])
        if items:
            # 첫 번째 아이템 검증
            item = items[0] if isinstance(items, list) else items
            assert 'faci_nm' in item  # 시설명
            assert 'fcob_nm' in item  # 시설구분
    
    @pytest.mark.asyncio
    async def test_parse_facility_data(self):
        """시설 데이터 파싱 테스트"""
        client = FacilitiesAPIClient()
        
        mock_data = {
            'faci_nm': '테스트 체육관',
            'fcob_nm': '체육관',
            'ftype_nm': '실내체육관',
            'fmng_cp_nm': '서울특별시',
            'faci_road_addr1': '서울특별시 중구 세종대로 110',
            'faci_point_x': '126.9780',
            'faci_point_y': '37.5665',
            'tel_no': '02-1234-5678',
            'homepage_url': 'http://test.com',
            'ar_totl_ar': '1000',
            'faciStat_nm': '운영중'
        }
        
        parsed = client.parse_facility_data(mock_data)
        
        assert parsed['name'] == '테스트 체육관'
        assert parsed['facility_type'] == '체육관'
        assert parsed['latitude'] == 37.5665
        assert parsed['longitude'] == 126.9780


class TestPerformanceAPI:
    """체육인복지 경기력성과포상금 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_performance_rewards(self):
        """성과포상금 조회 테스트"""
        client = PerformanceAPIClient()
        
        # 최근 월 데이터로 테스트
        current_year = datetime.now().year
        current_month = datetime.now().month
        payment_month = f"{current_year}{current_month:02d}"
        
        result = await client.get_performance_rewards(
            payment_month=payment_month,
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'
        body = result.get('response', {}).get('body', {})
        
        if body.get('totalCount', 0) > 0:
            items = body.get('items', {}).get('item', [])
            if items:
                item = items[0] if isinstance(items, list) else items
                assert 'pmt_yymm' in item  # 지급년월
                assert 'mmamt' in item  # 금액
    
    @pytest.mark.asyncio
    async def test_performance_by_sport(self):
        """종목별 성과 분석 테스트"""
        client = PerformanceAPIClient()
        
        current_year = datetime.now().year
        result = await client.get_performance_by_sport(current_year)
        
        assert isinstance(result, dict)
        # 결과가 있으면 검증
        if result:
            for sport, data in result.items():
                assert 'total_reward' in data
                assert 'count' in data


class TestFundAPI:
    """국민체육진흥기금 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_support_list(self):
        """지원실적 조회 테스트"""
        client = FundAPIClient()
        
        current_year = datetime.now().year
        result = await client.get_support_list(
            year=current_year,
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'
        body = result.get('response', {}).get('body', {})
        
        if body.get('totalCount', 0) > 0:
            items = body.get('items', {}).get('item', [])
            if items:
                item = items[0] if isinstance(items, list) else items
                assert 'year' in item or 'bsnsyear' in item  # 사업년도
    
    @pytest.mark.asyncio
    async def test_get_business_list(self):
        """사업지원 조회 테스트"""
        client = FundAPIClient()
        
        current_year = datetime.now().year
        result = await client.get_business_list(
            year=current_year,
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'


class TestFundEvaluationAPI:
    """기금평가 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_evaluation_list(self):
        """평가실적 조회 테스트"""
        client = FundEvaluationAPIClient()
        
        current_year = datetime.now().year
        result = await client.get_evaluation_list(
            year=current_year,
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'
        body = result.get('response', {}).get('body', {})
        
        if body.get('totalCount', 0) > 0:
            items = body.get('items', {}).get('item', [])
            if items:
                item = items[0] if isinstance(items, list) else items
                # 평가 관련 필드 확인
                assert any(key in item for key in ['bsis_year', 'year', 'evltrgt_nm'])


class TestFundComprehensiveAPI:
    """종합지원실적 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_comprehensive_list(self):
        """종합지원실적 조회 테스트"""
        client = FundComprehensiveAPIClient()
        
        current_year = datetime.now().year
        result = await client.get_comprehensive_list(
            year=current_year,
            page_no=1,
            num_of_rows=5
        )
        
        assert result.get('response', {}).get('header', {}).get('resultCode') == '00'
        body = result.get('response', {}).get('body', {})
        
        if body.get('totalCount', 0) > 0:
            items = body.get('items', {}).get('item', [])
            if items:
                item = items[0] if isinstance(items, list) else items
                # 종합지원 관련 필드 확인
                assert any(key in item for key in ['year', 'intrlck_nm', 'bsns_year'])


class TestIntegratedAPIs:
    """통합 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_all_apis_connectivity(self):
        """모든 API 연결 테스트"""
        results = {}
        
        # 1. 시설 API
        facilities_client = FacilitiesAPIClient()
        try:
            result = await facilities_client.get_facilities_list(page_no=1, num_of_rows=1)
            results['facilities'] = result.get('response', {}).get('header', {}).get('resultCode') == '00'
        except:
            results['facilities'] = False
        
        # 2. 성과금 API
        performance_client = PerformanceAPIClient()
        try:
            result = await performance_client.get_performance_rewards(page_no=1, num_of_rows=1)
            results['performance'] = result.get('response', {}).get('header', {}).get('resultCode') == '00'
        except:
            results['performance'] = False
        
        # 3. 기금 API
        fund_client = FundAPIClient()
        try:
            result = await fund_client.get_support_list(page_no=1, num_of_rows=1)
            results['fund'] = result.get('response', {}).get('header', {}).get('resultCode') == '00'
        except:
            results['fund'] = False
        
        # 4. 평가 API
        evaluation_client = FundEvaluationAPIClient()
        try:
            result = await evaluation_client.get_evaluation_list(page_no=1, num_of_rows=1)
            results['evaluation'] = result.get('response', {}).get('header', {}).get('resultCode') == '00'
        except:
            results['evaluation'] = False
        
        # 5. 종합 API
        comprehensive_client = FundComprehensiveAPIClient()
        try:
            result = await comprehensive_client.get_comprehensive_list(page_no=1, num_of_rows=1)
            results['comprehensive'] = result.get('response', {}).get('header', {}).get('resultCode') == '00'
        except:
            results['comprehensive'] = False
        
        # 최소 3개 이상 API가 작동해야 성공
        success_count = sum(1 for v in results.values() if v)
        assert success_count >= 3, f"API 연결 실패: {results}"
        
        return results


if __name__ == "__main__":
    # pytest가 없을 경우 직접 실행
    async def main():
        print("=== 공공데이터 API 클라이언트 테스트 ===\n")
        
        # 시설 API 테스트
        facilities_test = TestFacilitiesAPI()
        try:
            await facilities_test.test_get_facilities_list()
            print("✅ 시설 API 테스트 성공")
        except Exception as e:
            print(f"❌ 시설 API 테스트 실패: {e}")
        
        # 성과금 API 테스트
        performance_test = TestPerformanceAPI()
        try:
            await performance_test.test_get_performance_rewards()
            print("✅ 성과금 API 테스트 성공")
        except Exception as e:
            print(f"❌ 성과금 API 테스트 실패: {e}")
        
        # 기금 API 테스트
        fund_test = TestFundAPI()
        try:
            await fund_test.test_get_support_list()
            print("✅ 기금 API 테스트 성공")
        except Exception as e:
            print(f"❌ 기금 API 테스트 실패: {e}")
        
        # 통합 테스트
        integrated_test = TestIntegratedAPIs()
        try:
            results = await integrated_test.test_all_apis_connectivity()
            print(f"\n📊 통합 테스트 결과: {results}")
        except Exception as e:
            print(f"❌ 통합 테스트 실패: {e}")
    
    asyncio.run(main())
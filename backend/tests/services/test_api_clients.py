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
                assert 'medal_count' in data
                assert 'athlete_count' in data
    
    @pytest.mark.asyncio
    async def test_medal_and_athlete_aggregation(self, monkeypatch):
        """메달 및 선수 집계 테스트"""
        client = PerformanceAPIClient()
        
        async def mock_get_performance_rewards(self, payment_month=None, **kwargs):
            data_map = {
                "202301": [{
                    "pmt_yymm": "202301",
                    "spm_nm": "수영",
                    "mmamt": "1000",
                    "medal_se": "금메달",
                    "rcptn_nm": "홍길동",
                }],
                "202302": [{
                    "pmt_yymm": "202302",
                    "spm_nm": "수영",
                    "mmamt": "2000",
                    "medal_se": "은메달",
                    "rcptn_nm": "김철수",
                }],
                "202303": [{
                    "pmt_yymm": "202303",
                    "spm_nm": "양궁",
                    "mmamt": "3000",
                    "medal_se": "금메달",
                    "rcptn_nm": "김영희",
                }],
                "202304": [{
                    "pmt_yymm": "202304",
                    "spm_nm": "수영",
                    "mmamt": "500",
                    "medal_se": "금메달",
                    "rcptn_nm": "홍길동",  # 동일 선수
                }],
            }
            items = data_map.get(payment_month, [])
            return {"response": {"body": {"items": {"item": items}}}}
        
        monkeypatch.setattr(PerformanceAPIClient, "get_performance_rewards", mock_get_performance_rewards)
        
        result = await client.get_performance_by_sport(2023)
        
        # 수영 종목 검증
        assert result["수영"]["medal_count"]["금"] == 2
        assert result["수영"]["medal_count"]["은"] == 1
        assert result["수영"]["athlete_count"] == 2  # 홍길동, 김철수 (중복 제거)
        
        # 양궁 종목 검증
        assert result["양궁"]["medal_count"]["금"] == 1
        assert result["양궁"]["athlete_count"] == 1  # 김영희


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
    
    def test_parse_fund_data_contains_amounts(self):
        """지원실적 파싱 시 금액 필드 확인"""
        client = FundAPIClient()
        
        mock_data = {
            'biz_yr': '2023',
            'reqst_instt_nm': '서울특별시 체육회',
            'dtbz_nm': '축구 지원 사업',
            'govsuby_amt': '1000',
            'dvdc_amt': '800',
            'thisgive_coin_amt': '600'
        }
        
        parsed = client.parse_fund_data(mock_data)
        
        assert parsed['support_amount'] == 800
        assert parsed['execution_amount'] == 600
    
    @pytest.mark.asyncio
    async def test_budget_aggregations_use_new_keys(self, monkeypatch):
        """예산 집계 메서드가 새로운 필드를 사용하는지 확인"""
        sample = [
            {
                'biz_yr': '2023',
                'reqst_instt_nm': '서울특별시 체육회',
                'dtbz_nm': '축구 지원 사업',
                'govsuby_amt': '1000',
                'dvdc_amt': '800',
                'thisgive_coin_amt': '600'
            },
            {
                'biz_yr': '2023',
                'reqst_instt_nm': '부산광역시 체육회',
                'dtbz_nm': '야구 지원 사업',
                'govsuby_amt': '2000',
                'dvdc_amt': '1500',
                'thisgive_coin_amt': '1200'
            }
        ]
        
        async def mock_get_all(self, year, organization=None):
            return sample
        
        monkeypatch.setattr(FundAPIClient, 'get_all_fund_support', mock_get_all)
        
        client = FundAPIClient()
        
        # 지역별 예산 집계 테스트
        region_budget = await client.get_budget_by_region(2023)
        assert region_budget['서울'] == 800
        assert region_budget['부산'] == 1500
        
        # 종목별 예산 집계 테스트
        sport_budget = await client.get_budget_by_sport(2023)
        assert sport_budget['축구'] == 800
        assert sport_budget['야구'] == 1500
        
        # 효율성 분석 테스트
        analysis = await client.get_budget_efficiency_analysis(2023)
        assert analysis['total_budget'] == 2300  # 800 + 1500
        assert analysis['total_execution'] == 1800  # 600 + 1200
        assert analysis['by_region']['서울']['budget'] == 800
        assert analysis['by_region']['서울']['execution'] == 600
        assert analysis['by_region']['부산']['budget'] == 1500
        assert analysis['by_region']['부산']['execution'] == 1200
        assert analysis['by_sport']['축구']['budget'] == 800
        assert analysis['by_sport']['축구']['execution'] == 600
        assert analysis['by_sport']['야구']['budget'] == 1500
        assert analysis['by_sport']['야구']['execution'] == 1200


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
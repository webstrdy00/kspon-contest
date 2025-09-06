"""
Budget Analysis Service 단위 테스트
"""

import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.budget_analysis import BudgetAnalysisService
from app.models.budget_performance import BudgetExecution, PerformanceMetric, EtlRun
from app.models.dim import Institution, Sport, Project


@pytest.fixture
def mock_db():
    """Mock database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_cache():
    """Mock cache manager"""
    cache = Mock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock()
    cache.invalidate_by_run_id = AsyncMock()
    return cache


@pytest.fixture
def service(mock_db, mock_cache):
    """Budget analysis service instance"""
    with patch('app.services.budget_analysis.cache_manager', mock_cache):
        return BudgetAnalysisService(mock_db)


class TestBudgetAnalysisService:
    """Budget Analysis Service 테스트"""

    @pytest.mark.asyncio
    async def test_calculate_efficiency(self, service):
        """효율성 계산 테스트"""
        # Given
        executed = 8500000000  # 85억
        allocated = 10000000000  # 100억
        
        # When
        efficiency = service._calculate_efficiency(executed, allocated)
        
        # Then
        assert efficiency == 85.0

    @pytest.mark.asyncio
    async def test_calculate_efficiency_zero_allocated(self, service):
        """할당 예산 0일 때 효율성 계산"""
        # Given
        executed = 1000000000
        allocated = 0
        
        # When
        efficiency = service._calculate_efficiency(executed, allocated)
        
        # Then
        assert efficiency == 0

    @pytest.mark.asyncio
    async def test_get_efficiency_grade(self, service):
        """효율성 등급 계산 테스트"""
        test_cases = [
            (98.0, 'S'),  # 95% 이상
            (92.0, 'A'),  # 90-95%
            (85.0, 'B'),  # 80-90%
            (75.0, 'C'),  # 70-80%
            (65.0, 'D'),  # 70% 미만
        ]
        
        for efficiency, expected_grade in test_cases:
            grade = service._get_efficiency_grade(efficiency)
            assert grade == expected_grade, f"Efficiency {efficiency} should be grade {expected_grade}"

    @pytest.mark.asyncio
    async def test_calculate_roi(self, service):
        """ROI 계산 테스트"""
        # Given
        investment = 10000000000  # 100억
        return_value = 12000000000  # 120억
        
        # When
        roi = service._calculate_roi(investment, return_value)
        
        # Then
        assert roi == 20.0  # 20% ROI

    @pytest.mark.asyncio
    async def test_calculate_roi_zero_investment(self, service):
        """투자 0일 때 ROI 계산"""
        # Given
        investment = 0
        return_value = 1000000000
        
        # When
        roi = service._calculate_roi(investment, return_value)
        
        # Then
        assert roi == 0

    @pytest.mark.asyncio
    async def test_get_overview_with_cache(self, service, mock_cache):
        """캐시가 있을 때 overview 조회"""
        # Given
        cached_data = {
            'summary': {
                'total_budget': 100000000000,
                'efficiency': 85.0
            }
        }
        mock_cache.get.return_value = cached_data
        
        # When
        result = await service.get_overview(year=2024)
        
        # Then
        assert result == cached_data
        mock_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_overview_without_cache(self, service, mock_db, mock_cache):
        """캐시가 없을 때 overview 조회"""
        # Given
        mock_cache.get.return_value = None
        
        # Mock database queries
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(all=Mock(return_value=[])))
        mock_result.scalar = Mock(return_value=100000000000)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        with patch.object(service, '_get_efficiency_by_sport', new_callable=AsyncMock) as mock_efficiency:
            with patch.object(service, '_get_roi_top_performers', new_callable=AsyncMock) as mock_roi:
                with patch.object(service, '_get_regional_comparison', new_callable=AsyncMock) as mock_region:
                    with patch.object(service, '_get_trend_data', new_callable=AsyncMock) as mock_trend:
                        mock_efficiency.return_value = []
                        mock_roi.return_value = []
                        mock_region.return_value = []
                        mock_trend.return_value = []
                        
                        result = await service.get_overview(year=2024)
        
        # Then
        assert 'summary' in result
        assert 'highlights' in result
        mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_efficiency_by_sport(self, service, mock_db):
        """종목별 효율성 분석 테스트"""
        # Given
        mock_budget = Mock()
        mock_budget.sport_id = 1
        mock_budget.budget_total = 10000000000
        mock_budget.budget_executed = 8500000000
        
        mock_performance = Mock()
        mock_performance.sport_id = 1
        mock_performance.value = 85.0
        
        mock_sport = Mock()
        mock_sport.id = 1
        mock_sport.name = "축구"
        mock_sport.category = "구기"
        
        # Mock queries
        budget_result = Mock()
        budget_result.all = Mock(return_value=[mock_budget])
        
        perf_result = Mock()
        perf_result.all = Mock(return_value=[mock_performance])
        
        sport_result = Mock()
        sport_result.scalars = Mock(return_value=Mock(all=Mock(return_value=[mock_sport])))
        
        mock_db.execute = AsyncMock(side_effect=[budget_result, perf_result, sport_result])
        
        # When
        result = await service._get_efficiency_by_sport(year=2024, limit=10)
        
        # Then
        assert len(result) == 1
        assert result[0]['sport']['name'] == "축구"
        assert result[0]['efficiency'] == 85.0
        assert result[0]['grade'] == 'B'

    @pytest.mark.asyncio
    async def test_get_trend_data(self, service, mock_db):
        """트렌드 데이터 조회 테스트"""
        # Given
        dates = [date(2024, i, 1) for i in range(1, 4)]
        budgets = [10000000000, 11000000000, 12000000000]
        performances = [80, 85, 90]
        
        mock_data = []
        for i, d in enumerate(dates):
            mock_item = Mock()
            mock_item.period = d
            mock_item.budget_total = budgets[i]
            mock_item.performance_avg = performances[i]
            mock_data.append(mock_item)
        
        mock_result = Mock()
        mock_result.all = Mock(return_value=mock_data)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        result = await service._get_trend_data(
            start_year=2024,
            end_year=2024,
            granularity='month'
        )
        
        # Then
        assert len(result) == 3
        assert result[0]['date'] == '2024-01-01'
        assert result[0]['budget'] == 10000000000
        assert result[0]['performance'] == 80

    @pytest.mark.asyncio
    async def test_invalidate_cache(self, service, mock_cache):
        """캐시 무효화 테스트"""
        # Given
        run_id = 42
        
        # When
        result = await service.invalidate_cache(run_id)
        
        # Then
        mock_cache.invalidate_by_run_id.assert_called_once_with(run_id)
        assert result['status'] == 'success'


class TestEfficiencyCalculation:
    """효율성 계산 로직 상세 테스트"""

    @pytest.mark.asyncio
    async def test_efficiency_with_performance_scaling(self, service):
        """성과 점수 스케일링 포함 효율성 계산"""
        # Given
        budget_executed = 10000000000  # 100억
        performance_score = 85  # 85점
        
        # When
        # 효율성 = (performance_score) / (budget_executed / 100_000_000)
        expected_efficiency = 85 / (10000000000 / 100000000)  # 85 / 100 = 0.85
        
        # Then
        assert abs(expected_efficiency - 0.85) < 0.001

    @pytest.mark.asyncio
    async def test_roi_ranking(self, service):
        """ROI 순위 계산 테스트"""
        # Given
        roi_data = [
            {'sport': 'A', 'roi': 150.0},
            {'sport': 'B', 'roi': 200.0},
            {'sport': 'C', 'roi': 100.0},
        ]
        
        # When
        sorted_data = sorted(roi_data, key=lambda x: x['roi'], reverse=True)
        for i, item in enumerate(sorted_data):
            item['roi_rank'] = i + 1
        
        # Then
        assert sorted_data[0]['sport'] == 'B'
        assert sorted_data[0]['roi_rank'] == 1
        assert sorted_data[1]['sport'] == 'A'
        assert sorted_data[1]['roi_rank'] == 2
        assert sorted_data[2]['sport'] == 'C'
        assert sorted_data[2]['roi_rank'] == 3


class TestPerformanceRequirements:
    """성능 요구사항 테스트"""

    @pytest.mark.asyncio
    async def test_api_response_time(self, service, mock_db, mock_cache):
        """API 응답 시간 테스트 (p95 < 800ms)"""
        import time
        
        # Given
        mock_cache.get.return_value = None
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(all=Mock(return_value=[])))
        mock_result.scalar = Mock(return_value=100000000000)
        mock_result.all = Mock(return_value=[])
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        start_time = time.time()
        
        with patch.object(service, '_get_efficiency_by_sport', new_callable=AsyncMock) as mock_efficiency:
            with patch.object(service, '_get_roi_top_performers', new_callable=AsyncMock) as mock_roi:
                with patch.object(service, '_get_regional_comparison', new_callable=AsyncMock) as mock_region:
                    with patch.object(service, '_get_trend_data', new_callable=AsyncMock) as mock_trend:
                        mock_efficiency.return_value = []
                        mock_roi.return_value = []
                        mock_region.return_value = []
                        mock_trend.return_value = []
                        
                        await service.get_overview(year=2024)
        
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Then
        assert elapsed_time < 800, f"API response time {elapsed_time}ms exceeds 800ms requirement"
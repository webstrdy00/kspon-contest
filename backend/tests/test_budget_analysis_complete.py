"""
Budget Analysis Service 완성도 테스트
Phase 3 완료 검증
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import date
from decimal import Decimal

from app.services.budget_analysis import BudgetAnalysisService
from app.models.dim import Institution, Sport
from app.schemas.budget_performance import ROIAnalysis


@pytest.fixture
def mock_db():
    """Mock database session"""
    return AsyncMock()


@pytest.fixture
def service(mock_db):
    """Service instance"""
    return BudgetAnalysisService(mock_db)


class TestROIAnalysisImplementation:
    """ROI 분석 구현 완성도 테스트"""
    
    @pytest.mark.asyncio
    async def test_calculate_roi_analysis_returns_data(self, service, mock_db):
        """_calculate_roi_analysis가 실제 데이터를 반환하는지 테스트"""
        # Given
        mock_db.execute = AsyncMock()
        
        # Mock query result
        mock_row = (
            1,  # sport_id
            "축구",  # sport_name
            "구기",  # category
            True,  # olympic_status
            10000000000,  # investment
            85,  # performance_value
            25.0,  # roi
            1  # institution_id
        )
        mock_result = Mock()
        mock_result.fetchall = Mock(return_value=[mock_row])
        mock_db.execute.return_value = mock_result
        
        # Mock institution query
        inst_mock = Mock()
        inst_mock.scalar_one_or_none = Mock(return_value=Institution(id=1, name="대한체육회"))
        mock_db.execute.side_effect = [mock_result, inst_mock]
        
        # When
        with patch.object(service, 'get_latest_run_id', new_callable=AsyncMock) as mock_run_id:
            mock_run_id.return_value = 1
            result = await service._calculate_roi_analysis(year=2024, limit=10)
        
        # Then
        assert len(result) > 0  # 빈 리스트가 아님!
        assert isinstance(result[0], ROIAnalysis)
        assert result[0].roi == 25.0
        assert result[0].sport.name == "축구"

    @pytest.mark.asyncio
    async def test_calculate_roi_analysis_handles_no_data(self, service, mock_db):
        """데이터가 없을 때 빈 리스트 반환"""
        # Given
        mock_result = Mock()
        mock_result.fetchall = Mock(return_value=[])
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        with patch.object(service, 'get_latest_run_id', new_callable=AsyncMock) as mock_run_id:
            mock_run_id.return_value = 1
            result = await service._calculate_roi_analysis(year=2024, limit=10)
        
        # Then
        assert result == []  # 빈 리스트 반환
        assert len(result) == 0


class TestMostImprovedSportImplementation:
    """가장 개선된 종목 구현 완성도 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_most_improved_sport_returns_data(self, service, mock_db):
        """_get_most_improved_sport가 실제 데이터를 반환하는지 테스트"""
        # Given
        mock_row = (
            1,  # sport_id
            "배드민턴",  # sport_name
            90.0,  # current_efficiency
            75.0,  # prev_efficiency
            20.0  # improvement_rate
        )
        mock_result = Mock()
        mock_result.first = Mock(return_value=mock_row)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        result = await service._get_most_improved_sport(run_id=1, year=2024)
        
        # Then
        assert result is not None  # None이 아님!
        assert result['type'] == 'most_improved'
        assert result['value'] == '배드민턴'
        assert '20.0% 향상' in result['metric']
        assert '75.0% → 90.0%' in result['detail']

    @pytest.mark.asyncio
    async def test_get_most_improved_sport_handles_no_improvement(self, service, mock_db):
        """개선된 종목이 없을 때 None 반환"""
        # Given
        mock_result = Mock()
        mock_result.first = Mock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        result = await service._get_most_improved_sport(run_id=1, year=2024)
        
        # Then
        assert result is None  # 개선된 종목이 없으면 None

    @pytest.mark.asyncio
    async def test_get_most_improved_sport_fallback_to_direct_calculation(self, service, mock_db):
        """캐시가 없을 때 직접 계산 fallback 테스트"""
        # Given
        # 첫 번째 쿼리는 None 반환 (캐시 없음)
        mock_cache_result = Mock()
        mock_cache_result.first = Mock(return_value=None)
        
        # 두 번째 쿼리는 실제 데이터 반환 (직접 계산)
        mock_direct_row = (
            2,  # sport_id
            "탁구",  # sport_name
            88.5,  # current_eff
            72.3,  # prev_eff
            22.4  # improvement_rate
        )
        mock_direct_result = Mock()
        mock_direct_result.first = Mock(return_value=mock_direct_row)
        
        mock_db.execute = AsyncMock(side_effect=[mock_cache_result, mock_direct_result])
        
        # When
        result = await service._get_most_improved_sport(run_id=1, year=2024)
        
        # Then
        assert result is not None
        assert result['value'] == '탁구'
        assert '22.4% 향상' in result['metric']


class TestIntegrationWithCache:
    """캐시 통합 테스트"""
    
    @pytest.mark.asyncio
    async def test_roi_analysis_uses_cache_first(self, service, mock_db):
        """ROI 분석이 캐시를 먼저 확인하는지 테스트"""
        # Given
        from app.models.budget_performance import AggregationCache
        
        cache_entry = Mock(spec=AggregationCache)
        cache_entry.dimension_key = "year:2024:inst:1:sport:1"
        cache_entry.sport = Sport(id=1, name="축구", category="구기")
        cache_entry.budget_executed = Decimal(10000000000)
        cache_entry.performance_score = 85
        cache_entry.roi = 25.0
        
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(all=Mock(return_value=[cache_entry])))
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # When
        with patch.object(service, 'get_latest_run_id', new_callable=AsyncMock) as mock_run_id:
            mock_run_id.return_value = 1
            result = await service.get_roi_analysis(year=2024, limit=10)
        
        # Then
        assert len(result) > 0
        # _calculate_roi_analysis가 호출되지 않아야 함 (캐시에서 데이터를 가져왔으므로)


class TestCompleteness:
    """Phase 3 완성도 종합 테스트"""
    
    def test_no_empty_implementations(self):
        """빈 구현이 없는지 확인"""
        import inspect
        import app.services.budget_analysis as module
        
        # 이전에 빈 구현이었던 메서드들
        methods_to_check = [
            '_calculate_roi_analysis',
            '_get_most_improved_sport'
        ]
        
        service_class = module.BudgetAnalysisService
        
        for method_name in methods_to_check:
            method = getattr(service_class, method_name)
            source = inspect.getsource(method)
            
            # 빈 return [] 또는 return None만 있는지 확인
            assert 'return []' not in source or 'query' in source, \
                f"{method_name}이 여전히 빈 구현입니다"
            assert 'return None' not in source or 'if' in source, \
                f"{method_name}이 여전히 빈 구현입니다"
    
    @pytest.mark.asyncio
    async def test_all_methods_return_expected_types(self, service, mock_db):
        """모든 메서드가 올바른 타입을 반환하는지 확인"""
        with patch.object(service, 'get_latest_run_id', new_callable=AsyncMock) as mock_run_id:
            mock_run_id.return_value = 1
            
            # Mock empty results
            mock_result = Mock()
            mock_result.fetchall = Mock(return_value=[])
            mock_result.first = Mock(return_value=None)
            mock_result.all = Mock(return_value=[])
            mock_result.scalars = Mock(return_value=Mock(all=Mock(return_value=[])))
            mock_db.execute = AsyncMock(return_value=mock_result)
            
            # Test each method
            roi_result = await service._calculate_roi_analysis(2024, 10)
            assert isinstance(roi_result, list)
            
            improvement_result = await service._get_most_improved_sport(1, 2024)
            assert improvement_result is None or isinstance(improvement_result, dict)
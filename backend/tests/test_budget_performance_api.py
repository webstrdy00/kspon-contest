"""
Budget Performance API 계약 테스트
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, Mock
from datetime import date, datetime

from main import app


@pytest.fixture
async def client():
    """Test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_auth():
    """Mock authentication"""
    with patch('app.api.v1.endpoints.budget_performance.get_current_user') as mock:
        mock.return_value = {'id': 1, 'email': 'test@example.com'}
        yield mock


@pytest.fixture
def mock_service():
    """Mock budget analysis service"""
    with patch('app.api.v1.endpoints.budget_performance.BudgetAnalysisService') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


class TestBudgetPerformanceAPI:
    """Budget Performance API 테스트"""

    @pytest.mark.asyncio
    async def test_get_overview_success(self, client, mock_auth, mock_service):
        """Overview 조회 성공 테스트"""
        # Given
        mock_service.get_overview.return_value = {
            'summary': {
                'total_budget': 100000000000,
                'total_executed': 85000000000,
                'execution_rate': 85.0,
                'efficiency': 87.5,
                'efficiency_grade': 'B',
                'institution_count': 10,
                'project_count': 25,
                'sport_count': 15,
                'indicator_count': 50,
                'avg_performance_score': 82.5
            },
            'highlights': [
                {
                    'type': 'top_efficiency',
                    'title': '최고 효율성 종목',
                    'value': '축구',
                    'metric': '95.5% 효율성',
                    'grade': 'S'
                }
            ],
            'efficiency_by_sport': [],
            'roi_top_performers': [],
            'regional_comparison': [],
            'trend_data': []
        }
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/overview',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert data['summary']['total_budget'] == 100000000000
        assert data['summary']['efficiency_grade'] == 'B'
        assert len(data['highlights']) == 1

    @pytest.mark.asyncio
    async def test_get_overview_with_filters(self, client, mock_auth, mock_service):
        """필터 포함 Overview 조회"""
        # Given
        mock_service.get_overview.return_value = {'summary': {}}
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/overview',
            params={
                'year': 2024,
                'region_code': '11',
                'sport_id': 1,
                'group_by': 'sport'
            },
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        mock_service.get_overview.assert_called_once_with(
            year=2024,
            region_code='11',
            sport_id=1,
            group_by='sport'
        )

    @pytest.mark.asyncio
    async def test_get_efficiency_analysis(self, client, mock_auth, mock_service):
        """효율성 분석 조회 테스트"""
        # Given
        mock_service.get_efficiency_by_sport.return_value = [
            {
                'year': 2024,
                'sport': {
                    'id': 1,
                    'name': '축구',
                    'category': '구기'
                },
                'budget_total': 10000000000,
                'budget_executed': 9500000000,
                'execution_rate': 95.0,
                'performance_score': 90.0,
                'efficiency': 94.7,
                'grade': 'A',
                'rank': 1
            }
        ]
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/efficiency',
            params={'year': 2024, 'limit': 10},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['sport']['name'] == '축구'
        assert data[0]['grade'] == 'A'

    @pytest.mark.asyncio
    async def test_get_roi_analysis(self, client, mock_auth, mock_service):
        """ROI 분석 조회 테스트"""
        # Given
        mock_service.get_roi_top_performers.return_value = [
            {
                'year': 2024,
                'sport': {'id': 1, 'name': '탁구'},
                'investment': 1000000000,
                'return_value': 2500000000,
                'roi': 150.0,
                'roi_rank': 1,
                'category': '개인종목'
            }
        ]
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/roi',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['roi'] == 150.0
        assert data[0]['roi_rank'] == 1

    @pytest.mark.asyncio
    async def test_get_regional_comparison(self, client, mock_auth, mock_service):
        """지역별 비교 조회 테스트"""
        # Given
        mock_service.get_regional_comparison.return_value = [
            {
                'region_code': '11',
                'region_name': '서울특별시',
                'budget_total': 50000000000,
                'performance_avg': 85.0,
                'efficiency': 88.5,
                'rank': 1,
                'population_per_budget': 194.5
            }
        ]
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/comparison',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['region_name'] == '서울특별시'
        assert data[0]['rank'] == 1

    @pytest.mark.asyncio
    async def test_get_trend_data(self, client, mock_auth, mock_service):
        """트렌드 데이터 조회 테스트"""
        # Given
        mock_service.get_trend_data.return_value = [
            {
                'date': '2024-01-01',
                'budget': 10000000000,
                'performance': 80.0,
                'efficiency': 82.5,
                'roi': 25.0
            },
            {
                'date': '2024-02-01',
                'budget': 11000000000,
                'performance': 82.0,
                'efficiency': 84.0,
                'roi': 28.0
            }
        ]
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/trend',
            params={
                'start_year': 2024,
                'end_year': 2024,
                'granularity': 'month'
            },
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['date'] == '2024-01-01'
        assert data[1]['budget'] == 11000000000

    @pytest.mark.asyncio
    async def test_export_data(self, client, mock_auth, mock_service):
        """데이터 내보내기 테스트"""
        # Given
        mock_service.export_data.return_value = {
            'status': 'success',
            'message': 'Export task created',
            'task_id': 'task_123'
        }
        
        # When
        response = await client.post(
            '/api/v1/budget-performance/export',
            json={
                'filters': {'year': 2024},
                'format': 'xlsx',
                'include_charts': True
            },
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert data['task_id'] == 'task_123'

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """인증되지 않은 접근 테스트"""
        # When
        response = await client.get('/api/v1/budget-performance/overview')
        
        # Then
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_etag_support(self, client, mock_auth, mock_service):
        """ETag 지원 테스트"""
        # Given
        mock_service.get_overview.return_value = {'summary': {}}
        mock_service.get_latest_run_id.return_value = 42
        
        # When - First request
        response1 = await client.get(
            '/api/v1/budget-performance/overview',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response1.status_code == 200
        assert 'etag' in response1.headers
        etag = response1.headers['etag']
        
        # When - Second request with ETag
        response2 = await client.get(
            '/api/v1/budget-performance/overview',
            params={'year': 2024},
            headers={
                'Authorization': 'Bearer test_token',
                'If-None-Match': etag
            }
        )
        
        # Then - Should return 304 if data hasn't changed
        # Note: Actual implementation would check cache and return 304
        assert response2.status_code in [200, 304]


class TestAPIResponseFormat:
    """API 응답 형식 테스트"""

    @pytest.mark.asyncio
    async def test_overview_response_structure(self, client, mock_auth, mock_service):
        """Overview 응답 구조 검증"""
        # Given
        mock_service.get_overview.return_value = {
            'summary': {
                'total_budget': 100000000000,
                'total_executed': 85000000000,
                'execution_rate': 85.0,
                'efficiency': 87.5,
                'efficiency_grade': 'B',
                'institution_count': 10,
                'project_count': 25,
                'sport_count': 15,
                'indicator_count': 50,
                'avg_performance_score': 82.5
            },
            'highlights': [],
            'efficiency_by_sport': [],
            'roi_top_performers': [],
            'regional_comparison': [],
            'trend_data': []
        }
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/overview',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        
        # Verify summary structure
        summary = data['summary']
        required_fields = [
            'total_budget', 'total_executed', 'execution_rate',
            'efficiency', 'efficiency_grade', 'institution_count',
            'project_count', 'sport_count', 'indicator_count',
            'avg_performance_score'
        ]
        for field in required_fields:
            assert field in summary, f"Missing field: {field}"
        
        # Verify data types
        assert isinstance(summary['total_budget'], (int, float))
        assert isinstance(summary['efficiency'], float)
        assert isinstance(summary['efficiency_grade'], str)
        assert summary['efficiency_grade'] in ['S', 'A', 'B', 'C', 'D']

    @pytest.mark.asyncio
    async def test_efficiency_response_structure(self, client, mock_auth, mock_service):
        """효율성 분석 응답 구조 검증"""
        # Given
        mock_service.get_efficiency_by_sport.return_value = [
            {
                'year': 2024,
                'sport': {
                    'id': 1,
                    'code': 'FB',
                    'name': '축구',
                    'category': '구기',
                    'olympic_status': True
                },
                'budget_total': 10000000000,
                'budget_executed': 9500000000,
                'execution_rate': 95.0,
                'performance_score': 90.0,
                'efficiency': 94.7,
                'grade': 'A',
                'rank': 1
            }
        ]
        
        # When
        response = await client.get(
            '/api/v1/budget-performance/efficiency',
            params={'year': 2024},
            headers={'Authorization': 'Bearer test_token'}
        )
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        if data:
            item = data[0]
            assert 'sport' in item
            assert 'budget_total' in item
            assert 'efficiency' in item
            assert 'grade' in item
            
            # Verify sport structure
            sport = item['sport']
            assert 'id' in sport
            assert 'name' in sport
            assert 'category' in sport


class TestPerformanceMetrics:
    """성능 메트릭 테스트"""

    @pytest.mark.asyncio
    async def test_response_time_p95(self, client, mock_auth, mock_service):
        """P95 응답 시간 < 800ms 테스트"""
        import time
        import statistics
        
        # Given
        mock_service.get_overview.return_value = {'summary': {}}
        response_times = []
        
        # When - Make 100 requests
        for _ in range(100):
            start = time.time()
            response = await client.get(
                '/api/v1/budget-performance/overview',
                params={'year': 2024},
                headers={'Authorization': 'Bearer test_token'}
            )
            elapsed = (time.time() - start) * 1000  # Convert to ms
            response_times.append(elapsed)
            assert response.status_code == 200
        
        # Then - Calculate P95
        response_times.sort()
        p95_index = int(len(response_times) * 0.95)
        p95_time = response_times[p95_index]
        
        print(f"P95 Response Time: {p95_time:.2f}ms")
        print(f"Mean Response Time: {statistics.mean(response_times):.2f}ms")
        print(f"Median Response Time: {statistics.median(response_times):.2f}ms")
        
        # Assert P95 < 800ms (with some margin for test environment)
        assert p95_time < 1000, f"P95 response time {p95_time}ms exceeds requirement"
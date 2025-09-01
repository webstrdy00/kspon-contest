"""
API 엔드포인트 통합 테스트
"""
import pytest
from httpx import AsyncClient
from datetime import datetime


class TestAuthEndpoints:
    """인증 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_register(self, client: AsyncClient):
        """회원가입 테스트"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123",
                "username": "newuser"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient, test_user):
        """로그인 테스트"""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpassword"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient, auth_headers):
        """현재 사용자 정보 조회 테스트"""
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"


class TestSupplyDemandEndpoints:
    """수요-공급 분석 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_supply_demand_analysis(self, client: AsyncClient):
        """수요-공급 분석 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/analysis/supply-demand/11",
            params={"facility_type": "수영장"}
        )
        # 지역 데이터가 없을 수 있으므로 상태 코드만 확인
        assert response.status_code in [200, 404]
    
    @pytest.mark.asyncio
    async def test_mismatch_regions(self, client: AsyncClient):
        """불일치 지역 탐지 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/analysis/mismatch-regions",
            params={"threshold": 0.8, "limit": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert "regions" in data
        assert "threshold" in data
    
    @pytest.mark.asyncio
    async def test_accessibility_analysis(self, client: AsyncClient):
        """접근성 분석 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/analysis/accessibility",
            params={
                "lat": 37.5665,
                "lng": 126.9780,
                "max_distance_km": 3.0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "location" in data
        assert "nearby_facilities_count" in data
        assert "accessibility_score" in data
    
    @pytest.mark.asyncio
    async def test_facilities_map_data(self, client: AsyncClient):
        """시설 지도 데이터 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/facilities/map-data",
            params={"page": 1, "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "FeatureCollection"
        assert "features" in data
        assert "metadata" in data
    
    @pytest.mark.asyncio
    async def test_facility_types(self, client: AsyncClient):
        """시설 유형 목록 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/facilities/types"
        )
        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert "total_types" in data
    
    @pytest.mark.asyncio
    async def test_regional_demand_scores(self, client: AsyncClient):
        """지역별 수요 점수 테스트"""
        response = await client.get(
            "/api/v1/supply-demand/regions/demand-scores"
        )
        assert response.status_code == 200
        data = response.json()
        assert "regions" in data


class TestFacilitiesEndpoints:
    """시설 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_get_facilities(self, client: AsyncClient):
        """시설 목록 조회 테스트"""
        response = await client.get(
            "/api/v1/facilities/",
            params={"page": 1, "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
    
    @pytest.mark.asyncio
    async def test_search_facilities(self, client: AsyncClient):
        """시설 검색 테스트"""
        response = await client.get(
            "/api/v1/facilities/search",
            params={"q": "수영장", "region": "서울"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestProposalsEndpoints:
    """정책 제안 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_create_proposal(self, client: AsyncClient, auth_headers):
        """제안 생성 테스트"""
        response = await client.post(
            "/api/v1/proposals/",
            headers=auth_headers,
            json={
                "title": "테스트 정책 제안",
                "content": "이것은 테스트 제안입니다.",
                "category": "시설개선"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "테스트 정책 제안"
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_get_proposals(self, client: AsyncClient):
        """제안 목록 조회 테스트"""
        response = await client.get(
            "/api/v1/proposals/",
            params={"page": 1, "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


class TestReportsEndpoints:
    """리포트 API 테스트"""
    
    @pytest.mark.asyncio
    async def test_generate_report(self, client: AsyncClient, auth_headers):
        """리포트 생성 테스트"""
        response = await client.post(
            "/api/v1/reports/generate",
            headers=auth_headers,
            json={
                "region_code": "11",
                "report_type": "basic",
                "include_charts": True
            }
        )
        # 리포트 생성은 시간이 걸릴 수 있음
        assert response.status_code in [200, 202]
    
    @pytest.mark.asyncio
    async def test_get_reports(self, client: AsyncClient, auth_headers):
        """리포트 목록 조회 테스트"""
        response = await client.get(
            "/api/v1/reports/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestHealthCheck:
    """헬스체크 테스트"""
    
    @pytest.mark.asyncio
    async def test_health(self, client: AsyncClient):
        """헬스체크 엔드포인트 테스트"""
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
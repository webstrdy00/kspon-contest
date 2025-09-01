"""
수요-공급 분석 서비스
체육시설 데이터와 지역 수요 데이터를 결합하여 불일치 지역을 탐지
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from geopy.distance import geodesic

from app.models.facility import SportsFacility, FacilityDemand
from app.models.region import Region
from app.services.facilities_api_client import FacilitiesAPIClient
from app.etl.csv_processor import CSVDataProcessor

logger = logging.getLogger(__name__)


class SupplyDemandAnalyzer:
    """수요-공급 분석 클래스"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.facilities_client = FacilitiesAPIClient()
        self.csv_processor = CSVDataProcessor()
        
    async def calculate_supply_demand_ratio(
        self,
        region_code: str,
        facility_type: Optional[str] = None,
        radius_km: float = 5.0
    ) -> Dict[str, Any]:
        """
        지역별 수요-공급 비율 계산
        
        Args:
            region_code: 지역 코드
            facility_type: 시설 유형 (선택)
            radius_km: 분석 반경 (km)
            
        Returns:
            수요-공급 분석 결과
        """
        try:
            # 1. 지역 정보 조회
            region_query = select(Region).where(Region.code == region_code)
            region_result = await self.db.execute(region_query)
            region = region_result.scalar_one_or_none()
            
            if not region:
                logger.warning(f"지역 코드 {region_code}를 찾을 수 없습니다.")
                return {"error": "Region not found"}
            
            # 2. 시설 공급 데이터 조회
            facility_query = select(SportsFacility).where(
                SportsFacility.region_code == region_code
            )
            if facility_type:
                facility_query = facility_query.where(
                    SportsFacility.facility_type == facility_type
                )
            
            facilities_result = await self.db.execute(facility_query)
            facilities = facilities_result.scalars().all()
            
            # 3. 수요 데이터 조회
            demand_query = select(FacilityDemand).where(
                FacilityDemand.region_code == region_code
            )
            if facility_type:
                demand_query = demand_query.where(
                    FacilityDemand.facility_type == facility_type
                )
            
            demand_result = await self.db.execute(demand_query)
            demands = demand_result.scalars().all()
            
            # 4. 공급 지표 계산
            supply_metrics = self._calculate_supply_metrics(
                facilities, 
                region.population if region else 0
            )
            
            # 5. 수요 지표 계산
            demand_metrics = self._calculate_demand_metrics(demands)
            
            # 6. 수요-공급 비율 계산
            supply_demand_ratio = self._calculate_ratio(
                supply_metrics, 
                demand_metrics
            )
            
            # 7. 불일치 수준 판정
            mismatch_level = self._determine_mismatch_level(supply_demand_ratio)
            
            return {
                "region_code": region_code,
                "region_name": region.name if region else None,
                "facility_type": facility_type,
                "supply_metrics": supply_metrics,
                "demand_metrics": demand_metrics,
                "supply_demand_ratio": supply_demand_ratio,
                "mismatch_level": mismatch_level,
                "recommendations": self._generate_recommendations(
                    supply_demand_ratio, 
                    mismatch_level,
                    facility_type
                ),
                "analyzed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"수요-공급 분석 실패: {str(e)}")
            raise
    
    def _calculate_supply_metrics(
        self, 
        facilities: List[SportsFacility], 
        population: int
    ) -> Dict[str, Any]:
        """
        공급 지표 계산
        
        Args:
            facilities: 시설 목록
            population: 인구수
            
        Returns:
            공급 지표
        """
        total_facilities = len(facilities)
        
        # 공공시설 비율
        public_facilities = sum(1 for f in facilities if f.is_public)
        public_ratio = public_facilities / total_facilities if total_facilities > 0 else 0
        
        # 무료시설 비율  
        free_facilities = sum(1 for f in facilities if f.is_free)
        free_ratio = free_facilities / total_facilities if total_facilities > 0 else 0
        
        # 총 수용 인원
        total_capacity = sum(f.capacity or 0 for f in facilities)
        
        # 인구 1만명당 시설 수
        facilities_per_10k = (total_facilities / population * 10000) if population > 0 else 0
        
        # 인구 1만명당 수용 인원
        capacity_per_10k = (total_capacity / population * 10000) if population > 0 else 0
        
        return {
            "total_facilities": total_facilities,
            "public_facilities": public_facilities,
            "public_ratio": round(public_ratio, 3),
            "free_facilities": free_facilities,
            "free_ratio": round(free_ratio, 3),
            "total_capacity": total_capacity,
            "facilities_per_10k_population": round(facilities_per_10k, 2),
            "capacity_per_10k_population": round(capacity_per_10k, 2)
        }
    
    def _calculate_demand_metrics(self, demands: List[FacilityDemand]) -> Dict[str, Any]:
        """
        수요 지표 계산
        
        Args:
            demands: 수요 데이터 목록
            
        Returns:
            수요 지표
        """
        if not demands:
            return {
                "average_demand_percentage": 0,
                "max_demand_percentage": 0,
                "demand_score": 0,
                "priority_groups": []
            }
        
        # 평균 수요율
        avg_demand = np.mean([d.demand_percentage for d in demands])
        
        # 최대 수요율
        max_demand = max(d.demand_percentage for d in demands)
        
        # 수요 점수 (0-100)
        demand_score = min(avg_demand * 1.2, 100)  # 가중치 적용
        
        # 우선순위 그룹 (연령대, 성별 등)
        priority_groups = []
        for demand in demands:
            if demand.demand_percentage > 70:  # 높은 수요
                group = {
                    "age_group": demand.age_group,
                    "gender": demand.gender,
                    "demand": demand.demand_percentage
                }
                if group not in priority_groups:
                    priority_groups.append(group)
        
        return {
            "average_demand_percentage": round(avg_demand, 2),
            "max_demand_percentage": round(max_demand, 2),
            "demand_score": round(demand_score, 2),
            "priority_groups": priority_groups[:3]  # 상위 3개 그룹
        }
    
    def _calculate_ratio(
        self, 
        supply_metrics: Dict[str, Any], 
        demand_metrics: Dict[str, Any]
    ) -> float:
        """
        수요-공급 비율 계산
        
        Args:
            supply_metrics: 공급 지표
            demand_metrics: 수요 지표
            
        Returns:
            수요-공급 비율 (1.0이 균형, < 1.0은 공급 부족, > 1.0은 공급 과잉)
        """
        if demand_metrics["demand_score"] == 0:
            return float('inf')  # 수요가 없는 경우
        
        # 공급 점수 계산 (시설 수와 수용 인원 고려)
        supply_score = (
            supply_metrics["facilities_per_10k_population"] * 10 +
            supply_metrics["capacity_per_10k_population"] * 0.1 +
            supply_metrics["public_ratio"] * 20 +
            supply_metrics["free_ratio"] * 10
        )
        
        # 수요 점수
        demand_score = demand_metrics["demand_score"]
        
        # 비율 계산
        ratio = supply_score / demand_score if demand_score > 0 else float('inf')
        
        return round(ratio, 3)
    
    def _determine_mismatch_level(self, ratio: float) -> str:
        """
        불일치 수준 판정
        
        Args:
            ratio: 수요-공급 비율
            
        Returns:
            불일치 수준 (severe_shortage, shortage, balanced, surplus, severe_surplus)
        """
        if ratio == float('inf'):
            return "no_demand"
        elif ratio < 0.5:
            return "severe_shortage"  # 심각한 공급 부족
        elif ratio < 0.8:
            return "shortage"  # 공급 부족
        elif ratio <= 1.2:
            return "balanced"  # 균형
        elif ratio <= 1.5:
            return "surplus"  # 공급 과잉
        else:
            return "severe_surplus"  # 심각한 공급 과잉
    
    def _generate_recommendations(
        self, 
        ratio: float, 
        mismatch_level: str,
        facility_type: Optional[str]
    ) -> List[str]:
        """
        개선 권고사항 생성
        
        Args:
            ratio: 수요-공급 비율
            mismatch_level: 불일치 수준
            facility_type: 시설 유형
            
        Returns:
            권고사항 목록
        """
        recommendations = []
        
        if mismatch_level == "severe_shortage":
            recommendations.append(f"긴급: {facility_type or '체육시설'} 확충이 시급히 필요합니다.")
            recommendations.append("단기: 임시 시설 또는 이동식 시설 도입을 검토하세요.")
            recommendations.append("중장기: 신규 시설 건립 계획을 수립하세요.")
        elif mismatch_level == "shortage":
            recommendations.append(f"{facility_type or '체육시설'} 추가 확충을 검토하세요.")
            recommendations.append("기존 시설의 운영 시간 확대를 고려하세요.")
            recommendations.append("인근 지역과의 시설 공유 방안을 모색하세요.")
        elif mismatch_level == "balanced":
            recommendations.append("현재 수요-공급이 균형을 이루고 있습니다.")
            recommendations.append("시설 유지보수 및 서비스 품질 향상에 집중하세요.")
        elif mismatch_level in ["surplus", "severe_surplus"]:
            recommendations.append("시설 활용도 제고 방안을 마련하세요.")
            recommendations.append("프로그램 다양화로 수요 창출을 검토하세요.")
            recommendations.append("시설 전환 또는 복합화를 고려하세요.")
        
        return recommendations
    
    async def find_mismatch_regions(
        self,
        threshold: float = 0.8,
        facility_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        불일치 지역 자동 탐지
        
        Args:
            threshold: 불일치 판정 임계값
            facility_type: 시설 유형 (선택)
            
        Returns:
            불일치 지역 목록
        """
        try:
            # 모든 지역 조회
            regions_query = select(Region)
            regions_result = await self.db.execute(regions_query)
            regions = regions_result.scalars().all()
            
            mismatch_regions = []
            
            for region in regions:
                # 각 지역별 수요-공급 분석
                analysis = await self.calculate_supply_demand_ratio(
                    region.code,
                    facility_type
                )
                
                # 불일치 지역 필터링
                if analysis.get("supply_demand_ratio", 1.0) < threshold:
                    mismatch_regions.append({
                        "region_code": region.code,
                        "region_name": region.name,
                        "population": region.population,
                        "supply_demand_ratio": analysis["supply_demand_ratio"],
                        "mismatch_level": analysis["mismatch_level"],
                        "facility_shortage": 
                            analysis["demand_metrics"]["demand_score"] - 
                            analysis["supply_metrics"]["total_facilities"],
                        "priority_score": self._calculate_priority_score(
                            analysis["supply_demand_ratio"],
                            region.population
                        )
                    })
            
            # 우선순위 점수로 정렬
            mismatch_regions.sort(key=lambda x: x["priority_score"], reverse=True)
            
            return mismatch_regions
            
        except Exception as e:
            logger.error(f"불일치 지역 탐지 실패: {str(e)}")
            raise
    
    def _calculate_priority_score(self, ratio: float, population: int) -> float:
        """
        우선순위 점수 계산
        
        Args:
            ratio: 수요-공급 비율
            population: 인구수
            
        Returns:
            우선순위 점수
        """
        # 불일치 정도와 인구 규모를 고려한 우선순위
        mismatch_weight = max(0, 1 - ratio) * 100  # 불일치 정도
        population_weight = np.log10(population + 1)  # 인구 규모 (로그 스케일)
        
        return round(mismatch_weight * population_weight, 2)
    
    async def get_facility_accessibility(
        self,
        lat: float,
        lng: float,
        facility_type: Optional[str] = None,
        max_distance_km: float = 3.0
    ) -> Dict[str, Any]:
        """
        특정 위치에서의 시설 접근성 분석
        
        Args:
            lat: 위도
            lng: 경도
            facility_type: 시설 유형
            max_distance_km: 최대 거리 (km)
            
        Returns:
            접근성 분석 결과
        """
        try:
            # 모든 시설 조회
            facility_query = select(SportsFacility)
            if facility_type:
                facility_query = facility_query.where(
                    SportsFacility.facility_type == facility_type
                )
            
            facilities_result = await self.db.execute(facility_query)
            facilities = facilities_result.scalars().all()
            
            # 거리 계산 및 필터링
            nearby_facilities = []
            for facility in facilities:
                distance = geodesic(
                    (lat, lng),
                    (facility.latitude, facility.longitude)
                ).km
                
                if distance <= max_distance_km:
                    nearby_facilities.append({
                        "facility_id": facility.facility_code,
                        "name": facility.name,
                        "type": facility.facility_type,
                        "distance_km": round(distance, 2),
                        "is_public": facility.is_public,
                        "is_free": facility.is_free
                    })
            
            # 거리순 정렬
            nearby_facilities.sort(key=lambda x: x["distance_km"])
            
            # 접근성 점수 계산
            accessibility_score = self._calculate_accessibility_score(
                nearby_facilities,
                max_distance_km
            )
            
            return {
                "location": {"lat": lat, "lng": lng},
                "search_radius_km": max_distance_km,
                "nearby_facilities_count": len(nearby_facilities),
                "nearby_facilities": nearby_facilities[:10],  # 상위 10개
                "accessibility_score": accessibility_score,
                "accessibility_level": self._determine_accessibility_level(
                    accessibility_score
                )
            }
            
        except Exception as e:
            logger.error(f"접근성 분석 실패: {str(e)}")
            raise
    
    def _calculate_accessibility_score(
        self,
        nearby_facilities: List[Dict[str, Any]],
        max_distance: float
    ) -> float:
        """
        접근성 점수 계산
        
        Args:
            nearby_facilities: 인근 시설 목록
            max_distance: 최대 거리
            
        Returns:
            접근성 점수 (0-100)
        """
        if not nearby_facilities:
            return 0
        
        score = 0
        for facility in nearby_facilities:
            # 거리에 따른 가중치 (가까울수록 높은 점수)
            distance_weight = 1 - (facility["distance_km"] / max_distance)
            
            # 공공/무료 시설 가중치
            public_weight = 1.2 if facility["is_public"] else 1.0
            free_weight = 1.1 if facility["is_free"] else 1.0
            
            score += distance_weight * public_weight * free_weight * 10
        
        # 최대 100점으로 정규화
        return min(round(score, 2), 100)
    
    def _determine_accessibility_level(self, score: float) -> str:
        """
        접근성 수준 판정
        
        Args:
            score: 접근성 점수
            
        Returns:
            접근성 수준
        """
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "moderate"
        elif score >= 20:
            return "poor"
        else:
            return "very_poor"
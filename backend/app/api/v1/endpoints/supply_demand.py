"""
수요-공급 분석 API 엔드포인트
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.supply_demand_analyzer import SupplyDemandAnalyzer
from app.services.facilities_api_client import FacilitiesAPIClient
from app.models.facility import SportsFacility
from sqlalchemy import select, func
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/analysis/supply-demand/{region_code}")
async def get_supply_demand_analysis(
    region_code: str,
    facility_type: Optional[str] = Query(None, description="시설 유형"),
    radius_km: float = Query(5.0, description="분석 반경(km)"),
    db: AsyncSession = Depends(get_db)
):
    """
    특정 지역의 수요-공급 분석 조회
    
    Args:
        region_code: 지역 코드
        facility_type: 시설 유형 (선택)
        radius_km: 분석 반경
    
    Returns:
        수요-공급 분석 결과
    """
    try:
        analyzer = SupplyDemandAnalyzer(db)
        result = await analyzer.calculate_supply_demand_ratio(
            region_code=region_code,
            facility_type=facility_type,
            radius_km=radius_km
        )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"수요-공급 분석 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/mismatch-regions")
async def find_mismatch_regions(
    threshold: float = Query(0.8, description="불일치 판정 임계값"),
    facility_type: Optional[str] = Query(None, description="시설 유형"),
    limit: int = Query(10, description="최대 결과 수"),
    db: AsyncSession = Depends(get_db)
):
    """
    수요-공급 불일치 지역 자동 탐지
    
    Args:
        threshold: 불일치 판정 임계값 (0.8 = 공급이 수요의 80% 미만)
        facility_type: 시설 유형 (선택)
        limit: 최대 결과 수
    
    Returns:
        불일치 지역 목록
    """
    try:
        analyzer = SupplyDemandAnalyzer(db)
        mismatch_regions = await analyzer.find_mismatch_regions(
            threshold=threshold,
            facility_type=facility_type
        )
        
        # 상위 N개만 반환
        return {
            "total_count": len(mismatch_regions),
            "threshold": threshold,
            "facility_type": facility_type,
            "regions": mismatch_regions[:limit]
        }
        
    except Exception as e:
        logger.error(f"불일치 지역 탐지 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/accessibility")
async def check_facility_accessibility(
    lat: float = Query(..., description="위도"),
    lng: float = Query(..., description="경도"),
    facility_type: Optional[str] = Query(None, description="시설 유형"),
    max_distance_km: float = Query(3.0, description="최대 거리(km)"),
    db: AsyncSession = Depends(get_db)
):
    """
    특정 위치에서의 시설 접근성 분석
    
    Args:
        lat: 위도
        lng: 경도
        facility_type: 시설 유형 (선택)
        max_distance_km: 최대 거리
    
    Returns:
        접근성 분석 결과
    """
    try:
        analyzer = SupplyDemandAnalyzer(db)
        result = await analyzer.get_facility_accessibility(
            lat=lat,
            lng=lng,
            facility_type=facility_type,
            max_distance_km=max_distance_km
        )
        
        return result
        
    except Exception as e:
        logger.error(f"접근성 분석 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/facilities/map-data")
async def get_facilities_map_data(
    region_code: Optional[str] = Query(None, description="지역 코드"),
    facility_type: Optional[str] = Query(None, description="시설 유형"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(100, ge=1, le=1000, description="페이지당 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    """
    지도 표시용 시설 데이터 조회
    
    Args:
        region_code: 지역 코드 (선택)
        facility_type: 시설 유형 (선택)
        page: 페이지 번호
        limit: 페이지당 항목 수
    
    Returns:
        시설 위치 데이터
    """
    try:
        # 쿼리 구성
        query = select(SportsFacility)
        
        if region_code:
            query = query.where(SportsFacility.region_code == region_code)
        
        if facility_type:
            query = query.where(SportsFacility.facility_type == facility_type)
        
        # 페이징
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # 실행
        result = await db.execute(query)
        facilities = result.scalars().all()
        
        # GeoJSON 형식으로 변환
        features = []
        for facility in facilities:
            features.append({
                "type": "Feature",
                "properties": {
                    "id": facility.facility_code,
                    "name": facility.name,
                    "type": facility.facility_type,
                    "sub_type": facility.sub_facility_type,
                    "region_code": facility.region_code,
                    "address": facility.address,
                    "operator": facility.operator,
                    "phone": facility.phone,
                    "is_public": facility.is_public,
                    "is_free": facility.is_free,
                    "capacity": facility.capacity,
                    "website": facility.website
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [facility.longitude, facility.latitude]
                }
            })
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "page": page,
                "limit": limit,
                "count": len(features),
                "region_code": region_code,
                "facility_type": facility_type
            }
        }
        
    except Exception as e:
        logger.error(f"시설 지도 데이터 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/facilities/types")
async def get_facility_types(
    region_code: Optional[str] = Query(None, description="지역 코드"),
    db: AsyncSession = Depends(get_db)
):
    """
    사용 가능한 시설 유형 목록 조회

    Args:
        region_code: 지역 코드 (선택)

    Returns:
        시설 유형 목록
    """
    try:
        # GROUP BY를 사용한 효율적인 쿼리
        query = select(
            SportsFacility.facility_type,
            func.count().label("count")
        )

        if region_code:
            query = query.where(SportsFacility.region_code == region_code)

        query = query.group_by(SportsFacility.facility_type)

        result = await db.execute(query)
        rows = result.all()

        # 결과 포맷팅
        type_counts = [
            {
                "type": facility_type,
                "count": count,
                "label": facility_type  # 한글 라벨
            }
            for facility_type, count in rows
        ]

        # 시설 수 기준 정렬
        type_counts.sort(key=lambda x: x["count"], reverse=True)
        
        return {
            "total_types": len(type_counts),
            "region_code": region_code,
            "types": type_counts
        }
        
    except Exception as e:
        logger.error(f"시설 유형 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regions/demand-scores")
async def get_regional_demand_scores(
    facility_type: Optional[str] = Query(None, description="시설 유형"),
    db: AsyncSession = Depends(get_db)
):
    """
    지역별 수요 점수 조회
    
    Args:
        facility_type: 시설 유형 (선택)
    
    Returns:
        지역별 수요 점수
    """
    try:
        from app.models.region import Region
        from app.models.facility import FacilityDemand
        
        # 모든 지역 조회
        regions_query = select(Region)
        regions_result = await db.execute(regions_query)
        regions = regions_result.scalars().all()
        
        regional_scores = []
        
        for region in regions:
            # 수요 데이터 조회
            demand_query = select(FacilityDemand).where(
                FacilityDemand.region_code == region.code
            )
            
            if facility_type:
                demand_query = demand_query.where(
                    FacilityDemand.facility_type == facility_type
                )
            
            demand_result = await db.execute(demand_query)
            demands = demand_result.scalars().all()
            
            # 평균 수요 계산
            if demands:
                avg_demand = sum(d.demand_percentage for d in demands) / len(demands)
            else:
                avg_demand = 0
            
            # 시설 수 계산
            facility_query = select(SportsFacility).where(
                SportsFacility.region_code == region.code
            )
            if facility_type:
                facility_query = facility_query.where(
                    SportsFacility.facility_type == facility_type
                )
            
            facility_result = await db.execute(facility_query)
            facilities = facility_result.scalars().all()
            
            # 인구 1만명당 시설 수
            facilities_per_10k = (len(facilities) / region.population * 10000) if region.population > 0 else 0
            
            regional_scores.append({
                "region_code": region.code,
                "region_name": region.name,
                "population": region.population,
                "demand_score": round(avg_demand, 2),
                "facility_count": len(facilities),
                "facilities_per_10k": round(facilities_per_10k, 2),
                "center_lat": region.center_lat,
                "center_lng": region.center_lng
            })
        
        # 수요 점수 기준 정렬
        regional_scores.sort(key=lambda x: x["demand_score"], reverse=True)
        
        return {
            "facility_type": facility_type,
            "regions": regional_scores
        }
        
    except Exception as e:
        logger.error(f"지역별 수요 점수 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/facilities/sync")
async def sync_facilities_from_api(
    region_code: Optional[str] = Query(None, description="지역 코드"),
    db: AsyncSession = Depends(get_db)
):
    """
    공공데이터 API에서 시설 데이터 동기화
    
    Args:
        region_code: 지역 코드 (선택)
    
    Returns:
        동기화 결과
    """
    try:
        client = FacilitiesAPIClient()
        
        # API에서 데이터 조회
        facilities_data = await client.get_all_facilities(
            city_name=region_code if region_code else None
        )
        
        # 데이터베이스에 저장
        saved_count = 0
        updated_count = 0
        
        for facility_raw in facilities_data:
            # 파싱
            parsed = client.parse_facility_data(facility_raw)
            
            # 기존 데이터 확인
            existing_query = select(SportsFacility).where(
                SportsFacility.facility_code == parsed.get("facility_code", "")
            )
            existing_result = await db.execute(existing_query)
            existing = existing_result.scalar_one_or_none()
            
            if existing:
                # 업데이트
                for key, value in parsed.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                updated_count += 1
            else:
                # 신규 생성
                new_facility = SportsFacility(**parsed)
                db.add(new_facility)
                saved_count += 1
        
        await db.commit()
        
        return {
            "success": True,
            "total_processed": len(facilities_data),
            "new_facilities": saved_count,
            "updated_facilities": updated_count,
            "region_code": region_code
        }
        
    except Exception as e:
        logger.error(f"시설 데이터 동기화 실패: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
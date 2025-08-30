"""
전국공공체육시설 API 클라이언트
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class FacilitiesAPIClient(BaseAPIClient):
    """전국공공체육시설 API 클라이언트"""
    
    def __init__(self):
        super().__init__(settings.FACILITIES_API_URL)
        
    async def get_facilities_list(
        self,
        city_name: Optional[str] = None,
        facility_type: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        체육시설 목록 조회
        
        Args:
            city_name: 시도명
            facility_type: 시설유형명
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            체육시설 목록 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows
        }
        
        if city_name:
            params["cp_nm"] = city_name
        if facility_type:
            params["ftype_nm"] = facility_type
            
        return await self._request("getPublicSportsFacilitiesList", params)
    
    async def get_facility_detail(self, facility_id: str) -> Dict[str, Any]:
        """
        체육시설 상세정보 조회
        
        Args:
            facility_id: 시설 ID
            
        Returns:
            체육시설 상세 정보
        """
        params = {"faci_gb_cd": facility_id}
        return await self._request("getPublicSportsFacilitiesDetail", params)
    
    async def get_all_facilities(
        self,
        city_name: Optional[str] = None,
        facility_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 체육시설 데이터 조회 (페이지네이션 자동 처리)
        
        Args:
            city_name: 시도명
            facility_type: 시설유형명
            
        Returns:
            전체 체육시설 리스트
        """
        params = {}
        if city_name:
            params["cp_nm"] = city_name
        if facility_type:
            params["ftype_nm"] = facility_type
            
        logger.info(f"전체 체육시설 데이터 조회 시작: {params}")
        
        facilities = await self.get_paginated_data(
            "getPublicSportsFacilitiesList",
            params
        )
        
        logger.info(f"전체 체육시설 데이터 조회 완료: {len(facilities)}개")
        
        return facilities
    
    def parse_facility_data(self, raw_facility: Dict[str, Any]) -> Dict[str, Any]:
        """
        원시 API 데이터를 표준 형식으로 파싱
        
        Args:
            raw_facility: API 원시 데이터
            
        Returns:
            파싱된 시설 데이터
        """
        return {
            "facility_code": raw_facility.get("faci_gb_cd"),
            "name": raw_facility.get("faci_nm"),
            "facility_type": raw_facility.get("ftype_nm"),
            "facility_type_detail": raw_facility.get("fcob_nm"),
            "address": raw_facility.get("faci_road_addr1", raw_facility.get("faci_addr1")),
            "address_detail": raw_facility.get("faci_road_addr2", raw_facility.get("faci_addr2")),
            "latitude": float(raw_facility.get("faci_lat", 0)),
            "longitude": float(raw_facility.get("faci_lot", 0)),
            "city": raw_facility.get("cp_nm"),
            "district": raw_facility.get("cpb_nm"),
            "management_type": raw_facility.get("rmiby_nm"),
            "operation_type": raw_facility.get("trobl_ty_nm"),
            "floor_area": raw_facility.get("ar_ar"),
            "building_area": raw_facility.get("ar_bild_ar"),
            "land_area": raw_facility.get("ar_site_ar"),
            "establishment_year": raw_facility.get("esta_yy"),
            "phone": raw_facility.get("ripo_tel_no"),
            "homepage": raw_facility.get("homepg_url"),
            "weekday_open": raw_facility.get("wkdy_opt_tm_cn"),
            "weekend_open": raw_facility.get("wknd_opt_tm_cn"),
            "holiday_open": raw_facility.get("holi_opt_tm_cn"),
            "usage_fee": raw_facility.get("utztn_am_cn"),
            "parking_available": raw_facility.get("park_yn") == "Y",
            "parking_fee": raw_facility.get("park_fee_yn") == "Y",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    async def get_facilities_by_region(self, region_code: str) -> List[Dict[str, Any]]:
        """
        지역별 체육시설 조회
        
        Args:
            region_code: 지역 코드
            
        Returns:
            해당 지역의 체육시설 리스트
        """
        # 지역 코드를 시도명으로 변환 (매핑 테이블 필요)
        region_mapping = {
            "11": "서울특별시",
            "26": "부산광역시",
            "27": "대구광역시",
            "28": "인천광역시",
            "29": "광주광역시",
            "30": "대전광역시",
            "31": "울산광역시",
            "36": "세종특별자치시",
            "41": "경기도",
            "42": "강원도",
            "43": "충청북도",
            "44": "충청남도",
            "45": "전라북도",
            "46": "전라남도",
            "47": "경상북도",
            "48": "경상남도",
            "50": "제주특별자치도"
        }
        
        city_name = region_mapping.get(region_code[:2])
        if not city_name:
            logger.warning(f"알 수 없는 지역 코드: {region_code}")
            return []
        
        return await self.get_all_facilities(city_name=city_name)
    
    async def get_facility_statistics(self) -> Dict[str, Any]:
        """
        체육시설 통계 데이터 생성
        
        Returns:
            통계 데이터
        """
        # 전체 시설 조회
        all_facilities = await self.get_all_facilities()
        
        # 통계 계산
        stats = {
            "total_count": len(all_facilities),
            "by_type": {},
            "by_region": {},
            "by_management": {}
        }
        
        for facility in all_facilities:
            # 시설 유형별 집계
            ftype = facility.get("ftype_nm", "기타")
            stats["by_type"][ftype] = stats["by_type"].get(ftype, 0) + 1
            
            # 지역별 집계
            city = facility.get("cp_nm", "기타")
            stats["by_region"][city] = stats["by_region"].get(city, 0) + 1
            
            # 운영 주체별 집계
            management = facility.get("rmiby_nm", "기타")
            stats["by_management"][management] = stats["by_management"].get(management, 0) + 1
        
        return stats
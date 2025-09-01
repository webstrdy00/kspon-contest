"""
전국체육시설 API 클라이언트
서울올림픽기념국민체육진흥공단_전국체육시설 정보
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class FacilitiesAPIClient(BaseAPIClient):
    """전국체육시설 API 클라이언트"""
    
    def __init__(self):
        # 새로운 API URL: https://apis.data.go.kr/B551014/SRVC_API_SFMS_FACI
        super().__init__(settings.FACILITIES_API_URL or "https://apis.data.go.kr/B551014/SRVC_API_SFMS_FACI")
        
    async def get_facilities_list(
        self,
        city_name: Optional[str] = None,
        district_name: Optional[str] = None,
        facility_name: Optional[str] = None,
        facility_type: Optional[str] = None,
        facility_category: Optional[str] = None,
        business_type: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        체육시설 목록 조회
        
        Args:
            city_name: 시도명 (cp_nm)
            district_name: 시군구명 (cpb_nm)
            facility_name: 시설명 (faci_nm)
            facility_type: 시설유형명 (ftype_nm)
            facility_category: 시설구분명 (faci_gb_nm)
            business_type: 업종명 (fcob_nm)
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            체육시설 목록 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "resultType": "json"  # JSON 응답 형식 지정
        }
        
        if city_name:
            params["cp_nm"] = city_name
        if district_name:
            params["cpb_nm"] = district_name
        if facility_name:
            params["faci_nm"] = facility_name
        if facility_type:
            params["ftype_nm"] = facility_type
        if facility_category:
            params["faci_gb_nm"] = facility_category
        if business_type:
            params["fcob_nm"] = business_type
            
        # 새로운 엔드포인트: TODZ_API_SFMS_FACI
        return await self._request("TODZ_API_SFMS_FACI", params)
    
    async def get_facility_detail(self, facility_code: str) -> Dict[str, Any]:
        """
        체육시설 상세정보 조회
        
        Args:
            facility_code: 시설 코드 (faci_cd)
            
        Returns:
            체육시설 상세 정보
        """
        # 시설 코드로 특정 시설 조회
        params = {
            "faci_nm": facility_code,  # 시설코드 또는 시설명으로 검색
            "pageNo": 1,
            "numOfRows": 1,
            "resultType": "json"
        }
        return await self._request("TODZ_API_SFMS_FACI", params)
    
    async def get_all_facilities(
        self,
        city_name: Optional[str] = None,
        district_name: Optional[str] = None,
        facility_type: Optional[str] = None,
        facility_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 체육시설 데이터 조회 (페이지네이션 자동 처리)
        
        Args:
            city_name: 시도명
            district_name: 시군구명
            facility_type: 시설유형명
            facility_category: 시설구분명
            
        Returns:
            전체 체육시설 리스트
        """
        params = {"resultType": "json"}
        if city_name:
            params["cp_nm"] = city_name
        if district_name:
            params["cpb_nm"] = district_name
        if facility_type:
            params["ftype_nm"] = facility_type
        if facility_category:
            params["faci_gb_nm"] = facility_category
            
        logger.info(f"전체 체육시설 데이터 조회 시작: {params}")
        
        facilities = await self.get_paginated_data(
            "TODZ_API_SFMS_FACI",
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
            # 기본 정보
            "facility_code": raw_facility.get("faci_cd"),  # 시설코드
            "name": raw_facility.get("faci_nm"),  # 시설명
            "facility_category": raw_facility.get("faci_gb_nm"),  # 시설구분명
            "business_type": raw_facility.get("fcob_nm"),  # 업종명
            "facility_type": raw_facility.get("ftype_nm"),  # 시설유형명
            "facility_status": raw_facility.get("faci_stat_nm"),  # 시설상태명
            
            # 주소 정보
            "zip_code_road": raw_facility.get("faci_road_zip"),  # 도로명우편번호
            "address_road": raw_facility.get("faci_road_addr"),  # 도로명주소
            "address_road_detail": raw_facility.get("faci_road_daddr"),  # 도로명상세주소
            "zip_code": raw_facility.get("faci_zip"),  # 지번우편번호
            "address": raw_facility.get("faci_addr"),  # 지번주소
            "address_detail": raw_facility.get("faci_daddr"),  # 지번상세주소
            
            # 좌표 정보
            "longitude": float(raw_facility.get("faci_lot", 0)) if raw_facility.get("faci_lot") else None,  # 경도
            "latitude": float(raw_facility.get("faci_lat", 0)) if raw_facility.get("faci_lat") else None,  # 위도
            
            # 연락처 정보
            "phone": raw_facility.get("faci_tel_no"),  # 전화번호
            "homepage": raw_facility.get("faci_homepage"),  # 홈페이지
            
            # 지역 정보
            "city": raw_facility.get("cp_nm"),  # 시도명
            "district": raw_facility.get("cpb_nm"),  # 시군구명
            "address_city": raw_facility.get("addr_ctpv_nm"),  # 주소시도명
            "address_district": raw_facility.get("addr_cpb_nm"),  # 주소시군구명
            "address_town": raw_facility.get("addr_emd_nm"),  # 주소읍면동명
            "address_admin": raw_facility.get("addr_amd_nm"),  # 주소행정동명
            
            # 관리 정보
            "management_type_code": raw_facility.get("faci_mng_type_cd"),  # 시설관리유형코드
            "management_type": raw_facility.get("fmng_type_gb_nm"),  # 시설관리유형구분명
            "management_city": raw_facility.get("fmng_cp_nm"),  # 시설관리시도명
            "management_district": raw_facility.get("fmng_cpb_nm"),  # 시설관리시군구명
            "management_dept": raw_facility.get("fmng_dept_nm"),  # 시설관리부서명
            "management_phone": raw_facility.get("faci_mng_user_telno"),  # 시설관리자전화번호
            
            # 시설 정보
            "indoor_outdoor": raw_facility.get("inout_gbn_nm"),  # 실내외구분명
            "seat_count": raw_facility.get("stand_seat_cnt"),  # 관람석수
            "capacity": raw_facility.get("stand_cpt_psn_cnt"),  # 수용인원수
            "floor_area": raw_facility.get("faci_gfa"),  # 연면적
            "open_status": raw_facility.get("open_yn"),  # 개방여부
            "life_gym_name": raw_facility.get("life_gym_nm"),  # 생활체육관명
            "usage_target": raw_facility.get("use_asct_nm"),  # 이용대상명
            
            # 날짜 정보
            "base_date": raw_facility.get("base_ymd"),  # 기준일자
            "facility_reg_date": raw_facility.get("faci_reg_ymd"),  # 시설등록일자
            "completion_date": raw_facility.get("cp_ymd"),  # 준공일자
            "approval_date": raw_facility.get("th_ymd"),  # 인가일자
            "shutdown_date": raw_facility.get("sdwn_ymd"),  # 폐업일자
            
            # 기타 정보
            "national_team": raw_facility.get("nation_yn") == "Y",  # 국가대표여부
            "ssm_design": raw_facility.get("ssm_dsn_yn") == "Y",  # SSM설계여부
            "auto_check": raw_facility.get("atnm_chk_yn") == "Y",  # 자동점검여부
            
            # 시스템 정보
            "created_at": raw_facility.get("reg_dt"),  # 등록일시
            "updated_at": raw_facility.get("updt_dt")  # 수정일시
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
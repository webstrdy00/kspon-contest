"""
국민체육진흥기금 지원실적 API 클라이언트
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class FundAPIClient(BaseAPIClient):
    """국민체육진흥기금 API 클라이언트"""
    
    def __init__(self):
        super().__init__(settings.FUND_SUPPORT_API_URL)
        
    async def get_fund_support_list(
        self,
        year: Optional[int] = None,
        organization: Optional[str] = None,
        business_name: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        국민체육진흥기금 지원실적 조회
        
        Args:
            year: 지원년도
            organization: 지원기관명
            business_name: 사업명
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            지원실적 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows
        }
        
        if year:
            params["sprt_year"] = year
        if organization:
            params["reqst_instt_nm"] = organization
        if business_name:
            params["dtbz_nm"] = business_name
            
        return await self._request("getFundSupportList", params)
    
    async def get_all_fund_support(
        self,
        year: Optional[int] = None,
        organization: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 기금 지원실적 데이터 조회
        
        Args:
            year: 지원년도
            organization: 지원기관명
            
        Returns:
            전체 지원실적 리스트
        """
        params = {}
        if year:
            params["sprt_year"] = year
        if organization:
            params["reqst_instt_nm"] = organization
            
        logger.info(f"전체 기금 지원실적 조회 시작: {params}")
        
        support_list = await self.get_paginated_data(
            "getFundSupportList",
            params
        )
        
        logger.info(f"전체 기금 지원실적 조회 완료: {len(support_list)}개")
        
        return support_list
    
    def parse_fund_data(self, raw_fund: Dict[str, Any]) -> Dict[str, Any]:
        """
        원시 API 데이터를 표준 형식으로 파싱
        
        Args:
            raw_fund: API 원시 데이터
            
        Returns:
            파싱된 지원실적 데이터
        """
        # 지역 추정 (기관명에서 추출)
        region = self._extract_region_from_organization(raw_fund.get("reqst_instt_nm", ""))
        
        # 종목 추정 (사업명에서 추출)
        sport_type = self._extract_sport_from_business(raw_fund.get("dtbz_nm", ""))
        
        return {
            "year": int(raw_fund.get("sprt_year", 0)),
            "organization": raw_fund.get("reqst_instt_nm"),
            "business_name": raw_fund.get("dtbz_nm"),
            "business_detail": raw_fund.get("dtlbz_nm"),
            "support_amount": int(raw_fund.get("dvdc_amt", 0)),
            "execution_amount": int(raw_fund.get("excut_amt", 0)),
            "support_type": raw_fund.get("sprt_realm_nm"),
            "estimated_region": region,
            "estimated_sport": sport_type,
            "project_period": raw_fund.get("biz_prd_cn"),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    def _extract_region_from_organization(self, org_name: str) -> Optional[str]:
        """
        기관명에서 지역 정보 추출
        
        Args:
            org_name: 기관명
            
        Returns:
            추정된 지역명
        """
        regions = [
            "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
            "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"
        ]
        
        for region in regions:
            if region in org_name:
                return region
                
        # 전국 단위 기관
        if any(keyword in org_name for keyword in ["한국", "대한", "국민", "전국"]):
            return "전국"
            
        return None
    
    def _extract_sport_from_business(self, business_name: str) -> Optional[str]:
        """
        사업명에서 종목 정보 추출
        
        Args:
            business_name: 사업명
            
        Returns:
            추정된 종목명
        """
        sports = [
            "축구", "야구", "농구", "배구", "테니스", "배드민턴", "탁구",
            "수영", "육상", "체조", "태권도", "유도", "레슬링", "복싱",
            "골프", "양궁", "사격", "역도", "핸드볼", "하키", "럭비"
        ]
        
        for sport in sports:
            if sport in business_name:
                return sport
                
        # 생활체육 관련
        if any(keyword in business_name for keyword in ["생활체육", "생활스포츠", "동호회"]):
            return "생활체육"
            
        # 전문체육 관련
        if any(keyword in business_name for keyword in ["전문체육", "엘리트", "국가대표"]):
            return "전문체육"
            
        return None
    
    async def get_budget_by_region(self, year: int) -> Dict[str, int]:
        """
        지역별 예산 집계
        
        Args:
            year: 년도
            
        Returns:
            지역별 예산 합계
        """
        all_support = await self.get_all_fund_support(year=year)
        
        budget_by_region = {}
        for item in all_support:
            parsed = self.parse_fund_data(item)
            region = parsed.get("estimated_region")
            
            if region:
                budget_by_region[region] = budget_by_region.get(region, 0) + parsed["support_amount"]
        
        return budget_by_region
    
    async def get_budget_by_sport(self, year: int) -> Dict[str, int]:
        """
        종목별 예산 집계
        
        Args:
            year: 년도
            
        Returns:
            종목별 예산 합계
        """
        all_support = await self.get_all_fund_support(year=year)
        
        budget_by_sport = {}
        for item in all_support:
            parsed = self.parse_fund_data(item)
            sport = parsed.get("estimated_sport")
            
            if sport:
                budget_by_sport[sport] = budget_by_sport.get(sport, 0) + parsed["support_amount"]
        
        return budget_by_sport
    
    async def get_budget_efficiency_analysis(self, year: int) -> Dict[str, Any]:
        """
        예산 효율성 분석 데이터 생성
        
        Args:
            year: 년도
            
        Returns:
            효율성 분석 데이터
        """
        all_support = await self.get_all_fund_support(year=year)
        
        analysis = {
            "total_budget": 0,
            "total_execution": 0,
            "execution_rate": 0,
            "by_region": {},
            "by_sport": {},
            "by_type": {}
        }
        
        for item in all_support:
            parsed = self.parse_fund_data(item)
            
            # 총 예산 및 집행액
            analysis["total_budget"] += parsed["support_amount"]
            analysis["total_execution"] += parsed["execution_amount"]
            
            # 지역별 집계
            region = parsed.get("estimated_region", "기타")
            if region not in analysis["by_region"]:
                analysis["by_region"][region] = {"budget": 0, "execution": 0}
            analysis["by_region"][region]["budget"] += parsed["support_amount"]
            analysis["by_region"][region]["execution"] += parsed["execution_amount"]
            
            # 종목별 집계
            sport = parsed.get("estimated_sport", "기타")
            if sport not in analysis["by_sport"]:
                analysis["by_sport"][sport] = {"budget": 0, "execution": 0}
            analysis["by_sport"][sport]["budget"] += parsed["support_amount"]
            analysis["by_sport"][sport]["execution"] += parsed["execution_amount"]
            
            # 지원 유형별 집계
            support_type = parsed.get("support_type", "기타")
            if support_type not in analysis["by_type"]:
                analysis["by_type"][support_type] = {"budget": 0, "execution": 0}
            analysis["by_type"][support_type]["budget"] += parsed["support_amount"]
            analysis["by_type"][support_type]["execution"] += parsed["execution_amount"]
        
        # 전체 집행률 계산
        if analysis["total_budget"] > 0:
            analysis["execution_rate"] = (analysis["total_execution"] / analysis["total_budget"]) * 100
        
        return analysis
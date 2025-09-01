"""
국민체육진흥기금 종합지원실적지표 API 클라이언트
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class FundComprehensiveAPIClient(BaseAPIClient):
    """국민체육진흥기금 종합지원실적지표 API 클라이언트"""
    
    def __init__(self):
        # 종합지원실적지표 API URL 사용
        super().__init__("https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_INSTT_BSNS_RSLT_API")
        
    async def get_comprehensive_results(
        self,
        year: Optional[int] = None,
        program_name: Optional[str] = None,
        unit_business: Optional[str] = None,
        detail_business: Optional[str] = None,
        organization: Optional[str] = None,
        business_group: Optional[str] = None,
        business_name: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        종합지원실적지표정보 조회
        
        Args:
            year: 사업연도
            program_name: 프로그램명
            unit_business: 단위사업명
            detail_business: 세부사업명
            organization: 기관명
            business_group: 내역사업명
            business_name: 보조사업명
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            종합지원실적 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "resultType": "json"
        }
        
        if year:
            params["biz_yr"] = year
        if program_name:
            params["pgm_nm"] = program_name
        if unit_business:
            params["unit_busi_nm"] = unit_business
        if detail_business:
            params["dbs_nm"] = detail_business
        if organization:
            params["org_nm"] = organization
        if business_group:
            params["biz_grp_nm"] = business_group
        if business_name:
            params["biz_nm"] = business_name
            
        return await self._request("todz_api_fun_instt_api_i", params)
    
    async def get_all_comprehensive_results(
        self,
        year: Optional[int] = None,
        organization: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 종합지원실적 데이터 조회
        
        Args:
            year: 사업연도
            organization: 기관명
            
        Returns:
            전체 종합지원실적 리스트
        """
        params = {"resultType": "json"}
        if year:
            params["biz_yr"] = year
        if organization:
            params["org_nm"] = organization
            
        logger.info(f"전체 종합지원실적 조회 시작: {params}")
        
        results = await self.get_paginated_data(
            "todz_api_fun_instt_api_i",
            params
        )
        
        logger.info(f"전체 종합지원실적 조회 완료: {len(results)}개")
        
        return results
    
    def parse_comprehensive_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        원시 API 데이터를 표준 형식으로 파싱
        
        Args:
            raw_data: API 원시 데이터
            
        Returns:
            파싱된 종합지원실적 데이터
        """
        return {
            "year": int(raw_data.get("biz_yr", 0)),
            "program_name": raw_data.get("pgm_nm"),
            "unit_business": raw_data.get("unit_busi_nm"),
            "detail_business": raw_data.get("dbs_nm"),
            "organization": raw_data.get("org_nm"),
            "business_group": raw_data.get("biz_grp_nm"),
            "business_name": raw_data.get("biz_nm"),
            "budget_amount": int(raw_data.get("tgyl_year_bsns_amt", 0)),  # 사업예산금액
            "support_amount": int(raw_data.get("sprt_amt", 0)),  # 실적금액
            "expenditure_item": raw_data.get("exti_id_nm"),  # 세출목명
            "row_num": int(raw_data.get("row_num", 0)),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    async def get_execution_rate_analysis(self, year: int) -> Dict[str, Any]:
        """
        예산 대비 집행률 분석
        
        Args:
            year: 사업연도
            
        Returns:
            집행률 분석 데이터
        """
        all_results = await self.get_all_comprehensive_results(year=year)
        
        analysis = {
            "year": year,
            "total_budget": 0,
            "total_execution": 0,
            "overall_rate": 0,
            "by_program": {},
            "by_organization": {},
            "by_expenditure": {}
        }
        
        for item in all_results:
            parsed = self.parse_comprehensive_data(item)
            
            # 전체 합계
            analysis["total_budget"] += parsed["budget_amount"]
            analysis["total_execution"] += parsed["support_amount"]
            
            # 프로그램별 집계
            program = parsed["program_name"]
            if program and program not in analysis["by_program"]:
                analysis["by_program"][program] = {
                    "budget": 0,
                    "execution": 0,
                    "rate": 0
                }
            if program:
                analysis["by_program"][program]["budget"] += parsed["budget_amount"]
                analysis["by_program"][program]["execution"] += parsed["support_amount"]
            
            # 기관별 집계
            org = parsed["organization"]
            if org and org not in analysis["by_organization"]:
                analysis["by_organization"][org] = {
                    "budget": 0,
                    "execution": 0,
                    "rate": 0
                }
            if org:
                analysis["by_organization"][org]["budget"] += parsed["budget_amount"]
                analysis["by_organization"][org]["execution"] += parsed["support_amount"]
            
            # 세출목별 집계
            expenditure = parsed["expenditure_item"]
            if expenditure and expenditure not in analysis["by_expenditure"]:
                analysis["by_expenditure"][expenditure] = {
                    "budget": 0,
                    "execution": 0,
                    "rate": 0
                }
            if expenditure:
                analysis["by_expenditure"][expenditure]["budget"] += parsed["budget_amount"]
                analysis["by_expenditure"][expenditure]["execution"] += parsed["support_amount"]
        
        # 집행률 계산
        if analysis["total_budget"] > 0:
            analysis["overall_rate"] = (analysis["total_execution"] / analysis["total_budget"]) * 100
        
        # 프로그램별 집행률
        for program in analysis["by_program"]:
            if analysis["by_program"][program]["budget"] > 0:
                analysis["by_program"][program]["rate"] = (
                    analysis["by_program"][program]["execution"] / 
                    analysis["by_program"][program]["budget"]
                ) * 100
        
        # 기관별 집행률
        for org in analysis["by_organization"]:
            if analysis["by_organization"][org]["budget"] > 0:
                analysis["by_organization"][org]["rate"] = (
                    analysis["by_organization"][org]["execution"] / 
                    analysis["by_organization"][org]["budget"]
                ) * 100
        
        # 세출목별 집행률
        for expenditure in analysis["by_expenditure"]:
            if analysis["by_expenditure"][expenditure]["budget"] > 0:
                analysis["by_expenditure"][expenditure]["rate"] = (
                    analysis["by_expenditure"][expenditure]["execution"] / 
                    analysis["by_expenditure"][expenditure]["budget"]
                ) * 100
        
        return analysis
    
    async def get_top_organizations(
        self, 
        year: int, 
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        상위 지원 기관 조회
        
        Args:
            year: 사업연도
            top_n: 상위 N개
            
        Returns:
            상위 지원 기관 리스트
        """
        all_results = await self.get_all_comprehensive_results(year=year)
        
        # 기관별 집계
        org_totals = {}
        for item in all_results:
            parsed = self.parse_comprehensive_data(item)
            org = parsed["organization"]
            
            if org:
                if org not in org_totals:
                    org_totals[org] = {
                        "organization": org,
                        "total_budget": 0,
                        "total_support": 0,
                        "project_count": 0,
                        "programs": set()
                    }
                
                org_totals[org]["total_budget"] += parsed["budget_amount"]
                org_totals[org]["total_support"] += parsed["support_amount"]
                org_totals[org]["project_count"] += 1
                if parsed["program_name"]:
                    org_totals[org]["programs"].add(parsed["program_name"])
        
        # 프로그램 set을 리스트로 변환
        for org in org_totals:
            org_totals[org]["programs"] = list(org_totals[org]["programs"])
            org_totals[org]["program_count"] = len(org_totals[org]["programs"])
        
        # 지원금액 기준 정렬
        sorted_orgs = sorted(
            org_totals.values(),
            key=lambda x: x["total_support"],
            reverse=True
        )
        
        return sorted_orgs[:top_n]
    
    async def compare_yearly_results(
        self,
        year1: int,
        year2: int
    ) -> Dict[str, Any]:
        """
        연도별 지원실적 비교
        
        Args:
            year1: 비교 년도 1
            year2: 비교 년도 2
            
        Returns:
            연도별 비교 결과
        """
        results1 = await self.get_execution_rate_analysis(year1)
        results2 = await self.get_execution_rate_analysis(year2)
        
        comparison = {
            "comparison": f"{year1} vs {year2}",
            "budget_change": {
                "year1": results1["total_budget"],
                "year2": results2["total_budget"],
                "change_amount": results2["total_budget"] - results1["total_budget"],
                "change_rate": ((results2["total_budget"] - results1["total_budget"]) / 
                              results1["total_budget"] * 100) if results1["total_budget"] > 0 else 0
            },
            "execution_change": {
                "year1": results1["total_execution"],
                "year2": results2["total_execution"],
                "change_amount": results2["total_execution"] - results1["total_execution"],
                "change_rate": ((results2["total_execution"] - results1["total_execution"]) / 
                              results1["total_execution"] * 100) if results1["total_execution"] > 0 else 0
            },
            "execution_rate_change": {
                "year1": results1["overall_rate"],
                "year2": results2["overall_rate"],
                "change": results2["overall_rate"] - results1["overall_rate"]
            },
            "program_comparison": self._compare_programs(
                results1["by_program"], 
                results2["by_program"]
            ),
            "organization_comparison": self._compare_organizations(
                results1["by_organization"], 
                results2["by_organization"]
            )
        }
        
        return comparison
    
    def _compare_programs(self, programs1: Dict, programs2: Dict) -> Dict[str, Any]:
        """프로그램별 비교"""
        all_programs = set(programs1.keys()) | set(programs2.keys())
        
        comparison = {
            "new_programs": [],
            "removed_programs": [],
            "growth_programs": [],
            "decline_programs": []
        }
        
        for program in all_programs:
            if program in programs2 and program not in programs1:
                comparison["new_programs"].append({
                    "name": program,
                    "budget": programs2[program]["budget"]
                })
            elif program in programs1 and program not in programs2:
                comparison["removed_programs"].append({
                    "name": program,
                    "budget": programs1[program]["budget"]
                })
            elif program in programs1 and program in programs2:
                change = programs2[program]["budget"] - programs1[program]["budget"]
                if change > 0:
                    comparison["growth_programs"].append({
                        "name": program,
                        "change": change,
                        "rate": (change / programs1[program]["budget"] * 100) 
                               if programs1[program]["budget"] > 0 else 0
                    })
                elif change < 0:
                    comparison["decline_programs"].append({
                        "name": program,
                        "change": change,
                        "rate": (change / programs1[program]["budget"] * 100) 
                               if programs1[program]["budget"] > 0 else 0
                    })
        
        return comparison
    
    def _compare_organizations(self, orgs1: Dict, orgs2: Dict) -> Dict[str, Any]:
        """기관별 비교"""
        all_orgs = set(orgs1.keys()) | set(orgs2.keys())
        
        comparison = {
            "new_organizations": [],
            "removed_organizations": [],
            "top_growth": [],
            "top_decline": []
        }
        
        changes = []
        
        for org in all_orgs:
            if org in orgs2 and org not in orgs1:
                comparison["new_organizations"].append({
                    "name": org,
                    "budget": orgs2[org]["budget"]
                })
            elif org in orgs1 and org not in orgs2:
                comparison["removed_organizations"].append({
                    "name": org,
                    "budget": orgs1[org]["budget"]
                })
            elif org in orgs1 and org in orgs2:
                change = orgs2[org]["budget"] - orgs1[org]["budget"]
                if change != 0:
                    changes.append({
                        "name": org,
                        "change": change,
                        "rate": (change / orgs1[org]["budget"] * 100) 
                               if orgs1[org]["budget"] > 0 else 0
                    })
        
        # 상위 성장/감소 기관 정렬
        changes.sort(key=lambda x: x["change"], reverse=True)
        comparison["top_growth"] = [c for c in changes if c["change"] > 0][:5]
        comparison["top_decline"] = [c for c in changes if c["change"] < 0][:5]
        
        return comparison
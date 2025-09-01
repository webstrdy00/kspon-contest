"""
체육인복지 경기력향상성과금 API 클라이언트
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class PerformanceAPIClient(BaseAPIClient):
    """체육인복지 경기력향상성과금 API 클라이언트"""
    
    def __init__(self):
        super().__init__(settings.PERFORMANCE_REWARD_API_URL)
        
    async def get_performance_rewards(
        self,
        payment_month: Optional[str] = None,  # YYYYMM 형식
        sport_name: Optional[str] = None,
        recipient_name: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        경기력향상성과금 지급 정보 조회
        
        Args:
            payment_month: 지급년월 (YYYYMM 형식)
            sport_name: 종목명
            recipient_name: 수령인명
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            성과금 지급 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "resultType": "json"
        }
        
        if payment_month:
            params["pmt_yymm"] = payment_month
        if sport_name:
            params["spm_nm"] = sport_name
        if recipient_name:
            params["rcptn_nm"] = recipient_name
            
        return await self._request("TODZ_USFUN_PIRPEN_NON_DSPSN", params)
    
    async def get_all_performance_rewards(
        self,
        payment_month: Optional[str] = None,  # YYYYMM 형식
        sport_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 성과금 지급 데이터 조회
        
        Args:
            payment_month: 지급년월 (YYYYMM 형식)
            sport_name: 종목명
            
        Returns:
            전체 성과금 지급 리스트
        """
        params = {"resultType": "json"}
        if payment_month:
            params["pmt_yymm"] = payment_month
        if sport_name:
            params["spm_nm"] = sport_name
            
        logger.info(f"전체 성과금 지급 데이터 조회 시작: {params}")
        
        rewards = await self.get_paginated_data(
            "TODZ_USFUN_PIRPEN_NON_DSPSN",
            params
        )
        
        logger.info(f"전체 성과금 지급 데이터 조회 완료: {len(rewards)}개")
        
        return rewards
    
    def parse_performance_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        원시 API 데이터를 표준 형식으로 파싱
        
        Args:
            raw_data: API 원시 데이터
            
        Returns:
            파싱된 성과금 데이터
        """
        # 실제 API 응답 필드명에 맞게 수정
        return {
            "payment_month": raw_data.get("pmt_yymm"),  # 지급년월 (YYYYMM)
            "sport_name": raw_data.get("spm_nm") or raw_data.get("prg_item_nm"),  # 종목명
            "amount": int(raw_data.get("mmamt", 0)),  # 금액
            "recipient_name": raw_data.get("rcptn_nm"),  # 수령인명
            "row_num": raw_data.get("row_num"),  # 행 번호
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    async def get_performance_by_sport(self, year: int) -> Dict[str, Dict[str, Any]]:
        """
        종목별 성과 분석
        
        Args:
            year: 년도
            
        Returns:
            종목별 성과 데이터
        """
        # 연도별 12개월 데이터 조회
        all_rewards = []
        for month in range(1, 13):
            payment_month = f"{year}{month:02d}"
            try:
                monthly_data = await self.get_performance_rewards(payment_month=payment_month)
                items = monthly_data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
                if isinstance(items, dict):
                    items = [items]
                all_rewards.extend(items)
            except Exception as e:
                logger.warning(f"{payment_month} 데이터 조회 실패: {e}")
                continue
        
        performance_by_sport = {}
        
        for item in all_rewards:
            parsed = self.parse_performance_data(item)
            sport = parsed.get("sport_name")
            
            if not sport:
                continue
                
            if sport not in performance_by_sport:
                performance_by_sport[sport] = {
                    "total_reward": 0,
                    "count": 0
                }
            
            # 성과금 합계
            performance_by_sport[sport]["total_reward"] += parsed.get("amount", 0)
            performance_by_sport[sport]["count"] += 1
        
        return performance_by_sport
    
    async def calculate_roi_by_sport(
        self, 
        year: int,
        budget_by_sport: Dict[str, int]
    ) -> Dict[str, Dict[str, Any]]:
        """
        종목별 투자 대비 성과(ROI) 계산
        
        Args:
            year: 년도
            budget_by_sport: 종목별 예산 (FundAPIClient에서 가져옴)
            
        Returns:
            종목별 ROI 분석 데이터
        """
        performance = await self.get_performance_by_sport(year)
        
        roi_analysis = {}
        
        for sport, perf_data in performance.items():
            budget = budget_by_sport.get(sport, 0)
            
            if budget > 0:
                roi_analysis[sport] = {
                    "budget": budget,
                    "performance_reward": perf_data["total_reward"],
                    "count": perf_data.get("count", 0),
                    "roi_percentage": (perf_data["total_reward"] / budget * 100) if budget > 0 else 0,
                    "efficiency_rating": self._calculate_efficiency_rating(perf_data["total_reward"], budget)
                }
        
        return roi_analysis
    
    def _calculate_efficiency_rating(self, medal_score: int, budget: int) -> str:
        """
        효율성 등급 계산
        
        Args:
            medal_score: 메달 점수
            budget: 예산
            
        Returns:
            효율성 등급 (S, A, B, C, D)
        """
        if budget == 0:
            return "N/A"
            
        # 억원당 메달 점수
        efficiency = medal_score / (budget / 100000000)
        
        if efficiency >= 2.0:
            return "S"
        elif efficiency >= 1.5:
            return "A"
        elif efficiency >= 1.0:
            return "B"
        elif efficiency >= 0.5:
            return "C"
        else:
            return "D"
    
    async def get_top_performing_sports(self, year: int, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        성과 상위 종목 조회
        
        Args:
            year: 년도
            top_n: 상위 N개
            
        Returns:
            상위 성과 종목 리스트
        """
        performance = await self.get_performance_by_sport(year)
        
        # 메달 점수로 정렬
        sorted_sports = []
        for sport, data in performance.items():
            medal_score = (
                data["medal_count"]["금"] * 3 +
                data["medal_count"]["은"] * 2 +
                data["medal_count"]["동"] * 1
            )
            
            sorted_sports.append({
                "sport": sport,
                "medal_score": medal_score,
                "gold": data["medal_count"]["금"],
                "silver": data["medal_count"]["은"],
                "bronze": data["medal_count"]["동"],
                "total_reward": data["total_reward"],
                "athlete_count": data["athlete_count"]
            })
        
        # 메달 점수로 내림차순 정렬
        sorted_sports.sort(key=lambda x: x["medal_score"], reverse=True)
        
        return sorted_sports[:top_n]
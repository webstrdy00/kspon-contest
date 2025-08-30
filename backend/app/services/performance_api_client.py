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
        year: Optional[int] = None,
        sport_type: Optional[str] = None,
        athlete_name: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        경기력향상성과금 지급 정보 조회
        
        Args:
            year: 지급년도
            sport_type: 종목명
            athlete_name: 선수명
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            성과금 지급 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows
        }
        
        if year:
            params["pmnt_year"] = year
        if sport_type:
            params["prg_item_nm"] = sport_type
        if athlete_name:
            params["ath_nm"] = athlete_name
            
        return await self._request("getPerformanceRewardList", params)
    
    async def get_all_performance_rewards(
        self,
        year: Optional[int] = None,
        sport_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 성과금 지급 데이터 조회
        
        Args:
            year: 지급년도
            sport_type: 종목명
            
        Returns:
            전체 성과금 지급 리스트
        """
        params = {}
        if year:
            params["pmnt_year"] = year
        if sport_type:
            params["prg_item_nm"] = sport_type
            
        logger.info(f"전체 성과금 지급 데이터 조회 시작: {params}")
        
        rewards = await self.get_paginated_data(
            "getPerformanceRewardList",
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
        return {
            "year": int(raw_data.get("pmnt_year", 0)),
            "sport_type": raw_data.get("prg_item_nm"),
            "competition_name": raw_data.get("cmpt_nm"),
            "medal_type": raw_data.get("medal_cl_nm"),
            "athlete_name": raw_data.get("ath_nm"),
            "coach_name": raw_data.get("coach_nm"),
            "reward_amount": int(raw_data.get("mmamt", 0)),
            "payment_count": int(raw_data.get("pmnt_cnt", 0)),
            "organization": raw_data.get("blng_org_nm"),
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
        all_rewards = await self.get_all_performance_rewards(year=year)
        
        performance_by_sport = {}
        
        for item in all_rewards:
            parsed = self.parse_performance_data(item)
            sport = parsed["sport_type"]
            
            if sport not in performance_by_sport:
                performance_by_sport[sport] = {
                    "total_reward": 0,
                    "medal_count": {"금": 0, "은": 0, "동": 0},
                    "athlete_count": set(),
                    "competitions": set()
                }
            
            # 성과금 합계
            performance_by_sport[sport]["total_reward"] += parsed["reward_amount"]
            
            # 메달 카운트
            medal = parsed.get("medal_type", "")
            if "금" in medal:
                performance_by_sport[sport]["medal_count"]["금"] += 1
            elif "은" in medal:
                performance_by_sport[sport]["medal_count"]["은"] += 1
            elif "동" in medal:
                performance_by_sport[sport]["medal_count"]["동"] += 1
            
            # 선수 및 대회 수
            performance_by_sport[sport]["athlete_count"].add(parsed["athlete_name"])
            performance_by_sport[sport]["competitions"].add(parsed["competition_name"])
        
        # Set을 숫자로 변환
        for sport in performance_by_sport:
            performance_by_sport[sport]["athlete_count"] = len(performance_by_sport[sport]["athlete_count"])
            performance_by_sport[sport]["competition_count"] = len(performance_by_sport[sport]["competitions"])
            del performance_by_sport[sport]["competitions"]
        
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
                # 메달 점수 계산 (금:3점, 은:2점, 동:1점)
                medal_score = (
                    perf_data["medal_count"]["금"] * 3 +
                    perf_data["medal_count"]["은"] * 2 +
                    perf_data["medal_count"]["동"] * 1
                )
                
                roi_analysis[sport] = {
                    "budget": budget,
                    "performance_reward": perf_data["total_reward"],
                    "medal_score": medal_score,
                    "medal_count": perf_data["medal_count"],
                    "athlete_count": perf_data["athlete_count"],
                    "roi_score": (medal_score / (budget / 100000000)) if budget > 0 else 0,  # 억원당 메달 점수
                    "cost_per_medal": budget / (sum(perf_data["medal_count"].values()) or 1),
                    "efficiency_rating": self._calculate_efficiency_rating(medal_score, budget)
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
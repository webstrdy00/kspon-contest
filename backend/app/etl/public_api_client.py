"""
Public Data API Client for Budget and Performance Data
공공데이터 API 클라이언트 (예산 및 성과 데이터)
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = logging.getLogger(__name__)


class PublicDataAPIClient:
    """공공데이터 API 클라이언트"""
    
    def __init__(self):
        self.base_urls = {
            "budget": "https://api.odcloud.kr/api/15081584/v1/uddi:3f72f7e8-e89f-4e3d-8e72-e37538c8f266",  # 국민체육진흥기금
            "performance": "https://api.odcloud.kr/api/15081585/v1/uddi:4f72f7e8-e89f-4e3d-8e72-e37538c8f267",  # 체육성과
            "welfare": "https://api.odcloud.kr/api/15081586/v1/uddi:5f72f7e8-e89f-4e3d-8e72-e37538c8f268"  # 체육인복지
        }
        self.service_key = settings.PUBLIC_DATA_SERVICE_KEY if hasattr(settings, 'PUBLIC_DATA_SERVICE_KEY') else None
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "KSPON-Contest-Platform/1.0"
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_budget_data(self, year: int, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """예산 데이터 조회"""
        if not self.service_key:
            logger.warning("공공데이터 서비스 키가 설정되지 않음")
            return self._get_mock_budget_data(year)
        
        params = {
            "serviceKey": self.service_key,
            "page": page,
            "perPage": per_page,
            "returnType": "json",
            "cond[YEAR::EQ]": year
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_urls["budget"],
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"예산 데이터 API 호출 실패: {e}")
            return self._get_mock_budget_data(year)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_performance_data(self, year: int, sport_code: Optional[str] = None) -> Dict[str, Any]:
        """성과 데이터 조회"""
        if not self.service_key:
            logger.warning("공공데이터 서비스 키가 설정되지 않음")
            return self._get_mock_performance_data(year, sport_code)
        
        params = {
            "serviceKey": self.service_key,
            "page": 1,
            "perPage": 1000,
            "returnType": "json",
            "cond[YEAR::EQ]": year
        }
        
        if sport_code:
            params["cond[SPORT_CODE::EQ]"] = sport_code
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_urls["performance"],
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"성과 데이터 API 호출 실패: {e}")
            return self._get_mock_performance_data(year, sport_code)
    
    async def fetch_all_budget_data(self, year: int) -> List[Dict[str, Any]]:
        """전체 예산 데이터 조회 (페이징 처리)"""
        all_data = []
        page = 1
        
        while True:
            result = await self.fetch_budget_data(year, page=page)
            
            if "data" in result:
                all_data.extend(result["data"])
                
                # 다음 페이지가 있는지 확인
                total_count = result.get("totalCount", 0)
                current_count = result.get("currentCount", 0)
                
                if len(all_data) >= total_count or current_count == 0:
                    break
                
                page += 1
            else:
                break
        
        return all_data
    
    def parse_budget_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """예산 레코드 파싱"""
        return {
            "year": int(record.get("연도", 0)),
            "institution_name": record.get("기관명", ""),
            "project_name": record.get("사업명", ""),
            "allocated": self._parse_amount(record.get("예산액", "0")),
            "executed": self._parse_amount(record.get("집행액", "0")),
            "execution_rate": float(record.get("집행률", "0").replace("%", "")),
            "quarter": self._parse_quarter(record.get("분기", "")),
        }
    
    def parse_performance_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """성과 레코드 파싱"""
        return {
            "year": int(record.get("연도", 0)),
            "sport_code": record.get("종목코드", ""),
            "sport_name": record.get("종목명", ""),
            "indicator_name": record.get("지표명", ""),
            "value": float(record.get("실적값", 0)),
            "target": float(record.get("목표값", 0)),
            "achievement_rate": float(record.get("달성률", "0").replace("%", "")),
            "measured_date": self._parse_date(record.get("측정일", "")),
        }
    
    def _parse_amount(self, amount_str: str) -> float:
        """금액 문자열 파싱"""
        if not amount_str:
            return 0.0
        
        # 콤마 제거
        amount_str = amount_str.replace(",", "")
        
        # 단위 처리
        if "억" in amount_str:
            amount_str = amount_str.replace("억", "")
            return float(amount_str) * 100_000_000
        elif "천만" in amount_str:
            amount_str = amount_str.replace("천만", "")
            return float(amount_str) * 10_000_000
        elif "만" in amount_str:
            amount_str = amount_str.replace("만", "")
            return float(amount_str) * 10_000
        
        try:
            return float(amount_str)
        except ValueError:
            return 0.0
    
    def _parse_quarter(self, quarter_str: str) -> Optional[int]:
        """분기 문자열 파싱"""
        if not quarter_str:
            return None
        
        if "1분기" in quarter_str or "Q1" in quarter_str:
            return 1
        elif "2분기" in quarter_str or "Q2" in quarter_str:
            return 2
        elif "3분기" in quarter_str or "Q3" in quarter_str:
            return 3
        elif "4분기" in quarter_str or "Q4" in quarter_str:
            return 4
        
        return None
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """날짜 문자열 파싱"""
        if not date_str:
            return None
        
        try:
            # YYYY-MM-DD 형식
            if "-" in date_str:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            # YYYY/MM/DD 형식
            elif "/" in date_str:
                return datetime.strptime(date_str, "%Y/%m/%d").date()
            # YYYYMMDD 형식
            elif len(date_str) == 8 and date_str.isdigit():
                return datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            pass
        
        return None
    
    def _get_mock_budget_data(self, year: int) -> Dict[str, Any]:
        """모의 예산 데이터 생성"""
        import random
        
        institutions = [
            "대한체육회", "국민체육진흥공단", "한국스포츠정책과학원",
            "서울특별시체육회", "경기도체육회", "부산광역시체육회"
        ]
        
        projects = [
            "엘리트선수 육성 지원", "생활체육 활성화", "체육시설 확충",
            "장애인체육 지원", "스포츠과학 연구개발"
        ]
        
        data = []
        for inst in institutions:
            for proj in projects:
                allocated = random.randint(10, 100) * 1_000_000_000  # 10억 ~ 100억
                executed = allocated * random.uniform(0.7, 0.98)
                
                data.append({
                    "연도": str(year),
                    "기관명": inst,
                    "사업명": proj,
                    "예산액": f"{allocated / 100_000_000:.1f}억",
                    "집행액": f"{executed / 100_000_000:.1f}억",
                    "집행률": f"{(executed/allocated*100):.1f}%"
                })
        
        return {
            "currentCount": len(data),
            "totalCount": len(data),
            "data": data
        }
    
    def _get_mock_performance_data(self, year: int, sport_code: Optional[str] = None) -> Dict[str, Any]:
        """모의 성과 데이터 생성"""
        import random
        
        sports = [
            {"code": "SOCCER", "name": "축구"},
            {"code": "BASEBALL", "name": "야구"},
            {"code": "BASKETBALL", "name": "농구"},
            {"code": "SWIMMING", "name": "수영"},
            {"code": "TAEKWONDO", "name": "태권도"}
        ]
        
        if sport_code:
            sports = [s for s in sports if s["code"] == sport_code]
        
        indicators = [
            "참여인원", "만족도", "메달획득수", "시설이용률", "프로그램운영수"
        ]
        
        data = []
        for sport in sports:
            for indicator in indicators:
                target = random.randint(50, 100) if "만족도" in indicator else random.randint(100, 10000)
                value = target * random.uniform(0.8, 1.2)
                
                data.append({
                    "연도": str(year),
                    "종목코드": sport["code"],
                    "종목명": sport["name"],
                    "지표명": indicator,
                    "목표값": str(target),
                    "실적값": str(value),
                    "달성률": f"{(value/target*100):.1f}%",
                    "측정일": f"{year}-12-31"
                })
        
        return {
            "currentCount": len(data),
            "totalCount": len(data),
            "data": data
        }
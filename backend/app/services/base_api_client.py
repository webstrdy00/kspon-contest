"""
공공데이터 API 기본 클라이언트
모든 API 클라이언트의 베이스 클래스
"""
import logging
import time
from typing import Dict, Optional, Any
from urllib.parse import urlencode
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """공공데이터 API 기본 클라이언트"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_key = settings.DATA_GO_KR_API_KEY
        self.timeout = settings.API_TIMEOUT
        self.max_retries = settings.API_MAX_RETRIES
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET"
    ) -> Dict[str, Any]:
        """
        API 요청 실행
        
        Args:
            endpoint: API 엔드포인트
            params: 요청 파라미터
            method: HTTP 메서드
            
        Returns:
            API 응답 데이터
        """
        if not self.api_key:
            raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        
        # 기본 파라미터 설정
        request_params = {
            "serviceKey": self.api_key,
            "type": "json",
            **(params or {})
        }
        
        # URL 구성
        url = f"{self.base_url}/{endpoint}"
        
        # 로깅
        logger.info(f"API 요청: {method} {url}")
        logger.debug(f"파라미터: {request_params}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                start_time = time.time()
                
                if method == "GET":
                    response = await client.get(url, params=request_params)
                else:
                    response = await client.post(url, json=request_params)
                
                elapsed_time = time.time() - start_time
                logger.info(f"API 응답 시간: {elapsed_time:.2f}초")
                
                # 상태 코드 확인
                response.raise_for_status()
                
                # JSON 응답 파싱
                data = response.json()
                
                # 공공데이터 API 오류 체크
                if self._check_api_error(data):
                    error_msg = data.get("response", {}).get("header", {}).get("resultMsg", "Unknown error")
                    raise Exception(f"API 오류: {error_msg}")
                
                return data
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP 오류: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.TimeoutException:
            logger.error(f"API 요청 타임아웃: {url}")
            raise
        except Exception as e:
            logger.error(f"API 요청 실패: {str(e)}")
            raise
    
    def _check_api_error(self, data: Dict[str, Any]) -> bool:
        """
        공공데이터 API 응답 오류 체크
        
        Args:
            data: API 응답 데이터
            
        Returns:
            오류 여부
        """
        # 일반적인 공공데이터 API 오류 응답 형식 체크
        if isinstance(data, dict):
            response = data.get("response", {})
            header = response.get("header", {})
            result_code = header.get("resultCode", "00")
            
            if result_code != "00" and result_code != "0000":
                return True
                
        return False
    
    async def get_paginated_data(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None
    ) -> list:
        """
        페이지네이션된 데이터 전체 조회
        
        Args:
            endpoint: API 엔드포인트
            params: 요청 파라미터
            max_pages: 최대 페이지 수 (None이면 전체)
            
        Returns:
            전체 데이터 리스트
        """
        all_data = []
        page_no = 1
        num_of_rows = settings.API_PAGE_SIZE
        
        while True:
            # 페이지 파라미터 추가
            page_params = {
                **(params or {}),
                "pageNo": page_no,
                "numOfRows": num_of_rows
            }
            
            # API 요청
            response = await self._request(endpoint, page_params)
            
            # 데이터 추출 (API마다 응답 구조가 다를 수 있음)
            items = self._extract_items(response)
            
            if not items:
                break
                
            all_data.extend(items)
            
            # 총 개수 확인
            total_count = self._extract_total_count(response)
            
            logger.info(f"페이지 {page_no} 조회 완료: {len(items)}개 (전체: {len(all_data)}/{total_count})")
            
            # 다음 페이지 확인
            if len(all_data) >= total_count:
                break
                
            if max_pages and page_no >= max_pages:
                logger.info(f"최대 페이지 수({max_pages}) 도달")
                break
                
            page_no += 1
            
            # Rate limiting을 위한 대기
            await self._rate_limit_delay()
        
        return all_data
    
    def _extract_items(self, response: Dict[str, Any]) -> list:
        """
        API 응답에서 아이템 추출 (서브클래스에서 오버라이드)
        """
        # 일반적인 공공데이터 API 응답 구조
        try:
            return response.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        except:
            return []
    
    def _extract_total_count(self, response: Dict[str, Any]) -> int:
        """
        API 응답에서 총 개수 추출 (서브클래스에서 오버라이드)
        """
        try:
            return int(response.get("response", {}).get("body", {}).get("totalCount", 0))
        except:
            return 0
    
    async def _rate_limit_delay(self):
        """Rate limiting을 위한 대기"""
        import asyncio
        await asyncio.sleep(0.5)  # 0.5초 대기
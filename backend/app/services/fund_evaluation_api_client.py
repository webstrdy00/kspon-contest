"""
국민체육진흥기금 기금지원사업평가 API 클라이언트
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.services.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class FundEvaluationAPIClient(BaseAPIClient):
    """국민체육진흥기금 기금지원사업평가 API 클라이언트"""
    
    def __init__(self):
        # 새로운 API URL 사용
        super().__init__("https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_FLDESTM_QSTN_API")
        
    async def get_evaluation_items(
        self,
        apply_year: Optional[int] = None,
        page_no: int = 1,
        num_of_rows: int = 100
    ) -> Dict[str, Any]:
        """
        기금지원사업 평가항목 정보 조회
        
        Args:
            apply_year: 적용년도
            page_no: 페이지 번호
            num_of_rows: 한 페이지 결과 수
            
        Returns:
            평가항목 데이터
        """
        params = {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "resultType": "json"  # JSON 형식으로 요청
        }
        
        if apply_year:
            params["aply_yr"] = apply_year
            
        return await self._request("todz_api_fun_qstn_api_i", params)
    
    async def get_all_evaluation_items(
        self,
        apply_year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 평가항목 데이터 조회
        
        Args:
            apply_year: 적용년도
            
        Returns:
            전체 평가항목 리스트
        """
        params = {"resultType": "json"}
        if apply_year:
            params["aply_yr"] = apply_year
            
        logger.info(f"전체 평가항목 조회 시작: {params}")
        
        items = await self.get_paginated_data(
            "todz_api_fun_qstn_api_i",
            params
        )
        
        logger.info(f"전체 평가항목 조회 완료: {len(items)}개")
        
        return items
    
    def parse_evaluation_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        원시 API 데이터를 표준 형식으로 파싱
        
        Args:
            raw_data: API 원시 데이터
            
        Returns:
            파싱된 평가항목 데이터
        """
        return {
            "apply_year": int(raw_data.get("aply_yr", 0)),
            "question_id": int(raw_data.get("fldestm_qstn_id", 0)),
            "category_code": raw_data.get("fldqstn_cat_cd"),
            "question_name": raw_data.get("qstn_nm"),
            "question_description": raw_data.get("qstn_desc_cn"),
            "question_remark": raw_data.get("qstn_rmk_cn"),
            "score_level": raw_data.get("scr_level_val"),
            "division_code": raw_data.get("gbn_cd"),
            "row_num": int(raw_data.get("row_num", 0)),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    async def get_evaluation_by_category(self, year: int) -> Dict[str, List[Dict[str, Any]]]:
        """
        카테고리별 평가항목 분류
        
        Args:
            year: 년도
            
        Returns:
            카테고리별 평가항목 데이터
        """
        all_items = await self.get_all_evaluation_items(apply_year=year)
        
        evaluation_by_category = {}
        
        for item in all_items:
            parsed = self.parse_evaluation_data(item)
            category = parsed["category_code"]
            
            if category not in evaluation_by_category:
                evaluation_by_category[category] = []
            
            evaluation_by_category[category].append({
                "question_id": parsed["question_id"],
                "question_name": parsed["question_name"],
                "description": parsed["question_description"],
                "score_level": parsed["score_level"],
                "remark": parsed["question_remark"]
            })
        
        return evaluation_by_category
    
    async def get_evaluation_criteria(self, year: int) -> Dict[str, Any]:
        """
        평가 기준 및 통계 조회
        
        Args:
            year: 년도
            
        Returns:
            평가 기준 통계
        """
        all_items = await self.get_all_evaluation_items(apply_year=year)
        
        # 카테고리별 통계
        category_stats = {}
        
        for item in all_items:
            parsed = self.parse_evaluation_data(item)
            category = parsed["category_code"]
            
            if category not in category_stats:
                category_stats[category] = {
                    "count": 0,
                    "items": [],
                    "max_score": 0
                }
            
            category_stats[category]["count"] += 1
            category_stats[category]["items"].append(parsed["question_name"])
            
            # 점수 레벨 파싱
            score_level = parsed["score_level"]
            if score_level and score_level.isdigit():
                category_stats[category]["max_score"] += int(score_level)
        
        return {
            "year": year,
            "total_items": len(all_items),
            "categories": category_stats,
            "evaluation_criteria": {
                "category_count": len(category_stats),
                "total_questions": len(all_items),
                "average_questions_per_category": len(all_items) / len(category_stats) if category_stats else 0
            }
        }
    
    async def compare_evaluation_years(
        self, 
        year1: int, 
        year2: int
    ) -> Dict[str, Any]:
        """
        연도별 평가항목 비교
        
        Args:
            year1: 비교 년도 1
            year2: 비교 년도 2
            
        Returns:
            연도별 평가항목 비교 결과
        """
        items1 = await self.get_all_evaluation_items(apply_year=year1)
        items2 = await self.get_all_evaluation_items(apply_year=year2)
        
        # 평가항목 ID 기준으로 비교
        items1_dict = {item.get("fldestm_qstn_id"): item for item in items1}
        items2_dict = {item.get("fldestm_qstn_id"): item for item in items2}
        
        # 추가된 항목
        added_items = []
        for qid, item in items2_dict.items():
            if qid not in items1_dict:
                added_items.append(self.parse_evaluation_data(item))
        
        # 삭제된 항목
        removed_items = []
        for qid, item in items1_dict.items():
            if qid not in items2_dict:
                removed_items.append(self.parse_evaluation_data(item))
        
        # 변경된 항목
        modified_items = []
        for qid in items1_dict:
            if qid in items2_dict:
                item1 = items1_dict[qid]
                item2 = items2_dict[qid]
                
                # 주요 필드 비교
                if (item1.get("qstn_nm") != item2.get("qstn_nm") or
                    item1.get("qstn_desc_cn") != item2.get("qstn_desc_cn") or
                    item1.get("scr_level_val") != item2.get("scr_level_val")):
                    
                    modified_items.append({
                        "question_id": qid,
                        "before": self.parse_evaluation_data(item1),
                        "after": self.parse_evaluation_data(item2)
                    })
        
        return {
            "comparison": f"{year1} vs {year2}",
            "summary": {
                "total_items_year1": len(items1),
                "total_items_year2": len(items2),
                "added": len(added_items),
                "removed": len(removed_items),
                "modified": len(modified_items)
            },
            "added_items": added_items,
            "removed_items": removed_items,
            "modified_items": modified_items
        }
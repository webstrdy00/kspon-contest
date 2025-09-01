#!/usr/bin/env python3
"""
국민체육진흥기금 기금지원사업평가 API 테스트
"""
import asyncio
import logging
import sys
from datetime import datetime

# 프로젝트 경로 추가
sys.path.append('.')

from app.services.fund_evaluation_api_client import FundEvaluationAPIClient

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """메인 테스트 함수"""
    
    print("=" * 60)
    print("국민체육진흥기금 기금지원사업평가 API 테스트")
    print("=" * 60)
    
    client = FundEvaluationAPIClient()
    
    # 1. 평가항목 조회 테스트
    print("\n[1] 2023년 평가항목 조회")
    print("-" * 40)
    
    try:
        logger.info("2023년 평가항목 조회 중...")
        evaluation_data = await client.get_evaluation_items(
            apply_year=2023,
            page_no=1,
            num_of_rows=5
        )
        
        # 응답 확인
        response = evaluation_data.get("response", {})
        header = response.get("header", {})
        body = response.get("body", {})
        
        if header.get("resultCode") == "00":
            items = body.get("items", {}).get("item", [])
            if isinstance(items, dict):
                items = [items]
            
            print(f"✅ 조회 성공! 총 {body.get('totalCount', 0)}개 중 {len(items)}개 표시")
            
            for idx, item in enumerate(items, 1):
                print(f"\n  [{idx}] 평가항목")
                print(f"    - 적용년도: {item.get('aply_yr')}")
                print(f"    - 문항명: {item.get('qstn_nm')}")
                print(f"    - 카테고리: {item.get('fldqstn_cat_cd')}")
                print(f"    - 점수레벨: {item.get('scr_level_val')}")
                
                desc = item.get('qstn_desc_cn', '')
                if desc:
                    print(f"    - 설명: {desc[:50]}...")
        else:
            print(f"⚠️ API 응답 오류: {header.get('resultMsg')}")
    
    except Exception as e:
        logger.error(f"평가항목 조회 실패: {e}")
        print(f"❌ 오류 발생: {str(e)}")
    
    # 2. 카테고리별 평가항목 분류
    print("\n[2] 카테고리별 평가항목 분류")
    print("-" * 40)
    
    try:
        logger.info("카테고리별 평가항목 분류 중...")
        category_data = await client.get_evaluation_by_category(2023)
        
        print(f"✅ 총 {len(category_data)}개 카테고리 발견")
        
        for category, items in category_data.items():
            print(f"\n  카테고리 [{category}]: {len(items)}개 항목")
            for item in items[:2]:  # 각 카테고리에서 2개만 표시
                print(f"    - {item['question_name']}")
    
    except Exception as e:
        logger.error(f"카테고리별 분류 실패: {e}")
        print(f"❌ 오류 발생: {str(e)}")
    
    # 3. 평가 기준 통계
    print("\n[3] 평가 기준 통계")
    print("-" * 40)
    
    try:
        logger.info("평가 기준 통계 조회 중...")
        criteria = await client.get_evaluation_criteria(2023)
        
        print(f"✅ 2023년 평가 기준 통계")
        print(f"  - 총 평가항목 수: {criteria['total_items']}")
        print(f"  - 카테고리 수: {criteria['evaluation_criteria']['category_count']}")
        print(f"  - 카테고리당 평균 항목: {criteria['evaluation_criteria']['average_questions_per_category']:.1f}")
        
        print("\n  카테고리별 상세:")
        for category, stats in criteria['categories'].items():
            print(f"    [{category}]: {stats['count']}개 항목, 최대점수 {stats['max_score']}점")
    
    except Exception as e:
        logger.error(f"평가 기준 통계 조회 실패: {e}")
        print(f"❌ 오류 발생: {str(e)}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
    
    print("\n💡 참고사항:")
    print("1. API 키가 유효한지 확인")
    print("2. API 활용신청이 승인되었는지 확인")
    print("3. 적용년도 파라미터가 올바른지 확인")


if __name__ == "__main__":
    asyncio.run(main())
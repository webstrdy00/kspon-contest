#!/usr/bin/env python
"""
기금지원사업평가 API 디버깅
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

async def test_evaluation_api_debug():
    """기금지원사업평가 API 상세 디버깅"""
    print("\n=== 기금지원사업평가 API 상세 테스트 ===")
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    url = "https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_FLDESTM_QSTN_API/todz_api_fun_qstn_api_i"
    
    # 다양한 연도로 시도
    years = ["2023", "2022", "2021", None]
    
    for year in years:
        params = {
            "serviceKey": api_key,
            "pageNo": 1,
            "numOfRows": 3,
            "resultType": "json"
        }
        
        if year:
            params["aply_yr"] = year
            print(f"\n--- {year}년 데이터 조회 ---")
        else:
            print(f"\n--- 연도 파라미터 없이 조회 ---")
        
        print(f"Params: {params}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if 'response' in data:
                            header = data['response'].get('header', {})
                            body = data['response'].get('body', {})
                            
                            print(f"헤더: {header}")
                            print(f"총 개수: {body.get('totalCount', 0)}")
                            
                            # items 구조 확인
                            items = body.get('items', {})
                            if items:
                                item_list = items.get('item', [])
                                if item_list:
                                    print(f"발견된 항목 수: {len(item_list)}")
                                    
                                    # 첫 번째 아이템 출력
                                    if isinstance(item_list, list) and len(item_list) > 0:
                                        first_item = item_list[0]
                                    else:
                                        first_item = item_list
                                    
                                    print("첫 번째 항목:")
                                    for key, value in first_item.items():
                                        print(f"  {key}: {value}")
                                else:
                                    print("item이 비어있음")
                            else:
                                print("items가 None 또는 비어있음")
                    except Exception as e:
                        print(f"JSON 파싱 오류: {e}")
                        print(f"Response: {response.text[:500]}")
                        
            except Exception as e:
                print(f"Error: {e}")

async def main():
    await test_evaluation_api_debug()

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python
"""
종합지원실적지표 API 디버깅
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

async def test_comprehensive_api_debug():
    """종합지원실적지표 API 상세 디버깅"""
    print("\n=== 종합지원실적지표 API 상세 테스트 ===")
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    url = "https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_INSTT_BSNS_RSLT_API/todz_api_fun_instt_api_i"
    
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 3,
        "resultType": "json",
        "fiscal_yr": "2023"
    }
    
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 전체 응답 구조 확인
                    if 'response' in data:
                        header = data['response'].get('header', {})
                        body = data['response'].get('body', {})
                        
                        print(f"\n헤더: {header}")
                        print(f"총 개수: {body.get('totalCount', 0)}")
                        
                        # items 구조 확인
                        items = body.get('items', {})
                        if items:
                            item_list = items.get('item', [])
                            if item_list:
                                print(f"\n총 {len(item_list)}개 항목 발견")
                                
                                # 첫 번째 아이템의 모든 필드 출력
                                for idx, item in enumerate(item_list[:3], 1):
                                    print(f"\n=== 항목 {idx} ===")
                                    for key, value in item.items():
                                        print(f"  {key}: {value}")
                            else:
                                print("item 리스트가 비어있음")
                        else:
                            print("items가 비어있음")
                except Exception as e:
                    print(f"JSON 파싱 오류: {e}")
                    print(f"Response Text: {response.text[:1000]}")
            else:
                print(f"Response Text: {response.text[:500]}")
                
        except Exception as e:
            print(f"Error: {e}")

async def main():
    await test_comprehensive_api_debug()

if __name__ == "__main__":
    asyncio.run(main())
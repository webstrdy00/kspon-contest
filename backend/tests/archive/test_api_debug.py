#!/usr/bin/env python
"""
공공데이터 API 디버깅 테스트
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

async def test_facilities_api_direct():
    """전국체육시설 API 직접 테스트"""
    print("\n=== 전국체육시설 API 직접 테스트 ===")
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    url = "https://apis.data.go.kr/B551014/SRVC_API_SFMS_FACI/TODZ_API_SFMS_FACI"
    
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "resultType": "json",
        "cp_nm": "서울특별시"
    }
    
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Response (JSON): {data}")
                except:
                    print(f"Response (Text): {response.text[:500]}")
            else:
                print(f"Response Text: {response.text[:500]}")
                
        except Exception as e:
            print(f"Error: {e}")

async def test_performance_api_direct():
    """체육인복지 경기력성과포상금 API 직접 테스트"""
    print("\n=== 체육인복지 경기력성과포상금 API 직접 테스트 ===")
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    url = "https://apis.data.go.kr/B551014/SRVC_TODZ_USFUN_PIRPEN_NON_DSPSN/TODZ_USFUN_PIRPEN_NON_DSPSN"
    
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "resultType": "json",
        "pmt_yymm": "202401"  # YYYYMM 형식
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
                    print(f"Response (JSON): {data}")
                except:
                    print(f"Response (Text): {response.text[:500]}")
            else:
                print(f"Response Text: {response.text[:500]}")
                
        except Exception as e:
            print(f"Error: {e}")

async def test_fund_api_direct():
    """국민체육진흥기금 API 직접 테스트"""
    print("\n=== 국민체육진흥기금 API 직접 테스트 ===")
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    url = "https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_OBJ_ORG_API/todz_api_fun_dvdc_erp_api_i"
    
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "resultType": "json",
        "biz_yr": "2023"
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
                    print(f"Response (JSON): {data}")
                except:
                    print(f"Response (Text): {response.text[:500]}")
            else:
                print(f"Response Text: {response.text[:500]}")
                
        except Exception as e:
            print(f"Error: {e}")

async def main():
    """메인 함수"""
    print("=" * 60)
    print("공공데이터 API 디버깅 테스트")
    print("=" * 60)
    
    api_key = os.getenv("DATA_GO_KR_API_KEY")
    print(f"API Key: {api_key[:20]}...")
    
    await test_facilities_api_direct()
    await test_performance_api_direct()
    await test_fund_api_direct()
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
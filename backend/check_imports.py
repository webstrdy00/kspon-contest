#!/usr/bin/env python3
"""
Phase 1 구현 검증 스크립트
모든 모듈이 제대로 import 되는지 확인
"""
import sys
import os

# Python 경로에 현재 디렉토리 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_imports():
    """Import 테스트"""
    
    print("=" * 60)
    print("Phase 1 Import 검증 시작")
    print("=" * 60)
    
    results = []
    
    # 1. Services 모듈 테스트
    print("\n[1] Services 모듈 Import 테스트")
    print("-" * 40)
    
    try:
        from app.services.base_api_client import BaseAPIClient
        print("✅ BaseAPIClient import 성공")
        results.append(("BaseAPIClient", True))
    except Exception as e:
        print(f"❌ BaseAPIClient import 실패: {e}")
        results.append(("BaseAPIClient", False))
    
    try:
        from app.services.facilities_api_client import FacilitiesAPIClient
        print("✅ FacilitiesAPIClient import 성공")
        results.append(("FacilitiesAPIClient", True))
    except Exception as e:
        print(f"❌ FacilitiesAPIClient import 실패: {e}")
        results.append(("FacilitiesAPIClient", False))
    
    try:
        from app.services.fund_api_client import FundAPIClient
        print("✅ FundAPIClient import 성공")
        results.append(("FundAPIClient", True))
    except Exception as e:
        print(f"❌ FundAPIClient import 실패: {e}")
        results.append(("FundAPIClient", False))
    
    try:
        from app.services.performance_api_client import PerformanceAPIClient
        print("✅ PerformanceAPIClient import 성공")
        results.append(("PerformanceAPIClient", True))
    except Exception as e:
        print(f"❌ PerformanceAPIClient import 실패: {e}")
        results.append(("PerformanceAPIClient", False))
    
    # 2. ETL 모듈 테스트
    print("\n[2] ETL 모듈 Import 테스트")
    print("-" * 40)
    
    try:
        from app.etl.csv_processor import CSVDataProcessor
        print("✅ CSVDataProcessor import 성공")
        results.append(("CSVDataProcessor", True))
    except Exception as e:
        print(f"❌ CSVDataProcessor import 실패: {e}")
        results.append(("CSVDataProcessor", False))
    
    # 3. Tasks 모듈 테스트
    print("\n[3] Tasks 모듈 Import 테스트")
    print("-" * 40)
    
    try:
        from app.tasks.scheduler import DataCollectionScheduler
        print("✅ DataCollectionScheduler import 성공")
        results.append(("DataCollectionScheduler", True))
    except Exception as e:
        print(f"❌ DataCollectionScheduler import 실패: {e}")
        results.append(("DataCollectionScheduler", False))
    
    # 4. API Endpoints 테스트
    print("\n[4] API Endpoints Import 테스트")
    print("-" * 40)
    
    try:
        from app.api.v1.endpoints import data_import
        print("✅ data_import endpoint import 성공")
        results.append(("data_import", True))
    except Exception as e:
        print(f"❌ data_import endpoint import 실패: {e}")
        results.append(("data_import", False))
    
    try:
        from app.api.v1.endpoints import csv_upload
        print("✅ csv_upload endpoint import 성공")
        results.append(("csv_upload", True))
    except Exception as e:
        print(f"❌ csv_upload endpoint import 실패: {e}")
        results.append(("csv_upload", False))
    
    try:
        from app.api.v1.endpoints import scheduler as scheduler_endpoint
        print("✅ scheduler endpoint import 성공")
        results.append(("scheduler_endpoint", True))
    except Exception as e:
        print(f"❌ scheduler endpoint import 실패: {e}")
        results.append(("scheduler_endpoint", False))
    
    # 5. 설정 확인
    print("\n[5] Config 설정 확인")
    print("-" * 40)
    
    try:
        from app.core.config import settings
        
        # 새로운 설정들이 있는지 확인
        config_attrs = [
            "FACILITIES_API_URL",
            "FUND_SUPPORT_API_URL",
            "PERFORMANCE_REWARD_API_URL",
            "API_TIMEOUT",
            "API_MAX_RETRIES",
            "API_PAGE_SIZE",
            "AUTO_START_SCHEDULER"
        ]
        
        for attr in config_attrs:
            if hasattr(settings, attr):
                value = getattr(settings, attr)
                print(f"✅ {attr}: {value}")
                results.append((attr, True))
            else:
                print(f"❌ {attr}: 설정 없음")
                results.append((attr, False))
                
    except Exception as e:
        print(f"❌ Config import 실패: {e}")
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("검증 결과 요약")
    print("=" * 60)
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    print(f"\n전체: {total_count}개 중 {success_count}개 성공")
    print(f"성공률: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n✅ Phase 1 구현이 정상적으로 완료되었습니다!")
    else:
        print("\n⚠️ 일부 모듈에 문제가 있습니다. 확인이 필요합니다.")
        failed = [name for name, success in results if not success]
        print(f"실패한 모듈: {', '.join(failed)}")
    
    return success_count == total_count

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
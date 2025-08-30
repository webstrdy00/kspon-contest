"""
CSV 파일 업로드 및 처리 API 엔드포인트
한국스포츠과학원 실태조사 데이터 처리
"""
import os
import shutil
from typing import Dict, Any, List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.etl.csv_processor import CSVDataProcessor
from app.core.deps import get_current_user_optional

router = APIRouter()


@router.post("/upload/facility-demand")
async def upload_facility_demand_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    필요 체육시설 CSV 파일 업로드 및 처리
    
    파일 형식:
    - 피벗 테이블 형태의 CSV
    - 첫 번째 컬럼: 지역/구분
    - 나머지 컬럼: 시설 유형별 수요 비율
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")
    
    try:
        # 임시 파일로 저장
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # CSV 처리
        processor = CSVDataProcessor()
        processed_data = processor.process_facility_demand_data(temp_path)
        
        # 통계 생성
        stats = processor.generate_summary_statistics(processed_data)
        
        # 데이터베이스 형식으로 변환
        db_records = processor.export_to_database_format(processed_data)
        
        # TODO: 실제 DB 저장 로직
        # for record in db_records:
        #     db.add(FacilityDemand(**record))
        # db.commit()
        
        # 임시 파일 삭제
        os.remove(temp_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "records_processed": len(db_records),
            "statistics": stats,
            "message": "CSV 파일이 성공적으로 처리되었습니다."
        }
        
    except Exception as e:
        # 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        raise HTTPException(status_code=500, detail=f"파일 처리 실패: {str(e)}")


@router.post("/upload/leisure-time")
async def upload_leisure_time_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    하루 여가시간 CSV 파일 업로드 및 처리
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")
    
    try:
        # 임시 파일로 저장
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # CSV 처리
        processor = CSVDataProcessor()
        processed_data = processor.process_leisure_time_data(temp_path)
        
        # 통계 생성
        stats = processor.generate_summary_statistics(processed_data)
        
        # 데이터베이스 형식으로 변환
        db_records = processor.export_to_database_format(processed_data)
        
        # 임시 파일 삭제
        os.remove(temp_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "records_processed": len(db_records),
            "statistics": stats,
            "message": "여가시간 CSV 파일이 성공적으로 처리되었습니다."
        }
        
    except Exception as e:
        # 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        raise HTTPException(status_code=500, detail=f"파일 처리 실패: {str(e)}")


@router.post("/merge-analysis")
async def merge_demand_supply_analysis(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    수요-공급 데이터 병합 분석
    
    CSV 수요 데이터와 API 공급 데이터를 병합하여
    수요-공급 불균형 지역을 찾아냅니다.
    """
    try:
        processor = CSVDataProcessor()
        
        # TODO: DB에서 데이터 조회
        # demand_data = db.query(FacilityDemand).all()
        # supply_data = db.query(SportsFacility).all()
        
        # 모의 데이터로 테스트
        import pandas as pd
        
        # 모의 수요 데이터
        demand_df = pd.DataFrame({
            'region_code': ['11', '11', '26', '26'],
            'facility_type': ['수영장', '체육관', '수영장', '체육관'],
            'demand_percentage': [45.2, 38.5, 52.1, 41.3]
        })
        
        # 모의 공급 데이터
        supply_df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'region_code': ['11', '11', '11', '26', '26'],
            'facility_type': ['수영장', '수영장', '체육관', '수영장', '체육관']
        })
        
        # 병합 분석
        merged = processor.merge_demand_supply_data(demand_df, supply_df)
        
        # 불균형 지역 찾기
        imbalanced = merged[merged['is_imbalanced'] == True]
        
        return {
            "status": "success",
            "total_analyzed": len(merged),
            "imbalanced_regions": len(imbalanced),
            "top_imbalanced": imbalanced.head(10).to_dict('records') if len(imbalanced) > 0 else [],
            "message": "수요-공급 분석이 완료되었습니다."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")


@router.get("/csv-templates")
async def get_csv_templates() -> Dict[str, Any]:
    """
    CSV 파일 템플릿 정보 제공
    """
    return {
        "templates": [
            {
                "name": "facility_demand",
                "description": "필요 체육시설 데이터",
                "columns": [
                    "지역",
                    "수영장(%)",
                    "체육관(%)",
                    "축구장(%)",
                    "테니스장(%)",
                    "농구장(%)"
                ],
                "example": {
                    "지역": "서울특별시",
                    "수영장(%)": 45.2,
                    "체육관(%)": 38.5,
                    "축구장(%)": 28.3
                }
            },
            {
                "name": "leisure_time",
                "description": "하루 여가시간 데이터",
                "columns": [
                    "연령대",
                    "평일_여가시간",
                    "휴일_여가시간"
                ],
                "example": {
                    "연령대": "20대",
                    "평일_여가시간": 3.5,
                    "휴일_여가시간": 6.2
                }
            }
        ]
    }
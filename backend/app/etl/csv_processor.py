"""
한국스포츠과학원 실태조사 CSV 데이터 처리 모듈
피벗 테이블 형태의 CSV를 Long-form으로 변환
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CSVDataProcessor:
    """CSV 데이터 처리 클래스"""
    
    def __init__(self, data_dir: str = "data/csv"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def process_facility_demand_data(self, file_path: str) -> pd.DataFrame:
        """
        필요 체육시설 CSV 데이터 처리
        피벗 테이블 → Long-form 변환
        
        Args:
            file_path: CSV 파일 경로
            
        Returns:
            처리된 DataFrame
        """
        try:
            # CSV 읽기 (인코딩 자동 감지)
            encodings = ['utf-8', 'cp949', 'euc-kr']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"CSV 파일 읽기 성공: {encoding} 인코딩")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("CSV 파일을 읽을 수 없습니다.")
            
            # 데이터 구조 분석
            logger.info(f"원본 데이터 shape: {df.shape}")
            logger.info(f"컬럼: {df.columns.tolist()}")
            
            # 피벗 테이블을 Long-form으로 변환
            processed_data = self._unpivot_demand_data(df)
            
            # 데이터 정제
            processed_data = self._clean_demand_data(processed_data)
            
            logger.info(f"처리된 데이터 shape: {processed_data.shape}")
            
            return processed_data
            
        except Exception as e:
            logger.error(f"CSV 처리 실패: {str(e)}")
            raise
    
    def _unpivot_demand_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        피벗 테이블 형태의 데이터를 Long-form으로 변환
        
        예시:
        Input (피벗):
            지역    수영장  체육관  축구장
            서울    45%    32%    28%
            부산    38%    41%    22%
            
        Output (Long-form):
            지역    시설유형  수요비율
            서울    수영장    45
            서울    체육관    32
            서울    축구장    28
            부산    수영장    38
            ...
        """
        # 첫 번째 컬럼을 지역/구분 기준으로 가정
        id_vars = df.columns[0]
        
        # 나머지 컬럼은 시설 유형
        value_vars = df.columns[1:].tolist()
        
        # Unpivot (melt)
        long_df = pd.melt(
            df,
            id_vars=[id_vars],
            value_vars=value_vars,
            var_name='facility_type',
            value_name='demand_percentage'
        )
        
        # 컬럼명 표준화
        long_df.rename(columns={id_vars: 'category'}, inplace=True)
        
        return long_df
    
    def _clean_demand_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터 정제 및 타입 변환
        """
        # 퍼센트 기호 제거 및 숫자 변환
        if df['demand_percentage'].dtype == 'object':
            df['demand_percentage'] = df['demand_percentage'].str.replace('%', '')
            df['demand_percentage'] = pd.to_numeric(df['demand_percentage'], errors='coerce')
        
        # NaN 값 처리
        df = df.dropna(subset=['demand_percentage'])
        
        # 지역 코드 매핑 추가
        df['region_code'] = df['category'].apply(self._map_region_code)
        
        # 조사년도 추가 (파일명에서 추출하거나 기본값)
        df['survey_year'] = datetime.now().year
        
        # 메타데이터 추가
        df['created_at'] = datetime.now()
        df['data_source'] = '한국스포츠과학원 실태조사'
        
        return df
    
    def _map_region_code(self, region_name: str) -> Optional[str]:
        """
        지역명을 지역코드로 매핑
        """
        region_mapping = {
            '서울': '11',
            '서울특별시': '11',
            '부산': '26',
            '부산광역시': '26',
            '대구': '27',
            '대구광역시': '27',
            '인천': '28',
            '인천광역시': '28',
            '광주': '29',
            '광주광역시': '29',
            '대전': '30',
            '대전광역시': '30',
            '울산': '31',
            '울산광역시': '31',
            '세종': '36',
            '세종특별자치시': '36',
            '경기': '41',
            '경기도': '41',
            '강원': '42',
            '강원도': '42',
            '충북': '43',
            '충청북도': '43',
            '충남': '44',
            '충청남도': '44',
            '전북': '45',
            '전라북도': '45',
            '전남': '46',
            '전라남도': '46',
            '경북': '47',
            '경상북도': '47',
            '경남': '48',
            '경상남도': '48',
            '제주': '50',
            '제주특별자치도': '50'
        }
        
        for key, code in region_mapping.items():
            if key in region_name:
                return code
        
        return None
    
    def process_leisure_time_data(self, file_path: str) -> pd.DataFrame:
        """
        하루 여가시간 CSV 데이터 처리
        
        Args:
            file_path: CSV 파일 경로
            
        Returns:
            처리된 DataFrame
        """
        try:
            # CSV 읽기
            df = self._read_csv_with_encoding(file_path)
            
            # 피벗 테이블을 Long-form으로 변환
            processed_data = self._unpivot_leisure_data(df)
            
            # 데이터 정제
            processed_data = self._clean_leisure_data(processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"여가시간 CSV 처리 실패: {str(e)}")
            raise
    
    def _read_csv_with_encoding(self, file_path: str) -> pd.DataFrame:
        """
        인코딩 자동 감지하여 CSV 읽기
        """
        encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
        
        for encoding in encodings:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"파일을 읽을 수 없습니다: {file_path}")
    
    def _unpivot_leisure_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        여가시간 피벗 데이터를 Long-form으로 변환
        """
        # 구조에 따라 적절히 변환
        # 예: 연령대별, 지역별 여가시간
        
        if '지역' in df.columns:
            id_vars = ['지역']
        elif '연령' in df.columns:
            id_vars = ['연령']
        else:
            id_vars = [df.columns[0]]
        
        # 시간 관련 컬럼 찾기
        time_columns = [col for col in df.columns if any(
            keyword in str(col) for keyword in ['평일', '휴일', '주말', '시간']
        )]
        
        if not time_columns:
            time_columns = df.columns[1:].tolist()
        
        long_df = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=time_columns,
            var_name='time_type',
            value_name='leisure_hours'
        )
        
        return long_df
    
    def _clean_leisure_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        여가시간 데이터 정제
        """
        # 숫자 변환
        df['leisure_hours'] = pd.to_numeric(df['leisure_hours'], errors='coerce')
        
        # NaN 제거
        df = df.dropna(subset=['leisure_hours'])
        
        # 메타데이터 추가
        df['survey_year'] = datetime.now().year
        df['created_at'] = datetime.now()
        
        return df
    
    def merge_demand_supply_data(
        self,
        demand_df: pd.DataFrame,
        supply_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        수요 데이터와 공급 데이터 병합
        
        Args:
            demand_df: 수요 데이터 (CSV)
            supply_df: 공급 데이터 (API)
            
        Returns:
            병합된 DataFrame
        """
        # 지역과 시설 유형을 기준으로 병합
        merged = pd.merge(
            supply_df,
            demand_df,
            how='outer',
            left_on=['region_code', 'facility_type'],
            right_on=['region_code', 'facility_type'],
            suffixes=('_supply', '_demand')
        )
        
        # 수요-공급 비율 계산
        merged['supply_count'] = merged.groupby(['region_code', 'facility_type']).transform('count')['id_supply']
        merged['demand_supply_ratio'] = merged['demand_percentage'] / (merged['supply_count'] + 1) * 100
        
        # 불균형 지역 표시
        merged['is_imbalanced'] = merged['demand_supply_ratio'] > 150  # 150% 이상이면 불균형
        
        return merged
    
    def export_to_database_format(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        DataFrame을 데이터베이스 저장 형식으로 변환
        
        Args:
            df: 처리된 DataFrame
            
        Returns:
            딕셔너리 리스트
        """
        # NaN을 None으로 변환
        df = df.where(pd.notnull(df), None)
        
        # 딕셔너리 리스트로 변환
        records = df.to_dict('records')
        
        # 날짜 형식 변환
        for record in records:
            for key, value in record.items():
                if isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat()
                elif isinstance(value, (np.int64, np.int32)):
                    record[key] = int(value)
                elif isinstance(value, (np.float64, np.float32)):
                    record[key] = float(value)
        
        return records
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        데이터 요약 통계 생성
        
        Args:
            df: 분석할 DataFrame
            
        Returns:
            요약 통계 딕셔너리
        """
        stats = {
            'total_records': len(df),
            'data_range': {
                'min_year': df['survey_year'].min() if 'survey_year' in df else None,
                'max_year': df['survey_year'].max() if 'survey_year' in df else None
            }
        }
        
        # 지역별 통계
        if 'region_code' in df:
            stats['by_region'] = df.groupby('region_code').size().to_dict()
        
        # 시설 유형별 통계
        if 'facility_type' in df:
            stats['by_facility'] = df.groupby('facility_type').agg({
                'demand_percentage': 'mean'
            }).to_dict()['demand_percentage']
        
        # 수요 상위 5개
        if 'demand_percentage' in df:
            top_demand = df.nlargest(5, 'demand_percentage')[['category', 'facility_type', 'demand_percentage']]
            stats['top_demand'] = top_demand.to_dict('records')
        
        return stats
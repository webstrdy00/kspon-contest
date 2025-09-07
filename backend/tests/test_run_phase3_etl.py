"""
run_phase3_etl.py 스크립트 테스트
run_id 회귀 방지 및 ETL 실행 검증
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import date
import asyncio

# 프로젝트 루트 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

from scripts.run_phase3_etl import run_etl_pipeline, generate_sample_data
from app.models.budget_performance import EtlRun
from app.models.dim import Institution, Sport, Project


class TestRunPhase3ETL:
    """Phase 3 ETL 실행 스크립트 테스트"""
    
    @pytest.mark.asyncio
    async def test_run_etl_pipeline_returns_run_id(self):
        """ETL 파이프라인이 올바른 run_id를 반환하는지 테스트"""
        with patch('scripts.run_phase3_etl.AsyncSessionLocal') as mock_session_local:
            # Mock session 설정
            mock_session = AsyncMock()
            mock_session_local.return_value.__aenter__.return_value = mock_session
            
            # Mock BudgetPerformanceETL
            with patch('scripts.run_phase3_etl.BudgetPerformanceETL') as mock_etl_class:
                mock_etl = AsyncMock()
                mock_etl.run_full_pipeline.return_value = True
                mock_etl_class.return_value = mock_etl
                
                # Mock EtlRun 조회
                mock_etl_run = Mock(spec=EtlRun)
                mock_etl_run.run_id = 42  # run_id 필드 사용 (id가 아님!)
                mock_etl_run.status = "success"
                mock_etl_run.row_count = 100  # row_count 필드 사용
                
                mock_result = Mock()
                mock_result.scalar_one_or_none.return_value = mock_etl_run
                mock_session.execute = AsyncMock(return_value=mock_result)
                
                # Mock BudgetAnalysisService
                with patch('scripts.run_phase3_etl.BudgetAnalysisService') as mock_service_class:
                    mock_service = AsyncMock()
                    mock_service.invalidate_cache.return_value = None
                    mock_service_class.return_value = mock_service
                    
                    # 실행
                    result = await run_etl_pipeline(year=2024)
                    
                    # 검증
                    assert result is True
                    mock_etl.run_full_pipeline.assert_called_once_with(
                        source="manual",
                        year=2024
                    )
                    # run_id로 캐시 무효화 호출 확인
                    mock_service.invalidate_cache.assert_called_once_with(42)
    
    @pytest.mark.asyncio
    async def test_etl_run_field_names_regression(self):
        """EtlRun 필드명이 올바르게 사용되는지 회귀 테스트"""
        with patch('scripts.run_phase3_etl.AsyncSessionLocal') as mock_session_local:
            mock_session = AsyncMock()
            mock_session_local.return_value.__aenter__.return_value = mock_session
            
            with patch('scripts.run_phase3_etl.BudgetPerformanceETL') as mock_etl_class:
                mock_etl = AsyncMock()
                mock_etl.run_full_pipeline.return_value = True
                mock_etl_class.return_value = mock_etl
                
                # EtlRun 모델 검증
                mock_etl_run = Mock(spec=EtlRun)
                # 올바른 필드명 확인
                assert hasattr(mock_etl_run, 'run_id')  # run_id 존재
                assert hasattr(mock_etl_run, 'row_count')  # row_count 존재
                
                # 잘못된 필드명 사용 시도 시 AttributeError
                with pytest.raises(AttributeError):
                    _ = mock_etl_run.id  # id 필드는 없음
                with pytest.raises(AttributeError):
                    _ = mock_etl_run.records_processed  # records_processed 필드는 없음
    
    @pytest.mark.asyncio
    async def test_generate_sample_data_loads_json(self):
        """generate_sample_data가 JSON 파일을 로드하는지 테스트"""
        with patch('scripts.run_phase3_etl.AsyncSessionLocal') as mock_session_local:
            mock_session = AsyncMock()
            mock_session.add_all = Mock()
            mock_session.flush = AsyncMock()
            mock_session.commit = AsyncMock()
            mock_session_local.return_value.__aenter__.return_value = mock_session
            
            # Mock JSON 파일 존재
            with patch('pathlib.Path.exists') as mock_exists:
                mock_exists.return_value = True
                
                # Mock JSON 파일 읽기
                mock_json_data = {
                    "institutions.json": [
                        {"name": "대한체육회", "type": "중앙", "description": "test"}
                    ],
                    "sports.json": [
                        {"code": "FB", "name": "축구", "category": "구기", "olympic_status": True}
                    ],
                    "projects.json": [
                        {"code": "PRJ001", "name": "엘리트 선수 육성", "type": "육성"}
                    ],
                    "indicators.json": [
                        {"code": "IND001", "name": "메달 획득 수", "category": "성과", "unit": "개", "weight": 0.3}
                    ]
                }
                
                def mock_open_side_effect(file_path, *args, **kwargs):
                    file_name = Path(file_path).name
                    if file_name in mock_json_data:
                        mock_file = MagicMock()
                        mock_file.__enter__.return_value.read.return_value = str(mock_json_data[file_name])
                        return mock_file
                    raise FileNotFoundError(f"File not found: {file_path}")
                
                with patch('builtins.open', side_effect=mock_open_side_effect):
                    with patch('json.load') as mock_json_load:
                        def json_load_side_effect(f):
                            content = f.read()
                            return eval(content)  # 테스트용 간단한 파싱
                        
                        mock_json_load.side_effect = json_load_side_effect
                        
                        # 실행
                        result = await generate_sample_data()
                        
                        # 검증
                        assert result is True
                        # session.add_all이 호출되었는지 확인
                        assert mock_session.add_all.call_count > 0
    
    @pytest.mark.asyncio
    async def test_custom_seed_dir_parameter(self):
        """커스텀 시드 디렉토리 파라미터가 작동하는지 테스트"""
        custom_dir = "/custom/seed/path"
        
        with patch('scripts.run_phase3_etl.AsyncSessionLocal') as mock_session_local:
            mock_session = AsyncMock()
            mock_session_local.return_value.__aenter__.return_value = mock_session
            
            with patch('pathlib.Path') as mock_path:
                mock_path_instance = Mock()
                mock_path_instance.exists.return_value = False  # 파일 없음으로 설정
                mock_path.return_value = mock_path_instance
                
                # 실행
                result = await generate_sample_data(seed_dir=custom_dir)
                
                # Path가 custom_dir로 생성되었는지 확인
                mock_path.assert_called_with(custom_dir)
    
    def test_etl_run_model_fields(self):
        """EtlRun 모델의 필드 정의가 올바른지 확인"""
        # EtlRun 모델 import
        from app.models.budget_performance import EtlRun
        from sqlalchemy import inspect
        
        # 모델의 컬럼 확인
        mapper = inspect(EtlRun)
        columns = {col.key for col in mapper.columns}
        
        # 필수 필드 확인
        assert 'run_id' in columns, "EtlRun must have 'run_id' field"
        assert 'row_count' in columns, "EtlRun must have 'row_count' field"
        assert 'status' in columns, "EtlRun must have 'status' field"
        
        # 잘못된 필드가 없는지 확인
        assert 'id' not in columns, "EtlRun should not have 'id' field (use 'run_id' instead)"
        assert 'records_processed' not in columns, "EtlRun should not have 'records_processed' field (use 'row_count' instead)"


class TestETLDimensionLoading:
    """ETL 디멘션 로딩 테스트"""
    
    @pytest.mark.asyncio
    async def test_etl_loads_dimensions_from_json(self):
        """BudgetPerformanceETL이 JSON에서 디멘션을 로드하는지 테스트"""
        from app.etl.budget_performance_etl import BudgetPerformanceETL
        
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.commit = AsyncMock()
        
        # ETL 인스턴스 생성
        etl = BudgetPerformanceETL(mock_session)
        
        # Mock JSON 파일 존재 및 읽기
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            mock_json_data = [
                {"name": "테스트기관", "type": "중앙", "description": "테스트"}
            ]
            
            with patch('builtins.open', mock=True):
                with patch('json.load', return_value=mock_json_data):
                    # _load_dimensions 호출
                    await etl._load_dimensions()
                    
                    # execute가 호출되었는지 확인
                    assert mock_session.execute.called
                    # commit이 호출되었는지 확인  
                    mock_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
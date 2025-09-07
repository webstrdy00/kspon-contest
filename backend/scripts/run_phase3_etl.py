#!/usr/bin/env python
"""
Phase 3 ETL 실행 스크립트
초기 데이터 생성 및 캐시 구축
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, date

# 프로젝트 루트 경로 추가
sys.path.append(str(Path(__file__).parent.parent))

from app.db.database import AsyncSessionLocal
from app.etl.budget_performance_etl import BudgetPerformanceETL
from app.services.budget_analysis import BudgetAnalysisService
from app.models.budget_performance import EtlRun
from sqlalchemy import select
import logging
from typing import Optional

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_etl_pipeline(year: int = 2024, mapping_dir: Optional[str] = None):
    """ETL 파이프라인 실행"""
    async with AsyncSessionLocal() as session:
        try:
            logger.info(f"ETL 파이프라인 시작 - 연도: {year}")
            if mapping_dir:
                logger.info(f"커스텀 매핑 디렉토리 사용: {mapping_dir}")
            
            # ETL 인스턴스 생성
            etl = BudgetPerformanceETL(session, mapping_dir=mapping_dir)
            
            # 전체 파이프라인 실행
            success = await etl.run_full_pipeline(
                source="manual",
                year=year
            )
            
            if success:
                logger.info("ETL 파이프라인 성공적으로 완료")
                
                # 최신 run_id 조회
                stmt = select(EtlRun).order_by(EtlRun.run_id.desc()).limit(1)
                result = await session.execute(stmt)
                latest_run = result.scalar_one_or_none()
                
                if latest_run:
                    logger.info(f"ETL Run ID: {latest_run.run_id}")
                    logger.info(f"상태: {latest_run.status}")
                    logger.info(f"처리된 레코드 수: {latest_run.row_count}")
                    
                    # 캐시 무효화
                    service = BudgetAnalysisService(session)
                    await service.invalidate_cache(latest_run.run_id)
                    logger.info("캐시 무효화 완료")
                    
                return True
            else:
                logger.error("ETL 파이프라인 실패")
                return False
                
        except Exception as e:
            logger.error(f"ETL 실행 중 오류: {str(e)}")
            await session.rollback()
            return False


async def generate_sample_data(seed_dir: Optional[str] = None):
    """샘플 데이터 생성 (테스트용)"""
    async with AsyncSessionLocal() as session:
        try:
            logger.info("샘플 데이터 생성 시작")
            
            from app.models.dim import Institution, Sport, Project
            from app.models.budget_performance import BudgetExecution, PerformanceMetric
            from decimal import Decimal
            import json
            
            # 시드 데이터 디렉토리 설정
            seed_path = Path(seed_dir) if seed_dir else Path(__file__).parent.parent / "app" / "etl" / "seed_data"
            
            # 1. 기관 생성
            institutions_file = seed_path / "institutions.json"
            if institutions_file.exists():
                with open(institutions_file, "r", encoding="utf-8") as f:
                    institutions_data = json.load(f)
                    institutions = [
                        Institution(
                            name=inst["name"],
                            type=inst["type"],
                            description=inst.get("description")
                        )
                        for inst in institutions_data
                    ]
            else:
                logger.warning(f"Institutions seed file not found: {institutions_file}")
                institutions = []
            
            if institutions:
                session.add_all(institutions)
                await session.flush()
                logger.info(f"Created {len(institutions)} institutions")
            
            # 2. 종목 생성
            sports_file = seed_path / "sports.json"
            if sports_file.exists():
                with open(sports_file, "r", encoding="utf-8") as f:
                    sports_data = json.load(f)
                    sports = [
                        Sport(
                            code=sport["code"],
                            name=sport["name"],
                            category=sport["category"],
                            olympic_status=sport.get("olympic_status", False),
                            description=sport.get("description")
                        )
                        for sport in sports_data
                    ]
            else:
                logger.warning(f"Sports seed file not found: {sports_file}")
                sports = []
            
            if sports:
                session.add_all(sports)
                await session.flush()
                logger.info(f"Created {len(sports)} sports")
            
            # 3. 프로젝트 생성
            projects_file = seed_path / "projects.json"
            if projects_file.exists():
                with open(projects_file, "r", encoding="utf-8") as f:
                    projects_data = json.load(f)
                    projects = [
                        Project(
                            code=proj["code"],
                            name=proj["name"],
                            type=proj["type"],
                            description=proj.get("description")
                        )
                        for proj in projects_data
                    ]
            else:
                logger.warning(f"Projects seed file not found: {projects_file}")
                projects = []
            
            if projects:
                session.add_all(projects)
                await session.flush()
                logger.info(f"Created {len(projects)} projects")
            
            # 4. 예산 집행 데이터 생성
            run_id = 1  # 초기 run_id
            for inst in institutions[:2]:
                for proj in projects[:2]:
                    for year in [2023, 2024]:
                        budget = BudgetExecution(
                            run_id=run_id,
                            year=year,
                            institution_id=inst.id,
                            project_id=proj.id,
                            allocated=Decimal(10000000000),  # 100억
                            executed=Decimal(8500000000 + year * 100000000),  # 85억~
                            execution_date=date(year, 12, 31)
                        )
                        session.add(budget)
            
            # 5. 성과 지표 생성
            from app.models.budget_performance import PerformanceIndicator
            
            indicators_file = seed_path / "indicators.json"
            if indicators_file.exists():
                with open(indicators_file, "r", encoding="utf-8") as f:
                    indicators_data = json.load(f)
                    indicators = [
                        PerformanceIndicator(
                            code=ind["code"],
                            name=ind["name"],
                            category=ind["category"],
                            unit=ind["unit"],
                            weight=ind.get("weight", 0.2),
                            description=ind.get("description")
                        )
                        for ind in indicators_data
                    ]
            else:
                logger.warning(f"Indicators seed file not found: {indicators_file}")
                indicators = []
            
            if indicators:
                session.add_all(indicators)
                await session.flush()
                logger.info(f"Created {len(indicators)} indicators")
            
            # 6. 성과 메트릭 생성
            for sport in sports[:3]:
                for indicator in indicators:
                    metric = PerformanceMetric(
                        run_id=run_id,
                        indicator_id=indicator.id,
                        sport_id=sport.id,
                        measured_on=date(2024, 12, 31),
                        value=Decimal(80 + sport.id * 5),
                        normalized_value=0.85
                    )
                    session.add(metric)
            
            await session.commit()
            logger.info("샘플 데이터 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"샘플 데이터 생성 중 오류: {str(e)}")
            await session.rollback()
            return False


async def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 3 ETL 실행")
    parser.add_argument("--year", type=int, default=2024, help="처리할 연도")
    parser.add_argument("--sample", action="store_true", help="샘플 데이터 생성")
    parser.add_argument("--mapping-dir", type=str, help="커스텀 매핑 파일 디렉토리 경로")
    parser.add_argument("--seed-dir", type=str, help="커스텀 시드 데이터 디렉토리 경로")
    args = parser.parse_args()
    
    if args.sample:
        # 샘플 데이터 생성
        success = await generate_sample_data(seed_dir=args.seed_dir)
        if not success:
            logger.error("샘플 데이터 생성 실패")
            sys.exit(1)
    
    # ETL 파이프라인 실행
    success = await run_etl_pipeline(args.year, mapping_dir=args.mapping_dir)
    
    if success:
        logger.info("Phase 3 ETL 완료")
        sys.exit(0)
    else:
        logger.error("Phase 3 ETL 실패")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
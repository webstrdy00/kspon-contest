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

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_etl_pipeline(year: int = 2024):
    """ETL 파이프라인 실행"""
    async with AsyncSessionLocal() as session:
        try:
            logger.info(f"ETL 파이프라인 시작 - 연도: {year}")
            
            # ETL 인스턴스 생성
            etl = BudgetPerformanceETL(session)
            
            # 전체 파이프라인 실행
            success = await etl.run_full_pipeline(
                source="manual",
                year=year
            )
            
            if success:
                logger.info("ETL 파이프라인 성공적으로 완료")
                
                # 최신 run_id 조회
                stmt = select(EtlRun).order_by(EtlRun.id.desc()).limit(1)
                result = await session.execute(stmt)
                latest_run = result.scalar_one_or_none()
                
                if latest_run:
                    logger.info(f"ETL Run ID: {latest_run.id}")
                    logger.info(f"상태: {latest_run.status}")
                    logger.info(f"처리된 레코드 수: {latest_run.records_processed}")
                    
                    # 캐시 무효화
                    service = BudgetAnalysisService(session)
                    await service.invalidate_cache(latest_run.id)
                    logger.info("캐시 무효화 완료")
                    
                return True
            else:
                logger.error("ETL 파이프라인 실패")
                return False
                
        except Exception as e:
            logger.error(f"ETL 실행 중 오류: {str(e)}")
            await session.rollback()
            return False


async def generate_sample_data():
    """샘플 데이터 생성 (테스트용)"""
    async with AsyncSessionLocal() as session:
        try:
            logger.info("샘플 데이터 생성 시작")
            
            from app.models.dim import Institution, Sport, Project
            from app.models.budget_performance import BudgetExecution, PerformanceMetric
            from decimal import Decimal
            
            # 1. 기관 생성
            institutions = [
                Institution(name="대한체육회", type="중앙"),
                Institution(name="서울시체육회", type="지방"),
                Institution(name="국민체육진흥공단", type="산하기관"),
            ]
            session.add_all(institutions)
            await session.flush()
            
            # 2. 종목 생성
            sports = [
                Sport(code="FB", name="축구", category="구기", olympic_status=True),
                Sport(code="BB", name="야구", category="구기", olympic_status=False),
                Sport(code="SW", name="수영", category="개인", olympic_status=True),
                Sport(code="TN", name="테니스", category="개인", olympic_status=True),
                Sport(code="BD", name="배드민턴", category="개인", olympic_status=True),
            ]
            session.add_all(sports)
            await session.flush()
            
            # 3. 프로젝트 생성
            projects = [
                Project(code="PRJ001", name="엘리트 선수 육성", type="육성"),
                Project(code="PRJ002", name="생활체육 활성화", type="보급"),
                Project(code="PRJ003", name="체육시설 확충", type="시설"),
            ]
            session.add_all(projects)
            await session.flush()
            
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
            
            indicators = [
                PerformanceIndicator(
                    code="IND001",
                    name="메달 획득 수",
                    category="성과",
                    unit="개",
                    weight=0.3
                ),
                PerformanceIndicator(
                    code="IND002", 
                    name="참여 인원",
                    category="참여",
                    unit="명",
                    weight=0.2
                ),
            ]
            session.add_all(indicators)
            await session.flush()
            
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
    args = parser.parse_args()
    
    if args.sample:
        # 샘플 데이터 생성
        success = await generate_sample_data()
        if not success:
            logger.error("샘플 데이터 생성 실패")
            sys.exit(1)
    
    # ETL 파이프라인 실행
    success = await run_etl_pipeline(args.year)
    
    if success:
        logger.info("Phase 3 ETL 완료")
        sys.exit(0)
    else:
        logger.error("Phase 3 ETL 실패")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
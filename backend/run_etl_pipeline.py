#!/usr/bin/env python3
"""
ETL 파이프라인 실행 스크립트
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
import logging

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from app.db.session import get_async_db
from app.etl.budget_performance_etl import BudgetPerformanceETL

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_etl(year: int = 2024, source: str = "manual"):
    """ETL 파이프라인 실행"""
    logger.info("=" * 60)
    logger.info(f"ETL 파이프라인 실행 시작 - {year}년 데이터")
    logger.info("=" * 60)
    
    async for session in get_async_db():
        try:
            etl = BudgetPerformanceETL(session)
            result = await etl.run_full_pipeline(source=source, year=year)
            
            logger.info("\n✅ ETL 파이프라인 실행 완료!")
            logger.info(f"Run ID: {result['run_id']}")
            logger.info(f"Status: {result['status']}")
            logger.info("\n통계:")
            for key, value in result['stats'].items():
                if key != 'errors':
                    logger.info(f"  - {key}: {value}")
            
            if result['stats']['errors']:
                logger.warning("\n⚠️ 오류 발생:")
                for error in result['stats']['errors']:
                    logger.warning(f"  - {error}")
            
            return result
            
        except Exception as e:
            logger.error(f"ETL 파이프라인 실행 실패: {str(e)}")
            raise
        finally:
            await session.close()


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ETL 파이프라인 실행")
    parser.add_argument("--year", type=int, default=2024, help="처리할 연도")
    parser.add_argument("--source", default="manual", help="ETL 소스 (manual/scheduled)")
    
    args = parser.parse_args()
    
    try:
        result = await run_etl(year=args.year, source=args.source)
        sys.exit(0 if result['status'] == 'success' else 1)
    except Exception as e:
        logger.error(f"프로그램 실행 실패: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
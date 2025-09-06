#!/usr/bin/env python3
"""
Phase 3 마이그레이션 실행 스크립트
수동으로 마이그레이션을 적용하기 위한 스크립트
"""
import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from app.db.session import async_engine
from app.models.base import Base
from app.models import (
    # 기존 모델
    SportsFacility, Region, Proposal, ProposalVote, 
    User, UserBadge, RegionalReport,
    # Phase 3 모델
    Institution, Sport, Project, InstitutionRegion, ProjectSport,
    IndicatorMeta, PerformanceMetric, BudgetExecution, EtlRun, AggregationCache
)


async def create_phase3_tables():
    """Phase 3 테이블 생성"""
    try:
        print("Phase 3 테이블 생성 시작...")
        
        async with async_engine.begin() as conn:
            # 모든 테이블 생성 (이미 존재하는 테이블은 건너뜀)
            await conn.run_sync(Base.metadata.create_all)
            
            print("✅ 테이블 생성 완료")
            
            # 생성된 테이블 목록 확인
            result = await conn.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
            )
            tables = result.fetchall()
            
            print("\n현재 데이터베이스 테이블 목록:")
            phase3_tables = [
                'institution', 'sport', 'project', 
                'institution_region', 'project_sport',
                'indicator_meta', 'performance_metric', 
                'budget_execution', 'etl_runs', 'aggregation_cache'
            ]
            
            for table in tables:
                table_name = table[0]
                if table_name in phase3_tables:
                    print(f"  ✅ {table_name} (Phase 3)")
                else:
                    print(f"  - {table_name}")
            
            # Materialized View 생성 (PostgreSQL만 해당)
            print("\n머터리얼라이즈드 뷰 생성...")
            
            # 기존 뷰가 있으면 삭제
            await conn.execute("DROP MATERIALIZED VIEW IF EXISTS mv_efficiency_by_year_sport CASCADE")
            await conn.execute("DROP MATERIALIZED VIEW IF EXISTS mv_roi_by_year_sport CASCADE")
            await conn.execute("DROP MATERIALIZED VIEW IF EXISTS mv_region_summary CASCADE")
            
            # 효율성 분석 뷰
            await conn.execute("""
                CREATE MATERIALIZED VIEW mv_efficiency_by_year_sport AS
                SELECT 
                    be.run_id,
                    be.year,
                    ps.sport_id,
                    s.name as sport_name,
                    SUM(be.allocated) as total_allocated,
                    SUM(be.executed) as total_executed,
                    AVG(be.execution_rate) as avg_execution_rate,
                    COUNT(DISTINCT be.institution_id) as institution_count,
                    COUNT(DISTINCT be.project_id) as project_count
                FROM budget_execution be
                JOIN project_sport ps ON ps.project_id = be.project_id
                JOIN sport s ON s.id = ps.sport_id
                GROUP BY be.run_id, be.year, ps.sport_id, s.name
            """)
            
            # ROI 분석 뷰
            await conn.execute("""
                CREATE MATERIALIZED VIEW mv_roi_by_year_sport AS
                SELECT
                    pm.run_id,
                    EXTRACT(YEAR FROM pm.measured_on)::integer as year,
                    pm.sport_id,
                    s.name as sport_name,
                    COUNT(DISTINCT pm.indicator_id) as indicator_count,
                    AVG(pm.normalized_value) as avg_normalized_score,
                    SUM(pm.value) as total_value
                FROM performance_metric pm
                JOIN sport s ON s.id = pm.sport_id
                GROUP BY pm.run_id, EXTRACT(YEAR FROM pm.measured_on), pm.sport_id, s.name
            """)
            
            # 지역별 요약 뷰
            await conn.execute("""
                CREATE MATERIALIZED VIEW mv_region_summary AS
                SELECT
                    ir.region_code,
                    r.name as region_name,
                    be.run_id,
                    be.year,
                    COUNT(DISTINCT ir.institution_id) as institution_count,
                    SUM(be.allocated) as total_allocated,
                    SUM(be.executed) as total_executed,
                    AVG(be.execution_rate) as avg_execution_rate
                FROM institution_region ir
                JOIN region r ON r.code = ir.region_code
                JOIN budget_execution be ON be.institution_id = ir.institution_id
                WHERE ir.valid_to IS NULL
                GROUP BY ir.region_code, r.name, be.run_id, be.year
            """)
            
            # 인덱스 생성
            await conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_eff_run_year_sport ON mv_efficiency_by_year_sport(run_id, year, sport_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_eff_year ON mv_efficiency_by_year_sport(year)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_eff_sport ON mv_efficiency_by_year_sport(sport_id)")
            
            await conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_roi_run_year_sport ON mv_roi_by_year_sport(run_id, year, sport_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_roi_year ON mv_roi_by_year_sport(year)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_roi_sport ON mv_roi_by_year_sport(sport_id)")
            
            await conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_region_run_year_code ON mv_region_summary(run_id, year, region_code)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_region_year ON mv_region_summary(year)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_mv_region_code ON mv_region_summary(region_code)")
            
            print("✅ 머터리얼라이즈드 뷰 생성 완료")
            
            # 샘플 데이터 삽입 (초기 디멘션 데이터)
            print("\n초기 디멘션 데이터 삽입...")
            
            # 기본 기관 데이터
            await conn.execute("""
                INSERT INTO institution (name, type) VALUES 
                ('대한체육회', '체육단체'),
                ('대한장애인체육회', '체육단체'),
                ('국민체육진흥공단', '공공기관'),
                ('한국스포츠정책과학원', '연구기관'),
                ('문화체육관광부', '중앙정부')
                ON CONFLICT (name) DO NOTHING
            """)
            
            # 기본 종목 데이터
            await conn.execute("""
                INSERT INTO sport (code, name, category, olympic_status) VALUES 
                ('SOCCER', '축구', '단체구기', true),
                ('BASEBALL', '야구', '단체구기', true),
                ('BASKETBALL', '농구', '단체구기', true),
                ('VOLLEYBALL', '배구', '단체구기', true),
                ('TAEKWONDO', '태권도', '격투', true),
                ('SWIMMING', '수영', '기초체육', true),
                ('ATHLETICS', '육상', '기초체육', true),
                ('ARCHERY', '양궁', '표적', true),
                ('GOLF', '골프', '라켓', true),
                ('ESPORTS', 'e스포츠', '기타', false)
                ON CONFLICT (code) DO NOTHING
            """)
            
            # 기본 프로젝트 데이터
            await conn.execute("""
                INSERT INTO project (name, code, type) VALUES 
                ('엘리트선수 육성 지원', 'ELITE_01', '육성'),
                ('생활체육 활성화', 'LIFE_01', '지원'),
                ('체육시설 확충', 'FACILITY_01', '시설'),
                ('스포츠과학 연구개발', 'RND_01', '연구'),
                ('국제대회 개최 지원', 'EVENT_01', '대회운영')
                ON CONFLICT (name) DO NOTHING
            """)
            
            # 기본 지표 메타데이터
            await conn.execute("""
                INSERT INTO indicator_meta (name, description, value_type, aggregation_rule, scaling, unit, category) VALUES 
                ('참여인원', '프로그램 참여 인원수', 'int', 'sum', 'none', '명', '참여'),
                ('만족도', '프로그램 만족도 점수', 'float', 'avg', 'none', '점', '만족도'),
                ('메달획득', '국제대회 메달 획득 수', 'int', 'sum', 'none', '개', '성과'),
                ('시설이용률', '체육시설 이용률', 'percentage', 'avg', 'none', '%', '효율성'),
                ('예산집행률', '예산 집행 효율성', 'percentage', 'avg', 'none', '%', '효율성')
                ON CONFLICT (name) DO NOTHING
            """)
            
            # 첫 번째 ETL 실행 기록 생성
            await conn.execute("""
                INSERT INTO etl_runs (source, schema_version, status, row_count) 
                VALUES ('initial_setup', 'v1.0', 'success', 0)
                ON CONFLICT DO NOTHING
            """)
            
            print("✅ 초기 데이터 삽입 완료")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise


async def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Phase 3: 예산-성과 분석 시스템 데이터베이스 설정")
    print("=" * 60)
    
    await create_phase3_tables()
    
    print("\n✅ Phase 3 데이터베이스 설정 완료!")
    print("다음 단계: D2 - ETL 파이프라인 구축")


if __name__ == "__main__":
    asyncio.run(main())
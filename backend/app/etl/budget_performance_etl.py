"""
Budget and Performance ETL Pipeline
예산 및 성과 데이터 수집, 변환, 적재 파이프라인
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.db.session import get_async_db
from app.models import (
    Institution, Sport, Project, InstitutionRegion, ProjectSport,
    IndicatorMeta, PerformanceMetric, BudgetExecution, EtlRun, AggregationCache
)
from app.etl.normalization import DataNormalizer
from app.etl.public_api_client import PublicDataAPIClient

logger = logging.getLogger(__name__)


class BudgetPerformanceETL:
    """예산-성과 ETL 파이프라인"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.api_client = PublicDataAPIClient()
        self.normalizer = DataNormalizer()
        self.run_id: Optional[int] = None
        self.stats = {
            "institutions_created": 0,
            "sports_created": 0,
            "projects_created": 0,
            "budgets_loaded": 0,
            "metrics_loaded": 0,
            "errors": []
        }
    
    async def run_full_pipeline(self, source: str = "manual", year: int = 2024) -> Dict[str, Any]:
        """전체 ETL 파이프라인 실행"""
        try:
            # 1. ETL 실행 기록 생성
            self.run_id = await self._create_etl_run(source)
            logger.info(f"ETL 파이프라인 시작 - Run ID: {self.run_id}")
            
            # 2. 디멘션 데이터 로드/업데이트
            await self._load_dimensions()
            
            # 3. 예산 데이터 수집 및 적재
            await self._load_budget_data(year)
            
            # 4. 성과 데이터 수집 및 적재
            await self._load_performance_data(year)
            
            # 5. 매핑 테이블 업데이트
            await self._update_mappings()
            
            # 6. 집계 데이터 생성
            await self._build_aggregations(year)
            
            # 7. Materialized View 리프레시
            await self._refresh_materialized_views()
            
            # 8. ETL 실행 완료 마킹
            await self._complete_etl_run()
            
            logger.info(f"ETL 파이프라인 완료 - Run ID: {self.run_id}")
            return {
                "run_id": self.run_id,
                "status": "success",
                "stats": self.stats
            }
            
        except Exception as e:
            logger.error(f"ETL 파이프라인 실패: {str(e)}")
            await self._fail_etl_run(str(e))
            raise
    
    async def _create_etl_run(self, source: str) -> int:
        """ETL 실행 기록 생성"""
        etl_run = EtlRun(
            source=source,
            schema_version="v1.0",
            started_at=datetime.utcnow(),
            status="running"
        )
        self.session.add(etl_run)
        await self.session.flush()
        return etl_run.run_id
    
    async def _load_dimensions(self):
        """디멘션 테이블 로드/업데이트"""
        logger.info("디멘션 데이터 로드 시작...")
        
        # 기본 기관 데이터
        institutions = [
            {"name": "대한체육회", "type": "체육단체"},
            {"name": "대한장애인체육회", "type": "체육단체"},
            {"name": "국민체육진흥공단", "type": "공공기관"},
            {"name": "한국스포츠정책과학원", "type": "연구기관"},
            {"name": "문화체육관광부", "type": "중앙정부"},
            {"name": "서울특별시체육회", "type": "지방체육단체"},
            {"name": "경기도체육회", "type": "지방체육단체"},
            {"name": "부산광역시체육회", "type": "지방체육단체"},
        ]
        
        for inst_data in institutions:
            stmt = insert(Institution).values(**inst_data)
            stmt = stmt.on_conflict_do_nothing(index_elements=['name'])
            await self.session.execute(stmt)
            self.stats["institutions_created"] += 1
        
        # 종목 데이터
        sports = [
            {"code": "SOCCER", "name": "축구", "category": "단체구기", "olympic_status": True},
            {"code": "BASEBALL", "name": "야구", "category": "단체구기", "olympic_status": True},
            {"code": "BASKETBALL", "name": "농구", "category": "단체구기", "olympic_status": True},
            {"code": "VOLLEYBALL", "name": "배구", "category": "단체구기", "olympic_status": True},
            {"code": "TAEKWONDO", "name": "태권도", "category": "격투", "olympic_status": True},
            {"code": "JUDO", "name": "유도", "category": "격투", "olympic_status": True},
            {"code": "SWIMMING", "name": "수영", "category": "기초체육", "olympic_status": True},
            {"code": "ATHLETICS", "name": "육상", "category": "기초체육", "olympic_status": True},
            {"code": "ARCHERY", "name": "양궁", "category": "표적", "olympic_status": True},
            {"code": "SHOOTING", "name": "사격", "category": "표적", "olympic_status": True},
            {"code": "GOLF", "name": "골프", "category": "라켓", "olympic_status": True},
            {"code": "TENNIS", "name": "테니스", "category": "라켓", "olympic_status": True},
            {"code": "BADMINTON", "name": "배드민턴", "category": "라켓", "olympic_status": True},
            {"code": "TABLE_TENNIS", "name": "탁구", "category": "라켓", "olympic_status": True},
            {"code": "ESPORTS", "name": "e스포츠", "category": "기타", "olympic_status": False},
        ]
        
        for sport_data in sports:
            stmt = insert(Sport).values(**sport_data)
            stmt = stmt.on_conflict_do_nothing(index_elements=['code'])
            await self.session.execute(stmt)
            self.stats["sports_created"] += 1
        
        # 프로젝트 데이터
        projects = [
            {"name": "엘리트선수 육성 지원", "code": "ELITE_01", "type": "육성"},
            {"name": "꿈나무 선수 발굴", "code": "YOUTH_01", "type": "육성"},
            {"name": "생활체육 활성화", "code": "LIFE_01", "type": "지원"},
            {"name": "체육시설 확충", "code": "FACILITY_01", "type": "시설"},
            {"name": "공공체육시설 개보수", "code": "FACILITY_02", "type": "시설"},
            {"name": "스포츠과학 연구개발", "code": "RND_01", "type": "연구"},
            {"name": "국제대회 개최 지원", "code": "EVENT_01", "type": "대회운영"},
            {"name": "전국체전 운영", "code": "EVENT_02", "type": "대회운영"},
            {"name": "장애인체육 지원", "code": "PARA_01", "type": "지원"},
            {"name": "여성체육 활성화", "code": "WOMEN_01", "type": "지원"},
        ]
        
        for project_data in projects:
            stmt = insert(Project).values(**project_data)
            stmt = stmt.on_conflict_do_nothing(index_elements=['name'])
            await self.session.execute(stmt)
            self.stats["projects_created"] += 1
        
        await self.session.commit()
        logger.info("디멘션 데이터 로드 완료")
    
    async def _load_budget_data(self, year: int):
        """예산 데이터 수집 및 적재"""
        logger.info(f"{year}년 예산 데이터 로드 시작...")
        
        # 샘플 예산 데이터 (실제로는 API에서 가져옴)
        budget_data = await self._fetch_budget_data_from_api(year)
        
        # 예산 데이터가 없으면 샘플 생성
        if not budget_data:
            budget_data = await self._generate_sample_budget_data(year)
        
        for budget in budget_data:
            # 기관 ID 조회 또는 생성
            inst_id = await self._get_or_create_institution(budget["institution_name"])
            
            # 프로젝트 ID 조회 또는 생성
            proj_id = await self._get_or_create_project(budget["project_name"])
            
            # 예산 집행 데이터 삽입
            execution = BudgetExecution(
                year=year,
                quarter=budget.get("quarter"),
                institution_id=inst_id,
                project_id=proj_id,
                allocated=Decimal(str(budget["allocated"])),
                executed=Decimal(str(budget["executed"])),
                execution_rate=budget["executed"] / budget["allocated"] * 100 if budget["allocated"] > 0 else 0,
                run_id=self.run_id
            )
            self.session.add(execution)
            self.stats["budgets_loaded"] += 1
        
        await self.session.commit()
        logger.info(f"예산 데이터 로드 완료: {self.stats['budgets_loaded']}건")
    
    async def _load_performance_data(self, year: int):
        """성과 데이터 수집 및 적재"""
        logger.info(f"{year}년 성과 데이터 로드 시작...")
        
        # 샘플 성과 데이터
        perf_data = await self._generate_sample_performance_data(year)
        
        for perf in perf_data:
            # 종목 ID 조회
            sport_stmt = select(Sport).where(Sport.code == perf["sport_code"])
            sport = (await self.session.execute(sport_stmt)).scalar_one_or_none()
            if not sport:
                continue
            
            # 지표 ID 조회
            indicator_stmt = select(IndicatorMeta).where(IndicatorMeta.name == perf["indicator_name"])
            indicator = (await self.session.execute(indicator_stmt)).scalar_one_or_none()
            if not indicator:
                # 지표가 없으면 생성
                indicator = IndicatorMeta(
                    name=perf["indicator_name"],
                    value_type="float",
                    aggregation_rule="avg",
                    scaling="none",
                    unit=perf.get("unit", "점")
                )
                self.session.add(indicator)
                await self.session.flush()
            
            # 성과 메트릭 삽입
            metric = PerformanceMetric(
                sport_id=sport.id,
                indicator_id=indicator.id,
                measured_on=date(year, perf.get("month", 12), 1),
                value=perf["value"],
                normalized_value=perf.get("normalized_value"),
                run_id=self.run_id
            )
            self.session.add(metric)
            self.stats["metrics_loaded"] += 1
        
        await self.session.commit()
        logger.info(f"성과 데이터 로드 완료: {self.stats['metrics_loaded']}건")
    
    async def _update_mappings(self):
        """매핑 테이블 업데이트"""
        logger.info("매핑 테이블 업데이트 시작...")
        
        # 기관-지역 매핑
        mappings = [
            ("대한체육회", "11000"),  # 서울
            ("국민체육진흥공단", "11000"),  # 서울
            ("한국스포츠정책과학원", "11000"),  # 서울
            ("서울특별시체육회", "11000"),  # 서울
            ("경기도체육회", "41000"),  # 경기
            ("부산광역시체육회", "26000"),  # 부산
        ]
        
        for inst_name, region_code in mappings:
            inst_stmt = select(Institution).where(Institution.name == inst_name)
            inst = (await self.session.execute(inst_stmt)).scalar_one_or_none()
            
            if inst:
                # 현재 유효한 매핑이 있는지 확인
                existing = await self.session.execute(
                    select(InstitutionRegion).where(
                        and_(
                            InstitutionRegion.institution_id == inst.id,
                            InstitutionRegion.region_code == region_code,
                            InstitutionRegion.valid_to.is_(None)
                        )
                    )
                )
                
                if not existing.scalar_one_or_none():
                    mapping = InstitutionRegion(
                        institution_id=inst.id,
                        region_code=region_code,
                        confidence=1.0,
                        valid_from=date.today(),
                        source="manual"
                    )
                    self.session.add(mapping)
        
        # 프로젝트-종목 매핑
        project_sports = [
            ("엘리트선수 육성 지원", ["SOCCER", "BASEBALL", "BASKETBALL", "SWIMMING", "ATHLETICS"]),
            ("꿈나무 선수 발굴", ["SOCCER", "BASEBALL", "TAEKWONDO", "JUDO", "ARCHERY"]),
            ("생활체육 활성화", ["SOCCER", "BASKETBALL", "BADMINTON", "TENNIS", "GOLF"]),
            ("장애인체육 지원", ["SWIMMING", "ATHLETICS", "TABLE_TENNIS", "SHOOTING"]),
        ]
        
        for proj_name, sport_codes in project_sports:
            proj_stmt = select(Project).where(Project.name == proj_name)
            proj = (await self.session.execute(proj_stmt)).scalar_one_or_none()
            
            if proj:
                for sport_code in sport_codes:
                    sport_stmt = select(Sport).where(Sport.code == sport_code)
                    sport = (await self.session.execute(sport_stmt)).scalar_one_or_none()
                    
                    if sport:
                        # 매핑이 없으면 추가
                        existing = await self.session.execute(
                            select(ProjectSport).where(
                                and_(
                                    ProjectSport.project_id == proj.id,
                                    ProjectSport.sport_id == sport.id
                                )
                            )
                        )
                        
                        if not existing.scalar_one_or_none():
                            mapping = ProjectSport(
                                project_id=proj.id,
                                sport_id=sport.id,
                                priority=1
                            )
                            self.session.add(mapping)
        
        await self.session.commit()
        logger.info("매핑 테이블 업데이트 완료")
    
    async def _build_aggregations(self, year: int):
        """집계 데이터 생성"""
        logger.info(f"{year}년 집계 데이터 생성 시작...")
        
        # 종목별 효율성 집계
        await self._aggregate_efficiency_by_sport(year)
        
        # 지역별 집계
        await self._aggregate_by_region(year)
        
        # ROI 집계
        await self._aggregate_roi(year)
        
        await self.session.commit()
        logger.info("집계 데이터 생성 완료")
    
    async def _aggregate_efficiency_by_sport(self, year: int):
        """종목별 효율성 집계"""
        query = """
            SELECT 
                ps.sport_id,
                SUM(be.allocated) as total_allocated,
                SUM(be.executed) as total_executed,
                AVG(be.execution_rate) as avg_execution_rate
            FROM budget_execution be
            JOIN project_sport ps ON ps.project_id = be.project_id
            WHERE be.year = :year AND be.run_id = :run_id
            GROUP BY ps.sport_id
        """
        
        result = await self.session.execute(
            query, {"year": year, "run_id": self.run_id}
        )
        
        for row in result:
            sport_id, allocated, executed, exec_rate = row
            
            # 효율성 계산
            efficiency = self._calculate_efficiency(executed, allocated)
            grade = self._get_efficiency_grade(efficiency)
            
            # 집계 캐시에 저장
            cache_entry = AggregationCache(
                run_id=self.run_id,
                aggregation_type="efficiency",
                dimension_key=f"year:{year}:sport:{sport_id}",
                year=year,
                sport_id=sport_id,
                budget_total=allocated,
                budget_executed=executed,
                efficiency=efficiency,
                grade=grade
            )
            self.session.add(cache_entry)
    
    async def _refresh_materialized_views(self):
        """Materialized View 리프레시"""
        logger.info("Materialized View 리프레시 시작...")
        
        views = [
            "mv_efficiency_by_year_sport",
            "mv_roi_by_year_sport", 
            "mv_region_summary"
        ]
        
        for view in views:
            try:
                await self.session.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view}")
                logger.info(f"✅ {view} 리프레시 완료")
            except Exception as e:
                logger.warning(f"⚠️ {view} 리프레시 실패: {str(e)}")
                # CONCURRENTLY 옵션 없이 재시도
                await self.session.execute(f"REFRESH MATERIALIZED VIEW {view}")
        
        await self.session.commit()
        logger.info("Materialized View 리프레시 완료")
    
    async def _complete_etl_run(self):
        """ETL 실행 완료 마킹"""
        stmt = select(EtlRun).where(EtlRun.run_id == self.run_id)
        etl_run = (await self.session.execute(stmt)).scalar_one()
        
        etl_run.finished_at = datetime.utcnow()
        etl_run.status = "success"
        etl_run.row_count = (
            self.stats["budgets_loaded"] + 
            self.stats["metrics_loaded"]
        )
        
        await self.session.commit()
    
    async def _fail_etl_run(self, error_message: str):
        """ETL 실행 실패 마킹"""
        if self.run_id:
            stmt = select(EtlRun).where(EtlRun.run_id == self.run_id)
            etl_run = (await self.session.execute(stmt)).scalar_one_or_none()
            
            if etl_run:
                etl_run.finished_at = datetime.utcnow()
                etl_run.status = "failed"
                etl_run.error_message = error_message
                await self.session.commit()
    
    # === Helper Methods ===
    
    async def _get_or_create_institution(self, name: str) -> int:
        """기관 조회 또는 생성"""
        normalized_name = self.normalizer.normalize_institution_name(name)
        
        stmt = select(Institution).where(Institution.name == normalized_name)
        inst = (await self.session.execute(stmt)).scalar_one_or_none()
        
        if not inst:
            inst = Institution(
                name=normalized_name,
                type=self.normalizer.determine_institution_type(normalized_name)
            )
            self.session.add(inst)
            await self.session.flush()
        
        return inst.id
    
    async def _get_or_create_project(self, name: str) -> int:
        """프로젝트 조회 또는 생성"""
        normalized_name = self.normalizer.normalize_project_name(name)
        
        stmt = select(Project).where(Project.name == normalized_name)
        proj = (await self.session.execute(stmt)).scalar_one_or_none()
        
        if not proj:
            proj = Project(
                name=normalized_name,
                type=self.normalizer.determine_project_type(normalized_name)
            )
            self.session.add(proj)
            await self.session.flush()
        
        return proj.id
    
    async def _fetch_budget_data_from_api(self, year: int) -> List[Dict]:
        """API에서 예산 데이터 수집"""
        # TODO: 실제 API 호출 구현
        return []
    
    async def _generate_sample_budget_data(self, year: int) -> List[Dict]:
        """샘플 예산 데이터 생성"""
        import random
        
        institutions = ["대한체육회", "국민체육진흥공단", "서울특별시체육회", "경기도체육회"]
        projects = ["엘리트선수 육성 지원", "생활체육 활성화", "체육시설 확충", "장애인체육 지원"]
        
        data = []
        for inst in institutions:
            for proj in projects:
                allocated = random.randint(10, 100) * 100_000_000  # 10억 ~ 100억
                executed = allocated * random.uniform(0.7, 0.95)
                
                data.append({
                    "institution_name": inst,
                    "project_name": proj,
                    "allocated": allocated,
                    "executed": executed,
                    "quarter": None
                })
        
        return data
    
    async def _generate_sample_performance_data(self, year: int) -> List[Dict]:
        """샘플 성과 데이터 생성"""
        import random
        
        sports = ["SOCCER", "BASEBALL", "BASKETBALL", "SWIMMING", "TAEKWONDO"]
        indicators = ["참여인원", "만족도", "메달획득", "시설이용률"]
        
        data = []
        for sport in sports:
            for indicator in indicators:
                value = random.uniform(50, 100) if "만족도" in indicator else random.randint(100, 10000)
                
                data.append({
                    "sport_code": sport,
                    "indicator_name": indicator,
                    "value": value,
                    "normalized_value": value / 100 if "만족도" in indicator else None,
                    "month": 12,
                    "unit": "점" if "만족도" in indicator else "명"
                })
        
        return data
    
    async def _aggregate_by_region(self, year: int):
        """지역별 집계"""
        # 지역별 예산 집계 쿼리
        pass
    
    async def _aggregate_roi(self, year: int):
        """ROI 집계"""
        # ROI 계산 및 저장
        pass
    
    def _calculate_efficiency(self, executed: float, allocated: float) -> float:
        """효율성 계산"""
        if allocated == 0:
            return 0
        return (executed / allocated) * 100
    
    def _get_efficiency_grade(self, efficiency: float) -> str:
        """효율성 등급 결정"""
        if efficiency >= 95:
            return "S"
        elif efficiency >= 90:
            return "A"
        elif efficiency >= 80:
            return "B"
        elif efficiency >= 70:
            return "C"
        else:
            return "D"
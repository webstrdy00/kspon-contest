"""
Budget and Performance Analysis Service
예산 및 성과 분석 서비스 레이어
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal
from collections import defaultdict

from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.models import (
    Institution, Sport, Project, InstitutionRegion, ProjectSport,
    IndicatorMeta, PerformanceMetric, BudgetExecution, EtlRun, AggregationCache,
    Region
)
from app.schemas.budget_performance import (
    EfficiencyAnalysis, ROIAnalysis, TrendData, RegionComparison,
    BudgetPerformanceOverview, BudgetPerformanceFilter
)

logger = logging.getLogger(__name__)


class BudgetAnalysisService:
    """예산 성과 분석 서비스"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._latest_run_id: Optional[int] = None
    
    async def get_latest_run_id(self) -> int:
        """최신 ETL 실행 ID 조회"""
        if self._latest_run_id:
            return self._latest_run_id
        
        stmt = select(EtlRun.run_id).where(
            EtlRun.status == "success"
        ).order_by(desc(EtlRun.finished_at)).limit(1)
        
        result = await self.session.execute(stmt)
        run_id = result.scalar_one_or_none()
        
        if not run_id:
            raise ValueError("성공한 ETL 실행이 없습니다")
        
        self._latest_run_id = run_id
        return run_id
    
    async def get_overview(self, filters: BudgetPerformanceFilter) -> BudgetPerformanceOverview:
        """예산-성과 개요 조회"""
        run_id = await self.get_latest_run_id()
        
        # 요약 통계
        summary = await self._get_summary_stats(run_id, filters)
        
        # 하이라이트
        highlights = await self._get_highlights(run_id, filters)
        
        # 종목별 효율성
        efficiency_by_sport = await self.get_efficiency_by_sport(
            year=filters.year or datetime.now().year,
            limit=10
        )
        
        # ROI 상위 수행자
        roi_top = await self.get_roi_analysis(
            year=filters.year or datetime.now().year,
            limit=10
        )
        
        # 지역별 비교
        regional = await self.get_regional_comparison(
            year=filters.year or datetime.now().year
        )
        
        # 트렌드 데이터
        trend = await self.get_trend_data(
            start_year=2020,
            end_year=filters.year or datetime.now().year,
            sport_id=filters.sport_id
        )
        
        return BudgetPerformanceOverview(
            summary=summary,
            highlights=highlights,
            efficiency_by_sport=efficiency_by_sport,
            roi_top_performers=roi_top,
            regional_comparison=regional,
            trend_data=trend
        )
    
    async def get_efficiency_by_sport(
        self, year: int, limit: int = 10
    ) -> List[EfficiencyAnalysis]:
        """종목별 효율성 분석"""
        run_id = await self.get_latest_run_id()
        
        # 집계 캐시에서 조회
        stmt = select(AggregationCache).where(
            and_(
                AggregationCache.run_id == run_id,
                AggregationCache.aggregation_type == "efficiency",
                AggregationCache.year == year,
                AggregationCache.sport_id.isnot(None)
            )
        ).options(
            joinedload(AggregationCache.sport)
        ).order_by(
            desc(AggregationCache.efficiency)
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        cache_entries = result.scalars().all()
        
        analyses = []
        rank = 1
        
        for entry in cache_entries:
            analysis = EfficiencyAnalysis(
                year=year,
                sport=entry.sport,
                budget_total=entry.budget_total or Decimal(0),
                budget_executed=entry.budget_executed or Decimal(0),
                execution_rate=float(entry.budget_executed / entry.budget_total * 100) 
                    if entry.budget_total and entry.budget_total > 0 else 0,
                performance_score=entry.performance_score or 0,
                efficiency=entry.efficiency or 0,
                grade=entry.grade or "N/A",
                rank=rank
            )
            analyses.append(analysis)
            rank += 1
        
        # 캐시에 없으면 직접 계산
        if not analyses:
            analyses = await self._calculate_efficiency_by_sport(year, limit)
        
        return analyses
    
    async def get_roi_analysis(
        self, year: int, limit: int = 10
    ) -> List[ROIAnalysis]:
        """ROI 분석"""
        run_id = await self.get_latest_run_id()
        
        # 집계 캐시에서 조회
        stmt = select(AggregationCache).where(
            and_(
                AggregationCache.run_id == run_id,
                AggregationCache.aggregation_type == "roi",
                AggregationCache.year == year
            )
        ).options(
            joinedload(AggregationCache.sport)
        ).order_by(
            desc(AggregationCache.roi)
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        cache_entries = result.scalars().all()
        
        analyses = []
        rank = 1
        
        for entry in cache_entries:
            # 기관 조회 (필요한 경우)
            institution = None
            if entry.dimension_key:
                dimensions = self._parse_dimension_key(entry.dimension_key)
                inst_id = dimensions.get("inst")
                if inst_id:
                    inst_stmt = select(Institution).where(Institution.id == int(inst_id))
                    inst_result = await self.session.execute(inst_stmt)
                    institution = inst_result.scalar_one_or_none()
            
            analysis = ROIAnalysis(
                year=year,
                sport=entry.sport,
                institution=institution,
                investment=entry.budget_executed or Decimal(0),
                return_value=entry.performance_score or 0,
                roi=entry.roi or 0,
                roi_rank=rank,
                category=entry.sport.category if entry.sport else "기타"
            )
            analyses.append(analysis)
            rank += 1
        
        # 캐시에 없으면 직접 계산
        if not analyses:
            analyses = await self._calculate_roi_analysis(year, limit)
        
        return analyses
    
    async def get_regional_comparison(self, year: int) -> List[RegionComparison]:
        """지역별 비교 분석"""
        run_id = await self.get_latest_run_id()
        
        # Materialized View에서 조회
        query = """
            SELECT 
                r.code as region_code,
                r.name as region_name,
                COALESCE(mv.total_allocated, 0) as total_allocated,
                COALESCE(mv.total_executed, 0) as total_executed,
                COALESCE(mv.avg_execution_rate, 0) as avg_execution_rate,
                r.population
            FROM region r
            LEFT JOIN mv_region_summary mv ON 
                mv.region_code = r.code AND 
                mv.run_id = :run_id AND 
                mv.year = :year
            WHERE r.level = 'province'
            ORDER BY mv.total_allocated DESC NULLS LAST
        """
        
        result = await self.session.execute(
            query, {"run_id": run_id, "year": year}
        )
        rows = result.fetchall()
        
        comparisons = []
        rank = 1
        
        for row in rows:
            region_code, region_name, allocated, executed, exec_rate, population = row
            
            # 효율성 계산
            efficiency = self._calculate_efficiency(executed, allocated)
            
            # 인구당 예산
            pop_per_budget = float(allocated / population) if population and population > 0 else 0
            
            comparison = RegionComparison(
                region_code=region_code,
                region_name=region_name,
                budget_total=Decimal(str(allocated)),
                performance_avg=exec_rate,
                efficiency=efficiency,
                rank=rank,
                population_per_budget=pop_per_budget
            )
            comparisons.append(comparison)
            rank += 1
        
        return comparisons
    
    async def get_trend_data(
        self, 
        start_year: int, 
        end_year: int,
        sport_id: Optional[int] = None,
        region_code: Optional[str] = None
    ) -> List[TrendData]:
        """트렌드 데이터 조회"""
        run_id = await self.get_latest_run_id()
        
        # 연도별 집계 데이터 조회
        stmt = select(AggregationCache).where(
            and_(
                AggregationCache.run_id == run_id,
                AggregationCache.aggregation_type == "trend",
                AggregationCache.year >= start_year,
                AggregationCache.year <= end_year
            )
        )
        
        if sport_id:
            stmt = stmt.where(AggregationCache.sport_id == sport_id)
        
        if region_code:
            stmt = stmt.where(AggregationCache.region_code == region_code)
        
        stmt = stmt.order_by(asc(AggregationCache.year))
        
        result = await self.session.execute(stmt)
        cache_entries = result.scalars().all()
        
        trend_data = []
        
        if cache_entries:
            for entry in cache_entries:
                trend = TrendData(
                    date=date(entry.year, 12, 31),
                    budget=entry.budget_total or Decimal(0),
                    performance=entry.performance_score or 0,
                    efficiency=entry.efficiency or 0,
                    roi=entry.roi
                )
                trend_data.append(trend)
        else:
            # 캐시에 없으면 직접 계산
            trend_data = await self._calculate_trend_data(
                start_year, end_year, sport_id, region_code
            )
        
        return trend_data
    
    # === Private Helper Methods ===
    
    async def _get_summary_stats(
        self, run_id: int, filters: BudgetPerformanceFilter
    ) -> Dict[str, Any]:
        """요약 통계 조회"""
        year = filters.year or datetime.now().year
        
        # 전체 예산 및 집행 통계
        budget_stmt = select(
            func.sum(BudgetExecution.allocated).label("total_allocated"),
            func.sum(BudgetExecution.executed).label("total_executed"),
            func.avg(BudgetExecution.execution_rate).label("avg_execution_rate"),
            func.count(func.distinct(BudgetExecution.institution_id)).label("institution_count"),
            func.count(func.distinct(BudgetExecution.project_id)).label("project_count")
        ).where(
            and_(
                BudgetExecution.run_id == run_id,
                BudgetExecution.year == year
            )
        )
        
        if filters.institution_id:
            budget_stmt = budget_stmt.where(
                BudgetExecution.institution_id == filters.institution_id
            )
        
        budget_result = await self.session.execute(budget_stmt)
        budget_stats = budget_result.one()
        
        # 성과 통계
        perf_stmt = select(
            func.count(func.distinct(PerformanceMetric.sport_id)).label("sport_count"),
            func.count(func.distinct(PerformanceMetric.indicator_id)).label("indicator_count"),
            func.avg(PerformanceMetric.normalized_value).label("avg_performance")
        ).where(
            and_(
                PerformanceMetric.run_id == run_id,
                func.extract('year', PerformanceMetric.measured_on) == year
            )
        )
        
        perf_result = await self.session.execute(perf_stmt)
        perf_stats = perf_result.one()
        
        # 효율성 계산
        efficiency = self._calculate_efficiency(
            float(budget_stats.total_executed or 0),
            float(budget_stats.total_allocated or 0)
        )
        
        return {
            "total_budget": float(budget_stats.total_allocated or 0),
            "total_executed": float(budget_stats.total_executed or 0),
            "execution_rate": float(budget_stats.avg_execution_rate or 0),
            "efficiency": efficiency,
            "efficiency_grade": self._get_efficiency_grade(efficiency),
            "institution_count": budget_stats.institution_count or 0,
            "project_count": budget_stats.project_count or 0,
            "sport_count": perf_stats.sport_count or 0,
            "indicator_count": perf_stats.indicator_count or 0,
            "avg_performance_score": float(perf_stats.avg_performance or 0) * 100
        }
    
    async def _get_highlights(
        self, run_id: int, filters: BudgetPerformanceFilter
    ) -> List[Dict[str, Any]]:
        """하이라이트 조회"""
        year = filters.year or datetime.now().year
        highlights = []
        
        # 최고 효율성 종목
        top_eff_stmt = select(AggregationCache).where(
            and_(
                AggregationCache.run_id == run_id,
                AggregationCache.aggregation_type == "efficiency",
                AggregationCache.year == year,
                AggregationCache.sport_id.isnot(None)
            )
        ).options(
            joinedload(AggregationCache.sport)
        ).order_by(
            desc(AggregationCache.efficiency)
        ).limit(1)
        
        top_eff = (await self.session.execute(top_eff_stmt)).scalar_one_or_none()
        if top_eff and top_eff.sport:
            highlights.append({
                "type": "top_efficiency",
                "title": "최고 효율성 종목",
                "value": top_eff.sport.name,
                "metric": f"{top_eff.efficiency:.1f}%",
                "grade": top_eff.grade
            })
        
        # 최대 예산 집행 기관
        top_budget_stmt = select(
            Institution.name,
            func.sum(BudgetExecution.executed).label("total")
        ).join(
            BudgetExecution, BudgetExecution.institution_id == Institution.id
        ).where(
            and_(
                BudgetExecution.run_id == run_id,
                BudgetExecution.year == year
            )
        ).group_by(
            Institution.id, Institution.name
        ).order_by(
            desc("total")
        ).limit(1)
        
        top_budget = (await self.session.execute(top_budget_stmt)).first()
        if top_budget:
            highlights.append({
                "type": "top_budget",
                "title": "최대 예산 집행 기관",
                "value": top_budget[0],
                "metric": f"{top_budget[1] / 100_000_000:.1f}억원"
            })
        
        # 가장 개선된 종목 (전년 대비)
        if year > 2020:
            improvement = await self._get_most_improved_sport(run_id, year)
            if improvement:
                highlights.append(improvement)
        
        return highlights
    
    async def _calculate_efficiency_by_sport(
        self, year: int, limit: int
    ) -> List[EfficiencyAnalysis]:
        """종목별 효율성 직접 계산"""
        run_id = await self.get_latest_run_id()
        
        query = """
            SELECT 
                s.id as sport_id,
                s.name as sport_name,
                s.category,
                SUM(be.allocated) as total_allocated,
                SUM(be.executed) as total_executed,
                AVG(pm.normalized_value) as avg_performance
            FROM sport s
            JOIN project_sport ps ON ps.sport_id = s.id
            JOIN budget_execution be ON be.project_id = ps.project_id
            LEFT JOIN performance_metric pm ON 
                pm.sport_id = s.id AND 
                EXTRACT(YEAR FROM pm.measured_on) = :year AND
                pm.run_id = :run_id
            WHERE be.year = :year AND be.run_id = :run_id
            GROUP BY s.id, s.name, s.category
            ORDER BY SUM(be.executed) / NULLIF(SUM(be.allocated), 0) DESC
            LIMIT :limit
        """
        
        result = await self.session.execute(
            query, {"year": year, "run_id": run_id, "limit": limit}
        )
        rows = result.fetchall()
        
        analyses = []
        rank = 1
        
        for row in rows:
            sport_id, sport_name, category, allocated, executed, avg_perf = row
            
            # Sport 객체 생성
            sport = Sport(id=sport_id, name=sport_name, category=category)
            
            # 효율성 계산
            efficiency = self._calculate_efficiency(executed, allocated)
            grade = self._get_efficiency_grade(efficiency)
            
            analysis = EfficiencyAnalysis(
                year=year,
                sport=sport,
                budget_total=Decimal(str(allocated)),
                budget_executed=Decimal(str(executed)),
                execution_rate=float(executed / allocated * 100) if allocated > 0 else 0,
                performance_score=float(avg_perf or 0) * 100,
                efficiency=efficiency,
                grade=grade,
                rank=rank
            )
            analyses.append(analysis)
            rank += 1
        
        return analyses
    
    async def _calculate_roi_analysis(
        self, year: int, limit: int
    ) -> List[ROIAnalysis]:
        """ROI 직접 계산"""
        # ROI 계산 로직 구현
        return []
    
    async def _calculate_trend_data(
        self,
        start_year: int,
        end_year: int,
        sport_id: Optional[int],
        region_code: Optional[str]
    ) -> List[TrendData]:
        """트렌드 데이터 직접 계산"""
        run_id = await self.get_latest_run_id()
        trend_data = []
        
        for year in range(start_year, end_year + 1):
            # 연도별 데이터 집계
            budget_stmt = select(
                func.sum(BudgetExecution.allocated).label("total_allocated"),
                func.sum(BudgetExecution.executed).label("total_executed")
            ).where(
                and_(
                    BudgetExecution.run_id == run_id,
                    BudgetExecution.year == year
                )
            )
            
            if sport_id:
                budget_stmt = budget_stmt.join(
                    ProjectSport, ProjectSport.project_id == BudgetExecution.project_id
                ).where(ProjectSport.sport_id == sport_id)
            
            budget_result = await self.session.execute(budget_stmt)
            budget = budget_result.one()
            
            # 성과 데이터 집계
            perf_stmt = select(
                func.avg(PerformanceMetric.normalized_value).label("avg_performance")
            ).where(
                and_(
                    PerformanceMetric.run_id == run_id,
                    func.extract('year', PerformanceMetric.measured_on) == year
                )
            )
            
            if sport_id:
                perf_stmt = perf_stmt.where(PerformanceMetric.sport_id == sport_id)
            
            perf_result = await self.session.execute(perf_stmt)
            perf = perf_result.scalar()
            
            # 효율성 계산
            efficiency = self._calculate_efficiency(
                float(budget.total_executed or 0),
                float(budget.total_allocated or 0)
            )
            
            # ROI 계산
            roi = self._calculate_roi(
                float(budget.total_executed or 0),
                float(perf or 0) * 100
            )
            
            trend = TrendData(
                date=date(year, 12, 31),
                budget=Decimal(str(budget.total_allocated or 0)),
                performance=float(perf or 0) * 100,
                efficiency=efficiency,
                roi=roi
            )
            trend_data.append(trend)
        
        return trend_data
    
    async def _get_most_improved_sport(
        self, run_id: int, year: int
    ) -> Optional[Dict[str, Any]]:
        """가장 개선된 종목 조회"""
        # 전년도와 비교하여 가장 개선된 종목 찾기
        return None
    
    def _parse_dimension_key(self, dimension_key: Optional[str]) -> Dict[str, str]:
        """dimension_key 문자열에서 key-value 쌍 추출"""
        if not dimension_key:
            return {}
        parts = dimension_key.split(":")
        return {parts[i]: parts[i + 1] for i in range(0, len(parts) - 1, 2)}
    
    def _calculate_efficiency(self, executed: float, allocated: float) -> float:
        """효율성 계산"""
        if allocated == 0:
            return 0
        return (executed / allocated) * 100
    
    def _calculate_roi(self, investment: float, return_value: float) -> float:
        """ROI 계산"""
        if investment == 0:
            return 0
        return ((return_value - investment) / investment) * 100
    
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
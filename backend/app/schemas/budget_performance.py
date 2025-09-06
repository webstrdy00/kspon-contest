"""
Pydantic schemas for budget-performance analysis
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


# ========== Dimension Schemas ==========

class InstitutionBase(BaseModel):
    name: str
    type: Optional[str] = None
    created_at: Optional[date] = None


class InstitutionCreate(InstitutionBase):
    pass


class Institution(InstitutionBase):
    id: int
    
    class Config:
        from_attributes = True


class SportBase(BaseModel):
    code: str
    name: str
    category: Optional[str] = None
    olympic_status: bool = False


class SportCreate(SportBase):
    pass


class Sport(SportBase):
    id: int
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== Mapping Schemas ==========

class InstitutionRegionBase(BaseModel):
    institution_id: int
    region_code: str
    confidence: float = 1.0
    valid_from: date
    valid_to: Optional[date] = None
    source: Optional[str] = None


class InstitutionRegionCreate(InstitutionRegionBase):
    pass


class InstitutionRegion(InstitutionRegionBase):
    id: int
    
    class Config:
        from_attributes = True


class ProjectSportBase(BaseModel):
    project_id: int
    sport_id: int
    priority: int = 1


class ProjectSportCreate(ProjectSportBase):
    pass


class ProjectSport(ProjectSportBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== Metrics & Budget Schemas ==========

class IndicatorMetaBase(BaseModel):
    name: str
    description: Optional[str] = None
    value_type: str  # int/float/percentage
    aggregation_rule: str  # sum/avg/weighted/max/min
    scaling: str = "none"  # none/minmax/zscore/log
    direction_positive: bool = True
    unit: Optional[str] = None
    category: Optional[str] = None


class IndicatorMetaCreate(IndicatorMetaBase):
    pass


class IndicatorMeta(IndicatorMetaBase):
    id: int
    
    class Config:
        from_attributes = True


class PerformanceMetricBase(BaseModel):
    sport_id: int
    indicator_id: int
    institution_id: Optional[int] = None
    measured_on: date
    value: float
    normalized_value: Optional[float] = None
    run_id: int


class PerformanceMetricCreate(PerformanceMetricBase):
    pass


class PerformanceMetric(PerformanceMetricBase):
    id: int
    
    class Config:
        from_attributes = True


class BudgetExecutionBase(BaseModel):
    year: int
    quarter: Optional[int] = None
    institution_id: int
    project_id: int
    allocated: Decimal
    executed: Decimal
    execution_rate: Optional[float] = None
    run_id: int
    
    @field_validator('executed')
    def validate_executed(cls, v, values):
        if 'allocated' in values and v > values['allocated']:
            raise ValueError('Executed amount cannot exceed allocated amount')
        return v
    
    @field_validator('execution_rate')
    def validate_execution_rate(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Execution rate must be between 0 and 100')
        return v


class BudgetExecutionCreate(BudgetExecutionBase):
    pass


class BudgetExecution(BudgetExecutionBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== ETL & Aggregation Schemas ==========

class EtlRunBase(BaseModel):
    source: str
    schema_version: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str = "running"
    row_count: int = 0
    error_message: Optional[str] = None
    task_id: Optional[str] = None
    retry_count: int = 0
    metadata: Optional[str] = None


class EtlRunCreate(BaseModel):
    source: str
    schema_version: Optional[str] = None


class EtlRun(EtlRunBase):
    run_id: int
    
    class Config:
        from_attributes = True


class AggregationCacheBase(BaseModel):
    run_id: int
    aggregation_type: str
    dimension_key: str
    year: Optional[int] = None
    sport_id: Optional[int] = None
    region_code: Optional[str] = None
    budget_total: Optional[Decimal] = None
    budget_executed: Optional[Decimal] = None
    performance_score: Optional[float] = None
    efficiency: Optional[float] = None
    roi: Optional[float] = None
    rank: Optional[int] = None
    grade: Optional[str] = None


class AggregationCacheCreate(AggregationCacheBase):
    pass


class AggregationCache(AggregationCacheBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Analysis Response Schemas ==========

class EfficiencyAnalysis(BaseModel):
    year: int
    sport: Optional[Sport] = None
    region_code: Optional[str] = None
    budget_total: Decimal
    budget_executed: Decimal
    execution_rate: float
    performance_score: float
    efficiency: float
    grade: str
    rank: Optional[int] = None


class ROIAnalysis(BaseModel):
    year: int
    sport: Optional[Sport] = None
    institution: Optional[Institution] = None
    investment: Decimal
    return_value: float
    roi: float
    roi_rank: int
    category: str


class TrendData(BaseModel):
    date: date
    budget: Decimal
    performance: float
    efficiency: float
    roi: Optional[float] = None


class RegionComparison(BaseModel):
    region_code: str
    region_name: str
    budget_total: Decimal
    performance_avg: float
    efficiency: float
    rank: int
    population_per_budget: Optional[float] = None


class BudgetPerformanceOverview(BaseModel):
    summary: Dict[str, Any]
    highlights: List[Dict[str, Any]]
    efficiency_by_sport: List[EfficiencyAnalysis]
    roi_top_performers: List[ROIAnalysis]
    regional_comparison: List[RegionComparison]
    trend_data: List[TrendData]


class BudgetPerformanceFilter(BaseModel):
    year: Optional[int] = Field(None, ge=2020, le=2030)
    region_code: Optional[str] = None
    sport_id: Optional[int] = None
    institution_id: Optional[int] = None
    group_by: Optional[str] = Field(None, pattern="^(region|sport|institution|project)$")
    granularity: Optional[str] = Field(None, pattern="^(year|quarter|month)$")
    
    class Config:
        schema_extra = {
            "example": {
                "year": 2024,
                "region_code": "11000",
                "sport_id": 1,
                "group_by": "sport",
                "granularity": "year"
            }
        }


class ExportRequest(BaseModel):
    filters: BudgetPerformanceFilter
    format: str = Field("xlsx", pattern="^(csv|xlsx|json)$")
    include_charts: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "filters": {
                    "year": 2024,
                    "group_by": "region"
                },
                "format": "xlsx",
                "include_charts": True
            }
        }
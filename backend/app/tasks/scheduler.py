"""
데이터 수집 스케줄러
정기적으로 공공데이터 API를 호출하여 최신 데이터 유지
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.services.facilities_api_client import FacilitiesAPIClient
from app.services.fund_api_client import FundAPIClient
from app.services.performance_api_client import PerformanceAPIClient
from app.etl.csv_processor import CSVDataProcessor
from app.db import get_db
from app.core.config import settings

logger = logging.getLogger(__name__)


class DataCollectionScheduler:
    """데이터 수집 스케줄러"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.facilities_client = FacilitiesAPIClient()
        self.fund_client = FundAPIClient()
        self.performance_client = PerformanceAPIClient()
        self.csv_processor = CSVDataProcessor()
        self.is_running = False
        
    def start(self):
        """스케줄러 시작"""
        if self.is_running:
            logger.warning("스케줄러가 이미 실행 중입니다.")
            return
        
        try:
            # 작업 스케줄 등록
            self._register_jobs()
            
            # 스케줄러 시작
            self.scheduler.start()
            self.is_running = True
            
            logger.info("데이터 수집 스케줄러 시작됨")
            
        except Exception as e:
            logger.error(f"스케줄러 시작 실패: {str(e)}")
            raise
    
    def stop(self):
        """스케줄러 중지"""
        if not self.is_running:
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("데이터 수집 스케줄러 중지됨")
    
    def _register_jobs(self):
        """스케줄 작업 등록"""
        
        # 1. 체육시설 데이터 - 매일 새벽 2시
        self.scheduler.add_job(
            self.collect_facilities_data,
            CronTrigger(hour=2, minute=0),
            id='collect_facilities',
            name='체육시설 데이터 수집',
            replace_existing=True
        )
        
        # 2. 예산 데이터 - 매주 월요일 새벽 3시
        self.scheduler.add_job(
            self.collect_fund_data,
            CronTrigger(day_of_week='mon', hour=3, minute=0),
            id='collect_fund',
            name='예산 데이터 수집',
            replace_existing=True
        )
        
        # 3. 성과금 데이터 - 매주 월요일 새벽 4시
        self.scheduler.add_job(
            self.collect_performance_data,
            CronTrigger(day_of_week='mon', hour=4, minute=0),
            id='collect_performance',
            name='성과금 데이터 수집',
            replace_existing=True
        )
        
        # 4. 데이터 분석 및 캐시 갱신 - 매일 새벽 5시
        self.scheduler.add_job(
            self.update_analysis_cache,
            CronTrigger(hour=5, minute=0),
            id='update_cache',
            name='분석 캐시 갱신',
            replace_existing=True
        )
        
        # 5. 건강 체크 - 30분마다
        self.scheduler.add_job(
            self.health_check,
            IntervalTrigger(minutes=30),
            id='health_check',
            name='건강 체크',
            replace_existing=True
        )
        
        logger.info(f"총 {len(self.scheduler.get_jobs())}개 작업 등록됨")
    
    async def collect_facilities_data(self):
        """체육시설 데이터 수집"""
        start_time = datetime.now()
        logger.info("체육시설 데이터 수집 시작")
        
        try:
            # 전체 시설 데이터 수집
            facilities = await self.facilities_client.get_all_facilities()
            
            # 데이터베이스 저장
            await self._save_facilities_to_db(facilities)
            
            # 통계 생성
            stats = await self.facilities_client.get_facility_statistics()
            
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"체육시설 데이터 수집 완료: {len(facilities)}개 ({elapsed:.2f}초)")
            
            # 수집 기록 저장
            await self._save_collection_log('facilities', len(facilities), elapsed, 'success')
            
        except Exception as e:
            logger.error(f"체육시설 데이터 수집 실패: {str(e)}")
            await self._save_collection_log('facilities', 0, 0, 'failed', str(e))
    
    async def collect_fund_data(self):
        """예산 데이터 수집"""
        start_time = datetime.now()
        logger.info("예산 데이터 수집 시작")
        
        try:
            current_year = datetime.now().year
            
            # 최근 3년 데이터 수집
            all_data = []
            for year in range(current_year - 2, current_year + 1):
                data = await self.fund_client.get_all_fund_support(year=year)
                all_data.extend(data)
            
            # 데이터베이스 저장
            await self._save_fund_data_to_db(all_data)
            
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"예산 데이터 수집 완료: {len(all_data)}개 ({elapsed:.2f}초)")
            
            await self._save_collection_log('fund', len(all_data), elapsed, 'success')
            
        except Exception as e:
            logger.error(f"예산 데이터 수집 실패: {str(e)}")
            await self._save_collection_log('fund', 0, 0, 'failed', str(e))
    
    async def collect_performance_data(self):
        """성과금 데이터 수집"""
        start_time = datetime.now()
        logger.info("성과금 데이터 수집 시작")
        
        try:
            current_year = datetime.now().year
            
            # 최근 3년 데이터 수집
            all_data = []
            for year in range(current_year - 2, current_year + 1):
                data = await self.performance_client.get_all_performance_rewards(year=year)
                all_data.extend(data)
            
            # 데이터베이스 저장
            await self._save_performance_data_to_db(all_data)
            
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"성과금 데이터 수집 완료: {len(all_data)}개 ({elapsed:.2f}초)")
            
            await self._save_collection_log('performance', len(all_data), elapsed, 'success')
            
        except Exception as e:
            logger.error(f"성과금 데이터 수집 실패: {str(e)}")
            await self._save_collection_log('performance', 0, 0, 'failed', str(e))
    
    async def update_analysis_cache(self):
        """분석 데이터 캐시 갱신"""
        logger.info("분석 캐시 갱신 시작")
        
        try:
            current_year = datetime.now().year
            
            # 1. 지역별 예산 분석
            budget_by_region = await self.fund_client.get_budget_by_region(current_year)
            
            # 2. 종목별 예산 분석
            budget_by_sport = await self.fund_client.get_budget_by_sport(current_year)
            
            # 3. ROI 분석
            roi_analysis = await self.performance_client.calculate_roi_by_sport(
                current_year, 
                budget_by_sport
            )
            
            # 4. 캐시 저장 (Redis 또는 DB)
            await self._save_to_cache('budget_by_region', budget_by_region)
            await self._save_to_cache('budget_by_sport', budget_by_sport)
            await self._save_to_cache('roi_analysis', roi_analysis)
            
            logger.info("분석 캐시 갱신 완료")
            
        except Exception as e:
            logger.error(f"분석 캐시 갱신 실패: {str(e)}")
    
    async def health_check(self):
        """시스템 건강 체크"""
        try:
            # API 연결 상태 확인
            health_status = {
                'scheduler': 'running' if self.is_running else 'stopped',
                'jobs': len(self.scheduler.get_jobs()),
                'timestamp': datetime.now().isoformat()
            }
            
            # 다음 실행 시간 확인
            next_runs = {}
            for job in self.scheduler.get_jobs():
                next_runs[job.id] = job.next_run_time.isoformat() if job.next_run_time else None
            
            health_status['next_runs'] = next_runs
            
            logger.debug(f"건강 체크: {health_status}")
            
        except Exception as e:
            logger.error(f"건강 체크 실패: {str(e)}")
    
    # 데이터베이스 저장 헬퍼 메서드
    async def _save_facilities_to_db(self, facilities: list):
        """체육시설 데이터 DB 저장"""
        # TODO: 실제 DB 저장 로직 구현
        pass
    
    async def _save_fund_data_to_db(self, fund_data: list):
        """예산 데이터 DB 저장"""
        # TODO: 실제 DB 저장 로직 구현
        pass
    
    async def _save_performance_data_to_db(self, performance_data: list):
        """성과금 데이터 DB 저장"""
        # TODO: 실제 DB 저장 로직 구현
        pass
    
    async def _save_collection_log(
        self,
        data_type: str,
        record_count: int,
        elapsed_time: float,
        status: str,
        error_message: Optional[str] = None
    ):
        """데이터 수집 로그 저장"""
        log_entry = {
            'data_type': data_type,
            'record_count': record_count,
            'elapsed_time': elapsed_time,
            'status': status,
            'error_message': error_message,
            'collected_at': datetime.now()
        }
        # TODO: DB에 로그 저장
        logger.info(f"수집 로그: {log_entry}")
    
    async def _save_to_cache(self, key: str, data: Any):
        """캐시에 데이터 저장"""
        # TODO: Redis 캐시 구현
        pass
    
    def get_job_status(self) -> Dict[str, Any]:
        """현재 작업 상태 조회"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return {
            'is_running': self.is_running,
            'jobs': jobs,
            'total_jobs': len(jobs)
        }
    
    async def trigger_job(self, job_id: str):
        """수동으로 작업 실행"""
        job = self.scheduler.get_job(job_id)
        if not job:
            raise ValueError(f"작업을 찾을 수 없습니다: {job_id}")
        
        logger.info(f"수동 실행: {job.name}")
        job.func()


# 전역 스케줄러 인스턴스
scheduler = DataCollectionScheduler()
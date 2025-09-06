/**
 * Budget-Performance API Client
 * 예산-성과 분석 API 클라이언트
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// API 응답 타입 정의
export interface Sport {
  id: number;
  code: string;
  name: string;
  category: string;
  olympic_status: boolean;
}

export interface Institution {
  id: number;
  name: string;
  type: string;
}

export interface EfficiencyAnalysis {
  year: number;
  sport?: Sport;
  region_code?: string;
  budget_total: number;
  budget_executed: number;
  execution_rate: number;
  performance_score: number;
  efficiency: number;
  grade: string;
  rank?: number;
}

export interface ROIAnalysis {
  year: number;
  sport?: Sport;
  institution?: Institution;
  investment: number;
  return_value: number;
  roi: number;
  roi_rank: number;
  category: string;
}

export interface TrendData {
  date: string;
  budget: number;
  performance: number;
  efficiency: number;
  roi?: number;
}

export interface RegionComparison {
  region_code: string;
  region_name: string;
  budget_total: number;
  performance_avg: number;
  efficiency: number;
  rank: number;
  population_per_budget?: number;
}

export interface BudgetPerformanceOverview {
  summary: {
    total_budget: number;
    total_executed: number;
    execution_rate: number;
    efficiency: number;
    efficiency_grade: string;
    institution_count: number;
    project_count: number;
    sport_count: number;
    indicator_count: number;
    avg_performance_score: number;
  };
  highlights: Array<{
    type: string;
    title: string;
    value: string;
    metric: string;
    grade?: string;
  }>;
  efficiency_by_sport: EfficiencyAnalysis[];
  roi_top_performers: ROIAnalysis[];
  regional_comparison: RegionComparison[];
  trend_data: TrendData[];
}

export interface BudgetPerformanceFilter {
  year?: number;
  region_code?: string;
  sport_id?: number;
  institution_id?: number;
  group_by?: 'region' | 'sport' | 'institution' | 'project';
  granularity?: 'year' | 'quarter' | 'month';
}

export interface LatestRun {
  run_id: number;
  source: string;
  schema_version: string;
  started_at: string;
  finished_at: string;
  status: string;
  row_count: number;
}

class BudgetPerformanceAPI {
  private axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  constructor() {
    // 토큰 인터셉터 추가
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // ETag 응답 처리
    this.axiosInstance.interceptors.response.use(
      (response) => {
        // ETag 저장
        if (response.headers.etag) {
          const url = response.config.url;
          const params = JSON.stringify(response.config.params);
          const cacheKey = `etag:${url}:${params}`;
          localStorage.setItem(cacheKey, response.headers.etag);
        }
        return response;
      },
      (error) => {
        // 304 Not Modified 처리
        if (error.response?.status === 304) {
          // 캐시된 데이터 반환
          const url = error.config.url;
          const params = JSON.stringify(error.config.params);
          const cacheKey = `data:${url}:${params}`;
          const cachedData = localStorage.getItem(cacheKey);
          if (cachedData) {
            return { data: JSON.parse(cachedData), cached: true };
          }
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * 최신 ETL 실행 정보 조회
   */
  async getLatestRun(): Promise<LatestRun> {
    const response = await this.axiosInstance.get('/budget-performance/meta/latest-run');
    return response.data;
  }

  /**
   * 예산-성과 개요 조회
   */
  async getOverview(filters?: BudgetPerformanceFilter): Promise<BudgetPerformanceOverview> {
    // ETag 확인
    const url = '/budget-performance/overview';
    const params = JSON.stringify(filters);
    const cacheKey = `etag:${url}:${params}`;
    const etag = localStorage.getItem(cacheKey);

    const response = await this.axiosInstance.get(url, {
      params: filters,
      headers: etag ? { 'If-None-Match': etag } : {},
    });

    // 데이터 캐싱
    if (!response.cached) {
      const dataKey = `data:${url}:${params}`;
      localStorage.setItem(dataKey, JSON.stringify(response.data));
    }

    return response.data;
  }

  /**
   * 효율성 분석 조회
   */
  async getEfficiencyAnalysis(year: number, limit: number = 10): Promise<EfficiencyAnalysis[]> {
    const url = '/budget-performance/efficiency';
    const params = { year, limit };
    const cacheKey = `etag:${url}:${JSON.stringify(params)}`;
    const etag = localStorage.getItem(cacheKey);

    const response = await this.axiosInstance.get(url, {
      params,
      headers: etag ? { 'If-None-Match': etag } : {},
    });

    return response.data;
  }

  /**
   * ROI 분석 조회
   */
  async getROIAnalysis(year: number, limit: number = 10): Promise<ROIAnalysis[]> {
    const url = '/budget-performance/roi';
    const params = { year, limit };
    const cacheKey = `etag:${url}:${JSON.stringify(params)}`;
    const etag = localStorage.getItem(cacheKey);

    const response = await this.axiosInstance.get(url, {
      params,
      headers: etag ? { 'If-None-Match': etag } : {},
    });

    return response.data;
  }

  /**
   * 지역별 비교 조회
   */
  async getRegionalComparison(year: number): Promise<RegionComparison[]> {
    const url = '/budget-performance/comparison';
    const params = { year };
    const cacheKey = `etag:${url}:${JSON.stringify(params)}`;
    const etag = localStorage.getItem(cacheKey);

    const response = await this.axiosInstance.get(url, {
      params,
      headers: etag ? { 'If-None-Match': etag } : {},
    });

    return response.data;
  }

  /**
   * 트렌드 데이터 조회
   */
  async getTrendData(
    startYear: number,
    endYear: number,
    sportId?: number,
    regionCode?: string
  ): Promise<TrendData[]> {
    const url = '/budget-performance/trend';
    const params = {
      start_year: startYear,
      end_year: endYear,
      sport_id: sportId,
      region_code: regionCode,
    };
    const cacheKey = `etag:${url}:${JSON.stringify(params)}`;
    const etag = localStorage.getItem(cacheKey);

    const response = await this.axiosInstance.get(url, {
      params,
      headers: etag ? { 'If-None-Match': etag } : {},
    });

    return response.data;
  }

  /**
   * 데이터 내보내기
   */
  async exportData(
    filters: BudgetPerformanceFilter,
    format: 'csv' | 'xlsx' | 'json' = 'xlsx',
    includeCharts: boolean = false
  ): Promise<{ status: string; message: string; task_id: string }> {
    const response = await this.axiosInstance.post('/budget-performance/export', {
      filters,
      format,
      include_charts: includeCharts,
    });

    return response.data;
  }

  /**
   * 캐시 무효화 (관리자)
   */
  async invalidateCache(runId?: number): Promise<{ status: string; message: string; deleted_count: number }> {
    const response = await this.axiosInstance.post('/budget-performance/cache/invalidate', null, {
      params: { run_id: runId },
    });

    return response.data;
  }
}

// 싱글톤 인스턴스
export const budgetPerformanceAPI = new BudgetPerformanceAPI();
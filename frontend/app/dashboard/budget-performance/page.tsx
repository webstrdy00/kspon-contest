'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/header';
import { Sidebar } from '@/components/layout/sidebar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import ScatterPlot from '@/components/budget-performance/charts/ScatterPlot';
import TreemapChart from '@/components/budget-performance/charts/Treemap';
import TrendChart from '@/components/budget-performance/charts/TrendChart';
import { budgetPerformanceAPI, BudgetPerformanceOverview } from '@/lib/api/budget-performance';
import { TrendingUp, DollarSign, Trophy, Target, AlertCircle, Download, RefreshCw } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export default function BudgetPerformancePage() {
  const { user } = useAuth();
  const [selectedYear, setSelectedYear] = useState<string>('2024');
  const [selectedGroupBy, setSelectedGroupBy] = useState<string>('sport');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BudgetPerformanceOverview | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // 데이터 로드
  const loadData = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    setError(null);
    
    try {
      const overview = await budgetPerformanceAPI.getOverview({
        year: parseInt(selectedYear),
        group_by: selectedGroupBy as any,
      });
      setData(overview);
    } catch (err: any) {
      console.error('데이터 로드 실패:', err);
      setError(err.response?.data?.detail || '데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // 초기 로드 및 필터 변경 시 재로드
  useEffect(() => {
    loadData();
  }, [selectedYear, selectedGroupBy]);

  // 새로고침
  const handleRefresh = () => {
    setRefreshing(true);
    loadData(false);
  };

  // 데이터 내보내기
  const handleExport = async () => {
    try {
      const result = await budgetPerformanceAPI.exportData(
        {
          year: parseInt(selectedYear),
          group_by: selectedGroupBy as any,
        },
        'xlsx',
        true
      );
      alert(result.message);
    } catch (err) {
      console.error('내보내기 실패:', err);
      alert('데이터 내보내기에 실패했습니다.');
    }
  };

  // 로딩 상태
  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6">
            <div className="space-y-6">
              <Skeleton className="h-10 w-1/3" />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[1, 2, 3, 4].map((i) => (
                  <Card key={i}>
                    <CardHeader>
                      <Skeleton className="h-4 w-24" />
                    </CardHeader>
                    <CardContent>
                      <Skeleton className="h-8 w-32" />
                      <Skeleton className="h-3 w-20 mt-2" />
                    </CardContent>
                  </Card>
                ))}
              </div>
              <Skeleton className="h-96 w-full" />
            </div>
          </main>
        </div>
      </div>
    );
  }

  // 에러 상태
  if (error) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <Button onClick={() => loadData()} className="mt-4">
              다시 시도
            </Button>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="space-y-6">
            {/* 페이지 헤더 */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">예산-성과 분석</h1>
                <p className="text-muted-foreground">
                  체육 예산 투입과 경기력 성과의 상관관계를 분석합니다
                </p>
              </div>
              <div className="flex gap-3">
                <Select value={selectedYear} onValueChange={setSelectedYear}>
                  <SelectTrigger className="w-[120px]">
                    <SelectValue placeholder="연도" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2024">2024년</SelectItem>
                    <SelectItem value="2023">2023년</SelectItem>
                    <SelectItem value="2022">2022년</SelectItem>
                    <SelectItem value="2021">2021년</SelectItem>
                    <SelectItem value="2020">2020년</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedGroupBy} onValueChange={setSelectedGroupBy}>
                  <SelectTrigger className="w-[160px]">
                    <SelectValue placeholder="그룹별" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="sport">종목별</SelectItem>
                    <SelectItem value="region">지역별</SelectItem>
                    <SelectItem value="institution">기관별</SelectItem>
                    <SelectItem value="project">사업별</SelectItem>
                  </SelectContent>
                </Select>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={handleRefresh}
                  disabled={refreshing}
                >
                  <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                </Button>
                <Button variant="outline" onClick={handleExport}>
                  <Download className="h-4 w-4 mr-2" />
                  내보내기
                </Button>
              </div>
            </div>

            {/* 주요 지표 카드 */}
            {data && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">총 예산 투입액</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {(data.summary.total_budget / 100000000).toFixed(0)}억원
                    </div>
                    <p className="text-xs text-muted-foreground">
                      집행률 <span className="text-green-600">{data.summary.execution_rate.toFixed(1)}%</span>
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">평균 성과 점수</CardTitle>
                    <Trophy className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {data.summary.avg_performance_score.toFixed(1)}점
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {data.summary.indicator_count}개 지표 평균
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">예산 효율성</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{data.summary.efficiency.toFixed(1)}%</div>
                    <p className="text-xs text-muted-foreground">
                      <Badge variant={data.summary.efficiency_grade === 'S' || data.summary.efficiency_grade === 'A' ? 'default' : 'secondary'}>
                        {data.summary.efficiency_grade}등급
                      </Badge>
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">참여 기관</CardTitle>
                    <Target className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{data.summary.institution_count}개</div>
                    <p className="text-xs text-muted-foreground">
                      {data.summary.project_count}개 사업 진행
                    </p>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* 하이라이트 */}
            {data && data.highlights.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {data.highlights.map((highlight, idx) => (
                  <Card key={idx} className="bg-gradient-to-br from-blue-50 to-white dark:from-blue-950 dark:to-background">
                    <CardHeader>
                      <CardTitle className="text-sm">{highlight.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-xl font-bold">{highlight.value}</p>
                      <p className="text-sm text-muted-foreground">{highlight.metric}</p>
                      {highlight.grade && (
                        <Badge className="mt-2">{highlight.grade}등급</Badge>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* 차트 탭 */}
            {data && (
              <Tabs defaultValue="scatter" className="space-y-4">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="scatter">예산 vs 성과</TabsTrigger>
                  <TabsTrigger value="treemap">예산 배분</TabsTrigger>
                  <TabsTrigger value="trend">시계열 트렌드</TabsTrigger>
                </TabsList>

                <TabsContent value="scatter" className="space-y-4">
                  <ScatterPlot
                    data={data.efficiency_by_sport}
                    title="종목별 예산 대비 성과 분석"
                    description="예산 집행액과 성과 점수의 상관관계를 보여줍니다. 원의 크기는 효율성을 나타냅니다."
                  />
                </TabsContent>

                <TabsContent value="treemap" className="space-y-4">
                  <TreemapChart
                    data={selectedGroupBy === 'region' ? data.regional_comparison : data.efficiency_by_sport}
                    type={selectedGroupBy === 'region' ? 'region' : 'sport'}
                    title={`${selectedGroupBy === 'region' ? '지역별' : '종목별'} 예산 배분 현황`}
                    description="영역의 크기는 예산 규모를, 색상은 효율성을 나타냅니다."
                  />
                </TabsContent>

                <TabsContent value="trend" className="space-y-4">
                  <TrendChart
                    data={data.trend_data}
                    title="예산-성과 시계열 트렌드"
                    description="시간에 따른 예산, 성과, 효율성의 변화를 보여줍니다."
                    showROI={true}
                  />
                </TabsContent>
              </Tabs>
            )}

            {/* ROI 상위 수행자 */}
            {data && data.roi_top_performers.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>ROI 상위 종목</CardTitle>
                  <CardDescription>투자 대비 수익률이 높은 종목들입니다.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {data.roi_top_performers.slice(0, 5).map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-900">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 font-semibold text-sm">
                            {item.roi_rank}
                          </div>
                          <div>
                            <p className="font-medium">{item.sport?.name || '미분류'}</p>
                            <p className="text-xs text-muted-foreground">{item.category}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold text-green-600">ROI {item.roi.toFixed(1)}%</p>
                          <p className="text-xs text-muted-foreground">
                            투자 {(item.investment / 100000000).toFixed(1)}억
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
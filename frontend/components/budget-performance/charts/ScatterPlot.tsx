'use client';

import React, { useMemo } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { EfficiencyAnalysis } from '@/lib/api/budget-performance';

interface ScatterPlotProps {
  data: EfficiencyAnalysis[];
  title?: string;
  description?: string;
}

// 등급별 색상
const GRADE_COLORS: Record<string, string> = {
  S: '#10b981', // emerald-500
  A: '#3b82f6', // blue-500
  B: '#8b5cf6', // violet-500
  C: '#f59e0b', // amber-500
  D: '#ef4444', // red-500
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 rounded-lg shadow-lg border">
        <p className="font-semibold text-sm">{data.sport?.name || '종목'}</p>
        <div className="mt-1 space-y-1 text-xs">
          <p>예산: {(data.x / 100000000).toFixed(1)}억원</p>
          <p>성과: {data.y.toFixed(1)}점</p>
          <p>효율성: {data.efficiency.toFixed(1)}%</p>
          <p className="font-semibold">등급: {data.grade}</p>
        </div>
      </div>
    );
  }
  return null;
};

export default function ScatterPlot({ data, title, description }: ScatterPlotProps) {
  // 차트 데이터 변환
  const chartData = useMemo(() => {
    return data.map((item) => ({
      x: Number(item.budget_executed),
      y: item.performance_score,
      efficiency: item.efficiency,
      grade: item.grade,
      sport: item.sport,
      size: Math.max(10, Math.min(50, item.efficiency)), // 효율성에 따른 버블 크기
    }));
  }, [data]);

  // 축 범위 계산
  const xDomain = useMemo(() => {
    const values = chartData.map((d) => d.x);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const padding = (max - min) * 0.1;
    return [Math.max(0, min - padding), max + padding];
  }, [chartData]);

  const yDomain = useMemo(() => {
    const values = chartData.map((d) => d.y);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const padding = (max - min) * 0.1;
    return [Math.max(0, min - padding), max + padding];
  }, [chartData]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title || '예산 대비 성과 분석'}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart
            margin={{ top: 20, right: 20, bottom: 40, left: 60 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              type="number"
              dataKey="x"
              name="예산"
              domain={xDomain}
              tickFormatter={(value) => `${(value / 100000000).toFixed(0)}억`}
              label={{
                value: '집행 예산 (억원)',
                position: 'insideBottom',
                offset: -10,
                style: { textAnchor: 'middle', fill: '#6b7280' },
              }}
            />
            <YAxis
              type="number"
              dataKey="y"
              name="성과"
              domain={yDomain}
              tickFormatter={(value) => value.toFixed(0)}
              label={{
                value: '성과 점수',
                angle: -90,
                position: 'insideLeft',
                style: { textAnchor: 'middle', fill: '#6b7280' },
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="top"
              height={36}
              content={() => (
                <div className="flex justify-center gap-4 mb-2">
                  {Object.entries(GRADE_COLORS).map(([grade, color]) => (
                    <div key={grade} className="flex items-center gap-1">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: color }}
                      />
                      <span className="text-xs text-gray-600">{grade}등급</span>
                    </div>
                  ))}
                </div>
              )}
            />
            <Scatter name="종목별 효율성" data={chartData}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={GRADE_COLORS[entry.grade] || '#9ca3af'}
                  fillOpacity={0.8}
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>

        {/* 범례 설명 */}
        <div className="mt-4 text-xs text-gray-500 text-center">
          * 원의 크기는 효율성을 나타냅니다
        </div>
      </CardContent>
    </Card>
  );
}
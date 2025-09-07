'use client';

import React, { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendData } from '@/lib/api/budget-performance';
import { format, parseISO } from 'date-fns';
import { ko } from 'date-fns/locale';

interface TrendChartProps {
  data: TrendData[];
  title?: string;
  description?: string;
  showROI?: boolean;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 rounded-lg shadow-lg border">
        <p className="font-semibold text-sm">
          {format(parseISO(label), 'yyyy년 MM월', { locale: ko })}
        </p>
        <div className="mt-1 space-y-1 text-xs">
          {payload.map((entry: any) => (
            <p key={entry.dataKey} style={{ color: entry.color }}>
              {entry.name}: {
                entry.dataKey === 'budget' 
                  ? `${(entry.value / 100000000).toFixed(1)}억원`
                  : entry.dataKey === 'roi'
                  ? `${entry.value.toFixed(1)}%`
                  : `${entry.value.toFixed(1)}점`
              }
            </p>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

export default function TrendChart({ data, title, description, showROI = false }: TrendChartProps) {
  // 차트 데이터 변환
  const chartData = useMemo(() => {
    return data.map((item) => ({
      date: item.date,
      budget: Number(item.budget),
      performance: item.performance,
      efficiency: item.efficiency,
      roi: item.roi,
    }));
  }, [data]);

  // Y축 설정
  const yAxisConfig = useMemo(() => {
    if (chartData.length === 0) {
      return {
        budget: { domain: [0, 1], ticks: 5 },
        performance: { domain: [0, 100], ticks: 5 },
      };
    }

    const maxBudget = Math.max(...chartData.map((d) => d.budget));
    const maxPerf = Math.max(...chartData.map((d) => d.performance));
    
    return {
      budget: {
        domain: [0, maxBudget * 1.1],
        ticks: 5,
      },
      performance: {
        domain: [0, Math.max(100, maxPerf * 1.1)],
        ticks: 5,
      },
    };
  }, [chartData]);

  // 평균값 계산
  const averages = useMemo(() => {
    const count = chartData.length;
    if (count === 0) return { efficiency: 0, roi: 0 };
    
    const sumEfficiency = chartData.reduce((sum, d) => sum + d.efficiency, 0);
    const sumROI = chartData.reduce((sum, d) => sum + (d.roi || 0), 0);
    
    return {
      efficiency: sumEfficiency / count,
      roi: sumROI / count,
    };
  }, [chartData]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title || '시계열 트렌드 분석'}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart
            data={chartData}
            margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="date"
              tickFormatter={(value) => format(parseISO(value), 'yyyy.MM', { locale: ko })}
              angle={-45}
              textAnchor="end"
              height={60}
              style={{ fontSize: 11 }}
            />
            
            {/* 왼쪽 Y축 - 예산 */}
            <YAxis
              yAxisId="budget"
              orientation="left"
              domain={yAxisConfig.budget.domain}
              tickFormatter={(value) => `${(value / 100000000).toFixed(0)}억`}
              label={{
                value: '예산 (억원)',
                angle: -90,
                position: 'insideLeft',
                style: { textAnchor: 'middle', fill: '#6b7280' },
              }}
            />
            
            {/* 오른쪽 Y축 - 성과/효율성 */}
            <YAxis
              yAxisId="performance"
              orientation="right"
              domain={yAxisConfig.performance.domain}
              tickFormatter={(value) => value.toFixed(0)}
              label={{
                value: '성과/효율성 (%)',
                angle: 90,
                position: 'insideRight',
                style: { textAnchor: 'middle', fill: '#6b7280' },
              }}
            />
            
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              verticalAlign="top"
              height={36}
              iconType="line"
            />
            
            {/* 평균선 */}
            <ReferenceLine
              yAxisId="performance"
              y={averages.efficiency}
              stroke="#9ca3af"
              strokeDasharray="3 3"
              label={{
                value: `효율성 평균: ${averages.efficiency.toFixed(1)}%`,
                position: 'right',
                style: { fontSize: 10, fill: '#9ca3af' },
              }}
            />
            
            {/* 라인들 */}
            <Line
              yAxisId="budget"
              type="monotone"
              dataKey="budget"
              name="예산"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
            <Line
              yAxisId="performance"
              type="monotone"
              dataKey="performance"
              name="성과"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
            <Line
              yAxisId="performance"
              type="monotone"
              dataKey="efficiency"
              name="효율성"
              stroke="#8b5cf6"
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
            {showROI && (
              <Line
                yAxisId="performance"
                type="monotone"
                dataKey="roi"
                name="ROI"
                stroke="#f59e0b"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>

        {/* 추가 정보 */}
        <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-gray-600 text-xs">평균 효율성</p>
            <p className="font-semibold text-lg">{averages.efficiency.toFixed(1)}%</p>
          </div>
          {showROI && averages.roi > 0 && (
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-gray-600 text-xs">평균 ROI</p>
              <p className="font-semibold text-lg">{averages.roi.toFixed(1)}%</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
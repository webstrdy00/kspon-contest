'use client';

import React, { useMemo } from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { EfficiencyAnalysis, RegionComparison } from '@/lib/api/budget-performance';

interface TreemapProps {
  data: EfficiencyAnalysis[] | RegionComparison[];
  title?: string;
  description?: string;
  type: 'sport' | 'region';
}

// 효율성에 따른 색상 계산
const getColorByEfficiency = (efficiency: number): string => {
  if (efficiency >= 95) return '#10b981'; // S - emerald-500
  if (efficiency >= 90) return '#3b82f6'; // A - blue-500
  if (efficiency >= 80) return '#8b5cf6'; // B - violet-500
  if (efficiency >= 70) return '#f59e0b'; // C - amber-500
  return '#ef4444'; // D - red-500
};

// 커스텀 콘텐츠 렌더러
const CustomizedContent = (props: any) => {
  const { x, y, width, height, name, value, efficiency } = props;

  // 너무 작은 영역은 텍스트 표시 안 함
  if (width < 50 || height < 30) {
    return (
      <g>
        <rect
          x={x}
          y={y}
          width={width}
          height={height}
          fill={getColorByEfficiency(efficiency)}
          fillOpacity={0.8}
          stroke="#fff"
          strokeWidth={2}
        />
      </g>
    );
  }

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={getColorByEfficiency(efficiency)}
        fillOpacity={0.8}
        stroke="#fff"
        strokeWidth={2}
      />
      <text
        x={x + width / 2}
        y={y + height / 2 - 10}
        textAnchor="middle"
        fill="#fff"
        fontSize={12}
        fontWeight="600"
      >
        {name}
      </text>
      <text
        x={x + width / 2}
        y={y + height / 2 + 5}
        textAnchor="middle"
        fill="#fff"
        fontSize={10}
      >
        {(value / 100000000).toFixed(1)}억
      </text>
      <text
        x={x + width / 2}
        y={y + height / 2 + 18}
        textAnchor="middle"
        fill="#fff"
        fontSize={9}
      >
        효율: {efficiency.toFixed(1)}%
      </text>
    </g>
  );
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 rounded-lg shadow-lg border">
        <p className="font-semibold text-sm">{data.name}</p>
        <div className="mt-1 space-y-1 text-xs">
          <p>예산: {(data.value / 100000000).toFixed(1)}억원</p>
          <p>효율성: {data.efficiency.toFixed(1)}%</p>
          {data.grade && <p>등급: {data.grade}</p>}
          {data.rank && <p>순위: {data.rank}위</p>}
        </div>
      </div>
    );
  }
  return null;
};

export default function TreemapChart({ data, title, description, type }: TreemapProps) {
  // Treemap 데이터 변환
  const treemapData = useMemo(() => {
    if (type === 'sport') {
      const sportData = data as EfficiencyAnalysis[];
      return sportData.map((item) => ({
        name: item.sport?.name || '미분류',
        value: Number(item.budget_total),
        efficiency: item.efficiency,
        grade: item.grade,
        rank: item.rank,
      }));
    } else {
      const regionData = data as RegionComparison[];
      return regionData.map((item) => ({
        name: item.region_name,
        value: Number(item.budget_total),
        efficiency: item.efficiency,
        rank: item.rank,
      }));
    }
  }, [data, type]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title || '예산 배분 현황'}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <Treemap
            data={treemapData}
            dataKey="value"
            aspectRatio={4 / 3}
            stroke="#fff"
            content={<CustomizedContent />}
          >
            <Tooltip content={<CustomTooltip />} />
          </Treemap>
        </ResponsiveContainer>

        {/* 색상 범례 */}
        <div className="mt-4 flex justify-center gap-4">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#10b981' }} />
            <span className="text-xs text-gray-600">95% 이상</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#3b82f6' }} />
            <span className="text-xs text-gray-600">90-95%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#8b5cf6' }} />
            <span className="text-xs text-gray-600">80-90%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#f59e0b' }} />
            <span className="text-xs text-gray-600">70-80%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#ef4444' }} />
            <span className="text-xs text-gray-600">70% 미만</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
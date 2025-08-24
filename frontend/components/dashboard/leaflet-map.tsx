"use client"

import { useEffect, useRef } from "react"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

// Leaflet 아이콘 경로 수정
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

interface FacilityData {
  id: string
  name: string
  type: string
  lat: number
  lng: number
  region: string
  demandPercentage: number
  supplyDemandRatio: number
}

interface LeafletMapProps {
  selectedFacility: string
  showDemandLayer: boolean
  showHeatmap: boolean
}

export function LeafletMap({ selectedFacility, showDemandLayer, showHeatmap }: LeafletMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)

  // Mock 시설 데이터
  const facilities: FacilityData[] = [
    {
      id: '1',
      name: '서울시민수영장',
      type: '수영장',
      lat: 37.5665,
      lng: 126.9780,
      region: '서울특별시 중구',
      demandPercentage: 68.5,
      supplyDemandRatio: 0.7
    },
    {
      id: '2',
      name: '마포체육관',
      type: '체육관',
      lat: 37.5511,
      lng: 126.9398,
      region: '서울특별시 마포구',
      demandPercentage: 75.2,
      supplyDemandRatio: 0.6
    },
    {
      id: '3',
      name: '강남테니스장',
      type: '테니스장',
      lat: 37.4979,
      lng: 127.0276,
      region: '서울특별시 강남구',
      demandPercentage: 45.8,
      supplyDemandRatio: 1.2
    },
    {
      id: '4',
      name: '부산해운대수영장',
      type: '수영장',
      lat: 35.1588,
      lng: 129.1602,
      region: '부산광역시 해운대구',
      demandPercentage: 62.3,
      supplyDemandRatio: 0.8
    },
    {
      id: '5',
      name: '대구체육관',
      type: '체육관',
      lat: 35.8714,
      lng: 128.6014,
      region: '대구광역시 중구',
      demandPercentage: 72.1,
      supplyDemandRatio: 0.9
    },
    {
      id: '6',
      name: '인천축구장',
      type: '축구장',
      lat: 37.4563,
      lng: 126.7052,
      region: '인천광역시 남동구',
      demandPercentage: 55.3,
      supplyDemandRatio: 1.1
    }
  ]

  // 지도 초기화
  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return

    const map = L.map(mapRef.current, {
      center: [36.5, 127.8], // 한국 중심
      zoom: 7,
      zoomControl: true
    })

    mapInstanceRef.current = map

    // OpenStreetMap 타일 레이어 추가 (VWorld는 API 키 필요하므로 개발용으로 OSM 사용)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map)

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [])

  // 마커 업데이트
  useEffect(() => {
    if (!mapInstanceRef.current) return

    const map = mapInstanceRef.current

    // 기존 마커 제거
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer)
      }
    })

    // 필터링된 시설 데이터
    let filteredFacilities = facilities
    if (selectedFacility !== 'all') {
      const facilityTypeMap: { [key: string]: string } = {
        'swimming': '수영장',
        'gym': '체육관',
        'tennis': '테니스장',
        'football': '축구장'
      }
      const targetType = facilityTypeMap[selectedFacility]
      if (targetType) {
        filteredFacilities = filteredFacilities.filter(f => f.type === targetType)
      }
    }

    // 마커 추가
    filteredFacilities.forEach(facility => {
      const isHighDemandLowSupply = facility.supplyDemandRatio < 0.8 && facility.demandPercentage > 60
      const isBalanced = facility.supplyDemandRatio >= 0.8 && facility.supplyDemandRatio <= 1.2
      const isOverSupplied = facility.supplyDemandRatio > 1.2

      let iconColor = '#3B82F6' // 기본 파란색
      let statusText = '균형'

      if (isHighDemandLowSupply) {
        iconColor = '#EF4444' // 빨간색 - 공급 부족
        statusText = '공급 부족'
      } else if (isOverSupplied) {
        iconColor = '#10B981' // 초록색 - 공급 충분
        statusText = '공급 충분'
      }

      // 커스텀 아이콘 생성
      const customIcon = L.divIcon({
        html: `
          <div style="
            background-color: ${iconColor};
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
            font-weight: bold;
          ">
            ${facility.type === '수영장' ? '🏊' : 
              facility.type === '체육관' ? '🏟️' :
              facility.type === '테니스장' ? '🎾' : 
              facility.type === '축구장' ? '⚽' : '🏃'}
          </div>
        `,
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10]
      })

      const marker = L.marker([facility.lat, facility.lng], { icon: customIcon })
        .bindPopup(`
          <div style="font-family: system-ui, sans-serif; min-width: 200px;">
            <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold; color: #1f2937;">
              ${facility.name}
            </h3>
            <div style="background: #f3f4f6; padding: 8px; border-radius: 6px; margin-bottom: 8px;">
              <p style="margin: 2px 0; font-size: 12px;"><strong>유형:</strong> ${facility.type}</p>
              <p style="margin: 2px 0; font-size: 12px;"><strong>지역:</strong> ${facility.region}</p>
            </div>
            <div style="background: #fef3c7; padding: 8px; border-radius: 6px; margin-bottom: 8px;">
              <p style="margin: 2px 0; font-size: 12px;"><strong>주민 수요:</strong> ${facility.demandPercentage}%</p>
              <p style="margin: 2px 0; font-size: 12px;"><strong>공급-수요 비율:</strong> ${facility.supplyDemandRatio}</p>
            </div>
            <div style="text-align: center; padding: 4px;">
              <span style="
                color: ${iconColor}; 
                font-weight: bold; 
                background: ${iconColor}15; 
                padding: 2px 8px; 
                border-radius: 12px;
                font-size: 11px;
              ">
                ${statusText}
              </span>
            </div>
          </div>
        `, {
          maxWidth: 250,
          className: 'custom-popup'
        })
        .addTo(map)
    })

  }, [selectedFacility, showDemandLayer, showHeatmap])

  return (
    <div 
      ref={mapRef} 
      className="h-96 w-full rounded-lg border"
      style={{ minHeight: '384px' }}
    />
  )
}
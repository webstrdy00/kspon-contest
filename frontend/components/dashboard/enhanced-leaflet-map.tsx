"use client"

import { useEffect, useRef, useState } from "react"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import "leaflet.markercluster/dist/MarkerCluster.css"
import "leaflet.markercluster/dist/MarkerCluster.Default.css"
import "leaflet.markercluster"
import "leaflet.heat"

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
  address?: string
  operator?: string
  phone?: string
  is_public?: boolean
  capacity?: number
  demandPercentage: number
  supplyDemandRatio: number
}

interface RegionDemandData {
  region: string
  lat: number
  lng: number
  demandScore: number
  facilityCount: number
  population: number
  facilityPerCapita: number
}

interface EnhancedLeafletMapProps {
  selectedFacility: string
  showDemandLayer: boolean
  showHeatmap: boolean
  showClusters: boolean
  selectedRegion: string | null
  onRegionSelect?: (region: string | null) => void
  facilities?: FacilityData[]
  regionDemand?: RegionDemandData[]
}

// VWorld 타일 레이어 설정
const VWORLD_KEY = process.env.NEXT_PUBLIC_VWORLD_KEY || ""
const VWORLD_BASE_URL = "https://api.vworld.kr/req/wmts/1.0.0"

export function EnhancedLeafletMap({ 
  selectedFacility, 
  showDemandLayer, 
  showHeatmap,
  showClusters = true,
  selectedRegion,
  onRegionSelect,
  facilities: propFacilities,
  regionDemand: propRegionDemand
}: EnhancedLeafletMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const markersRef = useRef<L.MarkerClusterGroup | null>(null)
  const heatmapLayerRef = useRef<L.HeatLayer | null>(null)
  const demandLayerRef = useRef<L.LayerGroup | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  // 실제 API 데이터 또는 Mock 데이터
  const facilities: FacilityData[] = propFacilities || [
    {
      id: '1',
      name: '서울시민수영장',
      type: '수영장',
      lat: 37.5665,
      lng: 126.9780,
      region: '서울특별시',
      address: '서울특별시 중구 세종대로 110',
      operator: '서울시체육시설관리사업소',
      phone: '02-2133-2741',
      is_public: true,
      capacity: 500,
      demandPercentage: 68.5,
      supplyDemandRatio: 0.7
    },
    {
      id: '2',
      name: '마포체육관',
      type: '체육관',
      lat: 37.5511,
      lng: 126.9398,
      region: '서울특별시',
      address: '서울특별시 마포구 희우정로 16길 23',
      operator: '마포구시설관리공단',
      phone: '02-300-5000',
      is_public: true,
      capacity: 1200,
      demandPercentage: 75.2,
      supplyDemandRatio: 0.6
    },
    {
      id: '3',
      name: '강남테니스장',
      type: '테니스장',
      lat: 37.4979,
      lng: 127.0276,
      region: '서울특별시',
      address: '서울특별시 강남구 영동대로 513',
      operator: '강남구도시관리공단',
      phone: '02-3423-5600',
      is_public: true,
      capacity: 12,
      demandPercentage: 45.8,
      supplyDemandRatio: 1.2
    },
    {
      id: '4',
      name: '부산해운대수영장',
      type: '수영장',
      lat: 35.1588,
      lng: 129.1602,
      region: '부산광역시',
      address: '부산광역시 해운대구 우동 620',
      operator: '해운대구시설관리공단',
      phone: '051-749-7601',
      is_public: true,
      capacity: 800,
      demandPercentage: 62.3,
      supplyDemandRatio: 0.8
    },
    {
      id: '5',
      name: '대구체육관',
      type: '체육관',
      lat: 35.8714,
      lng: 128.6014,
      region: '대구광역시',
      address: '대구광역시 중구 국채보상로 140길 22',
      operator: '대구시설공단',
      phone: '053-803-6340',
      is_public: true,
      capacity: 2000,
      demandPercentage: 72.1,
      supplyDemandRatio: 0.9
    },
    // 클러스터링 테스트를 위한 추가 시설
    ...Array.from({ length: 50 }, (_, i) => ({
      id: `cluster-${i}`,
      name: `시설 ${i}`,
      type: ['수영장', '체육관', '테니스장', '축구장', '농구장'][Math.floor(Math.random() * 5)],
      lat: 35.5 + Math.random() * 3,
      lng: 126.5 + Math.random() * 2,
      region: ['서울특별시', '경기도', '인천광역시'][Math.floor(Math.random() * 3)],
      demandPercentage: 40 + Math.random() * 40,
      supplyDemandRatio: 0.5 + Math.random() * 1.5
    }))
  ]

  // 지역별 수요 데이터
  const regionDemand: RegionDemandData[] = propRegionDemand || [
    { region: '서울특별시', lat: 37.5665, lng: 126.9780, demandScore: 85, facilityCount: 2847, population: 9720846, facilityPerCapita: 0.29 },
    { region: '부산광역시', lat: 35.1796, lng: 129.0756, demandScore: 68, facilityCount: 1234, population: 3349016, facilityPerCapita: 0.37 },
    { region: '대구광역시', lat: 35.8714, lng: 128.6014, demandScore: 78, facilityCount: 987, population: 2410700, facilityPerCapita: 0.41 },
    { region: '인천광역시', lat: 37.4563, lng: 126.7052, demandScore: 61, facilityCount: 1456, population: 2954955, facilityPerCapita: 0.49 },
    { region: '광주광역시', lat: 35.1595, lng: 126.8526, demandScore: 45, facilityCount: 678, population: 1441970, facilityPerCapita: 0.47 },
    { region: '대전광역시', lat: 36.3504, lng: 127.3845, demandScore: 82, facilityCount: 789, population: 1454679, facilityPerCapita: 0.54 },
    { region: '울산광역시', lat: 35.5384, lng: 129.3114, demandScore: 55, facilityCount: 456, population: 1124459, facilityPerCapita: 0.41 },
    { region: '경기도', lat: 37.4138, lng: 127.5183, demandScore: 75, facilityCount: 4567, population: 13511909, facilityPerCapita: 0.34 },
    { region: '강원도', lat: 37.8228, lng: 128.1555, demandScore: 48, facilityCount: 789, population: 1536499, facilityPerCapita: 0.51 },
    { region: '충청북도', lat: 36.6357, lng: 127.4915, demandScore: 52, facilityCount: 567, population: 1598428, facilityPerCapita: 0.36 },
    { region: '충청남도', lat: 36.5184, lng: 126.8000, demandScore: 58, facilityCount: 890, population: 2123709, facilityPerCapita: 0.42 },
    { region: '전라북도', lat: 35.7175, lng: 127.1530, demandScore: 49, facilityCount: 678, population: 1780013, facilityPerCapita: 0.38 },
    { region: '전라남도', lat: 34.8161, lng: 126.4629, demandScore: 44, facilityCount: 789, population: 1799130, facilityPerCapita: 0.44 },
    { region: '경상북도', lat: 36.4919, lng: 128.8889, demandScore: 51, facilityCount: 890, population: 2630254, facilityPerCapita: 0.34 },
    { region: '경상남도', lat: 35.4606, lng: 128.2132, demandScore: 56, facilityCount: 1123, population: 3281950, facilityPerCapita: 0.34 },
    { region: '제주특별자치도', lat: 33.4996, lng: 126.5312, demandScore: 62, facilityCount: 234, population: 677656, facilityPerCapita: 0.35 }
  ]

  // 지도 초기화
  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return

    const map = L.map(mapRef.current, {
      center: [36.5, 127.8], // 한국 중심
      zoom: 7,
      zoomControl: true,
      preferCanvas: true // 성능 향상
    })

    mapInstanceRef.current = map

    // VWorld 타일 레이어 또는 OSM 타일 사용
    if (VWORLD_KEY) {
      // VWorld 타일 사용
      L.tileLayer(`${VWORLD_BASE_URL}/${VWORLD_KEY}/Base/{z}/{y}/{x}.png`, {
        attribution: '&copy; VWorld',
        maxZoom: 18,
        minZoom: 6
      }).addTo(map)
    } else {
      // 개발용 OSM 타일 사용
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map)
    }

    // 마커 클러스터 그룹 초기화
    markersRef.current = L.markerClusterGroup({
      chunkedLoading: true,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      maxClusterRadius: 50,
      iconCreateFunction: function(cluster) {
        const childCount = cluster.getChildCount()
        let c = ' marker-cluster-'
        if (childCount < 10) {
          c += 'small'
        } else if (childCount < 100) {
          c += 'medium'
        } else {
          c += 'large'
        }

        return new L.DivIcon({
          html: `<div><span>${childCount}</span></div>`,
          className: 'marker-cluster' + c,
          iconSize: new L.Point(40, 40)
        })
      }
    })

    // 수요 레이어 그룹 초기화
    demandLayerRef.current = L.layerGroup()

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [])

  // 시설 마커 업데이트
  useEffect(() => {
    if (!mapInstanceRef.current || !markersRef.current) return

    const map = mapInstanceRef.current
    const markerCluster = markersRef.current

    // 기존 마커 제거
    markerCluster.clearLayers()

    // 필터링된 시설 데이터
    let filteredFacilities = facilities
    if (selectedFacility !== 'all') {
      const facilityTypeMap: { [key: string]: string } = {
        'swimming': '수영장',
        'gym': '체육관',
        'tennis': '테니스장',
        'football': '축구장',
        'baseball': '야구장',
        'basketball': '농구장',
        'badminton': '배드민턴장',
        'golf': '골프장',
        'park_golf': '파크골프장'
      }
      const targetType = facilityTypeMap[selectedFacility]
      if (targetType) {
        filteredFacilities = filteredFacilities.filter(f => f.type === targetType)
      }
    }

    // 지역 필터링
    if (selectedRegion) {
      filteredFacilities = filteredFacilities.filter(f => f.region === selectedRegion)
    }

    // 마커 추가
    const markers: L.Marker[] = []
    filteredFacilities.forEach(facility => {
      const isHighDemandLowSupply = facility.supplyDemandRatio < 0.8 && facility.demandPercentage > 60
      const isBalanced = facility.supplyDemandRatio >= 0.8 && facility.supplyDemandRatio <= 1.2
      const isOverSupplied = facility.supplyDemandRatio > 1.2

      let iconColor = '#3B82F6' // 기본 파란색
      let statusText = '균형'
      let statusColor = 'blue'

      if (isHighDemandLowSupply) {
        iconColor = '#EF4444' // 빨간색 - 공급 부족
        statusText = '공급 부족'
        statusColor = 'red'
      } else if (isOverSupplied) {
        iconColor = '#10B981' // 초록색 - 공급 충분
        statusText = '공급 충분'
        statusColor = 'green'
      }

      // 시설 타입별 이모지
      const facilityEmoji: { [key: string]: string } = {
        '수영장': '🏊',
        '체육관': '🏟️',
        '테니스장': '🎾',
        '축구장': '⚽',
        '야구장': '⚾',
        '농구장': '🏀',
        '배드민턴장': '🏸',
        '골프장': '⛳',
        '파크골프장': '🏌️'
      }

      // 커스텀 아이콘 생성
      const customIcon = L.divIcon({
        html: `
          <div style="
            background-color: ${iconColor};
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 3px 6px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 14px;
            font-weight: bold;
          ">
            ${facilityEmoji[facility.type] || '🏃'}
          </div>
        `,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15],
        className: `facility-marker-${statusColor}`
      })

      const marker = L.marker([facility.lat, facility.lng], { icon: customIcon })
        .bindPopup(`
          <div style="font-family: system-ui, sans-serif; min-width: 250px;">
            <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold; color: #1f2937;">
              ${facility.name}
            </h3>
            <div style="background: #f3f4f6; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
              <p style="margin: 4px 0; font-size: 13px;"><strong>유형:</strong> ${facility.type}</p>
              <p style="margin: 4px 0; font-size: 13px;"><strong>지역:</strong> ${facility.region}</p>
              ${facility.address ? `<p style="margin: 4px 0; font-size: 13px;"><strong>주소:</strong> ${facility.address}</p>` : ''}
              ${facility.operator ? `<p style="margin: 4px 0; font-size: 13px;"><strong>운영:</strong> ${facility.operator}</p>` : ''}
              ${facility.phone ? `<p style="margin: 4px 0; font-size: 13px;"><strong>연락처:</strong> ${facility.phone}</p>` : ''}
              ${facility.capacity ? `<p style="margin: 4px 0; font-size: 13px;"><strong>수용인원:</strong> ${facility.capacity}명</p>` : ''}
            </div>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
              <p style="margin: 4px 0; font-size: 13px;"><strong>주민 수요:</strong> ${facility.demandPercentage.toFixed(1)}%</p>
              <p style="margin: 4px 0; font-size: 13px;"><strong>공급-수요 비율:</strong> ${facility.supplyDemandRatio.toFixed(2)}</p>
            </div>
            <div style="text-align: center; padding: 6px;">
              <span style="
                color: ${iconColor}; 
                font-weight: bold; 
                background: ${iconColor}15; 
                padding: 4px 12px; 
                border-radius: 16px;
                font-size: 12px;
                border: 1px solid ${iconColor}30;
              ">
                ${statusText}
              </span>
            </div>
          </div>
        `, {
          maxWidth: 300,
          className: 'custom-popup'
        })

      markers.push(marker)
    })

    // 클러스터링 사용 여부에 따라 마커 추가
    if (showClusters) {
      markerCluster.addLayers(markers)
      map.addLayer(markerCluster)
    } else {
      markers.forEach(marker => marker.addTo(map))
    }

  }, [selectedFacility, showClusters, selectedRegion])

  // 히트맵 레이어 업데이트
  useEffect(() => {
    if (!mapInstanceRef.current) return

    const map = mapInstanceRef.current

    // 기존 히트맵 제거
    if (heatmapLayerRef.current) {
      map.removeLayer(heatmapLayerRef.current)
      heatmapLayerRef.current = null
    }

    if (showHeatmap) {
      // 히트맵 데이터 생성 (수요가 높은 지역)
      const heatData = facilities
        .filter(f => f.demandPercentage > 60)
        .map(f => [f.lat, f.lng, f.demandPercentage / 100] as [number, number, number])

      // @ts-ignore - leaflet.heat 타입 정의 문제
      heatmapLayerRef.current = L.heatLayer(heatData, {
        radius: 25,
        blur: 15,
        maxZoom: 10,
        max: 1.0,
        gradient: {
          0.0: 'blue',
          0.25: 'cyan',
          0.5: 'lime',
          0.75: 'yellow',
          1.0: 'red'
        }
      }).addTo(map)
    }
  }, [showHeatmap])

  // 수요 레이어 업데이트
  useEffect(() => {
    if (!mapInstanceRef.current || !demandLayerRef.current) return

    const map = mapInstanceRef.current
    const demandLayer = demandLayerRef.current

    // 기존 레이어 제거
    demandLayer.clearLayers()
    map.removeLayer(demandLayer)

    if (showDemandLayer) {
      // 지역별 수요 서클 추가
      regionDemand.forEach(region => {
        const demandIntensity = region.demandScore / 100
        const fillColor = demandIntensity > 0.7 ? '#EF4444' : 
                         demandIntensity > 0.5 ? '#F59E0B' : '#10B981'
        
        const circle = L.circle([region.lat, region.lng], {
          color: fillColor,
          fillColor: fillColor,
          fillOpacity: 0.3,
          radius: Math.sqrt(region.population) * 10, // 인구 비례 크기
          weight: 2
        }).bindPopup(`
          <div style="font-family: system-ui, sans-serif;">
            <h4 style="margin: 0 0 8px 0; font-weight: bold;">${region.region}</h4>
            <p style="margin: 4px 0; font-size: 13px;"><strong>수요 점수:</strong> ${region.demandScore}점</p>
            <p style="margin: 4px 0; font-size: 13px;"><strong>시설 수:</strong> ${region.facilityCount.toLocaleString()}개</p>
            <p style="margin: 4px 0; font-size: 13px;"><strong>인구:</strong> ${region.population.toLocaleString()}명</p>
            <p style="margin: 4px 0; font-size: 13px;"><strong>1인당 시설:</strong> ${region.facilityPerCapita.toFixed(2)}개</p>
          </div>
        `)

        circle.on('click', () => {
          if (onRegionSelect) {
            onRegionSelect(region.region)
          }
        })

        demandLayer.addLayer(circle)
      })

      map.addLayer(demandLayer)
    }
  }, [showDemandLayer, regionDemand, onRegionSelect])

  return (
    <>
      <div 
        ref={mapRef} 
        className="h-[500px] w-full rounded-lg border relative"
        style={{ minHeight: '500px' }}
      />
      {isLoading && (
        <div className="absolute inset-0 bg-white/80 flex items-center justify-center rounded-lg">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">데이터 로딩 중...</p>
          </div>
        </div>
      )}
      <style jsx global>{`
        .marker-cluster-small {
          background-color: rgba(181, 226, 140, 0.6);
        }
        .marker-cluster-small div {
          background-color: rgba(110, 204, 57, 0.6);
        }
        .marker-cluster-medium {
          background-color: rgba(241, 211, 87, 0.6);
        }
        .marker-cluster-medium div {
          background-color: rgba(240, 194, 12, 0.6);
        }
        .marker-cluster-large {
          background-color: rgba(253, 156, 115, 0.6);
        }
        .marker-cluster-large div {
          background-color: rgba(241, 128, 23, 0.6);
        }
        .marker-cluster {
          background-clip: padding-box;
          border-radius: 20px;
        }
        .marker-cluster div {
          width: 30px;
          height: 30px;
          margin-left: 5px;
          margin-top: 5px;
          text-align: center;
          border-radius: 15px;
          font: 12px "Helvetica Neue", Arial, Helvetica, sans-serif;
          color: white;
          font-weight: bold;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .marker-cluster span {
          line-height: 30px;
        }
        .leaflet-popup-content-wrapper {
          border-radius: 12px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .leaflet-popup-content {
          margin: 12px !important;
        }
      `}</style>
    </>
  )
}
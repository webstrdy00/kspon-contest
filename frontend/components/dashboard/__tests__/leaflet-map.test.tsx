// @ts-nocheck
import React from 'react'
import { render } from '@testing-library/react'
import { LeafletMap } from '../leaflet-map'
import { afterEach, expect, test, vi } from 'vitest'

vi.mock('leaflet', () => {
  const mapInstance = {
    eachLayer: vi.fn(),
    removeLayer: vi.fn(),
    addLayer: vi.fn(),
    remove: vi.fn()
  }
  const heatLayerInstance = { addTo: vi.fn() }
  heatLayerInstance.addTo.mockReturnValue(heatLayerInstance)
  const demandLayerInstance = {
    addLayer: vi.fn(),
    clearLayers: vi.fn()
  }
  const defaultIcon = function () {}
  defaultIcon.prototype = {}
  defaultIcon.mergeOptions = vi.fn()
  const leafletMock = {
    map: vi.fn(() => mapInstance),
    tileLayer: vi.fn(() => ({ addTo: vi.fn() })),
    marker: vi.fn(() => ({ bindPopup: vi.fn().mockReturnValue({ addTo: vi.fn() }) })),
    Marker: class {},
    divIcon: vi.fn(() => ({})),
    heatLayer: vi.fn(() => heatLayerInstance),
    circle: vi.fn(() => ({ bindPopup: vi.fn().mockReturnValue({}) })),
    layerGroup: vi.fn(() => demandLayerInstance),
    Icon: { Default: defaultIcon },
    __mapInstance: mapInstance,
    __heatLayerInstance: heatLayerInstance,
    __demandLayerInstance: demandLayerInstance,
  }
  return { default: leafletMock }
})
vi.mock('leaflet/dist/leaflet.css', () => ({}))
vi.mock('leaflet.heat', () => ({}))

import L from 'leaflet'

afterEach(() => {
  vi.clearAllMocks()
})

test('toggles heatmap layer based on showHeatmap', () => {
  const { rerender } = render(<LeafletMap selectedFacility="all" showDemandLayer={false} showHeatmap={false} />)

  rerender(<LeafletMap selectedFacility="all" showDemandLayer={false} showHeatmap={true} />)
  expect(L.heatLayer).toHaveBeenCalled()
  expect(L.__heatLayerInstance.addTo).toHaveBeenCalledWith(L.__mapInstance)

  L.__mapInstance.removeLayer.mockClear()
  rerender(<LeafletMap selectedFacility="all" showDemandLayer={false} showHeatmap={false} />)
  expect(L.__mapInstance.removeLayer).toHaveBeenCalledWith(L.__heatLayerInstance)
})

test('toggles demand layer based on showDemandLayer', () => {
  const { rerender } = render(<LeafletMap selectedFacility="all" showDemandLayer={false} showHeatmap={false} />)

  rerender(<LeafletMap selectedFacility="all" showDemandLayer={true} showHeatmap={false} />)
  expect(L.circle).toHaveBeenCalled()
  expect(L.__mapInstance.addLayer).toHaveBeenCalledWith(L.__demandLayerInstance)

  L.__mapInstance.removeLayer.mockClear()
  rerender(<LeafletMap selectedFacility="all" showDemandLayer={false} showHeatmap={false} />)
  expect(L.__mapInstance.removeLayer).toHaveBeenCalledWith(L.__demandLayerInstance)
})
import { useEffect, useRef, useState, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
import cytoscape from 'cytoscape'
import {
  MagnifyingGlassPlusIcon,
  MagnifyingGlassMinusIcon,
  ArrowsPointingOutIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline'
import { assetService, AssetGraph } from '@/services/assetService'
import Button from '@/components/common/Button'
import Loading from '@/components/common/Loading'

interface GraphViewerProps {
  projectId: number
}

const CATEGORY_COLORS: Record<string, string> = {
  hardware: '#10b981', // green
  software: '#8b5cf6', // purple
  data: '#f59e0b', // amber
  interface: '#3b82f6', // blue
  function: '#ec4899', // pink
  default: '#6b7280', // gray
}

const EDGE_COLORS: Record<string, string> = {
  contains: '#9ca3af',
  communicates: '#3b82f6',
  depends: '#f59e0b',
  accesses: '#10b981',
  default: '#d1d5db',
}

export default function GraphViewer({ projectId }: GraphViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const cyRef = useRef<cytoscape.Core | null>(null)
  const [selectedNode, setSelectedNode] = useState<any>(null)
  const [layout, setLayout] = useState<'cose' | 'circle' | 'grid' | 'breadthfirst'>('cose')

  const { data: graphData, isLoading } = useQuery({
    queryKey: ['asset-graph', projectId],
    queryFn: () => assetService.getGraph(projectId),
  })

  const initCytoscape = useCallback((data: AssetGraph) => {
    if (!containerRef.current) return

    // Prepare elements
    const elements = [
      ...data.nodes.map((node) => ({
        data: {
          id: node.id,
          label: node.name,
          category: node.category,
          subcategory: node.subcategory,
        },
      })),
      ...data.edges.map((edge, idx) => ({
        data: {
          id: `e${idx}`,
          source: edge.source,
          target: edge.target,
          label: edge.type,
          protocol: edge.protocol,
        },
      })),
    ]

    // Initialize Cytoscape
    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (ele: any) =>
              CATEGORY_COLORS[ele.data('category')] || CATEGORY_COLORS.default,
            label: 'data(label)',
            color: '#1f2937',
            'text-valign': 'bottom',
            'text-margin-y': 8,
            'font-size': 12,
            width: 40,
            height: 40,
            'border-width': 2,
            'border-color': '#ffffff',
            'text-wrap': 'wrap',
            'text-max-width': 80,
          } as any,
        },
        {
          selector: 'node:selected',
          style: {
            'border-color': '#3b82f6',
            'border-width': 3,
            'background-color': '#dbeafe',
          },
        },
        {
          selector: 'edge',
          style: {
            width: 2,
            'line-color': (ele: any) =>
              EDGE_COLORS[ele.data('label')] || EDGE_COLORS.default,
            'target-arrow-color': (ele: any) =>
              EDGE_COLORS[ele.data('label')] || EDGE_COLORS.default,
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            label: 'data(label)',
            'font-size': 10,
            'text-rotation': 'autorotate',
            'text-margin-y': -10,
            color: '#6b7280',
          } as any,
        },
        {
          selector: 'edge:selected',
          style: {
            'line-color': '#3b82f6',
            'target-arrow-color': '#3b82f6',
            width: 3,
          },
        },
      ],
      layout: {
        name: layout,
        animate: true,
        fit: true,
        padding: 50,
      },
      minZoom: 0.2,
      maxZoom: 3,
    })

    // Event handlers
    cy.on('tap', 'node', (evt) => {
      const node = evt.target
      setSelectedNode({
        id: node.id(),
        ...node.data(),
      })
    })

    cy.on('tap', (evt) => {
      if (evt.target === cy) {
        setSelectedNode(null)
      }
    })

    cyRef.current = cy

    return () => {
      cy.destroy()
    }
  }, [layout])

  useEffect(() => {
    if (graphData && graphData.nodes.length > 0) {
      initCytoscape(graphData)
    }
  }, [graphData, initCytoscape])

  const handleZoomIn = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() * 1.2)
    }
  }

  const handleZoomOut = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() / 1.2)
    }
  }

  const handleFit = () => {
    if (cyRef.current) {
      cyRef.current.fit(undefined, 50)
    }
  }

  const handleRefreshLayout = () => {
    if (cyRef.current) {
      cyRef.current.layout({ name: layout, animate: true, fit: true, padding: 50 }).run()
    }
  }

  if (isLoading) {
    return <Loading text="加载知识图谱..." />
  }

  if (!graphData || graphData.nodes.length === 0) {
    return (
      <div className="h-96 flex items-center justify-center text-gray-500 border border-gray-200 rounded-lg">
        <div className="text-center">
          <p>暂无资产关系数据</p>
          <p className="text-sm mt-2">请先完成资产识别</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleZoomIn}
            leftIcon={<MagnifyingGlassPlusIcon className="h-4 w-4" />}
          >
            放大
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleZoomOut}
            leftIcon={<MagnifyingGlassMinusIcon className="h-4 w-4" />}
          >
            缩小
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleFit}
            leftIcon={<ArrowsPointingOutIcon className="h-4 w-4" />}
          >
            适应
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleRefreshLayout}
            leftIcon={<ArrowPathIcon className="h-4 w-4" />}
          >
            重排
          </Button>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">布局:</span>
          <select
            value={layout}
            onChange={(e) => setLayout(e.target.value as any)}
            className="rounded-md border-gray-300 text-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="cose">力导向</option>
            <option value="circle">圆形</option>
            <option value="grid">网格</option>
            <option value="breadthfirst">层次</option>
          </select>
        </div>
      </div>

      {/* Graph container */}
      <div className="relative border border-gray-200 rounded-lg bg-gray-50">
        <div ref={containerRef} className="h-[500px]" />

        {/* Legend */}
        <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow p-3">
          <h4 className="text-xs font-medium text-gray-700 mb-2">图例</h4>
          <div className="space-y-1">
            {Object.entries(CATEGORY_COLORS)
              .filter(([key]) => key !== 'default')
              .map(([category, color]) => (
                <div key={category} className="flex items-center text-xs">
                  <div
                    className="w-3 h-3 rounded-full mr-2"
                    style={{ backgroundColor: color }}
                  />
                  <span className="capitalize">{category}</span>
                </div>
              ))}
          </div>
        </div>

        {/* Selected node info */}
        {selectedNode && (
          <div className="absolute top-4 right-4 bg-white rounded-lg shadow p-4 max-w-xs">
            <h4 className="font-medium text-gray-900">{selectedNode.label}</h4>
            <dl className="mt-2 space-y-1 text-sm">
              <div className="flex">
                <dt className="text-gray-500 w-16">ID:</dt>
                <dd className="text-gray-900 font-mono">{selectedNode.id}</dd>
              </div>
              <div className="flex">
                <dt className="text-gray-500 w-16">分类:</dt>
                <dd className="text-gray-900 capitalize">{selectedNode.category}</dd>
              </div>
              {selectedNode.subcategory && (
                <div className="flex">
                  <dt className="text-gray-500 w-16">子分类:</dt>
                  <dd className="text-gray-900">{selectedNode.subcategory}</dd>
                </div>
              )}
            </dl>
          </div>
        )}
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-2xl font-bold text-gray-900">
            {graphData.nodes.length}
          </div>
          <div className="text-sm text-gray-500">资产节点</div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-2xl font-bold text-gray-900">
            {graphData.edges.length}
          </div>
          <div className="text-sm text-gray-500">关系边</div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-2xl font-bold text-gray-900">
            {new Set(graphData.nodes.map((n) => n.category)).size}
          </div>
          <div className="text-sm text-gray-500">资产类别</div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-2xl font-bold text-gray-900">
            {new Set(graphData.edges.map((e) => e.type)).size}
          </div>
          <div className="text-sm text-gray-500">关系类型</div>
        </div>
      </div>
    </div>
  )
}

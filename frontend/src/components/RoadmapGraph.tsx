import { useState } from 'react'
import {
  Background,
  Controls,
  MarkerType,
  Position,
  ReactFlow,
  type Edge as ReactFlowEdge,
  type Node as ReactFlowNode,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import './RoadmapGraph.css'
import type { CourseNode, RoadmapEdge } from '../types/roadmap'

interface RoadmapGraphProps {
  courses: CourseNode[]
  prerequisiteLinks: RoadmapEdge[]
}

function getCourseAccent(type: string) {
  if (type === 'Core') {
    return '#38bdf8'
  }

  if (type === 'Common-Core') {
    return '#a78bfa'
  }

  return '#94a3b8'
}

function RoadmapGraph({ courses, prerequisiteLinks }: RoadmapGraphProps) {
  const [hoveredCourseId, setHoveredCourseId] = useState<string | null>(null)
  const groupCounts = new Map<string, number>()
  const connectedCourseIds = new Set<string>()

  if (hoveredCourseId) {
    connectedCourseIds.add(hoveredCourseId)

    prerequisiteLinks.forEach((link) => {
      if (link.source === hoveredCourseId || link.target === hoveredCourseId) {
        connectedCourseIds.add(link.source)
        connectedCourseIds.add(link.target)
      }
    })
  }

  // Give each course a graph position.
  // Same year/semester = same column, later courses go lower.
  const graphNodes: ReactFlowNode[] = courses.map((course) => {
    const columnIndex = (course.year - 1) * 2 + (course.semester - 1)
    const groupKey = `${course.year}-${course.semester}`
    const rowIndex = groupCounts.get(groupKey) ?? 0
    const accent = getCourseAccent(course.type)
    const isHovered = hoveredCourseId === course.id
    const isDimmed = Boolean(hoveredCourseId) && !connectedCourseIds.has(course.id)

    groupCounts.set(groupKey, rowIndex + 1)

    // Returns 1 graph-node for 1 course
    return {
      id: course.id,
      position: {
        x: columnIndex * 320,
        y: rowIndex * 140,
      },
      data: {
        label: `${course.courseCode} - ${course.academicUnits} AU\n${course.title}`,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
      style: {
        width: 220,
        padding: 10,
        background: '#0f172a',
        borderColor: isHovered ? '#22d3ee' : accent,
        borderRadius: 8,
        boxShadow: isHovered
          ? '0 0 0 2px rgba(34, 211, 238, 0.38), 0 18px 42px rgba(34, 211, 238, 0.18)'
          : '0 16px 34px rgba(0, 0, 0, 0.28)',
        color: '#e5eefb',
        fontSize: 12,
        lineHeight: 1.35,
        opacity: isDimmed ? 0.25 : 1,
        whiteSpace: 'pre-line',
      },
    }
  })

  // Create graph edges between courses based on prerequisite links
  const graphEdges: ReactFlowEdge[] = prerequisiteLinks.map((link) => {
    const isHighlighted =
      hoveredCourseId === link.source || hoveredCourseId === link.target
    const isDimmed = Boolean(hoveredCourseId) && !isHighlighted

    return {
      id: `${link.source}-${link.target}`,
      source: link.source,
      target: link.target,
      type: 'smoothstep',
      animated: isHighlighted,
      pathOptions: {
        borderRadius: 24,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: isHighlighted ? '#22d3ee' : '#94a3b8',
      },
      style: {
        opacity: isDimmed ? 0.08 : 1,
        stroke: isHighlighted ? '#22d3ee' : '#94a3b8',
        strokeWidth: isHighlighted ? 3 : 2,
      },
    }
  })

  return (
    <section className="roadmap-graph-section">
      <h2>Roadmap Graph</h2>
      <div className="roadmap-graph">
        <ReactFlow
          nodes={graphNodes}
          edges={graphEdges}
          fitView
          onNodeMouseEnter={(_, node) => setHoveredCourseId(node.id)}
          onNodeMouseLeave={() => setHoveredCourseId(null)}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </section>
  )
}

export default RoadmapGraph

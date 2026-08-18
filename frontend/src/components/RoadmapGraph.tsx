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

function RoadmapGraph({ courses, prerequisiteLinks }: RoadmapGraphProps) {
  const groupCounts = new Map<string, number>()

  // Give each course a graph position.
  // Same year/semester = same column, later courses go lower.
  const graphNodes: ReactFlowNode[] = courses.map((course) => {
    const columnIndex = (course.year - 1) * 2 + (course.semester - 1)
    const groupKey = `${course.year}-${course.semester}`
    const rowIndex = groupCounts.get(groupKey) ?? 0

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
        background: '#ffffff',
        borderColor: '#2563eb',
        borderRadius: 8,
        boxShadow: '0 12px 28px rgba(37, 99, 235, 0.14)',
        color: '#111827',
        fontSize: 12,
        lineHeight: 1.35,
        whiteSpace: 'pre-line',
      },
    }
  })

  // Create graph edges between courses based on prerequisite links
  const graphEdges: ReactFlowEdge[] = prerequisiteLinks.map((link) => ({
    id: `${link.source}-${link.target}`,
    source: link.source,
    target: link.target,
    type: 'smoothstep',
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
    style: {
      stroke: '#64748b',
      strokeWidth: 2,
    },
  }))

  return (
    <section className="roadmap-graph-section">
      <h2>Roadmap Graph</h2>
      <div className="roadmap-graph">
        <ReactFlow nodes={graphNodes} edges={graphEdges} fitView>
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </section>
  )
}

export default RoadmapGraph

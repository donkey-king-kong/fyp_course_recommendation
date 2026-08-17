import type { RoadmapResponse } from '../types/roadmap'

const ROADMAP_API_URL = 'http://127.0.0.1:8000/roadmap'

export async function fetchRoadmap(): Promise<RoadmapResponse> {
  const response = await fetch(ROADMAP_API_URL)

  if (!response.ok) {
    throw new Error('Failed to load roadmap data')
  }

  return response.json() as Promise<RoadmapResponse>
}

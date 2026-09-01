import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CurriculumGuideResponse } from '../types/curriculum'
import type { CourseRecommendation } from '../types/recommendation'
import type {
  TranscriptCourse,
  TranscriptCurriculumMatchResponse,
  TranscriptMatchedCourse,
} from '../types/transcript'

export type RoadmapRecommendationStaleReason =
  | 'curriculum-guide'
  | 'transcript'
  | 'completed-courses'

export interface StudentProfile {
  studentId: string
  // CSC is the only supported major currently
  // More majors can be added here once the roadmap data supports them.
  major: 'CSC'
  careerGoal: string
  preferredRecommendationTags: string[]
}

interface SavedStudentProfile {
  profile: StudentProfile
  completedCourseIds: string[] // Checked roadmap course IDs.
  curriculumGuide: CurriculumGuideResponse | null // Uploaded roadmap data.
  curriculumGuideFileName: string // Uploaded guide filename.
  transcriptFileName: string // Uploaded transcript filename.
  transcriptCompletedCourseCodes: string[] // All completed transcript codes.
  transcriptCompletedCourses: TranscriptCourse[] // All completed transcript rows with term metadata.
  transcriptCompletedCourseCount: number // Total completed transcript modules.
  transcriptTotalAcademicUnitsEarned: number // Total AU earned from transcript.
  transcriptUnmatchedCourseCount: number // Transcript modules outside roadmap.
  transcriptMatchedCourses: TranscriptMatchedCourse[] // Transcript modules found in roadmap.
  transcriptUnmatchedCourseCodes: string[] // Transcript codes outside roadmap.
  isTranscriptAppliedToRoadmap: boolean // Whether saved transcript data is currently applied to the roadmap.
  roadmapRecommendations: CourseRecommendation[] // Last loaded recommendation results.
  roadmapRecommendationStaleReasons: RoadmapRecommendationStaleReason[] // Changed inputs since recommendations loaded.
}

// Reuse these defaults before anyone logs in and after logout
const DEFAULT_PROFILE: StudentProfile = {
  studentId: '',
  major: 'CSC',
  careerGoal: '',
  preferredRecommendationTags: [],
}

interface ProfileState {
  activeStudentId: string
  profilesByStudentId: Record<string, SavedStudentProfile>
  profile: StudentProfile
  completedCourseIds: string[] // Checked roadmap course IDs.
  curriculumGuide: CurriculumGuideResponse | null // Active uploaded roadmap.
  curriculumGuideFileName: string // Active guide filename.
  transcriptFileName: string // Active transcript filename.
  transcriptCompletedCourseCodes: string[] // All completed transcript codes.
  transcriptCompletedCourses: TranscriptCourse[] // All completed transcript rows with term metadata.
  transcriptCompletedCourseCount: number // Total completed transcript modules.
  transcriptTotalAcademicUnitsEarned: number // Total AU earned from transcript.
  transcriptUnmatchedCourseCount: number // Transcript modules outside roadmap.
  transcriptMatchedCourses: TranscriptMatchedCourse[] // Transcript modules found in roadmap.
  transcriptUnmatchedCourseCodes: string[] // Transcript codes outside roadmap.
  isTranscriptAppliedToRoadmap: boolean // Whether transcript effects are active on the roadmap.
  roadmapRecommendations: CourseRecommendation[] // Last loaded recommendation results.
  roadmapRecommendationStaleReasons: RoadmapRecommendationStaleReason[] // Changed inputs since recommendations loaded.
  loginWithStudentId: (studentId: string) => void // Load or create profile.
  updateProfile: (updates: Partial<StudentProfile>) => void // Save profile fields.
  toggleCourseCompletion: (courseId: string) => void // Toggle one roadmap checkbox.
  setCompletedCourses: (courseIds: string[]) => void // Replace checked roadmap IDs.
  setCurriculumGuide: (
    curriculumGuide: CurriculumGuideResponse,
    fileName: string,
    transcriptMatch?: TranscriptCurriculumMatchResponse,
  ) => void // Save guide.
  clearCurriculumGuide: () => void // Remove uploaded guide only.
  setRoadmapRecommendations: (recommendations: CourseRecommendation[]) => void // Save results.
  clearRoadmapRecommendations: () => void // Remove saved results.
  setTranscriptResults: (
    fileName: string,
    completedCourseCodes: string[],
    transcriptCompletedCourses: TranscriptCourse[],
    transcriptCompletedCourseCount: number,
    transcriptTotalAcademicUnitsEarned: number,
    transcriptMatch?: TranscriptCurriculumMatchResponse,
  ) => void // Save transcript results.
  clearAppliedTranscriptFromRoadmap: () => void // Remove transcript effects while keeping parsed transcript saved.
  clearTranscriptResults: () => void // Remove uploaded transcript data.
  logout: () => void // End active browser session.
}

function normalizeStudentId(studentId: string) {
  // Normalize studentIDs
  return studentId.trim().toUpperCase()
}

// Create the default profile values for a new Student ID.
// This keeps new users consistent with the same starting year, semester, and major
function createStudentProfile(studentId: string): StudentProfile {
  return {
    ...DEFAULT_PROFILE,
    studentId,
  }
}

function hydrateStudentProfile(profile: Partial<StudentProfile> | undefined, studentId: string): StudentProfile {
  return {
    studentId,
    major: profile?.major ?? DEFAULT_PROFILE.major,
    careerGoal: profile?.careerGoal ?? DEFAULT_PROFILE.careerGoal,
    preferredRecommendationTags:
      profile?.preferredRecommendationTags ?? DEFAULT_PROFILE.preferredRecommendationTags,
  }
}

// Create the full browser-saved record for one Student ID
// It includes profile details, roadmap completion state, and transcript upload stats.
function createSavedStudentProfile(studentId: string): SavedStudentProfile {
  return {
    profile: createStudentProfile(studentId),
    completedCourseIds: [],
    curriculumGuide: null,
    curriculumGuideFileName: '',
    transcriptFileName: '',
    transcriptCompletedCourseCodes: [],
    transcriptCompletedCourses: [],
    transcriptCompletedCourseCount: 0,
    transcriptTotalAcademicUnitsEarned: 0,
    transcriptUnmatchedCourseCount: 0,
    transcriptMatchedCourses: [],
    transcriptUnmatchedCourseCodes: [],
    isTranscriptAppliedToRoadmap: false,
    roadmapRecommendations: [],
    roadmapRecommendationStaleReasons: [],
  }
}

function createEmptyTranscriptMatch(): TranscriptCurriculumMatchResponse {
  return {
    completedCourseIds: [],
    transcriptMatchedCourses: [],
    transcriptUnmatchedCourseCodes: [],
  }
}

function getUpdatedStaleReasons(
  currentReasons: RoadmapRecommendationStaleReason[],
  changedReason: RoadmapRecommendationStaleReason,
  hasRecommendations: boolean,
) {
  if (!hasRecommendations) {
    return []
  }

  return [...new Set([...currentReasons, changedReason])]
}

export const useProfileStore = create<ProfileState>()(
  // persist saves this store to browser localStorage under the name below
  persist(
    (set) => ({
      activeStudentId: '',
      profilesByStudentId: {},
      profile: DEFAULT_PROFILE,
      completedCourseIds: [],
      curriculumGuide: null,
      curriculumGuideFileName: '',
      transcriptFileName: '',
      transcriptCompletedCourseCodes: [],
      transcriptCompletedCourses: [],
      transcriptCompletedCourseCount: 0,
      transcriptTotalAcademicUnitsEarned: 0,
      transcriptUnmatchedCourseCount: 0,
      transcriptMatchedCourses: [],
      transcriptUnmatchedCourseCodes: [],
      isTranscriptAppliedToRoadmap: false,
      roadmapRecommendations: [],
      roadmapRecommendationStaleReasons: [],

      loginWithStudentId: (studentId) =>
        set((state) => {
          // Use one consistent ID format as the lookup key
          const normalizedStudentId = normalizeStudentId(studentId)

          // Load saved profile if it exists
          const savedProfile = state.profilesByStudentId[normalizedStudentId]

          // Use the saved profile if it exists; otherwise start a new profile for this ID
          const activeProfile = savedProfile ?? createSavedStudentProfile(normalizedStudentId)
          const activeStudentProfile = hydrateStudentProfile(activeProfile.profile, normalizedStudentId)
          const hydratedProfile = {
            profile: activeStudentProfile,
            curriculumGuide: activeProfile.curriculumGuide ?? null,
            curriculumGuideFileName: activeProfile.curriculumGuideFileName ?? '',
            transcriptFileName: activeProfile.transcriptFileName ?? '',
            transcriptCompletedCourseCodes: activeProfile.transcriptCompletedCourseCodes ?? [],
            transcriptCompletedCourses: activeProfile.transcriptCompletedCourses ?? [],
            transcriptCompletedCourseCount: activeProfile.transcriptCompletedCourseCount ?? 0,
            transcriptTotalAcademicUnitsEarned:
              activeProfile.transcriptTotalAcademicUnitsEarned ?? 0,
            transcriptUnmatchedCourseCount: activeProfile.transcriptUnmatchedCourseCount ?? 0,
            transcriptMatchedCourses: activeProfile.transcriptMatchedCourses ?? [],
            transcriptUnmatchedCourseCodes: activeProfile.transcriptUnmatchedCourseCodes ?? [],
            isTranscriptAppliedToRoadmap: activeProfile.isTranscriptAppliedToRoadmap ?? false,
            roadmapRecommendations: activeProfile.roadmapRecommendations ?? [],
            roadmapRecommendationStaleReasons:
              activeProfile.roadmapRecommendationStaleReasons ?? [],
          }
          const completedCourseIds = hydratedProfile.curriculumGuide
            ? activeProfile.completedCourseIds ?? []
            : []

          return {
            // Controls whether the app shows login page or roadmap
            activeStudentId: normalizedStudentId,
            profile: hydratedProfile.profile,
            completedCourseIds,
            curriculumGuide: hydratedProfile.curriculumGuide,
            curriculumGuideFileName: hydratedProfile.curriculumGuideFileName,
            transcriptFileName: hydratedProfile.transcriptFileName,
            transcriptCompletedCourseCodes: hydratedProfile.transcriptCompletedCourseCodes,
            transcriptCompletedCourses: hydratedProfile.transcriptCompletedCourses,
            transcriptCompletedCourseCount: hydratedProfile.transcriptCompletedCourseCount,
            transcriptTotalAcademicUnitsEarned:
              hydratedProfile.transcriptTotalAcademicUnitsEarned,
            transcriptUnmatchedCourseCount: hydratedProfile.transcriptUnmatchedCourseCount,
            transcriptMatchedCourses: hydratedProfile.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: hydratedProfile.transcriptUnmatchedCourseCodes,
            isTranscriptAppliedToRoadmap: hydratedProfile.isTranscriptAppliedToRoadmap,
            roadmapRecommendations: hydratedProfile.roadmapRecommendations,
            roadmapRecommendationStaleReasons:
              hydratedProfile.roadmapRecommendationStaleReasons,
            // Store the active profile back into the map so it persists under this Student ID
            profilesByStudentId: {
              ...state.profilesByStudentId,
              [normalizedStudentId]: {
                ...hydratedProfile,
                completedCourseIds,
              },
            },
          }
        }),

      updateProfile: (updates) =>
        set((state) => {
          const studentId =
            updates.studentId === undefined
              ? state.profile.studentId
              : normalizeStudentId(updates.studentId)
          const nextProfile = hydrateStudentProfile({ ...state.profile, ...updates }, studentId)
          const nextProfilesByStudentId = { ...state.profilesByStudentId }
          const shouldClearRoadmapRecommendations =
            updates.major !== undefined ||
            updates.careerGoal !== undefined ||
            updates.preferredRecommendationTags !== undefined
          const nextRoadmapRecommendations = shouldClearRoadmapRecommendations
            ? []
            : state.roadmapRecommendations

          if (state.activeStudentId && state.activeStudentId !== nextProfile.studentId) {
            delete nextProfilesByStudentId[state.activeStudentId]
          }

          if (nextProfile.studentId) {
            nextProfilesByStudentId[nextProfile.studentId] = {
              profile: nextProfile,
              completedCourseIds: state.completedCourseIds,
              curriculumGuide: state.curriculumGuide,
              curriculumGuideFileName: state.curriculumGuideFileName,
              transcriptFileName: state.transcriptFileName,
              transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
              transcriptCompletedCourses: state.transcriptCompletedCourses,
              transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
              transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
              transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
              transcriptMatchedCourses: state.transcriptMatchedCourses,
              transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
              isTranscriptAppliedToRoadmap: state.isTranscriptAppliedToRoadmap,
              roadmapRecommendations: nextRoadmapRecommendations,
              roadmapRecommendationStaleReasons: shouldClearRoadmapRecommendations
                ? []
                : state.roadmapRecommendationStaleReasons,
            }
          }

          return {
            activeStudentId: nextProfile.studentId,
            profile: nextProfile,
            roadmapRecommendations: nextRoadmapRecommendations,
            roadmapRecommendationStaleReasons: shouldClearRoadmapRecommendations
              ? []
              : state.roadmapRecommendationStaleReasons,
            profilesByStudentId: nextProfilesByStudentId,
          }
        }),

      toggleCourseCompletion: (courseId) =>
        set((state) => {
          const isCompleted = state.completedCourseIds.includes(courseId)
          const nextCompletedCourseIds = isCompleted
            ? state.completedCourseIds.filter((id) => id !== courseId)
            : [...state.completedCourseIds, courseId]
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'completed-courses',
            state.roadmapRecommendations.length > 0,
          )

          return {
            completedCourseIds: nextCompletedCourseIds,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: nextCompletedCourseIds,
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                    transcriptMatchedCourses: state.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                    isTranscriptAppliedToRoadmap: state.isTranscriptAppliedToRoadmap,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      setCompletedCourses: (courseIds) =>
        set((state) => {
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'completed-courses',
            state.roadmapRecommendations.length > 0,
          )

          return {
            completedCourseIds: courseIds,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: courseIds,
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                    transcriptMatchedCourses: state.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                    isTranscriptAppliedToRoadmap: state.isTranscriptAppliedToRoadmap,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      setCurriculumGuide: (curriculumGuide, fileName, transcriptMatch) =>
        set((state) => {
          const matchedResults = transcriptMatch ?? createEmptyTranscriptMatch()
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'curriculum-guide',
            state.roadmapRecommendations.length > 0,
          )

          return {
            curriculumGuide,
            curriculumGuideFileName: fileName,
            completedCourseIds: matchedResults.completedCourseIds,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            transcriptUnmatchedCourseCount: matchedResults.transcriptUnmatchedCourseCodes.length,
            transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
            isTranscriptAppliedToRoadmap: Boolean(transcriptMatch),
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: matchedResults.completedCourseIds,
                    curriculumGuide,
                    curriculumGuideFileName: fileName,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
                    isTranscriptAppliedToRoadmap: Boolean(transcriptMatch),
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      clearCurriculumGuide: () =>
        set((state) => ({
          curriculumGuide: null,
          curriculumGuideFileName: '',
          completedCourseIds: [],
          transcriptMatchedCourses: [],
          transcriptUnmatchedCourseCodes: state.transcriptCompletedCourseCodes,
          transcriptUnmatchedCourseCount: state.transcriptCompletedCourseCodes.length,
          isTranscriptAppliedToRoadmap: false,
          roadmapRecommendations: [],
          roadmapRecommendationStaleReasons: [],
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: [],
                  curriculumGuide: null,
                  curriculumGuideFileName: '',
                  roadmapRecommendations: [],
                  roadmapRecommendationStaleReasons: [],
                  transcriptFileName: state.transcriptFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourses: state.transcriptCompletedCourses,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                  transcriptUnmatchedCourseCount: state.transcriptCompletedCourseCodes.length,
                  transcriptMatchedCourses: [],
                  transcriptUnmatchedCourseCodes: state.transcriptCompletedCourseCodes,
                  isTranscriptAppliedToRoadmap: false,
                },
              }
            : state.profilesByStudentId,
        })),

      setRoadmapRecommendations: (recommendations) =>
        set((state) => ({
          roadmapRecommendations: recommendations,
          roadmapRecommendationStaleReasons: [],
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: state.completedCourseIds,
                  curriculumGuide: state.curriculumGuide,
                  curriculumGuideFileName: state.curriculumGuideFileName,
                  roadmapRecommendations: recommendations,
                  roadmapRecommendationStaleReasons: [],
                  transcriptFileName: state.transcriptFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourses: state.transcriptCompletedCourses,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                  transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                  transcriptMatchedCourses: state.transcriptMatchedCourses,
                  transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                  isTranscriptAppliedToRoadmap: state.isTranscriptAppliedToRoadmap,
                },
              }
            : state.profilesByStudentId,
        })),

      clearRoadmapRecommendations: () =>
        set((state) => ({
          roadmapRecommendations: [],
          roadmapRecommendationStaleReasons: [],
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: state.completedCourseIds,
                  curriculumGuide: state.curriculumGuide,
                  curriculumGuideFileName: state.curriculumGuideFileName,
                  roadmapRecommendations: [],
                  roadmapRecommendationStaleReasons: [],
                  transcriptFileName: state.transcriptFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourses: state.transcriptCompletedCourses,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                  transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                  transcriptMatchedCourses: state.transcriptMatchedCourses,
                  transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                  isTranscriptAppliedToRoadmap: state.isTranscriptAppliedToRoadmap,
                },
              }
            : state.profilesByStudentId,
        })),

      setTranscriptResults: (
        fileName,
        completedCourseCodes,
        transcriptCompletedCourses,
        transcriptCompletedCourseCount,
        transcriptTotalAcademicUnitsEarned,
        transcriptMatch,
      ) =>
        set((state) => {
          const matchedResults = transcriptMatch ?? createEmptyTranscriptMatch()
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'transcript',
            state.roadmapRecommendations.length > 0,
          )

          return {
            completedCourseIds: matchedResults.completedCourseIds,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            transcriptFileName: fileName,
            transcriptCompletedCourseCodes: completedCourseCodes,
            transcriptCompletedCourses,
            transcriptCompletedCourseCount,
            transcriptTotalAcademicUnitsEarned,
            transcriptUnmatchedCourseCount: matchedResults.transcriptUnmatchedCourseCodes.length,
            transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
            isTranscriptAppliedToRoadmap: true,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: matchedResults.completedCourseIds,
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                    transcriptFileName: fileName,
                    transcriptCompletedCourseCodes: completedCourseCodes,
                    transcriptCompletedCourses,
                    transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
                    isTranscriptAppliedToRoadmap: true,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      clearAppliedTranscriptFromRoadmap: () =>
        set((state) => {
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'transcript',
            state.roadmapRecommendations.length > 0,
          )

          return {
            completedCourseIds: [],
            transcriptUnmatchedCourseCount: 0,
            transcriptMatchedCourses: [],
            transcriptUnmatchedCourseCodes: [],
            isTranscriptAppliedToRoadmap: false,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: [],
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount: 0,
                    transcriptMatchedCourses: [],
                    transcriptUnmatchedCourseCodes: [],
                    isTranscriptAppliedToRoadmap: false,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      clearTranscriptResults: () =>
        set((state) => {
          const nextStaleReasons = getUpdatedStaleReasons(
            state.roadmapRecommendationStaleReasons,
            'transcript',
            state.roadmapRecommendations.length > 0,
          )

          return {
            completedCourseIds: [],
            transcriptFileName: '',
            transcriptCompletedCourseCodes: [],
            transcriptCompletedCourses: [],
            transcriptCompletedCourseCount: 0,
            transcriptTotalAcademicUnitsEarned: 0,
            transcriptUnmatchedCourseCount: 0,
            transcriptMatchedCourses: [],
            transcriptUnmatchedCourseCodes: [],
            isTranscriptAppliedToRoadmap: false,
            roadmapRecommendationStaleReasons: nextStaleReasons,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: [],
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    roadmapRecommendations: state.roadmapRecommendations,
                    roadmapRecommendationStaleReasons: nextStaleReasons,
                    transcriptFileName: '',
                    transcriptCompletedCourseCodes: [],
                    transcriptCompletedCourses: [],
                    transcriptCompletedCourseCount: 0,
                    transcriptTotalAcademicUnitsEarned: 0,
                    transcriptUnmatchedCourseCount: 0,
                    transcriptMatchedCourses: [],
                    transcriptUnmatchedCourseCodes: [],
                    isTranscriptAppliedToRoadmap: false,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      logout: () =>
        set(() => ({
          activeStudentId: '',
          profile: DEFAULT_PROFILE,
          completedCourseIds: [],
          curriculumGuide: null,
          curriculumGuideFileName: '',
          transcriptFileName: '',
          transcriptCompletedCourseCodes: [],
          transcriptCompletedCourses: [],
          transcriptCompletedCourseCount: 0,
          transcriptTotalAcademicUnitsEarned: 0,
          transcriptUnmatchedCourseCount: 0,
          transcriptMatchedCourses: [],
          transcriptUnmatchedCourseCodes: [],
          isTranscriptAppliedToRoadmap: false,
          roadmapRecommendations: [],
          roadmapRecommendationStaleReasons: [],
        })),
    }),
    {
      // Browser storage key. Changing this would make existing saved profiles invisible
      name: 'student-profile-storage',
    },
  ),
)

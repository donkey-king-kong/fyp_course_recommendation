import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CurriculumGuideResponse } from '../types/curriculum'

export interface StudentProfile {
  studentId: string
  // CSC is the only supported major currently
  // More majors can be added here once the roadmap data supports them.
  major: 'CSC'
  yearOfStudy: number
  currentSemester: number
  careerGoal: string
}

export interface TranscriptMatchedCourse {
  courseCode: string
  title: string
}

interface SavedStudentProfile {
  profile: StudentProfile
  // Roadmap course IDs that should appear checked in the roadmap UI.
  completedCourseIds: string[]
  // Latest uploaded curriculum guide parsed into roadmap-shaped data.
  curriculumGuide: CurriculumGuideResponse | null
  // Original filename of the latest uploaded curriculum guide.
  curriculumGuideFileName: string
  // Completed module codes parsed from the latest uploaded transcript.
  transcriptCompletedCourseCodes: string[]
  // Last uploaded transcript's completed module count, including non-roadmap modules.
  transcriptCompletedCourseCount: number
  // Last uploaded transcript's completed module count that did not match the roadmap.
  transcriptUnmatchedCourseCount: number
  // Last uploaded transcript's completed courses that matched the roadmap.
  transcriptMatchedCourses: TranscriptMatchedCourse[]
  // Last uploaded transcript's completed course codes that did not match the roadmap.
  transcriptUnmatchedCourseCodes: string[]
}

// Reuse these defaults before anyone logs in and after logout
const DEFAULT_PROFILE: StudentProfile = {
  studentId: '',
  major: 'CSC',
  yearOfStudy: 1,
  currentSemester: 1,
  careerGoal: '',
}

interface ProfileState {
  activeStudentId: string
  profilesByStudentId: Record<string, SavedStudentProfile>
  profile: StudentProfile
  // Matched roadmap course IDs only; this drives roadmap checkboxes.
  completedCourseIds: string[]
  // Latest uploaded curriculum guide for the active profile.
  curriculumGuide: CurriculumGuideResponse | null
  // Original filename of the latest uploaded curriculum guide.
  curriculumGuideFileName: string
  // Completed module codes parsed from the latest uploaded transcript.
  transcriptCompletedCourseCodes: string[]
  // Parsed completed transcript rows, including rows that do not exist in the roadmap.
  transcriptCompletedCourseCount: number
  // Completed transcript rows that were parsed but not found in the current roadmap.
  transcriptUnmatchedCourseCount: number
  // Matched course details from the latest uploaded transcript.
  transcriptMatchedCourses: TranscriptMatchedCourse[]
  // Unmatched course codes from the latest uploaded transcript.
  transcriptUnmatchedCourseCodes: string[]
  // Activate an existing browser-saved profile, or create one for a new Student ID
  loginWithStudentId: (studentId: string) => void
  // Merge one or more profile fields into the existing profile
  updateProfile: (updates: Partial<StudentProfile>) => void
  // Used by roadmap checkboxes to add/remove one completed course
  toggleCourseCompletion: (courseId: string) => void
  // Used by roadmap actions to replace completed courses without changing transcript stats
  setCompletedCourses: (courseIds: string[]) => void
  // Used by curriculum guide upload to replace the active profile's parsed roadmap.
  setCurriculumGuide: (curriculumGuide: CurriculumGuideResponse, fileName: string) => void
  // Used by transcript upload to replace completed courses and save transcript stats
  setTranscriptResults: (
    completedCourseCodes: string[],
    transcriptCompletedCourseCount: number,
  ) => void
  // Used by logout to leave the active session while keeping saved browser profiles.
  logout: () => void
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

// Create the full browser-saved record for one Student ID
// It includes profile details, roadmap completion state, and transcript upload stats.
function createSavedStudentProfile(studentId: string): SavedStudentProfile {
  return {
    profile: createStudentProfile(studentId),
    completedCourseIds: [],
    curriculumGuide: null,
    curriculumGuideFileName: '',
    transcriptCompletedCourseCodes: [],
    transcriptCompletedCourseCount: 0,
    transcriptUnmatchedCourseCount: 0,
    transcriptMatchedCourses: [],
    transcriptUnmatchedCourseCodes: [],
  }
}

// Match raw transcript codes to the currently uploaded curriculum guide.
function matchTranscriptToCurriculum(
  completedCourseCodes: string[],
  curriculumGuide: CurriculumGuideResponse | null,
) {
  if (!curriculumGuide) {
    return {
      completedCourseIds: [],
      transcriptMatchedCourses: [],
      transcriptUnmatchedCourseCodes: [],
    }
  }

  const completedCodeSet = new Set(completedCourseCodes)
  const matchedCourses = curriculumGuide.nodes
    .filter((course) => completedCodeSet.has(course.courseCode))
    .map((course) => ({
      courseCode: course.courseCode,
      title: course.title,
    }))
  const matchedCodeSet = new Set(matchedCourses.map((course) => course.courseCode))
  const unmatchedCourseCodes = completedCourseCodes.filter(
    (courseCode) => !matchedCodeSet.has(courseCode),
  )

  return {
    completedCourseIds: curriculumGuide.nodes
      .filter((course) => completedCodeSet.has(course.courseCode))
      .map((course) => course.id),
    transcriptMatchedCourses: matchedCourses,
    transcriptUnmatchedCourseCodes: unmatchedCourseCodes,
  }
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
      transcriptCompletedCourseCodes: [],
      transcriptCompletedCourseCount: 0,
      transcriptUnmatchedCourseCount: 0,
      transcriptMatchedCourses: [],
      transcriptUnmatchedCourseCodes: [],

      loginWithStudentId: (studentId) =>
        set((state) => {
          // Use one consistent ID format as the lookup key
          const normalizedStudentId = normalizeStudentId(studentId)

          // Load saved profile if it exists
          const savedProfile = state.profilesByStudentId[normalizedStudentId]

          // Use the saved profile if it exists; otherwise start a new profile for this ID
          const activeProfile = savedProfile ?? createSavedStudentProfile(normalizedStudentId)
          const activeStudentProfile = {
            ...DEFAULT_PROFILE,
            ...activeProfile.profile,
            studentId: normalizedStudentId,
          }
          const hydratedProfile = {
            profile: activeStudentProfile,
            curriculumGuide: activeProfile.curriculumGuide ?? null,
            curriculumGuideFileName: activeProfile.curriculumGuideFileName ?? '',
            transcriptCompletedCourseCodes: activeProfile.transcriptCompletedCourseCodes ?? [],
            transcriptCompletedCourseCount: activeProfile.transcriptCompletedCourseCount ?? 0,
            transcriptUnmatchedCourseCount: activeProfile.transcriptUnmatchedCourseCount ?? 0,
            transcriptMatchedCourses: activeProfile.transcriptMatchedCourses ?? [],
            transcriptUnmatchedCourseCodes: activeProfile.transcriptUnmatchedCourseCodes ?? [],
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
            transcriptCompletedCourseCodes: hydratedProfile.transcriptCompletedCourseCodes,
            transcriptCompletedCourseCount: hydratedProfile.transcriptCompletedCourseCount,
            transcriptUnmatchedCourseCount: hydratedProfile.transcriptUnmatchedCourseCount,
            transcriptMatchedCourses: hydratedProfile.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: hydratedProfile.transcriptUnmatchedCourseCodes,
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
          const nextProfile = {
            ...state.profile,
            ...updates,
            // Keep the existing Student ID unless this update specifically changes it
            studentId:
              updates.studentId === undefined
                ? state.profile.studentId
                : normalizeStudentId(updates.studentId),
          }
          const nextProfilesByStudentId = { ...state.profilesByStudentId }

          if (state.activeStudentId && state.activeStudentId !== nextProfile.studentId) {
            delete nextProfilesByStudentId[state.activeStudentId]
          }

          if (nextProfile.studentId) {
            nextProfilesByStudentId[nextProfile.studentId] = {
              profile: nextProfile,
              completedCourseIds: state.completedCourseIds,
              curriculumGuide: state.curriculumGuide,
              curriculumGuideFileName: state.curriculumGuideFileName,
              transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
              transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
              transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
              transcriptMatchedCourses: state.transcriptMatchedCourses,
              transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
            }
          }

          return {
            activeStudentId: nextProfile.studentId,
            profile: nextProfile,
            profilesByStudentId: nextProfilesByStudentId,
          }
        }),

      toggleCourseCompletion: (courseId) =>
        set((state) => {
          const isCompleted = state.completedCourseIds.includes(courseId)
          const nextCompletedCourseIds = isCompleted
            ? state.completedCourseIds.filter((id) => id !== courseId)
            : [...state.completedCourseIds, courseId]

          return {
            completedCourseIds: nextCompletedCourseIds,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: nextCompletedCourseIds,
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                    transcriptMatchedCourses: state.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      setCompletedCourses: (courseIds) =>
        set((state) => ({
          completedCourseIds: courseIds,
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: courseIds,
                  curriculumGuide: state.curriculumGuide,
                  curriculumGuideFileName: state.curriculumGuideFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptUnmatchedCourseCount: state.transcriptUnmatchedCourseCount,
                  transcriptMatchedCourses: state.transcriptMatchedCourses,
                  transcriptUnmatchedCourseCodes: state.transcriptUnmatchedCourseCodes,
                },
              }
            : state.profilesByStudentId,
        })),

      setCurriculumGuide: (curriculumGuide, fileName) =>
        set((state) => {
          const matchedResults = matchTranscriptToCurriculum(
            state.transcriptCompletedCourseCodes,
            curriculumGuide,
          )

          return {
            curriculumGuide,
            curriculumGuideFileName: fileName,
            completedCourseIds: matchedResults.completedCourseIds,
            transcriptUnmatchedCourseCount: matchedResults.transcriptUnmatchedCourseCodes.length,
            transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: matchedResults.completedCourseIds,
                    curriculumGuide,
                    curriculumGuideFileName: fileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      setTranscriptResults: (completedCourseCodes, transcriptCompletedCourseCount) =>
        set((state) => {
          const matchedResults = matchTranscriptToCurriculum(
            completedCourseCodes,
            state.curriculumGuide,
          )

          return {
            completedCourseIds: matchedResults.completedCourseIds,
            transcriptCompletedCourseCodes: completedCourseCodes,
            transcriptCompletedCourseCount,
            transcriptUnmatchedCourseCount: matchedResults.transcriptUnmatchedCourseCodes.length,
            transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
            transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
            profilesByStudentId: state.activeStudentId
              ? {
                  ...state.profilesByStudentId,
                  [state.activeStudentId]: {
                    profile: state.profile,
                    completedCourseIds: matchedResults.completedCourseIds,
                    curriculumGuide: state.curriculumGuide,
                    curriculumGuideFileName: state.curriculumGuideFileName,
                    transcriptCompletedCourseCodes: completedCourseCodes,
                    transcriptCompletedCourseCount,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
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
          transcriptCompletedCourseCodes: [],
          transcriptCompletedCourseCount: 0,
          transcriptUnmatchedCourseCount: 0,
          transcriptMatchedCourses: [],
          transcriptUnmatchedCourseCodes: [],
        })),
    }),
    {
      // Browser storage key. Changing this would make existing saved profiles invisible
      name: 'student-profile-storage',
    },
  ),
)

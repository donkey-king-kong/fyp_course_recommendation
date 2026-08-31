import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CurriculumGuideResponse } from '../types/curriculum'
import type { TranscriptCourse } from '../types/transcript'

export interface StudentProfile {
  studentId: string
  // CSC is the only supported major currently
  // More majors can be added here once the roadmap data supports them.
  major: 'CSC'
  careerGoal: string
  preferredRecommendationTags: string[]
}

export interface TranscriptMatchedCourse {
  courseCode: string
  title: string
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
  loginWithStudentId: (studentId: string) => void // Load or create profile.
  updateProfile: (updates: Partial<StudentProfile>) => void // Save profile fields.
  toggleCourseCompletion: (courseId: string) => void // Toggle one roadmap checkbox.
  setCompletedCourses: (courseIds: string[]) => void // Replace checked roadmap IDs.
  setCurriculumGuide: (curriculumGuide: CurriculumGuideResponse, fileName: string) => void // Save guide.
  clearCurriculumGuide: () => void // Remove uploaded guide only.
  setTranscriptResults: (
    fileName: string,
    completedCourseCodes: string[],
    transcriptCompletedCourses: TranscriptCourse[],
    transcriptCompletedCourseCount: number,
    transcriptTotalAcademicUnitsEarned: number,
  ) => void // Save transcript results.
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
  }
}

function normalizeCourseTitle(title: string) {
  return title
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .join(' ')
}

function getCourseTitleSignature(title: string) {
  return normalizeCourseTitle(title)
    .split(' ')
    .filter((token) => token !== 'principle' && token !== 'principles')
    .map((token) => {
      if (token === 'systems') {
        return 'system'
      }

      if (token === 'databases') {
        return 'database'
      }

      return token
    })
    .join(' ')
}

function getTranscriptCourseKeys(course: TranscriptCourse) {
  return new Set([
    course.course_code,
    normalizeCourseTitle(course.title),
    getCourseTitleSignature(course.title),
  ])
}

// Match raw transcript codes to the currently uploaded curriculum guide.
function matchTranscriptToCurriculum(
  completedCourseCodes: string[],
  transcriptCompletedCourses: TranscriptCourse[],
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
  const transcriptCourseKeys = transcriptCompletedCourses.reduce<Set<string>>((keys, course) => {
    getTranscriptCourseKeys(course).forEach((key) => keys.add(key))
    return keys
  }, new Set())
  const matchedCourses = curriculumGuide.nodes
    // Some NTU modules change code across guide/transcript versions, so match by title too.
    .filter(
      (course) =>
        completedCodeSet.has(course.courseCode) ||
        transcriptCourseKeys.has(normalizeCourseTitle(course.title)) ||
        transcriptCourseKeys.has(getCourseTitleSignature(course.title)),
    )
    .map((course) => ({
      courseCode: course.courseCode,
      title: course.title,
    }))
  const matchedCourseKeys = curriculumGuide.nodes
    .filter((course) => matchedCourses.some((matchedCourse) => matchedCourse.courseCode === course.courseCode))
    .reduce<Set<string>>((keys, course) => {
      keys.add(course.courseCode)
      keys.add(normalizeCourseTitle(course.title))
      keys.add(getCourseTitleSignature(course.title))
      return keys
    }, new Set())
  const unmatchedCourseCodes = completedCourseCodes.filter(
    (courseCode) => {
      const transcriptCourse = transcriptCompletedCourses.find(
        (course) => course.course_code === courseCode,
      )

      if (!transcriptCourse) {
        return !matchedCourseKeys.has(courseCode)
      }

      return ![...getTranscriptCourseKeys(transcriptCourse)].some((key) =>
        matchedCourseKeys.has(key),
      )
    },
  )

  return {
    completedCourseIds: curriculumGuide.nodes
      .filter((course) =>
        matchedCourses.some((matchedCourse) => matchedCourse.courseCode === course.courseCode),
      )
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
      transcriptFileName: '',
      transcriptCompletedCourseCodes: [],
      transcriptCompletedCourses: [],
      transcriptCompletedCourseCount: 0,
      transcriptTotalAcademicUnitsEarned: 0,
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
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
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
                  transcriptFileName: state.transcriptFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourses: state.transcriptCompletedCourses,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
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
            state.transcriptCompletedCourses,
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
                    transcriptFileName: state.transcriptFileName,
                    transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                    transcriptCompletedCourses: state.transcriptCompletedCourses,
                    transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
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
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: [],
                  curriculumGuide: null,
                  curriculumGuideFileName: '',
                  transcriptFileName: state.transcriptFileName,
                  transcriptCompletedCourseCodes: state.transcriptCompletedCourseCodes,
                  transcriptCompletedCourses: state.transcriptCompletedCourses,
                  transcriptCompletedCourseCount: state.transcriptCompletedCourseCount,
                  transcriptTotalAcademicUnitsEarned: state.transcriptTotalAcademicUnitsEarned,
                  transcriptUnmatchedCourseCount: state.transcriptCompletedCourseCodes.length,
                  transcriptMatchedCourses: [],
                  transcriptUnmatchedCourseCodes: state.transcriptCompletedCourseCodes,
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
      ) =>
        set((state) => {
          const matchedResults = matchTranscriptToCurriculum(
            completedCourseCodes,
            transcriptCompletedCourses,
            state.curriculumGuide,
          )

          return {
            completedCourseIds: matchedResults.completedCourseIds,
            transcriptFileName: fileName,
            transcriptCompletedCourseCodes: completedCourseCodes,
            transcriptCompletedCourses,
            transcriptCompletedCourseCount,
            transcriptTotalAcademicUnitsEarned,
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
                    transcriptFileName: fileName,
                    transcriptCompletedCourseCodes: completedCourseCodes,
                    transcriptCompletedCourses,
                    transcriptCompletedCourseCount,
                    transcriptTotalAcademicUnitsEarned,
                    transcriptUnmatchedCourseCount:
                      matchedResults.transcriptUnmatchedCourseCodes.length,
                    transcriptMatchedCourses: matchedResults.transcriptMatchedCourses,
                    transcriptUnmatchedCourseCodes: matchedResults.transcriptUnmatchedCourseCodes,
                  },
                }
              : state.profilesByStudentId,
          }
        }),

      clearTranscriptResults: () =>
        set((state) => ({
          completedCourseIds: [],
          transcriptFileName: '',
          transcriptCompletedCourseCodes: [],
          transcriptCompletedCourses: [],
          transcriptCompletedCourseCount: 0,
          transcriptTotalAcademicUnitsEarned: 0,
          transcriptUnmatchedCourseCount: 0,
          transcriptMatchedCourses: [],
          transcriptUnmatchedCourseCodes: [],
          profilesByStudentId: state.activeStudentId
            ? {
                ...state.profilesByStudentId,
                [state.activeStudentId]: {
                  profile: state.profile,
                  completedCourseIds: [],
                  curriculumGuide: state.curriculumGuide,
                  curriculumGuideFileName: state.curriculumGuideFileName,
                  transcriptFileName: '',
                  transcriptCompletedCourseCodes: [],
                  transcriptCompletedCourses: [],
                  transcriptCompletedCourseCount: 0,
                  transcriptTotalAcademicUnitsEarned: 0,
                  transcriptUnmatchedCourseCount: 0,
                  transcriptMatchedCourses: [],
                  transcriptUnmatchedCourseCodes: [],
                },
              }
            : state.profilesByStudentId,
        })),

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
        })),
    }),
    {
      // Browser storage key. Changing this would make existing saved profiles invisible
      name: 'student-profile-storage',
    },
  ),
)

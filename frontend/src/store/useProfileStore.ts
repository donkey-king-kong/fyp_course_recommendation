import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface StudentProfile {
  studentId: string
  // CSC is the only supported major currently
  // More majors can be added here once the roadmap data supports them.
  major: 'CSC'
  yearOfStudy: number
  currentSemester: number
}

interface SavedStudentProfile {
  profile: StudentProfile
  completedCourseIds: string[]
}

// Reuse these defaults before anyone logs in and after logout
const DEFAULT_PROFILE: StudentProfile = {
  studentId: '',
  major: 'CSC',
  yearOfStudy: 1,
  currentSemester: 1,
}

interface ProfileState {
  activeStudentId: string
  profilesByStudentId: Record<string, SavedStudentProfile>
  profile: StudentProfile
  completedCourseIds: string[]
  // Activate an existing browser-saved profile, or create one for a new Student ID
  loginWithStudentId: (studentId: string) => void
  // Merge one or more profile fields into the existing profile
  updateProfile: (updates: Partial<StudentProfile>) => void
  // Used by roadmap checkboxes to add/remove one completed course
  toggleCourseCompletion: (courseId: string) => void
  // Used later by transcript upload to replace completed courses in bulk
  setCompletedCourses: (courseIds: string[]) => void
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
// It includes both profile details and roadmap completion state
function createSavedStudentProfile(studentId: string): SavedStudentProfile {
  return {
    profile: createStudentProfile(studentId),
    completedCourseIds: [],
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

      loginWithStudentId: (studentId) =>
        set((state) => {
          // Use one consistent ID format as the lookup key
          const normalizedStudentId = normalizeStudentId(studentId)

          // Load saved profile if it exists
          const savedProfile = state.profilesByStudentId[normalizedStudentId]

          // Use the saved profile if it exists; otherwise start a new profile for this ID
          const activeProfile = savedProfile ?? createSavedStudentProfile(normalizedStudentId)

          return {
            // Controls whether the app shows login page or roadmap
            activeStudentId: normalizedStudentId,
            profile: activeProfile.profile,
            completedCourseIds: activeProfile.completedCourseIds,
            // Store the active profile back into the map so it persists under this Student ID
            profilesByStudentId: {
              ...state.profilesByStudentId,
              [normalizedStudentId]: activeProfile,
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
                },
              }
            : state.profilesByStudentId,
        })),

      logout: () =>
        set(() => ({
          activeStudentId: '',
          profile: DEFAULT_PROFILE,
          completedCourseIds: [],
        })),
    }),
    {
      // Browser storage key. Changing this would make existing saved profiles invisible
      name: 'student-profile-storage',
    },
  ),
)

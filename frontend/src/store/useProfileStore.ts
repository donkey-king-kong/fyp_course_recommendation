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

// Reuse these defaults when the app first loads or when the user logs out
const DEFAULT_PROFILE: StudentProfile = {
  studentId: '',
  major: 'CSC',
  yearOfStudy: 1,
  currentSemester: 1,
}

interface ProfileState {
  profile: StudentProfile
  completedCourseIds: string[]
  // Merge one or more profile fields into the existing profile
  updateProfile: (updates: Partial<StudentProfile>) => void
  // Used by roadmap checkboxes to add/remove one completed course
  toggleCourseCompletion: (courseId: string) => void
  // Used later by transcript upload to replace completed courses in bulk
  setCompletedCourses: (courseIds: string[]) => void
  // Used by logout to clear the browser-stored profile state
  resetProfile: () => void
}

function normalizeStudentId(studentId: string) {
  // Normalize studentIDs
  return studentId.trim().toUpperCase()
}

export const useProfileStore = create<ProfileState>()(
  // persist saves this store to browser localStorage under the name below
  persist(
    (set) => ({
      profile: DEFAULT_PROFILE,
      completedCourseIds: [],
      
      updateProfile: (updates) =>
        set((state) => ({
          profile: {
            ...state.profile,
            ...updates,
            // Keep the existing Student ID unless this update specifically changes it
            studentId:
              updates.studentId === undefined
                ? state.profile.studentId
                : normalizeStudentId(updates.studentId),
          },
        })),
        
      toggleCourseCompletion: (courseId) =>
        set((state) => {
          const isCompleted = state.completedCourseIds.includes(courseId)
          if (isCompleted) {
            return {
              completedCourseIds: state.completedCourseIds.filter((id) => id !== courseId),
            }
          } else {
            return {
              completedCourseIds: [...state.completedCourseIds, courseId],
            }
          }
        }),
        
      setCompletedCourses: (courseIds) =>
        set(() => ({
          completedCourseIds: courseIds,
        })),

      resetProfile: () =>
        set(() => ({
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

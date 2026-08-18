import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface StudentProfile {
  name: string
  yearOfStudy: number
  currentSemester: number
}

interface ProfileState {
  profile: StudentProfile
  completedCourseIds: string[]
  updateProfile: (updates: Partial<StudentProfile>) => void
  toggleCourseCompletion: (courseId: string) => void
  setCompletedCourses: (courseIds: string[]) => void
}

export const useProfileStore = create<ProfileState>()(
  persist(
    (set) => ({
      profile: {
        name: '',
        yearOfStudy: 1,
        currentSemester: 1,
      },
      completedCourseIds: [],
      
      updateProfile: (updates) =>
        set((state) => ({
          profile: { ...state.profile, ...updates },
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
    }),
    {
      name: 'student-profile-storage',
    },
  ),
)

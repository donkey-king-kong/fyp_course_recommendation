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

interface ProfileState {
  profile: StudentProfile
  completedCourseIds: string[]
  updateProfile: (updates: Partial<StudentProfile>) => void
  toggleCourseCompletion: (courseId: string) => void
  setCompletedCourses: (courseIds: string[]) => void
}

function normalizeStudentId(studentId: string) {
  return studentId.trim().toUpperCase()
}

export const useProfileStore = create<ProfileState>()(
  persist(
    (set) => ({
      profile: {
        studentId: '',
        major: 'CSC',
        yearOfStudy: 1,
        currentSemester: 1,
      },
      completedCourseIds: [],
      
      updateProfile: (updates) =>
        set((state) => ({
          profile: {
            ...state.profile,
            ...updates,
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
    }),
    {
      name: 'student-profile-storage',
    },
  ),
)

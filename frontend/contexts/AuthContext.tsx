"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  id: number
  email: string
  name: string
  region: string
  role: 'user' | 'admin'
  createdAt: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>
  register: (userData: RegisterData) => Promise<{ success: boolean; error?: string }>
  logout: () => void
  updateProfile: (userData: Partial<User>) => Promise<{ success: boolean; error?: string }>
}

interface RegisterData {
  email: string
  password: string
  name: string
  region: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // 페이지 로드시 저장된 토큰으로 사용자 정보 복구
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('accessToken')
      if (!token) {
        setIsLoading(false)
        return
      }

      // 실제 구현시 API 호출로 토큰 검증 및 사용자 정보 가져오기
      // const response = await fetch('/api/auth/me', {
      //   headers: { Authorization: `Bearer ${token}` }
      // })
      
      // Mock 사용자 데이터로 시뮬레이션
      const mockUser: User = {
        id: 1,
        email: 'test@example.com',
        name: '김사용자',
        region: '서울특별시',
        role: 'user',
        createdAt: '2025-01-20'
      }
      
      setUser(mockUser)
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true)
      
      // 실제 구현시 API 호출
      // const response = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email, password })
      // })
      
      // Mock 로그인 로직
      if (email === 'test@example.com' && password === 'password123') {
        const mockUser: User = {
          id: 1,
          email: email,
          name: '김사용자',
          region: '서울특별시',
          role: 'user',
          createdAt: '2025-01-20'
        }
        
        // Mock 토큰 저장
        localStorage.setItem('accessToken', 'mock-access-token')
        localStorage.setItem('refreshToken', 'mock-refresh-token')
        
        setUser(mockUser)
        return { success: true }
      } else if (email === 'admin@example.com' && password === 'admin123') {
        const mockAdmin: User = {
          id: 2,
          email: email,
          name: '관리자',
          region: '서울특별시',
          role: 'admin',
          createdAt: '2025-01-15'
        }
        
        localStorage.setItem('accessToken', 'mock-admin-token')
        localStorage.setItem('refreshToken', 'mock-admin-refresh-token')
        
        setUser(mockAdmin)
        return { success: true }
      }
      
      return { success: false, error: '이메일 또는 비밀번호가 올바르지 않습니다.' }
    } catch (error) {
      return { success: false, error: '로그인 중 오류가 발생했습니다.' }
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      setIsLoading(true)
      
      // 실제 구현시 API 호출
      // const response = await fetch('/api/auth/register', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(userData)
      // })
      
      // Mock 회원가입 로직 - 이메일 중복 체크
      if (userData.email === 'test@example.com' || userData.email === 'admin@example.com') {
        return { success: false, error: '이미 사용 중인 이메일입니다.' }
      }
      
      // 비밀번호 강도 검증
      if (userData.password.length < 8) {
        return { success: false, error: '비밀번호는 8자 이상이어야 합니다.' }
      }
      
      const newUser: User = {
        id: Math.floor(Math.random() * 1000) + 3,
        email: userData.email,
        name: userData.name,
        region: userData.region,
        role: 'user',
        createdAt: new Date().toISOString().split('T')[0]
      }
      
      // Mock 토큰 저장
      localStorage.setItem('accessToken', 'mock-new-user-token')
      localStorage.setItem('refreshToken', 'mock-new-user-refresh-token')
      
      setUser(newUser)
      return { success: true }
    } catch (error) {
      return { success: false, error: '회원가입 중 오류가 발생했습니다.' }
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    setUser(null)
  }

  const updateProfile = async (userData: Partial<User>) => {
    try {
      if (!user) return { success: false, error: '로그인이 필요합니다.' }
      
      // 실제 구현시 API 호출
      // const response = await fetch('/api/auth/profile', {
      //   method: 'PUT',
      //   headers: { 
      //     'Content-Type': 'application/json',
      //     Authorization: `Bearer ${localStorage.getItem('accessToken')}`
      //   },
      //   body: JSON.stringify(userData)
      // })
      
      // Mock 프로필 업데이트
      const updatedUser = { ...user, ...userData }
      setUser(updatedUser)
      
      return { success: true }
    } catch (error) {
      return { success: false, error: '프로필 업데이트 중 오류가 발생했습니다.' }
    }
  }

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    updateProfile
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  id: number
  email: string
  username?: string
  display_name?: string
  region_code?: string
  role?: 'user' | 'admin'
  created_at?: string
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
  displayName: string
  region: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

  useEffect(() => {
    // 페이지 로드시 저장된 토큰으로 사용자 정보 복구
    checkAuthStatus()
  }, [])

  const refreshToken = async () => {
    const refresh = localStorage.getItem('refreshToken')
    if (!refresh) return false
    try {
      const res = await fetch(`${API_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refresh }),
        credentials: 'include'
      })
      if (!res.ok) return false
      const data = await res.json()
      localStorage.setItem('accessToken', data.access_token)
      if (data.refresh_token)
        localStorage.setItem('refreshToken', data.refresh_token)
      return true
    } catch {
      return false
    }
  }

  const fetchWithAuth = async (
    endpoint: string,
    options: RequestInit = {},
    retry = true
  ): Promise<Response> => {
    const token = localStorage.getItem('accessToken')
    const headers = {
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
    const res = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
      credentials: 'include'
    })
    if (res.status === 401 && retry) {
      const refreshed = await refreshToken()
      if (refreshed) return fetchWithAuth(endpoint, options, false)
      logout()
    }
    return res
  }

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('accessToken')
      if (!token) {
        setIsLoading(false)
        return
      }

      const res = await fetchWithAuth('/auth/me')
      if (!res.ok) {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        setUser(null)
      } else {
        const data = await res.json()
        setUser(data)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      logout()
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true)
      
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password }),
        credentials: 'include'
      })
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        return { success: false, error: err.detail || '이메일 또는 비밀번호가 올바르지 않습니다.' }
      }
      
      const data = await res.json()
      localStorage.setItem('accessToken', data.access_token)
      if (data.refresh_token) localStorage.setItem('refreshToken', data.refresh_token)
      
      await checkAuthStatus()
      return { success: true }
    } catch (error) {
      return { success: false, error: '로그인 중 오류가 발생했습니다.' }
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      setIsLoading(true)
      
      const res = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: userData.email,
          username: userData.email,
          password: userData.password,
          display_name: userData.displayName,
          region_code: userData.region
        }),
        credentials: 'include'
      })
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        return { success: false, error: err.detail || '회원가입에 실패했습니다.' }
      }
      
      // 회원가입 성공 후 자동 로그인
      const loginResult = await login(userData.email, userData.password)
      if (!loginResult.success) return loginResult
      
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
      
      const res = await fetchWithAuth('/auth/me', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        return { success: false, error: err.detail || '프로필 업데이트 중 오류가 발생했습니다.' }
      }
      
      const updatedUser = await res.json()
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
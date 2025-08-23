"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import Link from "next/link"

export function RegisterForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    region: "",
    interests: [] as string[],
    agreeTerms: false,
    agreePrivacy: false,
  })

  const regions = [
    "서울특별시",
    "부산광역시",
    "대구광역시",
    "인천광역시",
    "광주광역시",
    "대전광역시",
    "울산광역시",
    "세종특별자치시",
    "경기도",
    "강원도",
    "충청북도",
    "충청남도",
    "전라북도",
    "전라남도",
    "경상북도",
    "경상남도",
    "제주특별자치도",
  ]

  const interests = [
    "체육시설 확충",
    "생활체육 활성화",
    "엘리트 체육 지원",
    "체육 예산 분석",
    "지역 체육 정책",
    "청소년 체육",
    "노인 체육",
    "장애인 체육",
  ]

  const handleInterestChange = (interest: string, checked: boolean) => {
    if (checked) {
      setFormData((prev) => ({ ...prev, interests: [...prev.interests, interest] }))
    } else {
      setFormData((prev) => ({ ...prev, interests: prev.interests.filter((i) => i !== interest) }))
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>회원가입</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="name">이름</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
              placeholder="홍길동"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">이메일</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData((prev) => ({ ...prev, email: e.target.value }))}
              placeholder="hong@example.com"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="password">비밀번호</Label>
            <Input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData((prev) => ({ ...prev, password: e.target.value }))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">비밀번호 확인</Label>
            <Input
              id="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData((prev) => ({ ...prev, confirmPassword: e.target.value }))}
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label>거주 지역</Label>
          <Select
            value={formData.region}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, region: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="지역을 선택하세요" />
            </SelectTrigger>
            <SelectContent>
              {regions.map((region) => (
                <SelectItem key={region} value={region}>
                  {region}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>관심 분야 (복수 선택 가능)</Label>
          <div className="grid grid-cols-2 gap-2">
            {interests.map((interest) => (
              <div key={interest} className="flex items-center space-x-2">
                <Checkbox
                  id={interest}
                  checked={formData.interests.includes(interest)}
                  onCheckedChange={(checked) => handleInterestChange(interest, checked as boolean)}
                />
                <Label htmlFor={interest} className="text-sm">
                  {interest}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <Checkbox
              id="terms"
              checked={formData.agreeTerms}
              onCheckedChange={(checked) => setFormData((prev) => ({ ...prev, agreeTerms: checked as boolean }))}
            />
            <Label htmlFor="terms" className="text-sm">
              <Link href="/terms" className="text-cyan-600 hover:underline">
                이용약관
              </Link>
              에 동의합니다
            </Label>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              id="privacy"
              checked={formData.agreePrivacy}
              onCheckedChange={(checked) => setFormData((prev) => ({ ...prev, agreePrivacy: checked as boolean }))}
            />
            <Label htmlFor="privacy" className="text-sm">
              <Link href="/privacy" className="text-cyan-600 hover:underline">
                개인정보처리방침
              </Link>
              에 동의합니다
            </Label>
          </div>
        </div>

        <Button className="w-full" size="lg">
          가입하기
        </Button>

        <div className="text-center text-sm text-gray-600">
          이미 계정이 있으신가요?{" "}
          <Link href="/auth/login" className="text-cyan-600 hover:underline">
            로그인
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}

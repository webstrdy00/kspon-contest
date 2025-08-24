"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  FileText,
  MapPin,
  Tag,
  Users,
  Lightbulb,
  Send,
  X,
  Plus,
  AlertCircle,
  CheckCircle
} from "lucide-react"

interface CreateProposalModalProps {
  open: boolean
  onClose: () => void
}

interface ProposalForm {
  title: string
  category: string
  region: string
  content: string
  tags: string[]
  targetAudience: string
  expectedImpact: string
  implementation: string
}

export function CreateProposalModal({ open, onClose }: CreateProposalModalProps) {
  const [activeStep, setActiveStep] = useState(0)
  const [newTag, setNewTag] = useState("")
  const [form, setForm] = useState<ProposalForm>({
    title: "",
    category: "",
    region: "",
    content: "",
    tags: [],
    targetAudience: "",
    expectedImpact: "",
    implementation: ""
  })

  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  const steps = [
    { id: 0, title: "기본 정보", icon: <FileText className="h-4 w-4" /> },
    { id: 1, title: "상세 내용", icon: <Lightbulb className="h-4 w-4" /> },
    { id: 2, title: "미리보기", icon: <CheckCircle className="h-4 w-4" /> }
  ]

  const categories = [
    "시설 확충",
    "운영 개선", 
    "접근성 개선",
    "시설 개선",
    "프로그램 신설",
    "정책 개선",
    "예산 지원"
  ]

  const regions = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시",
    "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
    "경기도", "강원도", "충청북도", "충청남도", 
    "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
  ]

  const addTag = () => {
    if (newTag.trim() && !form.tags.includes(newTag.trim()) && form.tags.length < 5) {
      setForm({
        ...form,
        tags: [...form.tags, newTag.trim()]
      })
      setNewTag("")
    }
  }

  const removeTag = (tagToRemove: string) => {
    setForm({
      ...form,
      tags: form.tags.filter(tag => tag !== tagToRemove)
    })
  }

  const validateStep = (step: number) => {
    const newErrors: { [key: string]: string } = {}

    if (step === 0) {
      if (!form.title.trim()) newErrors.title = "제목을 입력해주세요"
      if (!form.category) newErrors.category = "카테고리를 선택해주세요"
      if (!form.region) newErrors.region = "지역을 선택해주세요"
      if (!form.content.trim()) newErrors.content = "제안 내용을 입력해주세요"
    }

    if (step === 1) {
      if (!form.targetAudience.trim()) newErrors.targetAudience = "대상층을 입력해주세요"
      if (!form.expectedImpact.trim()) newErrors.expectedImpact = "기대 효과를 입력해주세요"
      if (!form.implementation.trim()) newErrors.implementation = "구현 방안을 입력해주세요"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const nextStep = () => {
    if (validateStep(activeStep)) {
      setActiveStep(prev => Math.min(prev + 1, steps.length - 1))
    }
  }

  const prevStep = () => {
    setActiveStep(prev => Math.max(prev - 1, 0))
  }

  const handleSubmit = () => {
    if (validateStep(1)) {
      // 실제 구현시 API 호출
      console.log("제안 제출:", form)
      onClose()
      // 성공 메시지 또는 리다이렉트
    }
  }

  const resetForm = () => {
    setForm({
      title: "",
      category: "",
      region: "",
      content: "",
      tags: [],
      targetAudience: "",
      expectedImpact: "",
      implementation: ""
    })
    setActiveStep(0)
    setErrors({})
  }

  const handleClose = () => {
    resetForm()
    onClose()
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            새 정책 제안 작성
          </DialogTitle>
          <DialogDescription>
            지역 체육환경 개선을 위한 아이디어를 공유해주세요
          </DialogDescription>
        </DialogHeader>

        {/* 진행 단계 */}
        <div className="flex items-center justify-between mb-6 px-4">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                activeStep >= index 
                  ? 'bg-primary text-primary-foreground' 
                  : 'bg-muted text-muted-foreground'
              }`}>
                {step.icon}
              </div>
              <span className={`ml-2 text-sm ${
                activeStep >= index ? 'text-foreground' : 'text-muted-foreground'
              }`}>
                {step.title}
              </span>
              {index < steps.length - 1 && (
                <div className={`w-16 h-0.5 ml-4 ${
                  activeStep > index ? 'bg-primary' : 'bg-muted'
                }`} />
              )}
            </div>
          ))}
        </div>

        <Tabs value={activeStep.toString()} className="space-y-6">
          {/* Step 1: 기본 정보 */}
          <TabsContent value="0" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="title">제안 제목 *</Label>
                  <Input
                    id="title"
                    placeholder="구체적이고 명확한 제목을 입력하세요"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                    className={errors.title ? "border-red-500" : ""}
                  />
                  {errors.title && (
                    <p className="text-sm text-red-600 mt-1">{errors.title}</p>
                  )}
                </div>

                <div>
                  <Label htmlFor="category">카테고리 *</Label>
                  <Select 
                    value={form.category} 
                    onValueChange={(value) => setForm({ ...form, category: value })}
                  >
                    <SelectTrigger className={errors.category ? "border-red-500" : ""}>
                      <SelectValue placeholder="제안 카테고리를 선택하세요" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.category && (
                    <p className="text-sm text-red-600 mt-1">{errors.category}</p>
                  )}
                </div>

                <div>
                  <Label htmlFor="region">지역 *</Label>
                  <Select 
                    value={form.region} 
                    onValueChange={(value) => setForm({ ...form, region: value })}
                  >
                    <SelectTrigger className={errors.region ? "border-red-500" : ""}>
                      <SelectValue placeholder="해당 지역을 선택하세요" />
                    </SelectTrigger>
                    <SelectContent>
                      {regions.map((region) => (
                        <SelectItem key={region} value={region}>
                          {region}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.region && (
                    <p className="text-sm text-red-600 mt-1">{errors.region}</p>
                  )}
                </div>

                <div>
                  <Label htmlFor="tags">태그</Label>
                  <div className="flex gap-2 mb-2">
                    <Input
                      placeholder="태그 입력 (최대 5개)"
                      value={newTag}
                      onChange={(e) => setNewTag(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                      disabled={form.tags.length >= 5}
                    />
                    <Button 
                      type="button" 
                      variant="outline" 
                      size="sm"
                      onClick={addTag}
                      disabled={!newTag.trim() || form.tags.length >= 5}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {form.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">
                        #{tag}
                        <button
                          type="button"
                          onClick={() => removeTag(tag)}
                          className="ml-1 hover:text-red-600"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <Label htmlFor="content">제안 내용 *</Label>
                <Textarea
                  id="content"
                  placeholder="현재 상황과 개선이 필요한 이유를 구체적으로 설명해주세요"
                  value={form.content}
                  onChange={(e) => setForm({ ...form, content: e.target.value })}
                  className={`min-h-[200px] ${errors.content ? "border-red-500" : ""}`}
                />
                {errors.content && (
                  <p className="text-sm text-red-600 mt-1">{errors.content}</p>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Step 2: 상세 내용 */}
          <TabsContent value="1" className="space-y-6">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <Label htmlFor="targetAudience">주요 대상층 *</Label>
                <Textarea
                  id="targetAudience"
                  placeholder="이 제안의 주요 수혜 대상이 누구인지 설명해주세요 (예: 어린이, 어르신, 직장인, 장애인 등)"
                  value={form.targetAudience}
                  onChange={(e) => setForm({ ...form, targetAudience: e.target.value })}
                  className={`min-h-[100px] ${errors.targetAudience ? "border-red-500" : ""}`}
                />
                {errors.targetAudience && (
                  <p className="text-sm text-red-600 mt-1">{errors.targetAudience}</p>
                )}
              </div>

              <div>
                <Label htmlFor="expectedImpact">기대 효과 *</Label>
                <Textarea
                  id="expectedImpact"
                  placeholder="이 제안이 실현되었을 때 얻을 수 있는 구체적인 효과를 설명해주세요"
                  value={form.expectedImpact}
                  onChange={(e) => setForm({ ...form, expectedImpact: e.target.value })}
                  className={`min-h-[100px] ${errors.expectedImpact ? "border-red-500" : ""}`}
                />
                {errors.expectedImpact && (
                  <p className="text-sm text-red-600 mt-1">{errors.expectedImpact}</p>
                )}
              </div>

              <div>
                <Label htmlFor="implementation">구현 방안 *</Label>
                <Textarea
                  id="implementation"
                  placeholder="제안을 어떻게 실현할 수 있을지 구체적인 방안을 제시해주세요"
                  value={form.implementation}
                  onChange={(e) => setForm({ ...form, implementation: e.target.value })}
                  className={`min-h-[100px] ${errors.implementation ? "border-red-500" : ""}`}
                />
                {errors.implementation && (
                  <p className="text-sm text-red-600 mt-1">{errors.implementation}</p>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Step 3: 미리보기 */}
          <TabsContent value="2" className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">{form.category}</Badge>
                      <Badge variant="outline">검토 예정</Badge>
                    </div>
                    <CardTitle className="text-xl">{form.title}</CardTitle>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <MapPin className="h-3 w-3" />
                        {form.region}
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        작성자 (본인)
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h4 className="font-semibold mb-2">제안 내용</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {form.content}
                  </p>
                </div>

                <Separator />

                <div>
                  <h4 className="font-semibold mb-2">주요 대상층</h4>
                  <p className="text-sm text-muted-foreground">
                    {form.targetAudience}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold mb-2">기대 효과</h4>
                  <p className="text-sm text-muted-foreground">
                    {form.expectedImpact}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold mb-2">구현 방안</h4>
                  <p className="text-sm text-muted-foreground">
                    {form.implementation}
                  </p>
                </div>

                {form.tags.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">태그</h4>
                    <div className="flex flex-wrap gap-1">
                      {form.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          #{tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <DialogFooter className="flex justify-between">
          <div className="flex gap-2">
            {activeStep > 0 && (
              <Button variant="outline" onClick={prevStep}>
                이전
              </Button>
            )}
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleClose}>
              취소
            </Button>
            {activeStep < steps.length - 1 ? (
              <Button onClick={nextStep}>
                다음
              </Button>
            ) : (
              <Button onClick={handleSubmit}>
                <Send className="h-4 w-4 mr-2" />
                제안 제출
              </Button>
            )}
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
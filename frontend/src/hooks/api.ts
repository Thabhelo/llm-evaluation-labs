import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import * as api from '../api/client'
import type {
  Model,
  Prompt,
  Evaluation,
  FailureCase,
  ModelFilter,
  PromptFilter,
  EvaluationFilter,
  FailureFilter,
} from '../types/api'

// Models
export function useModels(filters?: ModelFilter) {
  return useQuery({
    queryKey: ['models', filters],
    queryFn: () => api.getModels(filters),
  })
}

export function useModel(id: string) {
  return useQuery({
    queryKey: ['model', id],
    queryFn: () => api.getModel(id),
    enabled: !!id,
  })
}

export function useCreateModel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (model: Partial<Model>) => api.createModel(model),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['models'] })
    },
  })
}

export function useUpdateModel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, model }: { id: string; model: Partial<Model> }) =>
      api.updateModel(id, model),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['models'] })
      queryClient.invalidateQueries({ queryKey: ['model', id] })
    },
  })
}

export function useDeleteModel() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => api.deleteModel(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['models'] })
    },
  })
}

// Prompts
export function usePrompts(filters?: PromptFilter) {
  return useQuery({
    queryKey: ['prompts', filters],
    queryFn: () => api.getPrompts(filters),
  })
}

export function usePrompt(id: string) {
  return useQuery({
    queryKey: ['prompt', id],
    queryFn: () => api.getPrompt(id),
    enabled: !!id,
  })
}

export function useCreatePrompt() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (prompt: Partial<Prompt>) => api.createPrompt(prompt),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] })
    },
  })
}

export function useUpdatePrompt() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, prompt }: { id: string; prompt: Partial<Prompt> }) =>
      api.updatePrompt(id, prompt),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] })
      queryClient.invalidateQueries({ queryKey: ['prompt', id] })
    },
  })
}

export function useDeletePrompt() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => api.deletePrompt(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] })
    },
  })
}

// Evaluations
export function useEvaluations(filters?: EvaluationFilter) {
  return useQuery({
    queryKey: ['evaluations', filters],
    queryFn: () => api.getEvaluations(filters),
  })
}

export function useEvaluation(id: string) {
  return useQuery({
    queryKey: ['evaluation', id],
    queryFn: () => api.getEvaluation(id),
    enabled: !!id,
  })
}

export function useCreateEvaluation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (evaluation: Partial<Evaluation>) => api.createEvaluation(evaluation),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
    },
  })
}

export function useDeleteEvaluation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => api.deleteEvaluation(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
    },
  })
}

// Failures
export function useFailures(filters?: FailureFilter) {
  return useQuery({
    queryKey: ['failures', filters],
    queryFn: () => api.getFailures(filters),
  })
}

export function useFailure(id: string) {
  return useQuery({
    queryKey: ['failure', id],
    queryFn: () => api.getFailure(id),
    enabled: !!id,
  })
}

export function useCreateFailure() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (failure: Partial<FailureCase>) => api.createFailure(failure),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['failures'] })
    },
  })
}

export function useUpdateFailure() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, failure }: { id: string; failure: Partial<FailureCase> }) =>
      api.updateFailure(id, failure),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['failures'] })
      queryClient.invalidateQueries({ queryKey: ['failure', id] })
    },
  })
}

export function useDeleteFailure() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => api.deleteFailure(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['failures'] })
    },
  })
}

// Analytics
export function useRegressionLogs(modelId: string) {
  return useQuery({
    queryKey: ['regressions', modelId],
    queryFn: () => api.getRegressionLogs(modelId),
    enabled: !!modelId,
  })
}

export function useModelPerformance(modelId: string) {
  return useQuery({
    queryKey: ['performance', modelId],
    queryFn: () => api.getModelPerformance(modelId),
    enabled: !!modelId,
  })
}

export function useEvaluationTrends() {
  return useQuery({
    queryKey: ['trends'],
    queryFn: () => api.getEvaluationTrends(),
  })
} 
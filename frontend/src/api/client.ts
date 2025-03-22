import axios from 'axios'
import type {
  Model,
  Prompt,
  Evaluation,
  FailureCase,
  RegressionLog,
  PaginatedResponse,
  ModelFilter,
  PromptFilter,
  EvaluationFilter,
  FailureFilter,
} from '../types/api'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Models
export const getModels = async (filters?: ModelFilter): Promise<PaginatedResponse<Model>> => {
  const { data } = await api.get('/models', { params: filters })
  return data
}

export const getModel = async (id: string): Promise<Model> => {
  const { data } = await api.get(`/models/${id}`)
  return data
}

export const createModel = async (model: Partial<Model>): Promise<Model> => {
  const { data } = await api.post('/models', model)
  return data
}

export const updateModel = async (id: string, model: Partial<Model>): Promise<Model> => {
  const { data } = await api.put(`/models/${id}`, model)
  return data
}

export const deleteModel = async (id: string): Promise<void> => {
  await api.delete(`/models/${id}`)
}

// Prompts
export const getPrompts = async (filters?: PromptFilter): Promise<PaginatedResponse<Prompt>> => {
  const { data } = await api.get('/prompts', { params: filters })
  return data
}

export const getPrompt = async (id: string): Promise<Prompt> => {
  const { data } = await api.get(`/prompts/${id}`)
  return data
}

export const createPrompt = async (prompt: Partial<Prompt>): Promise<Prompt> => {
  const { data } = await api.post('/prompts', prompt)
  return data
}

export const updatePrompt = async (id: string, prompt: Partial<Prompt>): Promise<Prompt> => {
  const { data } = await api.put(`/prompts/${id}`, prompt)
  return data
}

export const deletePrompt = async (id: string): Promise<void> => {
  await api.delete(`/prompts/${id}`)
}

// Evaluations
export const getEvaluations = async (filters?: EvaluationFilter): Promise<PaginatedResponse<Evaluation>> => {
  const { data } = await api.get('/evaluations', { params: filters })
  return data
}

export const getEvaluation = async (id: string): Promise<Evaluation> => {
  const { data } = await api.get(`/evaluations/${id}`)
  return data
}

export const createEvaluation = async (evaluation: Partial<Evaluation>): Promise<Evaluation> => {
  const { data } = await api.post('/evaluations', evaluation)
  return data
}

export const deleteEvaluation = async (id: string): Promise<void> => {
  await api.delete(`/evaluations/${id}`)
}

// Failures
export const getFailures = async (filters?: FailureFilter): Promise<PaginatedResponse<FailureCase>> => {
  const { data } = await api.get('/failures', { params: filters })
  return data
}

export const getFailure = async (id: string): Promise<FailureCase> => {
  const { data } = await api.get(`/failures/${id}`)
  return data
}

export const createFailure = async (failure: Partial<FailureCase>): Promise<FailureCase> => {
  const { data } = await api.post('/failures', failure)
  return data
}

export const updateFailure = async (id: string, failure: Partial<FailureCase>): Promise<FailureCase> => {
  const { data } = await api.put(`/failures/${id}`, failure)
  return data
}

export const deleteFailure = async (id: string): Promise<void> => {
  await api.delete(`/failures/${id}`)
}

// Analytics
export const getRegressionLogs = async (modelId: string): Promise<RegressionLog[]> => {
  const { data } = await api.get(`/analytics/regressions/${modelId}`)
  return data
}

export const getModelPerformance = async (modelId: string): Promise<Record<string, number>> => {
  const { data } = await api.get(`/analytics/performance/${modelId}`)
  return data
}

export const getEvaluationTrends = async (): Promise<Record<string, any>> => {
  const { data } = await api.get('/analytics/trends')
  return data
}

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message
    throw new Error(message)
  }
) 
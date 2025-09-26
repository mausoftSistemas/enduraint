import api from './api'
import { notificationService } from './notificationService'

class AnalyticsService {
  // Obtener datos de análisis para entrenadores
  async getCoachAnalytics(coachId, filters = {}) {
    try {
      const response = await api.get(`/coaches/${coachId}/analytics`, {
        params: filters
      })
      return response.data
    } catch (error) {
      console.error('Error fetching coach analytics:', error)
      throw error
    }
  }

  // Obtener datos de análisis para estudiantes
  async getStudentAnalytics(studentId, filters = {}) {
    try {
      const response = await api.get(`/students/${studentId}/analytics`, {
        params: filters
      })
      return response.data
    } catch (error) {
      console.error('Error fetching student analytics:', error)
      throw error
    }
  }

  // Obtener métricas de rendimiento
  async getPerformanceMetrics(userId, userType, period = '30d') {
    try {
      const endpoint = userType === 'coach' 
        ? `/coaches/${userId}/performance-metrics`
        : `/students/${userId}/performance-metrics`
      
      const response = await api.get(endpoint, {
        params: { period }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching performance metrics:', error)
      throw error
    }
  }

  // Obtener datos de progreso
  async getProgressData(userId, userType, timeRange = '3m') {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/progress`
        : `/students/${userId}/progress`
      
      const response = await api.get(endpoint, {
        params: { timeRange }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching progress data:', error)
      throw error
    }
  }

  // Obtener comparativas (solo para entrenadores)
  async getComparativeData(coachId, studentIds = [], metric = 'performance') {
    try {
      const response = await api.post(`/coaches/${coachId}/comparative-analysis`, {
        studentIds,
        metric
      })
      return response.data
    } catch (error) {
      console.error('Error fetching comparative data:', error)
      throw error
    }
  }

  // Obtener actividades recientes
  async getRecentActivities(userId, userType, limit = 10) {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/recent-activities`
        : `/students/${userId}/recent-activities`
      
      const response = await api.get(endpoint, {
        params: { limit }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching recent activities:', error)
      throw error
    }
  }

  // Obtener estadísticas de objetivos
  async getGoalsStatistics(userId, userType) {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/goals-statistics`
        : `/students/${userId}/goals-statistics`
      
      const response = await api.get(endpoint)
      return response.data
    } catch (error) {
      console.error('Error fetching goals statistics:', error)
      throw error
    }
  }

  // Exportar datos de análisis
  async exportAnalyticsData(userId, userType, format = 'csv', filters = {}) {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/analytics/export`
        : `/students/${userId}/analytics/export`
      
      const response = await api.get(endpoint, {
        params: { format, ...filters },
        responseType: 'blob'
      })
      
      // Crear y descargar el archivo
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `analytics-${userId}-${Date.now()}.${format}`
      link.click()
      window.URL.revokeObjectURL(url)
      
      notificationService.showSuccess('Datos exportados correctamente')
      return true
    } catch (error) {
      console.error('Error exporting analytics data:', error)
      notificationService.showError('Error al exportar los datos')
      throw error
    }
  }

  // Obtener insights automáticos
  async getAutomatedInsights(userId, userType) {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/insights`
        : `/students/${userId}/insights`
      
      const response = await api.get(endpoint)
      return response.data
    } catch (error) {
      console.error('Error fetching automated insights:', error)
      throw error
    }
  }

  // Generar reporte personalizado
  async generateCustomReport(userId, userType, reportConfig) {
    try {
      const endpoint = userType === 'coach'
        ? `/coaches/${userId}/custom-report`
        : `/students/${userId}/custom-report`
      
      const response = await api.post(endpoint, reportConfig)
      return response.data
    } catch (error) {
      console.error('Error generating custom report:', error)
      throw error
    }
  }
}

export const analyticsService = new AnalyticsService()
export default analyticsService
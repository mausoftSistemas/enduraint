import { fetchGetRequest, fetchPostRequest, fetchPutRequest, fetchDeleteRequest } from '@/utils/serviceUtils'
import { garminConnect } from './garminConnectService'
import { strava } from './stravaService'

export const coachStudentIntegrations = {
  // Métodos para entrenadores - gestión de integraciones de alumnos
  
  /**
   * Obtiene el estado de integraciones de un alumno específico
   * @param {number} studentId - ID del alumno
   */
  getStudentIntegrationStatus(studentId) {
    return fetchGetRequest(`coach/students/${studentId}/integrations`)
  },

  /**
   * Obtiene estadísticas de sincronización de un alumno
   * @param {number} studentId - ID del alumno
   */
  getStudentSyncStats(studentId) {
    return fetchGetRequest(`coach/students/${studentId}/integrations/stats`)
  },

  /**
   * Obtiene el historial de sincronización de un alumno
   * @param {number} studentId - ID del alumno
   * @param {number} limit - Límite de registros (opcional)
   */
  getStudentSyncHistory(studentId, limit = 10) {
    return fetchGetRequest(`coach/students/${studentId}/integrations/history?limit=${limit}`)
  },

  /**
   * Fuerza la sincronización de datos de un alumno desde Garmin
   * @param {number} studentId - ID del alumno
   * @param {number} days - Días hacia atrás para sincronizar
   */
  forceStudentGarminSync(studentId, days = 7) {
    return fetchPostRequest(`coach/students/${studentId}/integrations/garmin/sync`, { days })
  },

  /**
   * Fuerza la sincronización de datos de un alumno desde Strava
   * @param {number} studentId - ID del alumno
   * @param {number} days - Días hacia atrás para sincronizar
   */
  forceStudentStravaSync(studentId, days = 7) {
    return fetchPostRequest(`coach/students/${studentId}/integrations/strava/sync`, { days })
  },

  /**
   * Actualiza la configuración de sincronización de un alumno
   * @param {number} studentId - ID del alumno
   * @param {Object} settings - Configuración de sincronización
   */
  updateStudentSyncSettings(studentId, settings) {
    return fetchPutRequest(`coach/students/${studentId}/integrations/settings`, settings)
  },

  /**
   * Obtiene las actividades sincronizadas de un alumno por fuente
   * @param {number} studentId - ID del alumno
   * @param {string} source - Fuente ('garmin' o 'strava')
   * @param {number} days - Días hacia atrás
   */
  getStudentActivitiesBySource(studentId, source, days = 30) {
    return fetchGetRequest(`coach/students/${studentId}/integrations/${source}/activities?days=${days}`)
  },

  // Métodos para alumnos - gestión de sus propias integraciones
  
  /**
   * Obtiene el estado de integraciones del alumno actual
   */
  getMyIntegrationStatus() {
    return fetchGetRequest('student/integrations')
  },

  /**
   * Obtiene estadísticas de sincronización del alumno actual
   */
  getMySyncStats() {
    return fetchGetRequest('student/integrations/stats')
  },

  /**
   * Obtiene el historial de sincronización del alumno actual
   * @param {number} limit - Límite de registros
   */
  getMySyncHistory(limit = 20) {
    return fetchGetRequest(`student/integrations/history?limit=${limit}`)
  },

  /**
   * Actualiza la configuración de sincronización del alumno actual
   * @param {Object} settings - Configuración de sincronización
   */
  updateMySyncSettings(settings) {
    return fetchPutRequest('student/integrations/settings', settings)
  },

  /**
   * Solicita sincronización manual de Garmin para el alumno actual
   * @param {number} days - Días hacia atrás para sincronizar
   */
  requestGarminSync(days = 7) {
    return fetchPostRequest('student/integrations/garmin/sync', { days })
  },

  /**
   * Solicita sincronización manual de Strava para el alumno actual
   * @param {number} days - Días hacia atrás para sincronizar
   */
  requestStravaSync(days = 7) {
    return fetchPostRequest('student/integrations/strava/sync', { days })
  },

  /**
   * Obtiene las actividades del alumno actual por fuente
   * @param {string} source - Fuente ('garmin' o 'strava')
   * @param {number} days - Días hacia atrás
   */
  getMyActivitiesBySource(source, days = 30) {
    return fetchGetRequest(`student/integrations/${source}/activities?days=${days}`)
  },

  // Métodos de utilidad que extienden los servicios existentes
  
  /**
   * Wrapper para conectar Garmin con notificaciones mejoradas
   * @param {Object} credentials - Credenciales de Garmin
   */
  async connectGarminWithNotification(credentials) {
    try {
      const response = await garminConnect.linkGarminConnect(credentials)
      // Aquí se podría agregar lógica adicional como notificar al entrenador
      return response
    } catch (error) {
      throw new Error(`Error conectando con Garmin: ${error.message}`)
    }
  },

  /**
   * Wrapper para conectar Strava con notificaciones mejoradas
   * @param {string} state - Estado único para la conexión
   * @param {string} clientId - Client ID de Strava
   */
  async connectStravaWithNotification(state, clientId) {
    try {
      await strava.setUniqueUserStateStravaLink(state)
      strava.linkStrava(state, clientId)
      // Aquí se podría agregar lógica adicional como notificar al entrenador
    } catch (error) {
      throw new Error(`Error conectando con Strava: ${error.message}`)
    }
  },

  /**
   * Desconecta Garmin con notificaciones al entrenador
   */
  async disconnectGarminWithNotification() {
    try {
      const response = await garminConnect.unlinkGarminConnect()
      // Notificar al entrenador sobre la desconexión
      await this.notifyCoachIntegrationChange('garmin', 'disconnected')
      return response
    } catch (error) {
      throw new Error(`Error desconectando Garmin: ${error.message}`)
    }
  },

  /**
   * Desconecta Strava con notificaciones al entrenador
   */
  async disconnectStravaWithNotification() {
    try {
      const response = await strava.unlinkStrava()
      // Notificar al entrenador sobre la desconexión
      await this.notifyCoachIntegrationChange('strava', 'disconnected')
      return response
    } catch (error) {
      throw new Error(`Error desconectando Strava: ${error.message}`)
    }
  },

  /**
   * Notifica al entrenador sobre cambios en las integraciones
   * @param {string} integration - Tipo de integración ('garmin' o 'strava')
   * @param {string} action - Acción realizada ('connected', 'disconnected', 'sync_error')
   */
  notifyCoachIntegrationChange(integration, action) {
    return fetchPostRequest('student/integrations/notify-coach', {
      integration,
      action,
      timestamp: new Date().toISOString()
    })
  },

  /**
   * Obtiene recomendaciones de configuración de integraciones
   */
  getIntegrationRecommendations() {
    return fetchGetRequest('student/integrations/recommendations')
  },

  /**
   * Verifica la salud de las integraciones
   */
  checkIntegrationsHealth() {
    return fetchGetRequest('student/integrations/health-check')
  },

  /**
   * Obtiene métricas de rendimiento de las integraciones
   */
  getIntegrationMetrics() {
    return fetchGetRequest('student/integrations/metrics')
  },

  /**
   * Programa una sincronización automática
   * @param {Object} schedule - Configuración del horario
   */
  scheduleAutoSync(schedule) {
    return fetchPostRequest('student/integrations/schedule', schedule)
  },

  /**
   * Cancela la sincronización automática
   */
  cancelAutoSync() {
    return fetchDeleteRequest('student/integrations/schedule')
  }
}

export default coachStudentIntegrations
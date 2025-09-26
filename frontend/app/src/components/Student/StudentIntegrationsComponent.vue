<template>
  <div class="student-integrations">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="fas fa-link me-2"></i>
          Mis Integraciones
        </h5>
        <p class="text-muted mb-0">Conecta tus dispositivos y aplicaciones para sincronizar automáticamente tus entrenamientos</p>
      </div>
      <div class="card-body">
        <!-- Garmin Connect Integration -->
        <div class="integration-card mb-4">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <img src="/src/assets/garminconnect/Garmin_Connect_app_1024x1024-02.png" 
                   alt="Garmin Connect" height="48" class="me-3">
              <div>
                <h6 class="mb-1">Garmin Connect</h6>
                <p class="text-muted mb-0">Sincroniza actividades, métricas de salud y equipamiento</p>
                <span :class="garminStatus.class">{{ garminStatus.text }}</span>
              </div>
            </div>
            <div class="integration-actions">
              <div v-if="!isGarminConnected">
                <button class="btn btn-primary" 
                        @click="connectGarmin"
                        :disabled="connecting">
                  <i class="fas fa-plug" :class="{ 'fa-spin': connecting }"></i>
                  Conectar
                </button>
              </div>
              <div v-else class="d-flex flex-column align-items-end">
                <div class="mb-2">
                  <button class="btn btn-sm btn-outline-primary me-2" 
                          @click="syncGarmin"
                          :disabled="syncing">
                    <i class="fas fa-sync" :class="{ 'fa-spin': syncing }"></i>
                    Sincronizar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" 
                          @click="disconnectGarmin">
                    <i class="fas fa-unlink"></i>
                    Desconectar
                  </button>
                </div>
                <small class="text-muted">Última sync: {{ garminLastSync }}</small>
              </div>
            </div>
          </div>
          
          <!-- Garmin Settings -->
          <div v-if="isGarminConnected" class="mt-3 pt-3 border-top">
            <div class="row">
              <div class="col-md-6">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="garminSettings.syncActivities" 
                         @change="updateGarminSettings">
                  <label class="form-check-label">Sincronizar actividades</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="garminSettings.syncHealth" 
                         @change="updateGarminSettings">
                  <label class="form-check-label">Sincronizar datos de salud</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="garminSettings.syncGear" 
                         @change="updateGarminSettings">
                  <label class="form-check-label">Sincronizar equipamiento</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="garminSettings.autoSync" 
                         @change="updateGarminSettings">
                  <label class="form-check-label">Sincronización automática</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Strava Integration -->
        <div class="integration-card mb-4">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <img src="/src/assets/strava/strava-logo.png" 
                   alt="Strava" height="48" class="me-3">
              <div>
                <h6 class="mb-1">Strava</h6>
                <p class="text-muted mb-0">Importa actividades y segmentos de Strava</p>
                <span :class="stravaStatus.class">{{ stravaStatus.text }}</span>
              </div>
            </div>
            <div class="integration-actions">
              <div v-if="!isStravaConnected">
                <button class="btn btn-primary" 
                        @click="showStravaModal = true"
                        :disabled="connecting">
                  <i class="fas fa-plug" :class="{ 'fa-spin': connecting }"></i>
                  Conectar
                </button>
              </div>
              <div v-else class="d-flex flex-column align-items-end">
                <div class="mb-2">
                  <button class="btn btn-sm btn-outline-primary me-2" 
                          @click="syncStrava"
                          :disabled="syncing">
                    <i class="fas fa-sync" :class="{ 'fa-spin': syncing }"></i>
                    Sincronizar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" 
                          @click="disconnectStrava">
                    <i class="fas fa-unlink"></i>
                    Desconectar
                  </button>
                </div>
                <small class="text-muted">Última sync: {{ stravaLastSync }}</small>
              </div>
            </div>
          </div>
          
          <!-- Strava Settings -->
          <div v-if="isStravaConnected" class="mt-3 pt-3 border-top">
            <div class="row">
              <div class="col-md-6">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="stravaSettings.syncActivities" 
                         @change="updateStravaSettings">
                  <label class="form-check-label">Sincronizar actividades</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="stravaSettings.syncGear" 
                         @change="updateStravaSettings">
                  <label class="form-check-label">Sincronizar equipamiento</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" 
                         v-model="stravaSettings.autoSync" 
                         @change="updateStravaSettings">
                  <label class="form-check-label">Sincronización automática</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sync Statistics -->
        <div class="sync-statistics" v-if="isGarminConnected || isStravaConnected">
          <h6>Estadísticas de Sincronización</h6>
          <div class="row">
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.totalActivities }}</div>
                <div class="stat-label">Total Actividades</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.thisWeek }}</div>
                <div class="stat-label">Esta Semana</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.garminActivities }}</div>
                <div class="stat-label">Desde Garmin</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.stravaActivities }}</div>
                <div class="stat-label">Desde Strava</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Strava Connection Modal -->
    <div class="modal fade" id="stravaModal" tabindex="-1" v-if="showStravaModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Conectar con Strava</h5>
            <button type="button" class="btn-close" @click="showStravaModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Para conectar con Strava, necesitas proporcionar tu Client ID y Client Secret de la aplicación Strava.</p>
            <div class="mb-3">
              <label class="form-label">Client ID</label>
              <input type="text" class="form-control" v-model="stravaCredentials.clientId" 
                     placeholder="Tu Strava Client ID">
            </div>
            <div class="mb-3">
              <label class="form-label">Client Secret</label>
              <input type="password" class="form-control" v-model="stravaCredentials.clientSecret" 
                     placeholder="Tu Strava Client Secret">
            </div>
            <div class="alert alert-info">
              <small>
                <i class="fas fa-info-circle me-1"></i>
                Puedes obtener estas credenciales en tu 
                <a href="https://www.strava.com/settings/api" target="_blank">panel de desarrollador de Strava</a>
              </small>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showStravaModal = false">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="connectStrava" 
                    :disabled="!stravaCredentials.clientId || !stravaCredentials.clientSecret">
              Conectar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { garminConnect } from '@/services/garminConnectService'
import { strava } from '@/services/stravaService'

const authStore = useAuthStore()

const connecting = ref(false)
const syncing = ref(false)
const showStravaModal = ref(false)

const stravaCredentials = ref({
  clientId: '',
  clientSecret: ''
})

const garminSettings = ref({
  syncActivities: true,
  syncHealth: true,
  syncGear: true,
  autoSync: true
})

const stravaSettings = ref({
  syncActivities: true,
  syncGear: true,
  autoSync: true
})

const syncStats = ref({
  totalActivities: 0,
  thisWeek: 0,
  garminActivities: 0,
  stravaActivities: 0
})

const isGarminConnected = computed(() => {
  return authStore.user?.is_garminconnect_linked === 1
})

const isStravaConnected = computed(() => {
  return authStore.user?.is_strava_linked === 1
})

const garminStatus = computed(() => {
  if (isGarminConnected.value) {
    return {
      text: 'Conectado',
      class: 'badge bg-success'
    }
  }
  return {
    text: 'No conectado',
    class: 'badge bg-secondary'
  }
})

const stravaStatus = computed(() => {
  if (isStravaConnected.value) {
    return {
      text: 'Conectado',
      class: 'badge bg-success'
    }
  }
  return {
    text: 'No conectado',
    class: 'badge bg-secondary'
  }
})

const garminLastSync = ref('2 horas')
const stravaLastSync = ref('1 hora')

const connectGarmin = () => {
  // Implementar conexión con Garmin
  console.log('Conectando con Garmin...')
}

const connectStrava = async () => {
  connecting.value = true
  try {
    // Usar el servicio existente de Strava
    const array = new Uint8Array(16)
    window.crypto.getRandomValues(array)
    const state = Array.from(array, (byte) => byte.toString(16).padStart(2, '0')).join('')
    
    await strava.setUniqueUserStateStravaLink(state)
    await strava.setUserStravaClientSettings(stravaCredentials.value.clientId, stravaCredentials.value.clientSecret)
    strava.linkStrava(state, stravaCredentials.value.clientId)
    
    showStravaModal.value = false
  } catch (error) {
    console.error('Error conectando con Strava:', error)
  } finally {
    connecting.value = false
  }
}

const syncGarmin = async () => {
  syncing.value = true
  try {
    await garminConnect.getGarminConnectActivitiesLastDays(7)
    garminLastSync.value = 'Ahora'
    loadSyncStats()
  } catch (error) {
    console.error('Error sincronizando Garmin:', error)
  } finally {
    syncing.value = false
  }
}

const syncStrava = async () => {
  syncing.value = true
  try {
    await strava.getStravaActivitiesLastDays(7)
    stravaLastSync.value = 'Ahora'
    loadSyncStats()
  } catch (error) {
    console.error('Error sincronizando Strava:', error)
  } finally {
    syncing.value = false
  }
}

const disconnectGarmin = async () => {
  try {
    await garminConnect.unlinkGarminConnect()
    // Actualizar estado del usuario
    const user = authStore.user
    user.is_garminconnect_linked = 0
    authStore.setUser(user)
  } catch (error) {
    console.error('Error desconectando Garmin:', error)
  }
}

const disconnectStrava = async () => {
  try {
    await strava.unlinkStrava()
    // Actualizar estado del usuario
    const user = authStore.user
    user.is_strava_linked = 0
    authStore.setUser(user)
  } catch (error) {
    console.error('Error desconectando Strava:', error)
  }
}

const updateGarminSettings = () => {
  console.log('Configuración Garmin actualizada:', garminSettings.value)
}

const updateStravaSettings = () => {
  console.log('Configuración Strava actualizada:', stravaSettings.value)
}

const loadSyncStats = () => {
  // Simular carga de estadísticas
  syncStats.value = {
    totalActivities: Math.floor(Math.random() * 200) + 100,
    thisWeek: Math.floor(Math.random() * 15) + 5,
    garminActivities: Math.floor(Math.random() * 100) + 50,
    stravaActivities: Math.floor(Math.random() * 100) + 50
  }
}

onMounted(() => {
  loadSyncStats()
})
</script>

<style scoped>
.integration-card {
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  background-color: #f8f9fa;
}

.integration-actions {
  min-width: 200px;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: white;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.stat-number {
  font-size: 1.75rem;
  font-weight: bold;
  color: #0d6efd;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.sync-statistics {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e9ecef;
}

.modal {
  display: block;
  background-color: rgba(0,0,0,0.5);
}
</style>
<template>
  <div class="coach-student-integrations">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="fas fa-link me-2"></i>
          Integraciones del Alumno: {{ studentName }}
        </h5>
      </div>
      <div class="card-body">
        <!-- Estado de integraciones -->
        <div class="row mb-4">
          <div class="col-md-6">
            <div class="integration-status">
              <div class="d-flex align-items-center mb-3">
                <img src="/src/assets/garminconnect/Garmin_Connect_app_1024x1024-02.png" 
                     alt="Garmin Connect" height="32" class="me-3">
                <div>
                  <h6 class="mb-1">Garmin Connect</h6>
                  <span :class="garminStatus.class">{{ garminStatus.text }}</span>
                </div>
              </div>
              <div v-if="student.is_garminconnect_linked">
                <small class="text-muted">Última sincronización: {{ garminStatus.lastSync }}</small>
                <div class="mt-2">
                  <button class="btn btn-sm btn-outline-primary me-2" 
                          @click="syncGarminData"
                          :disabled="syncing">
                    <i class="fas fa-sync" :class="{ 'fa-spin': syncing }"></i>
                    Sincronizar
                  </button>
                  <button class="btn btn-sm btn-outline-info" 
                          @click="viewGarminActivities">
                    <i class="fas fa-eye"></i>
                    Ver Actividades
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="integration-status">
              <div class="d-flex align-items-center mb-3">
                <img src="/src/assets/strava/strava-logo.png" 
                     alt="Strava" height="32" class="me-3">
                <div>
                  <h6 class="mb-1">Strava</h6>
                  <span :class="stravaStatus.class">{{ stravaStatus.text }}</span>
                </div>
              </div>
              <div v-if="student.is_strava_linked">
                <small class="text-muted">Última sincronización: {{ stravaStatus.lastSync }}</small>
                <div class="mt-2">
                  <button class="btn btn-sm btn-outline-primary me-2" 
                          @click="syncStravaData"
                          :disabled="syncing">
                    <i class="fas fa-sync" :class="{ 'fa-spin': syncing }"></i>
                    Sincronizar
                  </button>
                  <button class="btn btn-sm btn-outline-info" 
                          @click="viewStravaActivities">
                    <i class="fas fa-eye"></i>
                    Ver Actividades
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Estadísticas de sincronización -->
        <div class="sync-stats mb-4" v-if="student.is_garminconnect_linked || student.is_strava_linked">
          <h6>Estadísticas de Sincronización</h6>
          <div class="row">
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.totalActivities }}</div>
                <div class="stat-label">Actividades Totales</div>
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
                <div class="stat-number">{{ syncStats.thisMonth }}</div>
                <div class="stat-label">Este Mes</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-number">{{ syncStats.lastSync }}</div>
                <div class="stat-label">Última Sync</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Configuración de sincronización -->
        <div class="sync-settings">
          <h6>Configuración de Sincronización</h6>
          <div class="row">
            <div class="col-md-6">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" 
                       v-model="syncSettings.autoSync" 
                       @change="updateSyncSettings">
                <label class="form-check-label">
                  Sincronización automática
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" 
                       v-model="syncSettings.syncGear" 
                       @change="updateSyncSettings">
                <label class="form-check-label">
                  Sincronizar equipamiento
                </label>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label class="form-label">Frecuencia de sincronización</label>
                <select class="form-select" v-model="syncSettings.frequency" 
                        @change="updateSyncSettings">
                  <option value="hourly">Cada hora</option>
                  <option value="daily">Diaria</option>
                  <option value="weekly">Semanal</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Historial de sincronización -->
        <div class="sync-history mt-4" v-if="syncHistory.length > 0">
          <h6>Historial de Sincronización</h6>
          <div class="table-responsive">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Fuente</th>
                  <th>Actividades</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sync in syncHistory" :key="sync.id">
                  <td>{{ formatDate(sync.date) }}</td>
                  <td>
                    <span class="badge" :class="sync.source === 'garmin' ? 'bg-success' : 'bg-primary'">
                      {{ sync.source === 'garmin' ? 'Garmin' : 'Strava' }}
                    </span>
                  </td>
                  <td>{{ sync.activities }}</td>
                  <td>
                    <span class="badge" :class="sync.status === 'success' ? 'bg-success' : 'bg-danger'">
                      {{ sync.status === 'success' ? 'Exitoso' : 'Error' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { garminConnect } from '@/services/garminConnectService'
import { strava } from '@/services/stravaService'

const props = defineProps({
  student: {
    type: Object,
    required: true
  },
  studentName: {
    type: String,
    required: true
  }
})

const syncing = ref(false)
const syncSettings = ref({
  autoSync: true,
  syncGear: true,
  frequency: 'daily'
})

const syncStats = ref({
  totalActivities: 0,
  thisWeek: 0,
  thisMonth: 0,
  lastSync: '2 horas'
})

const syncHistory = ref([
  {
    id: 1,
    date: new Date(Date.now() - 2 * 60 * 60 * 1000),
    source: 'garmin',
    activities: 3,
    status: 'success'
  },
  {
    id: 2,
    date: new Date(Date.now() - 24 * 60 * 60 * 1000),
    source: 'strava',
    activities: 1,
    status: 'success'
  }
])

const garminStatus = computed(() => {
  if (props.student.is_garminconnect_linked) {
    return {
      text: 'Conectado',
      class: 'badge bg-success',
      lastSync: '2 horas'
    }
  }
  return {
    text: 'No conectado',
    class: 'badge bg-secondary',
    lastSync: null
  }
})

const stravaStatus = computed(() => {
  if (props.student.is_strava_linked) {
    return {
      text: 'Conectado',
      class: 'badge bg-success',
      lastSync: '1 hora'
    }
  }
  return {
    text: 'No conectado',
    class: 'badge bg-secondary',
    lastSync: null
  }
})

const syncGarminData = async () => {
  syncing.value = true
  try {
    await garminConnect.getGarminConnectActivitiesLastDays(7)
    // Actualizar estadísticas
    loadSyncStats()
  } catch (error) {
    console.error('Error sincronizando Garmin:', error)
  } finally {
    syncing.value = false
  }
}

const syncStravaData = async () => {
  syncing.value = true
  try {
    await strava.getStravaActivitiesLastDays(7)
    // Actualizar estadísticas
    loadSyncStats()
  } catch (error) {
    console.error('Error sincronizando Strava:', error)
  } finally {
    syncing.value = false
  }
}

const viewGarminActivities = () => {
  // Navegar a vista de actividades filtradas por Garmin
  console.log('Ver actividades de Garmin')
}

const viewStravaActivities = () => {
  // Navegar a vista de actividades filtradas por Strava
  console.log('Ver actividades de Strava')
}

const updateSyncSettings = () => {
  // Guardar configuración de sincronización
  console.log('Configuración actualizada:', syncSettings.value)
}

const loadSyncStats = () => {
  // Simular carga de estadísticas
  syncStats.value = {
    totalActivities: Math.floor(Math.random() * 100) + 50,
    thisWeek: Math.floor(Math.random() * 10) + 5,
    thisMonth: Math.floor(Math.random() * 30) + 15,
    lastSync: 'Ahora'
  }
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  loadSyncStats()
})
</script>

<style scoped>
.integration-status {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: white;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0d6efd;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.sync-settings {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
}

.sync-history {
  max-height: 300px;
  overflow-y: auto;
}
</style>
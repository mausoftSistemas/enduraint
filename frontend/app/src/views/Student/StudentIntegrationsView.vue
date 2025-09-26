<template>
  <div class="student-integrations-view">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">
                <i class="fas fa-link me-2"></i>
                Integraciones
              </h2>
              <p class="text-muted mb-0">
                Conecta tus dispositivos y aplicaciones para sincronizar automáticamente tus entrenamientos
              </p>
            </div>
            <div>
              <button class="btn btn-outline-primary me-2" @click="refreshIntegrations">
                <i class="fas fa-refresh" :class="{ 'fa-spin': refreshing }"></i>
                Actualizar
              </button>
              <button class="btn btn-primary" @click="syncAllData" :disabled="syncing">
                <i class="fas fa-sync" :class="{ 'fa-spin': syncing }"></i>
                Sincronizar Todo
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Integration Status Cards -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card integration-status-card">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="integration-icon garmin-icon">
                  <img src="/src/assets/garminconnect/Garmin_Connect_app_1024x1024-02.png" 
                       alt="Garmin" height="40">
                </div>
                <div class="flex-grow-1 ms-3">
                  <h5 class="mb-1">Garmin Connect</h5>
                  <p class="text-muted mb-2">Dispositivos Garmin y datos de salud</p>
                  <span :class="garminStatusClass">{{ garminStatusText }}</span>
                </div>
                <div class="integration-stats">
                  <div class="stat-item">
                    <div class="stat-number">{{ garminStats.activities }}</div>
                    <div class="stat-label">Actividades</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card integration-status-card">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="integration-icon strava-icon">
                  <img src="/src/assets/strava/strava-logo.png" 
                       alt="Strava" height="40">
                </div>
                <div class="flex-grow-1 ms-3">
                  <h5 class="mb-1">Strava</h5>
                  <p class="text-muted mb-2">Actividades y segmentos</p>
                  <span :class="stravaStatusClass">{{ stravaStatusText }}</span>
                </div>
                <div class="integration-stats">
                  <div class="stat-item">
                    <div class="stat-number">{{ stravaStats.activities }}</div>
                    <div class="stat-label">Actividades</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Integration Component -->
      <div class="row">
        <div class="col-12">
          <StudentIntegrationsComponent />
        </div>
      </div>

      <!-- Recent Sync Activity -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">
                <i class="fas fa-history me-2"></i>
                Actividad de Sincronización Reciente
              </h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Fuente</th>
                      <th>Tipo</th>
                      <th>Elementos</th>
                      <th>Estado</th>
                      <th>Duración</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sync in recentSyncs" :key="sync.id">
                      <td>{{ formatDateTime(sync.date) }}</td>
                      <td>
                        <span class="badge" :class="sync.source === 'garmin' ? 'bg-success' : 'bg-primary'">
                          <i :class="sync.source === 'garmin' ? 'fas fa-heartbeat' : 'fab fa-strava'"></i>
                          {{ sync.source === 'garmin' ? 'Garmin' : 'Strava' }}
                        </span>
                      </td>
                      <td>{{ sync.type }}</td>
                      <td>
                        <span class="badge bg-info">{{ sync.items }}</span>
                      </td>
                      <td>
                        <span class="badge" :class="sync.status === 'success' ? 'bg-success' : sync.status === 'error' ? 'bg-danger' : 'bg-warning'">
                          <i :class="sync.status === 'success' ? 'fas fa-check' : sync.status === 'error' ? 'fas fa-times' : 'fas fa-clock'"></i>
                          {{ sync.status === 'success' ? 'Exitoso' : sync.status === 'error' ? 'Error' : 'En progreso' }}
                        </span>
                      </td>
                      <td>{{ sync.duration }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import StudentIntegrationsComponent from '@/components/Student/StudentIntegrationsComponent.vue'

const authStore = useAuthStore()

const refreshing = ref(false)
const syncing = ref(false)

const garminStats = ref({
  activities: 0,
  lastSync: null
})

const stravaStats = ref({
  activities: 0,
  lastSync: null
})

const recentSyncs = ref([
  {
    id: 1,
    date: new Date(Date.now() - 2 * 60 * 60 * 1000),
    source: 'garmin',
    type: 'Actividades',
    items: 3,
    status: 'success',
    duration: '2.3s'
  },
  {
    id: 2,
    date: new Date(Date.now() - 4 * 60 * 60 * 1000),
    source: 'strava',
    type: 'Actividades',
    items: 1,
    status: 'success',
    duration: '1.8s'
  },
  {
    id: 3,
    date: new Date(Date.now() - 24 * 60 * 60 * 1000),
    source: 'garmin',
    type: 'Datos de Salud',
    items: 7,
    status: 'success',
    duration: '3.1s'
  },
  {
    id: 4,
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    source: 'strava',
    type: 'Equipamiento',
    items: 2,
    status: 'error',
    duration: '0.5s'
  }
])

const garminStatusClass = computed(() => {
  if (authStore.user?.is_garminconnect_linked === 1) {
    return 'badge bg-success'
  }
  return 'badge bg-secondary'
})

const garminStatusText = computed(() => {
  if (authStore.user?.is_garminconnect_linked === 1) {
    return 'Conectado'
  }
  return 'No conectado'
})

const stravaStatusClass = computed(() => {
  if (authStore.user?.is_strava_linked === 1) {
    return 'badge bg-success'
  }
  return 'badge bg-secondary'
})

const stravaStatusText = computed(() => {
  if (authStore.user?.is_strava_linked === 1) {
    return 'Conectado'
  }
  return 'No conectado'
})

const refreshIntegrations = async () => {
  refreshing.value = true
  try {
    // Simular actualización de estado de integraciones
    await new Promise(resolve => setTimeout(resolve, 1000))
    loadStats()
  } catch (error) {
    console.error('Error actualizando integraciones:', error)
  } finally {
    refreshing.value = false
  }
}

const syncAllData = async () => {
  syncing.value = true
  try {
    // Simular sincronización de todos los datos
    await new Promise(resolve => setTimeout(resolve, 3000))
    loadStats()
    // Agregar nueva entrada al historial
    recentSyncs.value.unshift({
      id: Date.now(),
      date: new Date(),
      source: 'garmin',
      type: 'Sincronización Completa',
      items: Math.floor(Math.random() * 10) + 1,
      status: 'success',
      duration: '3.2s'
    })
  } catch (error) {
    console.error('Error sincronizando datos:', error)
  } finally {
    syncing.value = false
  }
}

const loadStats = () => {
  // Simular carga de estadísticas
  garminStats.value = {
    activities: Math.floor(Math.random() * 50) + 20,
    lastSync: new Date(Date.now() - 2 * 60 * 60 * 1000)
  }
  
  stravaStats.value = {
    activities: Math.floor(Math.random() * 30) + 10,
    lastSync: new Date(Date.now() - 1 * 60 * 60 * 1000)
  }
}

const formatDateTime = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.integration-status-card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.integration-status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.integration-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.garmin-icon {
  background-color: #e8f5e8;
}

.strava-icon {
  background-color: #fff3e0;
}

.integration-stats {
  text-align: center;
}

.stat-item {
  margin-bottom: 0.5rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0d6efd;
  display: block;
}

.stat-label {
  font-size: 0.75rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
  font-size: 0.875rem;
}

.table td {
  vertical-align: middle;
}

.badge {
  font-size: 0.75rem;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}
</style>
<template>
  <div class="training-analytics">
    <div class="row mb-4">
      <!-- Filtros y controles -->
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-3">
                <label class="form-label">Período de análisis</label>
                <select class="form-select" v-model="selectedPeriod" @change="updateAnalytics">
                  <option value="7">Última semana</option>
                  <option value="30">Último mes</option>
                  <option value="90">Últimos 3 meses</option>
                  <option value="365">Último año</option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Tipo de actividad</label>
                <select class="form-select" v-model="selectedActivityType" @change="updateAnalytics">
                  <option value="all">Todas</option>
                  <option value="running">Carrera</option>
                  <option value="cycling">Ciclismo</option>
                  <option value="swimming">Natación</option>
                  <option value="strength">Fuerza</option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Métrica principal</label>
                <select class="form-select" v-model="selectedMetric" @change="updateAnalytics">
                  <option value="distance">Distancia</option>
                  <option value="duration">Duración</option>
                  <option value="calories">Calorías</option>
                  <option value="heart_rate">Frecuencia Cardíaca</option>
                  <option value="pace">Ritmo</option>
                </select>
              </div>
              <div class="col-md-3">
                <div class="d-flex gap-2 mt-4">
                  <button class="btn btn-primary" @click="updateAnalytics" :disabled="loading">
                    <i class="fas fa-chart-line" :class="{ 'fa-spin': loading }"></i>
                    Actualizar
                  </button>
                  <button class="btn btn-outline-secondary" @click="exportData">
                    <i class="fas fa-download"></i>
                    Exportar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Métricas clave -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="metric-card">
          <div class="metric-icon bg-primary">
            <i class="fas fa-route"></i>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ formatMetric(keyMetrics.totalDistance, 'distance') }}</div>
            <div class="metric-label">Distancia Total</div>
            <div class="metric-change" :class="keyMetrics.distanceChange >= 0 ? 'positive' : 'negative'">
              <i :class="keyMetrics.distanceChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(keyMetrics.distanceChange) }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card">
          <div class="metric-icon bg-success">
            <i class="fas fa-clock"></i>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ formatMetric(keyMetrics.totalDuration, 'duration') }}</div>
            <div class="metric-label">Tiempo Total</div>
            <div class="metric-change" :class="keyMetrics.durationChange >= 0 ? 'positive' : 'negative'">
              <i :class="keyMetrics.durationChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(keyMetrics.durationChange) }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card">
          <div class="metric-icon bg-warning">
            <i class="fas fa-fire"></i>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ formatMetric(keyMetrics.totalCalories, 'calories') }}</div>
            <div class="metric-label">Calorías Quemadas</div>
            <div class="metric-change" :class="keyMetrics.caloriesChange >= 0 ? 'positive' : 'negative'">
              <i :class="keyMetrics.caloriesChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(keyMetrics.caloriesChange) }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card">
          <div class="metric-icon bg-info">
            <i class="fas fa-heartbeat"></i>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ formatMetric(keyMetrics.avgHeartRate, 'heart_rate') }}</div>
            <div class="metric-label">FC Promedio</div>
            <div class="metric-change" :class="keyMetrics.heartRateChange >= 0 ? 'positive' : 'negative'">
              <i :class="keyMetrics.heartRateChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(keyMetrics.heartRateChange) }}%
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficos principales -->
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-chart-line me-2"></i>
              Progreso de {{ getMetricLabel(selectedMetric) }}
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="progressChart" width="400" height="200"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-chart-pie me-2"></i>
              Distribución por Tipo
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="distributionChart" width="300" height="300"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Análisis de rendimiento -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-tachometer-alt me-2"></i>
              Análisis de Ritmo
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="paceChart" width="400" height="200"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-heart me-2"></i>
              Zonas de Frecuencia Cardíaca
            </h5>
          </div>
          <div class="card-body">
            <div class="hr-zones">
              <div class="hr-zone" v-for="zone in heartRateZones" :key="zone.name">
                <div class="zone-info">
                  <div class="zone-name" :style="{ color: zone.color }">{{ zone.name }}</div>
                  <div class="zone-range">{{ zone.range }}</div>
                </div>
                <div class="zone-bar">
                  <div class="zone-progress" 
                       :style="{ width: zone.percentage + '%', backgroundColor: zone.color }"></div>
                </div>
                <div class="zone-time">{{ zone.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de actividades recientes -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-list me-2"></i>
              Actividades Recientes
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Distancia</th>
                    <th>Duración</th>
                    <th>Ritmo</th>
                    <th>FC Promedio</th>
                    <th>Calorías</th>
                    <th>Fuente</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivities" :key="activity.id">
                    <td>{{ formatDate(activity.date) }}</td>
                    <td>
                      <span class="badge" :class="getActivityTypeClass(activity.type)">
                        <i :class="getActivityTypeIcon(activity.type)"></i>
                        {{ activity.type }}
                      </span>
                    </td>
                    <td>{{ formatMetric(activity.distance, 'distance') }}</td>
                    <td>{{ formatMetric(activity.duration, 'duration') }}</td>
                    <td>{{ formatMetric(activity.pace, 'pace') }}</td>
                    <td>{{ formatMetric(activity.avgHeartRate, 'heart_rate') }}</td>
                    <td>{{ formatMetric(activity.calories, 'calories') }}</td>
                    <td>
                      <span class="badge" :class="activity.source === 'garmin' ? 'bg-success' : 'bg-primary'">
                        {{ activity.source === 'garmin' ? 'Garmin' : 'Strava' }}
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
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  userId: {
    type: Number,
    default: null
  },
  isCoachView: {
    type: Boolean,
    default: false
  }
})

const loading = ref(false)
const selectedPeriod = ref('30')
const selectedActivityType = ref('all')
const selectedMetric = ref('distance')

const progressChart = ref(null)
const distributionChart = ref(null)
const paceChart = ref(null)

let progressChartInstance = null
let distributionChartInstance = null
let paceChartInstance = null

const keyMetrics = ref({
  totalDistance: 0,
  totalDuration: 0,
  totalCalories: 0,
  avgHeartRate: 0,
  distanceChange: 0,
  durationChange: 0,
  caloriesChange: 0,
  heartRateChange: 0
})

const heartRateZones = ref([
  { name: 'Zona 1 - Recuperación', range: '50-60%', percentage: 25, time: '2h 30m', color: '#28a745' },
  { name: 'Zona 2 - Aeróbica', range: '60-70%', percentage: 40, time: '4h 15m', color: '#17a2b8' },
  { name: 'Zona 3 - Tempo', range: '70-80%', percentage: 20, time: '1h 45m', color: '#ffc107' },
  { name: 'Zona 4 - Umbral', range: '80-90%', percentage: 10, time: '45m', color: '#fd7e14' },
  { name: 'Zona 5 - Neuromuscular', range: '90-100%', percentage: 5, time: '15m', color: '#dc3545' }
])

const recentActivities = ref([
  {
    id: 1,
    date: new Date(Date.now() - 24 * 60 * 60 * 1000),
    type: 'Carrera',
    distance: 10.5,
    duration: 3600,
    pace: 342,
    avgHeartRate: 165,
    calories: 650,
    source: 'garmin'
  },
  {
    id: 2,
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    type: 'Ciclismo',
    distance: 45.2,
    duration: 7200,
    pace: 159,
    avgHeartRate: 145,
    calories: 1200,
    source: 'strava'
  },
  {
    id: 3,
    date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    type: 'Natación',
    distance: 2.0,
    duration: 2400,
    pace: 1200,
    avgHeartRate: 155,
    calories: 400,
    source: 'garmin'
  }
])

const updateAnalytics = async () => {
  loading.value = true
  try {
    // Simular carga de datos
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Actualizar métricas clave
    keyMetrics.value = {
      totalDistance: Math.random() * 200 + 100,
      totalDuration: Math.random() * 50000 + 20000,
      totalCalories: Math.random() * 5000 + 2000,
      avgHeartRate: Math.random() * 40 + 140,
      distanceChange: (Math.random() - 0.5) * 20,
      durationChange: (Math.random() - 0.5) * 15,
      caloriesChange: (Math.random() - 0.5) * 25,
      heartRateChange: (Math.random() - 0.5) * 10
    }
    
    // Actualizar gráficos
    await nextTick()
    updateCharts()
  } catch (error) {
    console.error('Error actualizando analytics:', error)
  } finally {
    loading.value = false
  }
}

const updateCharts = () => {
  updateProgressChart()
  updateDistributionChart()
  updatePaceChart()
}

const updateProgressChart = () => {
  if (progressChartInstance) {
    progressChartInstance.destroy()
  }
  
  const ctx = progressChart.value.getContext('2d')
  const labels = generateDateLabels(parseInt(selectedPeriod.value))
  const data = generateProgressData(labels.length)
  
  progressChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: getMetricLabel(selectedMetric.value),
        data,
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

const updateDistributionChart = () => {
  if (distributionChartInstance) {
    distributionChartInstance.destroy()
  }
  
  const ctx = distributionChart.value.getContext('2d')
  
  distributionChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Carrera', 'Ciclismo', 'Natación', 'Fuerza'],
      datasets: [{
        data: [45, 30, 15, 10],
        backgroundColor: ['#0d6efd', '#198754', '#ffc107', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  })
}

const updatePaceChart = () => {
  if (paceChartInstance) {
    paceChartInstance.destroy()
  }
  
  const ctx = paceChart.value.getContext('2d')
  const labels = generateDateLabels(7)
  const paceData = generatePaceData(labels.length)
  
  paceChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Ritmo Promedio (min/km)',
        data: paceData,
        backgroundColor: '#198754'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

const generateDateLabels = (days) => {
  const labels = []
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(Date.now() - i * 24 * 60 * 60 * 1000)
    labels.push(date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }))
  }
  return labels
}

const generateProgressData = (length) => {
  const data = []
  let baseValue = Math.random() * 50 + 25
  for (let i = 0; i < length; i++) {
    baseValue += (Math.random() - 0.5) * 10
    data.push(Math.max(0, baseValue))
  }
  return data
}

const generatePaceData = (length) => {
  const data = []
  for (let i = 0; i < length; i++) {
    data.push(Math.random() * 2 + 4) // Entre 4 y 6 min/km
  }
  return data
}

const formatMetric = (value, type) => {
  if (!value) return '-'
  
  switch (type) {
    case 'distance':
      return `${value.toFixed(1)} km`
    case 'duration':
      const hours = Math.floor(value / 3600)
      const minutes = Math.floor((value % 3600) / 60)
      return `${hours}h ${minutes}m`
    case 'calories':
      return `${Math.round(value)} kcal`
    case 'heart_rate':
      return `${Math.round(value)} bpm`
    case 'pace':
      const paceMinutes = Math.floor(value / 60)
      const paceSeconds = value % 60
      return `${paceMinutes}:${paceSeconds.toString().padStart(2, '0')} /km`
    default:
      return value.toString()
  }
}

const getMetricLabel = (metric) => {
  const labels = {
    distance: 'Distancia',
    duration: 'Duración',
    calories: 'Calorías',
    heart_rate: 'Frecuencia Cardíaca',
    pace: 'Ritmo'
  }
  return labels[metric] || metric
}

const getActivityTypeClass = (type) => {
  const classes = {
    'Carrera': 'bg-primary',
    'Ciclismo': 'bg-success',
    'Natación': 'bg-info',
    'Fuerza': 'bg-warning'
  }
  return classes[type] || 'bg-secondary'
}

const getActivityTypeIcon = (type) => {
  const icons = {
    'Carrera': 'fas fa-running',
    'Ciclismo': 'fas fa-biking',
    'Natación': 'fas fa-swimmer',
    'Fuerza': 'fas fa-dumbbell'
  }
  return icons[type] || 'fas fa-dumbbell'
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

const exportData = () => {
  // Implementar exportación de datos
  console.log('Exportando datos...')
}

onMounted(() => {
  updateAnalytics()
})
</script>

<style scoped>
.metric-card {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  margin-right: 1rem;
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: bold;
  color: #212529;
  line-height: 1;
}

.metric-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0.25rem 0;
}

.metric-change {
  font-size: 0.75rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #198754;
}

.metric-change.negative {
  color: #dc3545;
}

.hr-zones {
  space-y: 1rem;
}

.hr-zone {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.zone-info {
  flex: 1;
  margin-right: 1rem;
}

.zone-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.zone-range {
  font-size: 0.75rem;
  color: #6c757d;
}

.zone-bar {
  flex: 2;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  margin: 0 1rem;
  overflow: hidden;
}

.zone-progress {
  height: 100%;
  transition: width 0.3s ease;
}

.zone-time {
  font-size: 0.75rem;
  font-weight: 600;
  color: #495057;
  min-width: 60px;
  text-align: right;
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
</style>
<template>
  <div class="student-progress">
    <!-- Header -->
    <div class="progress-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-1 text-white">Mi Progreso de Entrenamiento</h1>
          <p class="mb-0 text-white-50">Analiza tu rendimiento y evolución deportiva</p>
        </div>
        <div class="col-md-4 text-end">
          <div class="progress-summary text-white">
            <div class="row text-center">
              <div class="col-4">
                <div class="h4 mb-0">{{ totalActivities }}</div>
                <small class="text-white-50">Actividades</small>
              </div>
              <div class="col-4">
                <div class="h4 mb-0">{{ totalHours }}</div>
                <small class="text-white-50">Horas</small>
              </div>
              <div class="col-4">
                <div class="h4 mb-0">{{ totalDistance }}</div>
                <small class="text-white-50">Kilómetros</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Time Period Selector -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-6">
                <div class="btn-group" role="group">
                  <button 
                    v-for="period in timePeriods" 
                    :key="period.value"
                    class="btn" 
                    :class="selectedPeriod === period.value ? 'btn-primary' : 'btn-outline-primary'"
                    @click="selectedPeriod = period.value"
                  >
                    {{ period.label }}
                  </button>
                </div>
              </div>
              <div class="col-md-6 text-end">
                <div class="d-flex gap-2 justify-content-end">
                  <select class="form-select" style="width: auto;" v-model="selectedSport">
                    <option value="all">Todos los deportes</option>
                    <option value="running">Carrera</option>
                    <option value="cycling">Ciclismo</option>
                    <option value="swimming">Natación</option>
                  </select>
                  <button class="btn btn-outline-secondary" @click="exportData">
                    <font-awesome-icon icon="fas fa-download" class="me-2" />
                    Exportar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Metrics Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="metric-icon bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-running" />
            </div>
            <h3 class="mb-1">{{ currentPeriodStats.activities }}</h3>
            <p class="text-muted mb-2 small">Actividades</p>
            <div class="trend" :class="getTrendClass(currentPeriodStats.activitiesTrend)">
              <font-awesome-icon :icon="getTrendIcon(currentPeriodStats.activitiesTrend)" class="me-1" />
              <small>{{ Math.abs(currentPeriodStats.activitiesTrend) }}% vs período anterior</small>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="metric-icon bg-success bg-opacity-10 text-success rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-route" />
            </div>
            <h3 class="mb-1">{{ currentPeriodStats.distance }}</h3>
            <p class="text-muted mb-2 small">Kilómetros</p>
            <div class="trend" :class="getTrendClass(currentPeriodStats.distanceTrend)">
              <font-awesome-icon :icon="getTrendIcon(currentPeriodStats.distanceTrend)" class="me-1" />
              <small>{{ Math.abs(currentPeriodStats.distanceTrend) }}% vs período anterior</small>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="metric-icon bg-info bg-opacity-10 text-info rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-clock" />
            </div>
            <h3 class="mb-1">{{ currentPeriodStats.duration }}</h3>
            <p class="text-muted mb-2 small">Horas entrenadas</p>
            <div class="trend" :class="getTrendClass(currentPeriodStats.durationTrend)">
              <font-awesome-icon :icon="getTrendIcon(currentPeriodStats.durationTrend)" class="me-1" />
              <small>{{ Math.abs(currentPeriodStats.durationTrend) }}% vs período anterior</small>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="metric-icon bg-warning bg-opacity-10 text-warning rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-tachometer-alt" />
            </div>
            <h3 class="mb-1">{{ currentPeriodStats.avgPace }}</h3>
            <p class="text-muted mb-2 small">Ritmo promedio</p>
            <div class="trend" :class="getTrendClass(currentPeriodStats.paceTrend)">
              <font-awesome-icon :icon="getTrendIcon(currentPeriodStats.paceTrend)" class="me-1" />
              <small>{{ Math.abs(currentPeriodStats.paceTrend) }}% vs período anterior</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Activity Chart -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-chart-line" class="me-2 text-primary" />
                Evolución de Actividades
              </h5>
              <div class="chart-controls">
                <div class="btn-group btn-group-sm" role="group">
                  <button 
                    v-for="metric in chartMetrics" 
                    :key="metric.value"
                    class="btn" 
                    :class="selectedMetric === metric.value ? 'btn-primary' : 'btn-outline-primary'"
                    @click="selectedMetric = metric.value"
                  >
                    {{ metric.label }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="chart-placeholder text-center py-5">
              <font-awesome-icon icon="fas fa-chart-area" class="fa-3x text-muted mb-3" />
              <h5 class="text-muted">Gráfico de {{ getMetricLabel(selectedMetric) }}</h5>
              <p class="text-muted">Aquí se mostraría un gráfico interactivo con la evolución de {{ getMetricLabel(selectedMetric).toLowerCase() }} durante {{ getPeriodLabel(selectedPeriod).toLowerCase() }}</p>
              <small class="text-muted">Integración con Chart.js próximamente</small>
            </div>
          </div>
        </div>

        <!-- Personal Records -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-trophy" class="me-2 text-warning" />
              Récords Personales
            </h5>
          </div>
          <div class="card-body">
            <div v-if="personalRecords.length === 0" class="text-center py-4 text-muted">
              <font-awesome-icon icon="fas fa-medal" class="fa-2x mb-3" />
              <p class="mb-0">Aún no tienes récords personales registrados</p>
              <small>¡Sigue entrenando para establecer tus primeros récords!</small>
            </div>
            
            <div v-else class="row">
              <div v-for="record in personalRecords" :key="record.id" class="col-md-6 mb-3">
                <div class="record-card p-3 border rounded">
                  <div class="d-flex align-items-center mb-2">
                    <div class="record-icon me-3">
                      <font-awesome-icon :icon="getActivityIcon(record.sport)" class="text-warning" />
                    </div>
                    <div class="flex-grow-1">
                      <h6 class="mb-0">{{ record.title }}</h6>
                      <small class="text-muted">{{ record.sport }}</small>
                    </div>
                    <div class="record-badge">
                      <span class="badge bg-warning text-dark">
                        <font-awesome-icon icon="fas fa-trophy" class="me-1" />
                        PR
                      </span>
                    </div>
                  </div>
                  
                  <div class="record-details">
                    <div class="row text-center">
                      <div class="col-6">
                        <div class="h5 mb-0 text-warning">{{ record.value }}</div>
                        <small class="text-muted">Récord</small>
                      </div>
                      <div class="col-6">
                        <div class="small text-muted">{{ formatDate(record.date) }}</div>
                        <small class="text-muted">Fecha</small>
                      </div>
                    </div>
                  </div>
                  
                  <div class="record-improvement mt-2">
                    <small class="text-success">
                      <font-awesome-icon icon="fas fa-arrow-up" class="me-1" />
                      Mejora de {{ record.improvement }} vs récord anterior
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Weekly Summary -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-calendar-week" class="me-2 text-info" />
              Resumen Semanal
            </h5>
          </div>
          <div class="card-body">
            <div class="weekly-stats">
              <div class="stat-item d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-primary bg-opacity-10 text-primary rounded me-3">
                    <font-awesome-icon icon="fas fa-running" />
                  </div>
                  <div>
                    <div class="fw-bold">{{ weeklyStats.activities }}</div>
                    <small class="text-muted">Actividades</small>
                  </div>
                </div>
                <div class="progress-ring">
                  <div class="progress-circle" :style="getProgressStyle(weeklyStats.activities, weeklyStats.activitiesGoal)">
                    <small class="text-muted">{{ Math.round((weeklyStats.activities / weeklyStats.activitiesGoal) * 100) }}%</small>
                  </div>
                </div>
              </div>
              
              <div class="stat-item d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-success bg-opacity-10 text-success rounded me-3">
                    <font-awesome-icon icon="fas fa-route" />
                  </div>
                  <div>
                    <div class="fw-bold">{{ weeklyStats.distance }} km</div>
                    <small class="text-muted">Distancia</small>
                  </div>
                </div>
                <div class="progress-ring">
                  <div class="progress-circle" :style="getProgressStyle(weeklyStats.distance, weeklyStats.distanceGoal)">
                    <small class="text-muted">{{ Math.round((weeklyStats.distance / weeklyStats.distanceGoal) * 100) }}%</small>
                  </div>
                </div>
              </div>
              
              <div class="stat-item d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-info bg-opacity-10 text-info rounded me-3">
                    <font-awesome-icon icon="fas fa-clock" />
                  </div>
                  <div>
                    <div class="fw-bold">{{ weeklyStats.duration }}h</div>
                    <small class="text-muted">Tiempo</small>
                  </div>
                </div>
                <div class="progress-ring">
                  <div class="progress-circle" :style="getProgressStyle(weeklyStats.duration, weeklyStats.durationGoal)">
                    <small class="text-muted">{{ Math.round((weeklyStats.duration / weeklyStats.durationGoal) * 100) }}%</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Activity Distribution -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-chart-pie" class="me-2 text-success" />
              Distribución por Deporte
            </h5>
          </div>
          <div class="card-body">
            <div class="sport-distribution">
              <div v-for="sport in sportsDistribution" :key="sport.name" class="sport-item mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <div class="d-flex align-items-center">
                    <font-awesome-icon :icon="getActivityIcon(sport.name)" :class="sport.color" class="me-2" />
                    <span class="small">{{ sport.label }}</span>
                  </div>
                  <span class="small fw-bold">{{ sport.percentage }}%</span>
                </div>
                <div class="progress" style="height: 6px;">
                  <div 
                    class="progress-bar" 
                    :class="sport.color.replace('text-', 'bg-')"
                    :style="{ width: sport.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Achievements -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-star" class="me-2 text-warning" />
              Logros Recientes
            </h5>
          </div>
          <div class="card-body">
            <div v-if="recentAchievements.length === 0" class="text-center py-3 text-muted">
              <font-awesome-icon icon="fas fa-award" class="fa-2x mb-2" />
              <p class="mb-0 small">No hay logros recientes</p>
            </div>
            
            <div v-else>
              <div v-for="achievement in recentAchievements" :key="achievement.id" class="achievement-item d-flex align-items-center mb-3">
                <div class="achievement-icon me-3">
                  <font-awesome-icon :icon="achievement.icon" :class="achievement.color" />
                </div>
                <div class="flex-grow-1">
                  <h6 class="mb-0 small">{{ achievement.title }}</h6>
                  <small class="text-muted">{{ achievement.description }}</small>
                  <div class="small text-muted">{{ formatTimeAgo(achievement.date) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'StudentProgressView',
  setup() {
    // Reactive data
    const selectedPeriod = ref('month')
    const selectedSport = ref('all')
    const selectedMetric = ref('distance')
    
    const timePeriods = ref([
      { value: 'week', label: 'Semana' },
      { value: 'month', label: 'Mes' },
      { value: 'quarter', label: 'Trimestre' },
      { value: 'year', label: 'Año' }
    ])
    
    const chartMetrics = ref([
      { value: 'distance', label: 'Distancia' },
      { value: 'duration', label: 'Tiempo' },
      { value: 'pace', label: 'Ritmo' },
      { value: 'frequency', label: 'Frecuencia' }
    ])
    
    const currentPeriodStats = ref({
      activities: 12,
      activitiesTrend: 15,
      distance: '85.2 km',
      distanceTrend: 8,
      duration: '12.5h',
      durationTrend: -5,
      avgPace: '5:24 min/km',
      paceTrend: 3
    })
    
    const weeklyStats = ref({
      activities: 4,
      activitiesGoal: 5,
      distance: 32.5,
      distanceGoal: 40,
      duration: 6.5,
      durationGoal: 8
    })
    
    const personalRecords = ref([
      {
        id: 1,
        title: 'Mejor 10K',
        sport: 'Carrera',
        value: '48:32',
        date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000),
        improvement: '2:15'
      },
      {
        id: 2,
        title: 'Mayor distancia',
        sport: 'Ciclismo',
        value: '65 km',
        date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
        improvement: '8 km'
      },
      {
        id: 3,
        title: 'Mejor ritmo 5K',
        sport: 'Carrera',
        value: '4:58 min/km',
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
        improvement: '0:12 min/km'
      }
    ])
    
    const sportsDistribution = ref([
      { name: 'running', label: 'Carrera', percentage: 60, color: 'text-primary' },
      { name: 'cycling', label: 'Ciclismo', percentage: 25, color: 'text-success' },
      { name: 'swimming', label: 'Natación', percentage: 10, color: 'text-info' },
      { name: 'gym', label: 'Gimnasio', percentage: 5, color: 'text-warning' }
    ])
    
    const recentAchievements = ref([
      {
        id: 1,
        title: 'Récord Personal',
        description: 'Nuevo mejor tiempo en 10K',
        icon: 'fas fa-trophy',
        color: 'text-warning',
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
      },
      {
        id: 2,
        title: 'Racha de 7 días',
        description: 'Entrenaste 7 días consecutivos',
        icon: 'fas fa-fire',
        color: 'text-danger',
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      },
      {
        id: 3,
        title: 'Meta mensual',
        description: 'Completaste tu objetivo de distancia',
        icon: 'fas fa-target',
        color: 'text-success',
        date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
      }
    ])
    
    // Computed
    const totalActivities = computed(() => 156)
    const totalHours = computed(() => '248h')
    const totalDistance = computed(() => '1,245 km')
    
    // Methods
    const getTrendClass = (trend) => {
      return trend >= 0 ? 'text-success' : 'text-danger'
    }
    
    const getTrendIcon = (trend) => {
      return trend >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'
    }
    
    const getActivityIcon = (sport) => {
      const iconMap = {
        running: 'fas fa-running',
        cycling: 'fas fa-biking',
        swimming: 'fas fa-swimmer',
        gym: 'fas fa-dumbbell',
        Carrera: 'fas fa-running',
        Ciclismo: 'fas fa-biking',
        Natación: 'fas fa-swimmer'
      }
      return iconMap[sport] || 'fas fa-running'
    }
    
    const getMetricLabel = (metric) => {
      const labels = {
        distance: 'Distancia',
        duration: 'Tiempo',
        pace: 'Ritmo',
        frequency: 'Frecuencia'
      }
      return labels[metric] || metric
    }
    
    const getPeriodLabel = (period) => {
      const labels = {
        week: 'Esta semana',
        month: 'Este mes',
        quarter: 'Este trimestre',
        year: 'Este año'
      }
      return labels[period] || period
    }
    
    const getProgressStyle = (current, goal) => {
      const percentage = Math.min((current / goal) * 100, 100)
      return {
        background: `conic-gradient(#0d6efd ${percentage * 3.6}deg, #e9ecef 0deg)`
      }
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const formatTimeAgo = (date) => {
      const now = new Date()
      const diff = now - date
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (days === 0) return 'Hoy'
      if (days === 1) return 'Ayer'
      return `Hace ${days} días`
    }
    
    const exportData = () => {
      console.log('Exportar datos de progreso')
      // Implementar exportación de datos
      alert('Función de exportación próximamente disponible')
    }
    
    const loadProgressData = async () => {
      try {
        // Aquí se cargarían los datos reales del backend
        console.log('Cargando datos de progreso...')
      } catch (error) {
        console.error('Error loading progress data:', error)
      }
    }
    
    onMounted(() => {
      loadProgressData()
    })
    
    return {
      selectedPeriod,
      selectedSport,
      selectedMetric,
      timePeriods,
      chartMetrics,
      currentPeriodStats,
      weeklyStats,
      personalRecords,
      sportsDistribution,
      recentAchievements,
      totalActivities,
      totalHours,
      totalDistance,
      getTrendClass,
      getTrendIcon,
      getActivityIcon,
      getMetricLabel,
      getPeriodLabel,
      getProgressStyle,
      formatDate,
      formatTimeAgo,
      exportData
    }
  }
}
</script>

<style scoped>
.student-progress {
  padding: 1.5rem;
}

.progress-header {
  background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.metric-card {
  transition: transform 0.2s ease-in-out;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.trend {
  font-size: 0.75rem;
}

.chart-placeholder {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}

.record-card {
  transition: transform 0.2s ease-in-out;
  background-color: #fff;
}

.record-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}

.record-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff3cd;
  border-radius: 50%;
  font-size: 1.1rem;
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.progress-ring {
  width: 50px;
  height: 50px;
}

.progress-circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.progress-circle::before {
  content: '';
  position: absolute;
  inset: 4px;
  background: white;
  border-radius: 50%;
  z-index: 1;
}

.progress-circle small {
  position: relative;
  z-index: 2;
}

.sport-item .progress {
  border-radius: 10px;
}

.achievement-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 50%;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .student-progress {
    padding: 1rem;
  }
  
  .progress-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .progress-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
  
  .btn-group {
    flex-direction: column;
    width: 100%;
  }
  
  .chart-controls .btn-group {
    flex-direction: row;
    width: auto;
  }
}
</style>
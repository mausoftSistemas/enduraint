<template>
  <div class="performance-charts">
    <!-- Selector de comparación -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-4">
                <label class="form-label">Tipo de comparación</label>
                <select class="form-select" v-model="comparisonType" @change="updateCharts">
                  <option value="progress">Progreso personal</option>
                  <option value="goals" v-if="isCoachView">Vs. Objetivos</option>
                  <option value="students" v-if="isCoachView">Comparar estudiantes</option>
                  <option value="coach" v-if="!isCoachView">Vs. Entrenador</option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Período de tiempo</label>
                <select class="form-select" v-model="timePeriod" @change="updateCharts">
                  <option value="week">Semanal</option>
                  <option value="month">Mensual</option>
                  <option value="quarter">Trimestral</option>
                  <option value="year">Anual</option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Métrica a analizar</label>
                <select class="form-select" v-model="selectedMetric" @change="updateCharts">
                  <option value="volume">Volumen de entrenamiento</option>
                  <option value="intensity">Intensidad promedio</option>
                  <option value="consistency">Consistencia</option>
                  <option value="improvement">Mejora de rendimiento</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráfico principal de progreso -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-chart-area me-2"></i>
              {{ getChartTitle() }}
            </h5>
            <div class="card-tools">
              <button class="btn btn-sm btn-outline-primary" @click="toggleChartType">
                <i :class="chartType === 'line' ? 'fas fa-chart-bar' : 'fas fa-chart-line'"></i>
                {{ chartType === 'line' ? 'Barras' : 'Líneas' }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <canvas ref="mainChart" width="800" height="400"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficos de comparación -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-bullseye me-2"></i>
              Cumplimiento de Objetivos
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="goalsChart" width="400" height="300"></canvas>
            <div class="goals-summary mt-3">
              <div class="row text-center">
                <div class="col-4">
                  <div class="goal-stat">
                    <div class="stat-value text-success">{{ goalsStats.completed }}</div>
                    <div class="stat-label">Completados</div>
                  </div>
                </div>
                <div class="col-4">
                  <div class="goal-stat">
                    <div class="stat-value text-warning">{{ goalsStats.inProgress }}</div>
                    <div class="stat-label">En Progreso</div>
                  </div>
                </div>
                <div class="col-4">
                  <div class="goal-stat">
                    <div class="stat-value text-danger">{{ goalsStats.overdue }}</div>
                    <div class="stat-label">Atrasados</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-tachometer-alt me-2"></i>
              Análisis de Intensidad
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="intensityChart" width="400" height="300"></canvas>
            <div class="intensity-legend mt-3">
              <div class="d-flex justify-content-between">
                <span class="legend-item">
                  <span class="legend-color bg-success"></span>
                  Baja (50-60%)
                </span>
                <span class="legend-item">
                  <span class="legend-color bg-warning"></span>
                  Moderada (60-80%)
                </span>
                <span class="legend-item">
                  <span class="legend-color bg-danger"></span>
                  Alta (80-100%)
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Métricas de rendimiento -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-trophy me-2"></i>
              Métricas de Rendimiento
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3">
                <div class="performance-metric">
                  <div class="metric-icon bg-primary">
                    <i class="fas fa-chart-line"></i>
                  </div>
                  <div class="metric-info">
                    <div class="metric-title">Mejora General</div>
                    <div class="metric-value">+{{ performanceMetrics.overallImprovement }}%</div>
                    <div class="metric-period">Últimos 3 meses</div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="performance-metric">
                  <div class="metric-icon bg-success">
                    <i class="fas fa-calendar-check"></i>
                  </div>
                  <div class="metric-info">
                    <div class="metric-title">Consistencia</div>
                    <div class="metric-value">{{ performanceMetrics.consistency }}%</div>
                    <div class="metric-period">Entrenamientos completados</div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="performance-metric">
                  <div class="metric-icon bg-warning">
                    <i class="fas fa-fire"></i>
                  </div>
                  <div class="metric-info">
                    <div class="metric-title">Intensidad Promedio</div>
                    <div class="metric-value">{{ performanceMetrics.avgIntensity }}%</div>
                    <div class="metric-period">FC máxima</div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="performance-metric">
                  <div class="metric-icon bg-info">
                    <i class="fas fa-stopwatch"></i>
                  </div>
                  <div class="metric-info">
                    <div class="metric-title">Mejor Tiempo</div>
                    <div class="metric-value">{{ performanceMetrics.bestTime }}</div>
                    <div class="metric-period">5K personal</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comparación con otros usuarios (solo para entrenadores) -->
    <div class="row" v-if="isCoachView && comparisonType === 'students'">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">
              <i class="fas fa-users me-2"></i>
              Comparación entre Estudiantes
            </h5>
          </div>
          <div class="card-body">
            <canvas ref="comparisonChart" width="800" height="400"></canvas>
            <div class="students-ranking mt-4">
              <h6>Ranking de Rendimiento</h6>
              <div class="table-responsive">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Posición</th>
                      <th>Estudiante</th>
                      <th>Puntuación</th>
                      <th>Mejora</th>
                      <th>Consistencia</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(student, index) in studentsRanking" :key="student.id">
                      <td>
                        <span class="badge" :class="getRankingBadgeClass(index)">
                          {{ index + 1 }}
                        </span>
                      </td>
                      <td>{{ student.name }}</td>
                      <td>{{ student.score }}</td>
                      <td>
                        <span :class="student.improvement >= 0 ? 'text-success' : 'text-danger'">
                          {{ student.improvement >= 0 ? '+' : '' }}{{ student.improvement }}%
                        </span>
                      </td>
                      <td>
                        <div class="progress" style="height: 6px;">
                          <div class="progress-bar" 
                               :style="{ width: student.consistency + '%' }"
                               :class="getConsistencyClass(student.consistency)"></div>
                        </div>
                        <small>{{ student.consistency }}%</small>
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

const comparisonType = ref('progress')
const timePeriod = ref('month')
const selectedMetric = ref('volume')
const chartType = ref('line')

const mainChart = ref(null)
const goalsChart = ref(null)
const intensityChart = ref(null)
const comparisonChart = ref(null)

let mainChartInstance = null
let goalsChartInstance = null
let intensityChartInstance = null
let comparisonChartInstance = null

const goalsStats = ref({
  completed: 8,
  inProgress: 3,
  overdue: 2
})

const performanceMetrics = ref({
  overallImprovement: 15.3,
  consistency: 87,
  avgIntensity: 72,
  bestTime: '21:45'
})

const studentsRanking = ref([
  { id: 1, name: 'Ana García', score: 95, improvement: 12.5, consistency: 92 },
  { id: 2, name: 'Carlos López', score: 88, improvement: 8.3, consistency: 85 },
  { id: 3, name: 'María Rodríguez', score: 82, improvement: -2.1, consistency: 78 },
  { id: 4, name: 'Juan Martínez', score: 79, improvement: 15.7, consistency: 71 },
  { id: 5, name: 'Laura Sánchez', score: 76, improvement: 5.2, consistency: 89 }
])

const updateCharts = async () => {
  await nextTick()
  updateMainChart()
  updateGoalsChart()
  updateIntensityChart()
  if (comparisonType.value === 'students' && props.isCoachView) {
    updateComparisonChart()
  }
}

const updateMainChart = () => {
  if (mainChartInstance) {
    mainChartInstance.destroy()
  }
  
  const ctx = mainChart.value.getContext('2d')
  const labels = generateTimeLabels()
  const datasets = generateMainChartData()
  
  mainChartInstance = new Chart(ctx, {
    type: chartType.value,
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: getPeriodLabel()
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: getMetricLabel()
          },
          beginAtZero: true
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  })
}

const updateGoalsChart = () => {
  if (goalsChartInstance) {
    goalsChartInstance.destroy()
  }
  
  const ctx = goalsChart.value.getContext('2d')
  
  goalsChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Completados', 'En Progreso', 'Atrasados'],
      datasets: [{
        data: [goalsStats.value.completed, goalsStats.value.inProgress, goalsStats.value.overdue],
        backgroundColor: ['#198754', '#ffc107', '#dc3545'],
        borderWidth: 2,
        borderColor: '#fff'
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

const updateIntensityChart = () => {
  if (intensityChartInstance) {
    intensityChartInstance.destroy()
  }
  
  const ctx = intensityChart.value.getContext('2d')
  const labels = generateTimeLabels()
  
  intensityChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Baja Intensidad',
          data: generateIntensityData('low'),
          backgroundColor: '#198754',
          stack: 'intensity'
        },
        {
          label: 'Intensidad Moderada',
          data: generateIntensityData('moderate'),
          backgroundColor: '#ffc107',
          stack: 'intensity'
        },
        {
          label: 'Alta Intensidad',
          data: generateIntensityData('high'),
          backgroundColor: '#dc3545',
          stack: 'intensity'
        }
      ]
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
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          beginAtZero: true,
          title: {
            display: true,
            text: 'Tiempo (minutos)'
          }
        }
      }
    }
  })
}

const updateComparisonChart = () => {
  if (comparisonChartInstance) {
    comparisonChartInstance.destroy()
  }
  
  const ctx = comparisonChart.value.getContext('2d')
  const labels = generateTimeLabels()
  
  const datasets = studentsRanking.value.slice(0, 5).map((student, index) => ({
    label: student.name,
    data: generateStudentProgressData(),
    borderColor: getStudentColor(index),
    backgroundColor: getStudentColor(index, 0.1),
    tension: 0.4
  }))
  
  comparisonChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: getMetricLabel()
          }
        }
      }
    }
  })
}

const generateTimeLabels = () => {
  const labels = []
  const periods = {
    week: 7,
    month: 4,
    quarter: 12,
    year: 12
  }
  
  const count = periods[timePeriod.value] || 7
  
  for (let i = count - 1; i >= 0; i--) {
    if (timePeriod.value === 'week') {
      const date = new Date(Date.now() - i * 24 * 60 * 60 * 1000)
      labels.push(date.toLocaleDateString('es-ES', { weekday: 'short' }))
    } else if (timePeriod.value === 'month') {
      labels.push(`Semana ${count - i}`)
    } else {
      const date = new Date()
      date.setMonth(date.getMonth() - i)
      labels.push(date.toLocaleDateString('es-ES', { month: 'short' }))
    }
  }
  
  return labels
}

const generateMainChartData = () => {
  const datasets = []
  const dataLength = generateTimeLabels().length
  
  if (comparisonType.value === 'progress') {
    datasets.push({
      label: 'Rendimiento Actual',
      data: generateRandomData(dataLength, 50, 100),
      borderColor: '#0d6efd',
      backgroundColor: 'rgba(13, 110, 253, 0.1)',
      tension: 0.4,
      fill: chartType.value === 'line'
    })
  } else if (comparisonType.value === 'goals') {
    datasets.push(
      {
        label: 'Objetivo',
        data: Array(dataLength).fill(80),
        borderColor: '#198754',
        backgroundColor: 'rgba(25, 135, 84, 0.1)',
        borderDash: [5, 5]
      },
      {
        label: 'Rendimiento Real',
        data: generateRandomData(dataLength, 60, 90),
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        tension: 0.4
      }
    )
  }
  
  return datasets
}

const generateRandomData = (length, min, max) => {
  const data = []
  for (let i = 0; i < length; i++) {
    data.push(Math.random() * (max - min) + min)
  }
  return data
}

const generateIntensityData = (type) => {
  const length = generateTimeLabels().length
  const ranges = {
    low: [20, 40],
    moderate: [30, 60],
    high: [10, 30]
  }
  
  const [min, max] = ranges[type]
  return generateRandomData(length, min, max)
}

const generateStudentProgressData = () => {
  return generateRandomData(generateTimeLabels().length, 60, 95)
}

const getStudentColor = (index, alpha = 1) => {
  const colors = [
    `rgba(13, 110, 253, ${alpha})`,
    `rgba(25, 135, 84, ${alpha})`,
    `rgba(255, 193, 7, ${alpha})`,
    `rgba(220, 53, 69, ${alpha})`,
    `rgba(111, 66, 193, ${alpha})`
  ]
  return colors[index % colors.length]
}

const getChartTitle = () => {
  const titles = {
    progress: 'Progreso Personal',
    goals: 'Progreso vs Objetivos',
    students: 'Comparación entre Estudiantes',
    coach: 'Comparación con Entrenador'
  }
  return titles[comparisonType.value] || 'Análisis de Rendimiento'
}

const getPeriodLabel = () => {
  const labels = {
    week: 'Días',
    month: 'Semanas',
    quarter: 'Meses',
    year: 'Meses'
  }
  return labels[timePeriod.value] || 'Período'
}

const getMetricLabel = () => {
  const labels = {
    volume: 'Volumen (km)',
    intensity: 'Intensidad (%)',
    consistency: 'Consistencia (%)',
    improvement: 'Mejora (%)'
  }
  return labels[selectedMetric.value] || 'Métrica'
}

const toggleChartType = () => {
  chartType.value = chartType.value === 'line' ? 'bar' : 'line'
  updateMainChart()
}

const getRankingBadgeClass = (index) => {
  if (index === 0) return 'bg-warning text-dark'
  if (index === 1) return 'bg-secondary'
  if (index === 2) return 'bg-warning text-dark'
  return 'bg-light text-dark'
}

const getConsistencyClass = (consistency) => {
  if (consistency >= 80) return 'bg-success'
  if (consistency >= 60) return 'bg-warning'
  return 'bg-danger'
}

onMounted(() => {
  updateCharts()
})
</script>

<style scoped>
.card-tools {
  margin-left: auto;
}

.performance-metric {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background: white;
  height: 100%;
}

.metric-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
  margin-right: 1rem;
}

.metric-info {
  flex: 1;
}

.metric-title {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #212529;
  line-height: 1;
}

.metric-period {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.goal-stat {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 0.5rem;
}

.students-ranking {
  margin-top: 1rem;
}

.progress {
  width: 60px;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
  font-size: 0.875rem;
}

.table td {
  vertical-align: middle;
  font-size: 0.875rem;
}
</style>
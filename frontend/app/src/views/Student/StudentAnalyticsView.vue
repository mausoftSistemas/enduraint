<template>
  <div class="student-analytics-view">
    <!-- Header personalizado -->
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="page-title">
            <i class="fas fa-chart-line me-2"></i>
            Mi Progreso y Análisis
          </h1>
          <p class="page-subtitle">Visualiza tu rendimiento y evolución en el entrenamiento</p>
        </div>
        <div class="col-md-4">
          <div class="d-flex gap-2 justify-content-end">
            <button class="btn btn-outline-light" @click="shareProgress">
              <i class="fas fa-share-alt"></i>
              Compartir
            </button>
            <button class="btn btn-light" @click="exportData">
              <i class="fas fa-download"></i>
              Exportar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Resumen personal -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="personal-stat-card">
          <div class="stat-icon bg-primary">
            <i class="fas fa-trophy"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ personalStats.totalAchievements }}</div>
            <div class="stat-label">Logros Obtenidos</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ personalStats.newAchievements }} este mes
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="personal-stat-card">
          <div class="stat-icon bg-success">
            <i class="fas fa-fire"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ personalStats.currentStreak }}</div>
            <div class="stat-label">Días Consecutivos</div>
            <div class="stat-change" :class="personalStats.streakChange >= 0 ? 'positive' : 'negative'">
              <i :class="personalStats.streakChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(personalStats.streakChange) }} vs semana anterior
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="personal-stat-card">
          <div class="stat-icon bg-warning">
            <i class="fas fa-bullseye"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ personalStats.goalsProgress }}%</div>
            <div class="stat-label">Progreso de Objetivos</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ personalStats.goalsImprovement }}% este mes
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="personal-stat-card">
          <div class="stat-icon bg-info">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ personalStats.performanceScore }}</div>
            <div class="stat-label">Puntuación General</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ personalStats.scoreImprovement }} puntos
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pestañas de análisis -->
    <div class="analytics-tabs mb-4">
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'overview' }" 
                  @click="activeTab = 'overview'" type="button">
            <i class="fas fa-chart-pie me-2"></i>
            Resumen
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'progress' }" 
                  @click="activeTab = 'progress'" type="button">
            <i class="fas fa-chart-area me-2"></i>
            Mi Progreso
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'goals' }" 
                  @click="activeTab = 'goals'" type="button">
            <i class="fas fa-target me-2"></i>
            Objetivos
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'comparison' }" 
                  @click="activeTab = 'comparison'" type="button">
            <i class="fas fa-users me-2"></i>
            Comparación
          </button>
        </li>
      </ul>
    </div>

    <!-- Contenido de las pestañas -->
    <div class="tab-content">
      <!-- Pestaña Resumen -->
      <div v-show="activeTab === 'overview'" class="tab-pane">
        <TrainingAnalyticsComponent 
          :userId="currentUserId"
          :isCoachView="false" />
      </div>

      <!-- Pestaña Mi Progreso -->
      <div v-show="activeTab === 'progress'" class="tab-pane">
        <div class="row mb-4">
          <div class="col-md-8">
            <PerformanceChartsComponent 
              :userId="currentUserId"
              :isCoachView="false" />
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-medal me-2"></i>
                  Logros Recientes
                </h5>
              </div>
              <div class="card-body">
                <div class="achievements-list">
                  <div class="achievement-item" v-for="achievement in recentAchievements" :key="achievement.id">
                    <div class="achievement-icon" :class="achievement.type">
                      <i :class="achievement.icon"></i>
                    </div>
                    <div class="achievement-content">
                      <div class="achievement-title">{{ achievement.title }}</div>
                      <div class="achievement-description">{{ achievement.description }}</div>
                      <div class="achievement-date">{{ formatDate(achievement.date) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pestaña Objetivos -->
      <div v-show="activeTab === 'goals'" class="tab-pane">
        <div class="row">
          <div class="col-md-8">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-bullseye me-2"></i>
                  Progreso de Objetivos
                </h5>
              </div>
              <div class="card-body">
                <div class="goals-progress">
                  <div class="goal-progress-item" v-for="goal in currentGoals" :key="goal.id">
                    <div class="goal-header">
                      <div class="goal-info">
                        <h6 class="goal-title">{{ goal.title }}</h6>
                        <p class="goal-description">{{ goal.description }}</p>
                      </div>
                      <div class="goal-status">
                        <span class="badge" :class="getGoalStatusClass(goal.status)">{{ goal.status }}</span>
                      </div>
                    </div>
                    <div class="goal-progress-bar">
                      <div class="progress mb-2">
                        <div class="progress-bar" 
                             :class="getGoalProgressClass(goal.progress)"
                             :style="{ width: goal.progress + '%' }"
                             role="progressbar"
                             :aria-valuenow="goal.progress"
                             aria-valuemin="0"
                             aria-valuemax="100">
                          {{ goal.progress }}%
                        </div>
                      </div>
                      <div class="goal-meta">
                        <small class="text-muted">
                          <i class="fas fa-calendar me-1"></i>
                          Fecha límite: {{ formatDate(goal.deadline) }}
                        </small>
                        <small class="text-muted">
                          <i class="fas fa-clock me-1"></i>
                          {{ getDaysRemaining(goal.deadline) }} días restantes
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-chart-donut me-2"></i>
                  Resumen de Objetivos
                </h5>
              </div>
              <div class="card-body">
                <canvas ref="goalsChart" width="300" height="300"></canvas>
                <div class="goals-summary mt-3">
                  <div class="row text-center">
                    <div class="col-4">
                      <div class="summary-stat">
                        <div class="stat-number text-success">{{ goalsSummary.completed }}</div>
                        <div class="stat-text">Completados</div>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="summary-stat">
                        <div class="stat-number text-primary">{{ goalsSummary.inProgress }}</div>
                        <div class="stat-text">En Progreso</div>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="summary-stat">
                        <div class="stat-number text-warning">{{ goalsSummary.pending }}</div>
                        <div class="stat-text">Pendientes</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Feedback del entrenador -->
            <div class="card mt-4">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-comment-dots me-2"></i>
                  Feedback del Entrenador
                </h5>
              </div>
              <div class="card-body">
                <div class="feedback-list">
                  <div class="feedback-item" v-for="feedback in recentFeedback" :key="feedback.id">
                    <div class="feedback-header">
                      <img :src="feedback.coachAvatar" :alt="feedback.coachName" class="coach-avatar">
                      <div class="feedback-meta">
                        <div class="coach-name">{{ feedback.coachName }}</div>
                        <div class="feedback-date">{{ formatRelativeDate(feedback.date) }}</div>
                      </div>
                    </div>
                    <div class="feedback-content">
                      <p>{{ feedback.message }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pestaña Comparación -->
      <div v-show="activeTab === 'comparison'" class="tab-pane">
        <div class="row mb-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-chart-bar me-2"></i>
                  Mi Posición vs Otros Estudiantes
                </h5>
              </div>
              <div class="card-body">
                <div class="comparison-metrics">
                  <div class="row">
                    <div class="col-md-3">
                      <div class="comparison-card">
                        <div class="comparison-rank">#{{ myRanking.position }}</div>
                        <div class="comparison-label">Mi Posición</div>
                        <div class="comparison-total">de {{ myRanking.total }} estudiantes</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="comparison-card">
                        <div class="comparison-rank">{{ myRanking.percentile }}%</div>
                        <div class="comparison-label">Percentil</div>
                        <div class="comparison-total">mejor que {{ myRanking.betterThan }}%</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="comparison-card">
                        <div class="comparison-rank">{{ myRanking.score }}</div>
                        <div class="comparison-label">Mi Puntuación</div>
                        <div class="comparison-total">promedio: {{ myRanking.average }}</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="comparison-card">
                        <div class="comparison-rank" :class="myRanking.trend >= 0 ? 'text-success' : 'text-danger'">
                          {{ myRanking.trend >= 0 ? '+' : '' }}{{ myRanking.trend }}
                        </div>
                        <div class="comparison-label">Cambio Mensual</div>
                        <div class="comparison-total">posiciones</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="mt-4">
                  <canvas ref="comparisonChart" width="800" height="400"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import TrainingAnalyticsComponent from '@/components/Analytics/TrainingAnalyticsComponent.vue'
import PerformanceChartsComponent from '@/components/Analytics/PerformanceChartsComponent.vue'
import Chart from 'chart.js/auto'

const authStore = useAuthStore()
const activeTab = ref('overview')
const goalsChart = ref(null)
const comparisonChart = ref(null)

let goalsChartInstance = null
let comparisonChartInstance = null

const currentUserId = computed(() => authStore.user?.id)

const personalStats = ref({
  totalAchievements: 12,
  newAchievements: 3,
  currentStreak: 15,
  streakChange: 2,
  goalsProgress: 78,
  goalsImprovement: 12,
  performanceScore: 85,
  scoreImprovement: 8
})

const recentAchievements = ref([
  {
    id: 1,
    title: '¡Primera carrera de 10K!',
    description: 'Completaste tu primera carrera de 10 kilómetros',
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    type: 'gold',
    icon: 'fas fa-medal'
  },
  {
    id: 2,
    title: 'Racha de 2 semanas',
    description: 'Entrenaste durante 14 días consecutivos',
    date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    type: 'silver',
    icon: 'fas fa-fire'
  },
  {
    id: 3,
    title: 'Objetivo cumplido',
    description: 'Completaste el objetivo de resistencia cardiovascular',
    date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    type: 'bronze',
    icon: 'fas fa-bullseye'
  }
])

const currentGoals = ref([
  {
    id: 1,
    title: 'Correr 5K en menos de 25 minutos',
    description: 'Mejorar tu tiempo personal en la distancia de 5 kilómetros',
    status: 'En Progreso',
    progress: 75,
    deadline: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000)
  },
  {
    id: 2,
    title: 'Completar 20 entrenamientos este mes',
    description: 'Mantener consistencia en tu rutina de entrenamiento',
    status: 'En Progreso',
    progress: 65,
    deadline: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000)
  },
  {
    id: 3,
    title: 'Mejorar resistencia cardiovascular',
    description: 'Aumentar tu capacidad aeróbica y resistencia general',
    status: 'Completado',
    progress: 100,
    deadline: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
  }
])

const goalsSummary = ref({
  completed: 1,
  inProgress: 2,
  pending: 0
})

const recentFeedback = ref([
  {
    id: 1,
    coachName: 'Carlos Entrenador',
    coachAvatar: '/avatars/coach.jpg',
    message: '¡Excelente progreso en tu resistencia! Sigue así y pronto alcanzarás tu objetivo de 5K.',
    date: new Date(Date.now() - 24 * 60 * 60 * 1000)
  },
  {
    id: 2,
    coachName: 'Carlos Entrenador',
    coachAvatar: '/avatars/coach.jpg',
    message: 'Recuerda incluir días de descanso en tu rutina. La recuperación es tan importante como el entrenamiento.',
    date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
  }
])

const myRanking = ref({
  position: 3,
  total: 25,
  percentile: 88,
  betterThan: 88,
  score: 85,
  average: 72,
  trend: 2
})

const shareProgress = () => {
  // Implementar funcionalidad de compartir
  console.log('Compartiendo progreso...')
}

const exportData = () => {
  // Implementar exportación de datos
  console.log('Exportando datos...')
}

const getGoalStatusClass = (status) => {
  const classes = {
    'Completado': 'bg-success',
    'En Progreso': 'bg-primary',
    'Atrasado': 'bg-danger',
    'Pendiente': 'bg-warning'
  }
  return classes[status] || 'bg-secondary'
}

const getGoalProgressClass = (progress) => {
  if (progress >= 80) return 'bg-success'
  if (progress >= 50) return 'bg-warning'
  return 'bg-danger'
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

const formatRelativeDate = (date) => {
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)
  
  if (hours < 1) return 'Hace menos de 1 hora'
  if (hours < 24) return `Hace ${hours} horas`
  if (days === 1) return 'Ayer'
  return `Hace ${days} días`
}

const getDaysRemaining = (deadline) => {
  const now = new Date()
  const diff = deadline - now
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return Math.max(0, days)
}

const updateGoalsChart = () => {
  if (goalsChartInstance) {
    goalsChartInstance.destroy()
  }
  
  const ctx = goalsChart.value.getContext('2d')
  
  goalsChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Completados', 'En Progreso', 'Pendientes'],
      datasets: [{
        data: [goalsSummary.value.completed, goalsSummary.value.inProgress, goalsSummary.value.pending],
        backgroundColor: ['#198754', '#0d6efd', '#ffc107'],
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

const updateComparisonChart = () => {
  if (comparisonChartInstance) {
    comparisonChartInstance.destroy()
  }
  
  const ctx = comparisonChart.value.getContext('2d')
  
  comparisonChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Mi Puntuación',
          data: [65, 70, 75, 80, 82, 85],
          backgroundColor: '#0d6efd',
          borderColor: '#0d6efd',
          borderWidth: 2
        },
        {
          label: 'Promedio del Grupo',
          data: [60, 65, 68, 70, 71, 72],
          backgroundColor: '#6c757d',
          borderColor: '#6c757d',
          borderWidth: 2
        }
      ]
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
          max: 100
        }
      }
    }
  })
}

onMounted(() => {
  updateGoalsChart()
  updateComparisonChart()
})
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  opacity: 0.9;
  margin-bottom: 0;
}

.personal-stat-card {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  height: 100%;
}

.personal-stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  margin-right: 1rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #212529;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0.25rem 0;
}

.stat-change {
  font-size: 0.75rem;
  font-weight: 600;
}

.stat-change.positive {
  color: #198754;
}

.stat-change.negative {
  color: #dc3545;
}

.analytics-tabs .nav-tabs {
  border-bottom: 2px solid #e9ecef;
}

.analytics-tabs .nav-link {
  border: none;
  color: #6c757d;
  font-weight: 500;
  padding: 1rem 1.5rem;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.analytics-tabs .nav-link:hover {
  color: #0d6efd;
  border-bottom-color: #0d6efd;
}

.analytics-tabs .nav-link.active {
  color: #0d6efd;
  border-bottom-color: #0d6efd;
  background: none;
}

.achievements-list {
  max-height: 400px;
  overflow-y: auto;
}

.achievement-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background: #f8f9fa;
}

.achievement-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
  margin-right: 1rem;
}

.achievement-icon.gold {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #8b6914;
}

.achievement-icon.silver {
  background: linear-gradient(45deg, #c0c0c0, #e8e8e8);
  color: #666;
}

.achievement-icon.bronze {
  background: linear-gradient(45deg, #cd7f32, #daa520);
  color: white;
}

.achievement-content {
  flex: 1;
}

.achievement-title {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
}

.achievement-description {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.achievement-date {
  font-size: 0.75rem;
  color: #adb5bd;
}

.goals-progress {
  space-y: 1.5rem;
}

.goal-progress-item {
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  background: white;
  margin-bottom: 1.5rem;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.goal-title {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.5rem;
}

.goal-description {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0;
}

.goal-meta {
  display: flex;
  justify-content: space-between;
}

.summary-stat {
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1;
}

.stat-text {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.feedback-list {
  max-height: 300px;
  overflow-y: auto;
}

.feedback-item {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background: #f8f9fa;
}

.feedback-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.coach-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 0.75rem;
  object-fit: cover;
}

.coach-name {
  font-weight: 600;
  color: #212529;
  font-size: 0.875rem;
}

.feedback-date {
  font-size: 0.75rem;
  color: #6c757d;
}

.feedback-content p {
  font-size: 0.875rem;
  color: #495057;
  margin-bottom: 0;
}

.comparison-metrics {
  margin-bottom: 2rem;
}

.comparison-card {
  text-align: center;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  background: white;
  height: 100%;
}

.comparison-rank {
  font-size: 2rem;
  font-weight: bold;
  color: #0d6efd;
  line-height: 1;
}

.comparison-label {
  font-size: 0.875rem;
  color: #212529;
  font-weight: 600;
  margin: 0.5rem 0;
}

.comparison-total {
  font-size: 0.75rem;
  color: #6c757d;
}
</style>
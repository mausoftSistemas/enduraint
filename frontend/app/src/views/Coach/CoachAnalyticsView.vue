<template>
  <div class="coach-analytics-view">
    <!-- Header con filtros globales -->
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h1 class="page-title">
            <i class="fas fa-chart-bar me-2"></i>
            Análisis y Estadísticas
          </h1>
          <p class="page-subtitle">Visualiza el rendimiento y progreso de tus estudiantes</p>
        </div>
        <div class="col-md-6">
          <div class="d-flex gap-2 justify-content-end">
            <select class="form-select" v-model="selectedStudent" @change="updateAnalytics">
              <option value="all">Todos los estudiantes</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.name }}
              </option>
            </select>
            <button class="btn btn-primary" @click="generateReport">
              <i class="fas fa-file-pdf"></i>
              Generar Reporte
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Resumen general -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="summary-card">
          <div class="card-icon bg-primary">
            <i class="fas fa-users"></i>
          </div>
          <div class="card-content">
            <div class="card-value">{{ summaryStats.totalStudents }}</div>
            <div class="card-label">Estudiantes Activos</div>
            <div class="card-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ summaryStats.newStudents }} este mes
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="summary-card">
          <div class="card-icon bg-success">
            <i class="fas fa-dumbbell"></i>
          </div>
          <div class="card-content">
            <div class="card-value">{{ summaryStats.totalWorkouts }}</div>
            <div class="card-label">Entrenamientos Completados</div>
            <div class="card-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ summaryStats.workoutGrowth }}% vs mes anterior
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="summary-card">
          <div class="card-icon bg-warning">
            <i class="fas fa-bullseye"></i>
          </div>
          <div class="card-content">
            <div class="card-value">{{ summaryStats.goalsCompleted }}%</div>
            <div class="card-label">Objetivos Cumplidos</div>
            <div class="card-change" :class="summaryStats.goalsChange >= 0 ? 'positive' : 'negative'">
              <i :class="summaryStats.goalsChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
              {{ Math.abs(summaryStats.goalsChange) }}% vs mes anterior
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="summary-card">
          <div class="card-icon bg-info">
            <i class="fas fa-clock"></i>
          </div>
          <div class="card-content">
            <div class="card-value">{{ summaryStats.avgSessionTime }}min</div>
            <div class="card-label">Duración Promedio</div>
            <div class="card-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ summaryStats.timeIncrease }}min vs mes anterior
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
            Resumen General
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'performance' }" 
                  @click="activeTab = 'performance'" type="button">
            <i class="fas fa-chart-line me-2"></i>
            Rendimiento
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{ active: activeTab === 'progress' }" 
                  @click="activeTab = 'progress'" type="button">
            <i class="fas fa-trophy me-2"></i>
            Progreso
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
      <!-- Pestaña Resumen General -->
      <div v-show="activeTab === 'overview'" class="tab-pane">
        <TrainingAnalyticsComponent 
          :userId="selectedStudent === 'all' ? null : selectedStudent"
          :isCoachView="true" />
      </div>

      <!-- Pestaña Rendimiento -->
      <div v-show="activeTab === 'performance'" class="tab-pane">
        <PerformanceChartsComponent 
          :userId="selectedStudent === 'all' ? null : selectedStudent"
          :isCoachView="true" />
      </div>

      <!-- Pestaña Progreso -->
      <div v-show="activeTab === 'progress'" class="tab-pane">
        <div class="row">
          <div class="col-md-8">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-chart-area me-2"></i>
                  Progreso de Objetivos
                </h5>
              </div>
              <div class="card-body">
                <canvas ref="progressChart" width="600" height="300"></canvas>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">
                  <i class="fas fa-list-check me-2"></i>
                  Estado de Objetivos
                </h5>
              </div>
              <div class="card-body">
                <div class="goals-list">
                  <div class="goal-item" v-for="goal in currentGoals" :key="goal.id">
                    <div class="goal-header">
                      <span class="goal-title">{{ goal.title }}</span>
                      <span class="badge" :class="getGoalStatusClass(goal.status)">{{ goal.status }}</span>
                    </div>
                    <div class="goal-progress">
                      <div class="progress mb-1">
                        <div class="progress-bar" 
                             :class="getGoalProgressClass(goal.progress)"
                             :style="{ width: goal.progress + '%' }"></div>
                      </div>
                      <small class="text-muted">{{ goal.progress }}% completado</small>
                    </div>
                    <div class="goal-meta">
                      <small class="text-muted">
                        <i class="fas fa-user me-1"></i>{{ goal.studentName }}
                        <i class="fas fa-calendar ms-2 me-1"></i>{{ formatDate(goal.deadline) }}
                      </small>
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
                  <i class="fas fa-ranking-star me-2"></i>
                  Ranking de Estudiantes
                </h5>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Ranking</th>
                        <th>Estudiante</th>
                        <th>Puntuación Total</th>
                        <th>Entrenamientos</th>
                        <th>Objetivos Cumplidos</th>
                        <th>Consistencia</th>
                        <th>Última Actividad</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(student, index) in rankedStudents" :key="student.id">
                        <td>
                          <span class="ranking-badge" :class="getRankingClass(index)">
                            {{ index + 1 }}
                          </span>
                        </td>
                        <td>
                          <div class="student-info">
                            <img :src="student.avatar" :alt="student.name" class="student-avatar">
                            <div>
                              <div class="student-name">{{ student.name }}</div>
                              <small class="text-muted">{{ student.email }}</small>
                            </div>
                          </div>
                        </td>
                        <td>
                          <span class="score-badge">{{ student.totalScore }}</span>
                        </td>
                        <td>{{ student.completedWorkouts }}</td>
                        <td>
                          <span class="text-success">{{ student.completedGoals }}</span> / 
                          <span class="text-muted">{{ student.totalGoals }}</span>
                        </td>
                        <td>
                          <div class="consistency-indicator">
                            <div class="progress" style="height: 6px;">
                              <div class="progress-bar" 
                                   :class="getConsistencyClass(student.consistency)"
                                   :style="{ width: student.consistency + '%' }"></div>
                            </div>
                            <small>{{ student.consistency }}%</small>
                          </div>
                        </td>
                        <td>
                          <small class="text-muted">{{ formatRelativeDate(student.lastActivity) }}</small>
                        </td>
                        <td>
                          <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" @click="viewStudentDetail(student.id)">
                              <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-outline-success" @click="sendMessage(student.id)">
                              <i class="fas fa-comment"></i>
                            </button>
                          </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import TrainingAnalyticsComponent from '@/components/Analytics/TrainingAnalyticsComponent.vue'
import PerformanceChartsComponent from '@/components/Analytics/PerformanceChartsComponent.vue'
import Chart from 'chart.js/auto'

const router = useRouter()

const activeTab = ref('overview')
const selectedStudent = ref('all')
const progressChart = ref(null)
let progressChartInstance = null

const summaryStats = ref({
  totalStudents: 24,
  newStudents: 3,
  totalWorkouts: 156,
  workoutGrowth: 12,
  goalsCompleted: 78,
  goalsChange: 5,
  avgSessionTime: 45,
  timeIncrease: 8
})

const students = ref([
  { id: 1, name: 'Ana García', email: 'ana@email.com', avatar: '/avatars/ana.jpg' },
  { id: 2, name: 'Carlos López', email: 'carlos@email.com', avatar: '/avatars/carlos.jpg' },
  { id: 3, name: 'María Rodríguez', email: 'maria@email.com', avatar: '/avatars/maria.jpg' },
  { id: 4, name: 'Juan Martínez', email: 'juan@email.com', avatar: '/avatars/juan.jpg' },
  { id: 5, name: 'Laura Sánchez', email: 'laura@email.com', avatar: '/avatars/laura.jpg' }
])

const currentGoals = ref([
  {
    id: 1,
    title: 'Correr 5K en menos de 25 minutos',
    status: 'En Progreso',
    progress: 75,
    studentName: 'Ana García',
    deadline: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000)
  },
  {
    id: 2,
    title: 'Completar 20 entrenamientos este mes',
    status: 'Completado',
    progress: 100,
    studentName: 'Carlos López',
    deadline: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000)
  },
  {
    id: 3,
    title: 'Mejorar resistencia cardiovascular',
    status: 'En Progreso',
    progress: 45,
    studentName: 'María Rodríguez',
    deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
  },
  {
    id: 4,
    title: 'Perder 5kg de peso corporal',
    status: 'Atrasado',
    progress: 30,
    studentName: 'Juan Martínez',
    deadline: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
  }
])

const rankedStudents = ref([
  {
    id: 1,
    name: 'Ana García',
    email: 'ana@email.com',
    avatar: '/avatars/ana.jpg',
    totalScore: 95,
    completedWorkouts: 28,
    completedGoals: 8,
    totalGoals: 10,
    consistency: 92,
    lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000)
  },
  {
    id: 2,
    name: 'Carlos López',
    email: 'carlos@email.com',
    avatar: '/avatars/carlos.jpg',
    totalScore: 88,
    completedWorkouts: 25,
    completedGoals: 7,
    totalGoals: 9,
    consistency: 85,
    lastActivity: new Date(Date.now() - 5 * 60 * 60 * 1000)
  },
  {
    id: 3,
    name: 'María Rodríguez',
    email: 'maria@email.com',
    avatar: '/avatars/maria.jpg',
    totalScore: 82,
    completedWorkouts: 22,
    completedGoals: 6,
    totalGoals: 8,
    consistency: 78,
    lastActivity: new Date(Date.now() - 24 * 60 * 60 * 1000)
  },
  {
    id: 4,
    name: 'Juan Martínez',
    email: 'juan@email.com',
    avatar: '/avatars/juan.jpg',
    totalScore: 79,
    completedWorkouts: 20,
    completedGoals: 5,
    totalGoals: 8,
    consistency: 71,
    lastActivity: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
  },
  {
    id: 5,
    name: 'Laura Sánchez',
    email: 'laura@email.com',
    avatar: '/avatars/laura.jpg',
    totalScore: 76,
    completedWorkouts: 18,
    completedGoals: 4,
    totalGoals: 7,
    consistency: 89,
    lastActivity: new Date(Date.now() - 6 * 60 * 60 * 1000)
  }
])

const updateAnalytics = () => {
  // Actualizar datos basados en el estudiante seleccionado
  console.log('Actualizando analytics para:', selectedStudent.value)
}

const generateReport = () => {
  // Generar reporte PDF
  console.log('Generando reporte...')
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

const getRankingClass = (index) => {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return 'default'
}

const getConsistencyClass = (consistency) => {
  if (consistency >= 80) return 'bg-success'
  if (consistency >= 60) return 'bg-warning'
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

const viewStudentDetail = (studentId) => {
  router.push(`/coach/students/${studentId}`)
}

const sendMessage = (studentId) => {
  router.push(`/coach/communication?student=${studentId}`)
}

onMounted(() => {
  updateAnalytics()
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

.summary-card {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  height: 100%;
}

.summary-card:hover {
  transform: translateY(-2px);
}

.card-icon {
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

.card-content {
  flex: 1;
}

.card-value {
  font-size: 2rem;
  font-weight: bold;
  color: #212529;
  line-height: 1;
}

.card-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0.25rem 0;
}

.card-change {
  font-size: 0.75rem;
  font-weight: 600;
}

.card-change.positive {
  color: #198754;
}

.card-change.negative {
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

.goals-list {
  max-height: 400px;
  overflow-y: auto;
}

.goal-item {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background: #f8f9fa;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.goal-title {
  font-weight: 600;
  color: #212529;
}

.goal-progress {
  margin-bottom: 0.5rem;
}

.goal-meta {
  display: flex;
  justify-content: space-between;
}

.ranking-badge {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
}

.ranking-badge.gold {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #8b6914;
}

.ranking-badge.silver {
  background: linear-gradient(45deg, #c0c0c0, #e8e8e8);
  color: #666;
}

.ranking-badge.bronze {
  background: linear-gradient(45deg, #cd7f32, #daa520);
  color: white;
}

.ranking-badge.default {
  background: #6c757d;
}

.student-info {
  display: flex;
  align-items: center;
}

.student-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 0.75rem;
  object-fit: cover;
}

.student-name {
  font-weight: 600;
  color: #212529;
}

.score-badge {
  background: linear-gradient(45deg, #0d6efd, #6610f2);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-weight: bold;
}

.consistency-indicator {
  min-width: 80px;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
  background: #f8f9fa;
}

.table td {
  vertical-align: middle;
}
</style>
<template>
  <div class="coach-student-detail">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Student Not Found -->
    <div v-else-if="!student" class="text-center py-5">
      <font-awesome-icon icon="fas fa-user-slash" class="fa-3x text-muted mb-3" />
      <h4 class="text-muted">Alumno no encontrado</h4>
      <router-link to="/coach/students" class="btn btn-primary">
        Volver a Mis Alumnos
      </router-link>
    </div>

    <!-- Student Detail Content -->
    <div v-else>
      <!-- Header -->
      <div class="student-header mb-4">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="d-flex align-items-center">
              <router-link to="/coach/students" class="btn btn-outline-light me-3">
                <font-awesome-icon icon="fas fa-arrow-left" />
              </router-link>
              <div class="student-info d-flex align-items-center">
                <img 
                  :src="student.avatar || '/logo/default-avatar.png'" 
                  :alt="student.name" 
                  class="rounded-circle me-3"
                  width="80"
                  height="80"
                >
                <div>
                  <h1 class="h2 mb-0 text-white">{{ student.name }}</h1>
                  <p class="mb-1 text-white-50">{{ student.email }}</p>
                  <span 
                    class="badge" 
                    :class="{
                      'bg-success': student.status === 'active',
                      'bg-warning': student.status === 'pending',
                      'bg-secondary': student.status === 'inactive'
                    }"
                  >
                    {{ getStatusText(student.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4 text-end">
            <div class="btn-group" role="group">
              <button class="btn btn-light" @click="sendMessage">
                <font-awesome-icon icon="fas fa-comment" class="me-2" />
                Mensaje
              </button>
              <button class="btn btn-success" @click="createGoal">
                <font-awesome-icon icon="fas fa-target" class="me-2" />
                Nuevo Objetivo
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="card stats-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="stats-icon bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-2">
                <font-awesome-icon icon="fas fa-running" />
              </div>
              <h3 class="mb-0">{{ student.stats.totalActivities }}</h3>
              <p class="text-muted mb-0 small">Actividades Totales</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card stats-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="stats-icon bg-success bg-opacity-10 text-success rounded-circle mx-auto mb-2">
                <font-awesome-icon icon="fas fa-target" />
              </div>
              <h3 class="mb-0">{{ student.stats.activeGoals }}</h3>
              <p class="text-muted mb-0 small">Objetivos Activos</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card stats-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="stats-icon bg-info bg-opacity-10 text-info rounded-circle mx-auto mb-2">
                <font-awesome-icon icon="fas fa-clock" />
              </div>
              <h3 class="mb-0">{{ student.stats.weeklyHours }}</h3>
              <p class="text-muted mb-0 small">Horas/Semana</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card stats-card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="stats-icon bg-warning bg-opacity-10 text-warning rounded-circle mx-auto mb-2">
                <font-awesome-icon icon="fas fa-chart-line" />
              </div>
              <h3 class="mb-0">{{ student.monthlyProgress }}%</h3>
              <p class="text-muted mb-0 small">Progreso Mensual</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row">
        <!-- Left Column -->
        <div class="col-lg-8">
          <!-- Navigation Tabs -->
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white border-0">
              <ul class="nav nav-tabs card-header-tabs" role="tablist">
                <li class="nav-item" role="presentation">
                  <button 
                    class="nav-link" 
                    :class="{ active: activeTab === 'activities' }"
                    @click="activeTab = 'activities'"
                  >
                    <font-awesome-icon icon="fas fa-running" class="me-2" />
                    Actividades
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button 
                    class="nav-link" 
                    :class="{ active: activeTab === 'goals' }"
                    @click="activeTab = 'goals'"
                  >
                    <font-awesome-icon icon="fas fa-target" class="me-2" />
                    Objetivos
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button 
                    class="nav-link" 
                    :class="{ active: activeTab === 'progress' }"
                    @click="activeTab = 'progress'"
                  >
                    <font-awesome-icon icon="fas fa-chart-bar" class="me-2" />
                    Progreso
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button 
                    class="nav-link" 
                    :class="{ active: activeTab === 'integrations' }"
                    @click="activeTab = 'integrations'"
                  >
                    <font-awesome-icon icon="fas fa-plug" class="me-2" />
                    Integraciones
                  </button>
                </li>
              </ul>
            </div>
            
            <div class="card-body">
              <!-- Activities Tab -->
              <div v-if="activeTab === 'activities'">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="mb-0">Actividades Recientes</h5>
                  <select class="form-select form-select-sm" style="width: auto;" v-model="activitiesFilter">
                    <option value="all">Todas</option>
                    <option value="running">Carrera</option>
                    <option value="cycling">Ciclismo</option>
                    <option value="swimming">Natación</option>
                  </select>
                </div>
                
                <div v-if="filteredActivities.length === 0" class="text-center py-4 text-muted">
                  <font-awesome-icon icon="fas fa-inbox" class="fa-2x mb-3" />
                  <p>No hay actividades registradas</p>
                </div>
                
                <div v-else>
                  <div v-for="activity in filteredActivities" :key="activity.id" class="activity-item border-bottom py-3">
                    <div class="d-flex align-items-center">
                      <div class="activity-icon me-3">
                        <font-awesome-icon 
                          :icon="getActivityIcon(activity.type)" 
                          class="text-primary"
                        />
                      </div>
                      <div class="flex-grow-1">
                        <h6 class="mb-1">{{ activity.name }}</h6>
                        <div class="row text-muted small">
                          <div class="col-md-3">
                            <font-awesome-icon icon="fas fa-clock" class="me-1" />
                            {{ activity.duration }}
                          </div>
                          <div class="col-md-3">
                            <font-awesome-icon icon="fas fa-route" class="me-1" />
                            {{ activity.distance }}
                          </div>
                          <div class="col-md-3">
                            <font-awesome-icon icon="fas fa-tachometer-alt" class="me-1" />
                            {{ activity.pace }}
                          </div>
                          <div class="col-md-3">
                            <font-awesome-icon icon="fas fa-calendar" class="me-1" />
                            {{ formatDate(activity.date) }}
                          </div>
                        </div>
                      </div>
                      <div class="activity-actions">
                        <button class="btn btn-sm btn-outline-primary me-2" @click="viewActivity(activity.id)">
                          <font-awesome-icon icon="fas fa-eye" />
                        </button>
                        <button class="btn btn-sm btn-outline-success" @click="giveFeedback(activity)">
                          <font-awesome-icon icon="fas fa-comment" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Goals Tab -->
              <div v-if="activeTab === 'goals'">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="mb-0">Objetivos de Entrenamiento</h5>
                  <button class="btn btn-primary btn-sm" @click="createGoal">
                    <font-awesome-icon icon="fas fa-plus" class="me-2" />
                    Nuevo Objetivo
                  </button>
                </div>
                
                <div v-if="student.goals.length === 0" class="text-center py-4 text-muted">
                  <font-awesome-icon icon="fas fa-target" class="fa-2x mb-3" />
                  <p>No hay objetivos definidos</p>
                  <button class="btn btn-primary" @click="createGoal">
                    Crear Primer Objetivo
                  </button>
                </div>
                
                <div v-else>
                  <div v-for="goal in student.goals" :key="goal.id" class="goal-item card mb-3">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="mb-0">{{ goal.title }}</h6>
                        <span 
                          class="badge" 
                          :class="{
                            'bg-success': goal.status === 'completed',
                            'bg-primary': goal.status === 'active',
                            'bg-warning': goal.status === 'paused'
                          }"
                        >
                          {{ getGoalStatusText(goal.status) }}
                        </span>
                      </div>
                      <p class="text-muted mb-2">{{ goal.description }}</p>
                      <div class="progress mb-2" style="height: 8px;">
                        <div 
                          class="progress-bar" 
                          :style="{ width: goal.progress + '%' }"
                          :class="{
                            'bg-success': goal.progress >= 80,
                            'bg-warning': goal.progress >= 50 && goal.progress < 80,
                            'bg-danger': goal.progress < 50
                          }"
                        ></div>
                      </div>
                      <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                          Progreso: {{ goal.progress }}% | 
                          Fecha límite: {{ formatDate(goal.deadline) }}
                        </small>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="editGoal(goal)">
                            <font-awesome-icon icon="fas fa-edit" />
                          </button>
                          <button class="btn btn-outline-success" @click="updateGoalProgress(goal)">
                            <font-awesome-icon icon="fas fa-chart-line" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Progress Tab -->
              <div v-if="activeTab === 'progress'">
                <h5 class="mb-3">Análisis de Progreso</h5>
                <div class="text-center py-5 text-muted">
                  <font-awesome-icon icon="fas fa-chart-area" class="fa-3x mb-3" />
                  <p>Gráficos de progreso próximamente</p>
                  <small>Aquí se mostrarán gráficos detallados del rendimiento del alumno</small>
                </div>
              </div>
              
              <!-- Integrations Tab -->
              <div v-if="activeTab === 'integrations'">
                <CoachStudentIntegrationsComponent 
                  :student="student" 
                  :student-name="student.name" />
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column -->
        <div class="col-lg-4">
          <!-- Student Info -->
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white border-0">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-info-circle" class="me-2 text-primary" />
                Información del Alumno
              </h5>
            </div>
            <div class="card-body">
              <div class="info-item mb-3">
                <label class="text-muted small">Fecha de registro</label>
                <p class="mb-0">{{ formatDate(student.registrationDate) }}</p>
              </div>
              <div class="info-item mb-3">
                <label class="text-muted small">Última actividad</label>
                <p class="mb-0">{{ formatLastActivity(student.lastActivity) }}</p>
              </div>
              <div class="info-item mb-3">
                <label class="text-muted small">Nivel de experiencia</label>
                <p class="mb-0">{{ student.experienceLevel || 'No especificado' }}</p>
              </div>
              <div class="info-item">
                <label class="text-muted small">Objetivos principales</label>
                <p class="mb-0">{{ student.mainGoals || 'No especificados' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Recent Feedback -->
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-comments" class="me-2 text-success" />
                Feedback Reciente
              </h5>
            </div>
            <div class="card-body">
              <div v-if="student.recentFeedback.length === 0" class="text-center py-3 text-muted">
                <font-awesome-icon icon="fas fa-comment-slash" class="fa-2x mb-2" />
                <p class="mb-0 small">No hay feedback reciente</p>
              </div>
              
              <div v-else>
                <div v-for="feedback in student.recentFeedback" :key="feedback.id" class="feedback-item border-bottom py-2">
                  <div class="d-flex justify-content-between align-items-start mb-1">
                    <small class="text-muted">{{ formatDate(feedback.date) }}</small>
                    <span 
                      class="badge badge-sm" 
                      :class="{
                        'bg-success': feedback.type === 'positive',
                        'bg-warning': feedback.type === 'neutral',
                        'bg-info': feedback.type === 'suggestion'
                      }"
                    >
                      {{ getFeedbackTypeText(feedback.type) }}
                    </span>
                  </div>
                  <p class="mb-0 small">{{ feedback.message }}</p>
                </div>
              </div>
              
              <div class="d-grid mt-3">
                <button class="btn btn-success btn-sm" @click="giveFeedback()">
                  <font-awesome-icon icon="fas fa-plus" class="me-2" />
                  Dar Feedback
                </button>
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
import { useRoute, useRouter } from 'vue-router'
import CoachStudentIntegrationsComponent from '@/components/Coach/CoachStudentIntegrationsComponent.vue'

export default {
  name: 'CoachStudentDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const student = ref(null)
    const activeTab = ref('activities')
    const activitiesFilter = ref('all')
    
    // Computed
    const filteredActivities = computed(() => {
      if (!student.value || !student.value.activities) return []
      
      if (activitiesFilter.value === 'all') {
        return student.value.activities
      }
      
      return student.value.activities.filter(activity => 
        activity.type.toLowerCase() === activitiesFilter.value
      )
    })
    
    // Methods
    const loadStudent = async () => {
      try {
        loading.value = true
        const studentId = route.params.id
        
        // Simular carga de datos - aquí se conectaría con el backend
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Datos simulados
        student.value = {
          id: parseInt(studentId),
          name: 'Ana García',
          email: 'ana.garcia@email.com',
          avatar: null,
          status: 'active',
          registrationDate: '2024-01-15',
          lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000),
          monthlyProgress: 85,
          experienceLevel: 'Intermedio',
          mainGoals: 'Mejorar resistencia cardiovascular',
          stats: {
            totalActivities: 24,
            activeGoals: 3,
            weeklyHours: 8
          },
          activities: [
            {
              id: 1,
              name: 'Carrera matutina',
              type: 'running',
              duration: '45 min',
              distance: '8.5 km',
              pace: '5:18 min/km',
              date: new Date(Date.now() - 2 * 60 * 60 * 1000)
            },
            {
              id: 2,
              name: 'Entrenamiento en bicicleta',
              type: 'cycling',
              duration: '1h 20min',
              distance: '35 km',
              pace: '26.2 km/h',
              date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
            }
          ],
          goals: [
            {
              id: 1,
              title: 'Correr 10K en menos de 50 minutos',
              description: 'Mejorar el tiempo en distancia de 10 kilómetros',
              status: 'active',
              progress: 75,
              deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
            },
            {
              id: 2,
              title: 'Entrenar 5 días por semana',
              description: 'Mantener consistencia en el entrenamiento',
              status: 'active',
              progress: 60,
              deadline: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000)
            }
          ],
          recentFeedback: [
            {
              id: 1,
              type: 'positive',
              message: 'Excelente progreso en la última semana. Sigue así!',
              date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
            },
            {
              id: 2,
              type: 'suggestion',
              message: 'Considera agregar más ejercicios de fuerza a tu rutina',
              date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
            }
          ]
        }
        
      } catch (error) {
        console.error('Error loading student:', error)
      } finally {
        loading.value = false
      }
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        active: 'Activo',
        pending: 'Pendiente',
        inactive: 'Inactivo'
      }
      return statusMap[status] || status
    }
    
    const getActivityIcon = (type) => {
      const iconMap = {
        running: 'fas fa-running',
        cycling: 'fas fa-biking',
        swimming: 'fas fa-swimmer',
        gym: 'fas fa-dumbbell'
      }
      return iconMap[type] || 'fas fa-running'
    }
    
    const getGoalStatusText = (status) => {
      const statusMap = {
        active: 'Activo',
        completed: 'Completado',
        paused: 'Pausado'
      }
      return statusMap[status] || status
    }
    
    const getFeedbackTypeText = (type) => {
      const typeMap = {
        positive: 'Positivo',
        neutral: 'Neutral',
        suggestion: 'Sugerencia'
      }
      return typeMap[type] || type
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const formatLastActivity = (date) => {
      const now = new Date()
      const diff = now - date
      const hours = Math.floor(diff / (1000 * 60 * 60))
      
      if (hours < 1) {
        return 'Hace menos de 1 hora'
      } else if (hours < 24) {
        return `Hace ${hours} hora${hours > 1 ? 's' : ''}`
      } else {
        const days = Math.floor(hours / 24)
        return `Hace ${days} día${days > 1 ? 's' : ''}`
      }
    }
    
    const viewActivity = (activityId) => {
      router.push(`/activity/${activityId}`)
    }
    
    const sendMessage = () => {
      console.log('Enviar mensaje al alumno')
      // Implementar modal de mensaje
    }
    
    const createGoal = () => {
      console.log('Crear nuevo objetivo')
      // Implementar modal de creación de objetivo
    }
    
    const giveFeedback = (activity = null) => {
      console.log('Dar feedback', activity ? `para actividad ${activity.id}` : 'general')
      // Implementar modal de feedback
    }
    
    const editGoal = (goal) => {
      console.log('Editar objetivo:', goal.title)
      // Implementar modal de edición de objetivo
    }
    
    const updateGoalProgress = (goal) => {
      console.log('Actualizar progreso del objetivo:', goal.title)
      // Implementar modal de actualización de progreso
    }
    
    onMounted(() => {
      loadStudent()
    })
    
    return {
      loading,
      student,
      activeTab,
      activitiesFilter,
      filteredActivities,
      getStatusText,
      getActivityIcon,
      getGoalStatusText,
      getFeedbackTypeText,
      formatDate,
      formatLastActivity,
      viewActivity,
      sendMessage,
      createGoal,
      giveFeedback,
      editGoal,
      updateGoalProgress
    }
  }
}
</script>

<style scoped>
.coach-student-detail {
  padding: 1.5rem;
}

.student-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.student-info img {
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.stats-card {
  transition: transform 0.2s ease-in-out;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.stats-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.nav-tabs .nav-link {
  border: none;
  color: #6c757d;
}

.nav-tabs .nav-link.active {
  background-color: transparent;
  border-bottom: 2px solid #0d6efd;
  color: #0d6efd;
}

.activity-item:last-child {
  border-bottom: none !important;
}

.activity-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 50%;
  font-size: 1.1rem;
}

.goal-item {
  border-left: 4px solid #0d6efd;
}

.feedback-item:last-child {
  border-bottom: none !important;
}

.info-item label {
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@media (max-width: 768px) {
  .coach-student-detail {
    padding: 1rem;
  }
  
  .student-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .student-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
  
  .student-info {
    flex-direction: column;
    text-align: center;
  }
  
  .student-info img {
    margin-bottom: 1rem;
  }
}
</style>
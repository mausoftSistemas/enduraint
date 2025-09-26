<template>
  <div class="student-dashboard">
    <!-- Welcome Header -->
    <div class="welcome-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-1 text-white">¡Hola, {{ user.name }}!</h1>
          <p class="mb-0 text-white-50">Aquí tienes un resumen de tu progreso de entrenamiento</p>
        </div>
        <div class="col-md-4 text-end">
          <div class="welcome-stats text-white">
            <div class="d-flex justify-content-end align-items-center">
              <div class="text-end me-3">
                <div class="h4 mb-0">{{ todayStats.activities }}</div>
                <small class="text-white-50">Actividades hoy</small>
              </div>
              <div class="text-end">
                <div class="h4 mb-0">{{ todayStats.duration }}</div>
                <small class="text-white-50">Tiempo total</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card stats-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="stats-icon bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-running" />
            </div>
            <h3 class="mb-1">{{ weeklyStats.activities }}</h3>
            <p class="text-muted mb-0 small">Actividades esta semana</p>
            <div class="progress mt-2" style="height: 4px;">
              <div class="progress-bar bg-primary" :style="{ width: (weeklyStats.activities / weeklyStats.goal * 100) + '%' }"></div>
            </div>
            <small class="text-muted">Meta: {{ weeklyStats.goal }} actividades</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card stats-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="stats-icon bg-success bg-opacity-10 text-success rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-clock" />
            </div>
            <h3 class="mb-1">{{ weeklyStats.duration }}</h3>
            <p class="text-muted mb-0 small">Horas entrenadas</p>
            <div class="progress mt-2" style="height: 4px;">
              <div class="progress-bar bg-success" :style="{ width: (parseFloat(weeklyStats.duration) / weeklyStats.durationGoal * 100) + '%' }"></div>
            </div>
            <small class="text-muted">Meta: {{ weeklyStats.durationGoal }}h semanales</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card stats-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="stats-icon bg-info bg-opacity-10 text-info rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-route" />
            </div>
            <h3 class="mb-1">{{ weeklyStats.distance }}</h3>
            <p class="text-muted mb-0 small">Kilómetros recorridos</p>
            <div class="progress mt-2" style="height: 4px;">
              <div class="progress-bar bg-info" :style="{ width: (parseFloat(weeklyStats.distance) / weeklyStats.distanceGoal * 100) + '%' }"></div>
            </div>
            <small class="text-muted">Meta: {{ weeklyStats.distanceGoal }}km semanales</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card stats-card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="stats-icon bg-warning bg-opacity-10 text-warning rounded-circle mx-auto mb-3">
              <font-awesome-icon icon="fas fa-target" />
            </div>
            <h3 class="mb-1">{{ activeGoals.length }}</h3>
            <p class="text-muted mb-0 small">Objetivos activos</p>
            <div class="progress mt-2" style="height: 4px;">
              <div class="progress-bar bg-warning" :style="{ width: averageGoalProgress + '%' }"></div>
            </div>
            <small class="text-muted">Progreso promedio: {{ averageGoalProgress }}%</small>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Recent Activities -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-history" class="me-2 text-primary" />
                Actividades Recientes
              </h5>
              <router-link to="/activities" class="btn btn-outline-primary btn-sm">
                Ver todas
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="recentActivities.length === 0" class="text-center py-4 text-muted">
              <font-awesome-icon icon="fas fa-inbox" class="fa-2x mb-3" />
              <p class="mb-2">No tienes actividades registradas</p>
              <router-link to="/activity/new" class="btn btn-primary">
                <font-awesome-icon icon="fas fa-plus" class="me-2" />
                Registrar Primera Actividad
              </router-link>
            </div>
            
            <div v-else>
              <div v-for="activity in recentActivities" :key="activity.id" class="activity-item border-bottom py-3">
                <div class="d-flex align-items-center">
                  <div class="activity-icon me-3">
                    <font-awesome-icon 
                      :icon="getActivityIcon(activity.type)" 
                      class="text-primary"
                    />
                  </div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                      <div>
                        <h6 class="mb-1">{{ activity.name }}</h6>
                        <div class="activity-stats text-muted small">
                          <span class="me-3">
                            <font-awesome-icon icon="fas fa-clock" class="me-1" />
                            {{ activity.duration }}
                          </span>
                          <span class="me-3">
                            <font-awesome-icon icon="fas fa-route" class="me-1" />
                            {{ activity.distance }}
                          </span>
                          <span>
                            <font-awesome-icon icon="fas fa-tachometer-alt" class="me-1" />
                            {{ activity.pace }}
                          </span>
                        </div>
                      </div>
                      <div class="text-end">
                        <small class="text-muted">{{ formatTimeAgo(activity.date) }}</small>
                        <div class="mt-1">
                          <span v-if="activity.coachFeedback" class="badge bg-success me-1">
                            <font-awesome-icon icon="fas fa-comment" class="me-1" />
                            Feedback
                          </span>
                          <span v-if="activity.personalRecord" class="badge bg-warning">
                            <font-awesome-icon icon="fas fa-trophy" class="me-1" />
                            PR
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="text-center mt-3">
                <router-link to="/activities" class="btn btn-outline-primary">
                  Ver todas las actividades
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Training Goals Progress -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-target" class="me-2 text-success" />
                Progreso de Objetivos
              </h5>
              <router-link to="/student/goals" class="btn btn-outline-success btn-sm">
                Gestionar objetivos
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="activeGoals.length === 0" class="text-center py-4 text-muted">
              <font-awesome-icon icon="fas fa-target" class="fa-2x mb-3" />
              <p class="mb-2">No tienes objetivos activos</p>
              <p class="small mb-3">Habla con tu entrenador para establecer objetivos personalizados</p>
            </div>
            
            <div v-else>
              <div v-for="goal in activeGoals" :key="goal.id" class="goal-item mb-4">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h6 class="mb-1">{{ goal.title }}</h6>
                    <p class="text-muted mb-0 small">{{ goal.description }}</p>
                  </div>
                  <span class="badge bg-primary">{{ goal.progress }}%</span>
                </div>
                
                <div class="progress mb-2" style="height: 10px;">
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
                    <font-awesome-icon icon="fas fa-calendar" class="me-1" />
                    Fecha límite: {{ formatDate(goal.deadline) }}
                  </small>
                  <small class="text-muted">
                    {{ getDaysRemaining(goal.deadline) }} días restantes
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Coach Info -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-user-tie" class="me-2 text-info" />
              Mi Entrenador
            </h5>
          </div>
          <div class="card-body">
            <div v-if="!coach" class="text-center py-3 text-muted">
              <font-awesome-icon icon="fas fa-user-plus" class="fa-2x mb-2" />
              <p class="mb-2 small">No tienes entrenador asignado</p>
              <button class="btn btn-primary btn-sm">
                Buscar entrenador
              </button>
            </div>
            
            <div v-else class="coach-info">
              <div class="d-flex align-items-center mb-3">
                <img 
                  :src="coach.avatar || '/logo/default-avatar.png'" 
                  :alt="coach.name" 
                  class="rounded-circle me-3"
                  width="50"
                  height="50"
                >
                <div>
                  <h6 class="mb-0">{{ coach.name }}</h6>
                  <small class="text-muted">{{ coach.specialization }}</small>
                </div>
              </div>
              
              <div class="coach-stats mb-3">
                <div class="row text-center">
                  <div class="col-4">
                    <div class="h6 mb-0">{{ coach.experience }}</div>
                    <small class="text-muted">Años exp.</small>
                  </div>
                  <div class="col-4">
                    <div class="h6 mb-0">{{ coach.students }}</div>
                    <small class="text-muted">Alumnos</small>
                  </div>
                  <div class="col-4">
                    <div class="h6 mb-0">{{ coach.rating }}</div>
                    <small class="text-muted">Rating</small>
                  </div>
                </div>
              </div>
              
              <div class="d-grid gap-2">
                <button class="btn btn-primary btn-sm" @click="contactCoach">
                  <font-awesome-icon icon="fas fa-comment" class="me-2" />
                  Enviar mensaje
                </button>
                <button class="btn btn-outline-primary btn-sm" @click="scheduleSession">
                  <font-awesome-icon icon="fas fa-calendar-plus" class="me-2" />
                  Agendar sesión
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Feedback -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-comments" class="me-2 text-warning" />
              Feedback Reciente
            </h5>
          </div>
          <div class="card-body">
            <div v-if="recentFeedback.length === 0" class="text-center py-3 text-muted">
              <font-awesome-icon icon="fas fa-comment-slash" class="fa-2x mb-2" />
              <p class="mb-0 small">No hay feedback reciente</p>
            </div>
            
            <div v-else>
              <div v-for="feedback in recentFeedback" :key="feedback.id" class="feedback-item border-bottom py-2">
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
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-bolt" class="me-2 text-danger" />
              Acciones Rápidas
            </h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <router-link to="/activity/new" class="btn btn-primary">
                <font-awesome-icon icon="fas fa-plus" class="me-2" />
                Registrar Actividad
              </router-link>
              <router-link to="/student/progress" class="btn btn-outline-primary">
                <font-awesome-icon icon="fas fa-chart-line" class="me-2" />
                Ver Progreso
              </router-link>
              <router-link to="/student/goals" class="btn btn-outline-success">
                <font-awesome-icon icon="fas fa-target" class="me-2" />
                Mis Objetivos
              </router-link>
              <button class="btn btn-outline-info" @click="syncDevices">
                <font-awesome-icon icon="fas fa-sync" class="me-2" />
                Sincronizar Dispositivos
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'StudentDashboardView',
  setup() {
    const authStore = useAuthStore()
    const user = computed(() => authStore.user)
    
    // Reactive data
    const todayStats = ref({
      activities: 1,
      duration: '45min'
    })
    
    const weeklyStats = ref({
      activities: 4,
      goal: 5,
      duration: '6.5',
      durationGoal: 8,
      distance: '32.5',
      distanceGoal: 40
    })
    
    const recentActivities = ref([
      {
        id: 1,
        name: 'Carrera matutina',
        type: 'running',
        duration: '45 min',
        distance: '8.5 km',
        pace: '5:18 min/km',
        date: new Date(Date.now() - 2 * 60 * 60 * 1000),
        coachFeedback: true,
        personalRecord: false
      },
      {
        id: 2,
        name: 'Entrenamiento en bicicleta',
        type: 'cycling',
        duration: '1h 20min',
        distance: '35 km',
        pace: '26.2 km/h',
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
        coachFeedback: false,
        personalRecord: true
      },
      {
        id: 3,
        name: 'Natación en piscina',
        type: 'swimming',
        duration: '30 min',
        distance: '1.5 km',
        pace: '2:00 min/100m',
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
        coachFeedback: true,
        personalRecord: false
      }
    ])
    
    const activeGoals = ref([
      {
        id: 1,
        title: 'Correr 10K en menos de 50 minutos',
        description: 'Mejorar el tiempo en distancia de 10 kilómetros',
        progress: 75,
        deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
      },
      {
        id: 2,
        title: 'Entrenar 5 días por semana',
        description: 'Mantener consistencia en el entrenamiento',
        progress: 60,
        deadline: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000)
      }
    ])
    
    const coach = ref({
      id: 1,
      name: 'Carlos Mendoza',
      specialization: 'Entrenamiento de resistencia',
      experience: 8,
      students: 25,
      rating: 4.9,
      avatar: null
    })
    
    const recentFeedback = ref([
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
    ])
    
    // Computed
    const averageGoalProgress = computed(() => {
      if (activeGoals.value.length === 0) return 0
      const total = activeGoals.value.reduce((sum, goal) => sum + goal.progress, 0)
      return Math.round(total / activeGoals.value.length)
    })
    
    // Methods
    const getActivityIcon = (type) => {
      const iconMap = {
        running: 'fas fa-running',
        cycling: 'fas fa-biking',
        swimming: 'fas fa-swimmer',
        gym: 'fas fa-dumbbell'
      }
      return iconMap[type] || 'fas fa-running'
    }
    
    const formatTimeAgo = (date) => {
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
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const getDaysRemaining = (deadline) => {
      const now = new Date()
      const diff = deadline - now
      const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
      return Math.max(0, days)
    }
    
    const getFeedbackTypeText = (type) => {
      const typeMap = {
        positive: 'Positivo',
        neutral: 'Neutral',
        suggestion: 'Sugerencia'
      }
      return typeMap[type] || type
    }
    
    const contactCoach = () => {
      console.log('Contactar entrenador')
      // Implementar modal de mensaje
    }
    
    const scheduleSession = () => {
      console.log('Agendar sesión')
      // Implementar modal de agendamiento
    }
    
    const syncDevices = () => {
      console.log('Sincronizar dispositivos')
      // Implementar sincronización con Garmin/Strava
    }
    
    const loadDashboardData = async () => {
      try {
        // Aquí se cargarían los datos reales del backend
        console.log('Cargando datos del dashboard...')
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      user,
      todayStats,
      weeklyStats,
      recentActivities,
      activeGoals,
      coach,
      recentFeedback,
      averageGoalProgress,
      getActivityIcon,
      formatTimeAgo,
      formatDate,
      getDaysRemaining,
      getFeedbackTypeText,
      contactCoach,
      scheduleSession,
      syncDevices
    }
  }
}
</script>

<style scoped>
.student-dashboard {
  padding: 1.5rem;
}

.welcome-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.stats-card {
  transition: transform 0.2s ease-in-out;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.stats-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
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
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  border-left: 4px solid #0d6efd;
}

.coach-info img {
  object-fit: cover;
}

.feedback-item:last-child {
  border-bottom: none !important;
}

@media (max-width: 768px) {
  .student-dashboard {
    padding: 1rem;
  }
  
  .welcome-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .welcome-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
  
  .activity-stats {
    display: block;
  }
  
  .activity-stats span {
    display: block;
    margin-bottom: 0.25rem;
  }
}
</style>
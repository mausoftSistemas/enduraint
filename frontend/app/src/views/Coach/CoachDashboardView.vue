<template>
  <div class="coach-dashboard">
    <!-- Header -->
    <div class="dashboard-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-0">
            <font-awesome-icon icon="fas fa-user-tie" class="me-2 text-primary" />
            Panel de Entrenador
          </h1>
          <p class="text-muted mb-0">Gestiona a tus alumnos y sus entrenamientos</p>
        </div>
        <div class="col-md-4 text-end">
          <router-link to="/coach/students" class="btn btn-primary">
            <font-awesome-icon icon="fas fa-users" class="me-2" />
            Ver Todos los Alumnos
          </router-link>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="card stats-card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stats-icon bg-primary bg-opacity-10 text-primary rounded-circle me-3">
                <font-awesome-icon icon="fas fa-users" />
              </div>
              <div>
                <h3 class="mb-0">{{ totalStudents }}</h3>
                <p class="text-muted mb-0 small">Alumnos Activos</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card stats-card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stats-icon bg-success bg-opacity-10 text-success rounded-circle me-3">
                <font-awesome-icon icon="fas fa-target" />
              </div>
              <div>
                <h3 class="mb-0">{{ activeGoals }}</h3>
                <p class="text-muted mb-0 small">Objetivos Activos</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card stats-card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stats-icon bg-warning bg-opacity-10 text-warning rounded-circle me-3">
                <font-awesome-icon icon="fas fa-clock" />
              </div>
              <div>
                <h3 class="mb-0">{{ pendingFeedback }}</h3>
                <p class="text-muted mb-0 small">Feedback Pendiente</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card stats-card border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stats-icon bg-info bg-opacity-10 text-info rounded-circle me-3">
                <font-awesome-icon icon="fas fa-chart-line" />
              </div>
              <div>
                <h3 class="mb-0">{{ thisWeekActivities }}</h3>
                <p class="text-muted mb-0 small">Actividades Esta Semana</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Students Activity -->
    <div class="row">
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-activity" class="me-2 text-primary" />
              Actividad Reciente de Alumnos
            </h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </div>
            
            <div v-else-if="recentActivities.length === 0" class="text-center py-4 text-muted">
              <font-awesome-icon icon="fas fa-inbox" class="fa-2x mb-3" />
              <p>No hay actividades recientes</p>
            </div>
            
            <div v-else>
              <div v-for="activity in recentActivities" :key="activity.id" class="activity-item border-bottom py-3">
                <div class="d-flex align-items-center">
                  <div class="activity-avatar me-3">
                    <img :src="activity.student.avatar || '/logo/default-avatar.png'" 
                         :alt="activity.student.name" 
                         class="rounded-circle" 
                         width="40" 
                         height="40">
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ activity.student.name }}</h6>
                    <p class="mb-1 text-muted small">{{ activity.type }} - {{ activity.duration }}</p>
                    <p class="mb-0 text-muted small">{{ formatDate(activity.date) }}</p>
                  </div>
                  <div class="activity-actions">
                    <button class="btn btn-sm btn-outline-primary" @click="viewActivity(activity.id)">
                      <font-awesome-icon icon="fas fa-eye" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="col-lg-4 mb-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-bolt" class="me-2 text-primary" />
              Acciones Rápidas
            </h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button class="btn btn-outline-primary" @click="createNewGoal">
                <font-awesome-icon icon="fas fa-plus" class="me-2" />
                Crear Nuevo Objetivo
              </button>
              
              <button class="btn btn-outline-success" @click="sendFeedback">
                <font-awesome-icon icon="fas fa-comment" class="me-2" />
                Enviar Feedback
              </button>
              
              <button class="btn btn-outline-info" @click="viewReports">
                <font-awesome-icon icon="fas fa-chart-bar" class="me-2" />
                Ver Reportes
              </button>
              
              <router-link to="/coach/students" class="btn btn-outline-secondary">
                <font-awesome-icon icon="fas fa-users-cog" class="me-2" />
                Gestionar Alumnos
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Pending Tasks -->
        <div class="card border-0 shadow-sm mt-3">
          <div class="card-header bg-white border-0 pb-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-tasks" class="me-2 text-warning" />
              Tareas Pendientes
            </h5>
          </div>
          <div class="card-body">
            <div v-if="pendingTasks.length === 0" class="text-center py-3 text-muted">
              <font-awesome-icon icon="fas fa-check-circle" class="fa-2x mb-2" />
              <p class="mb-0 small">¡Todo al día!</p>
            </div>
            
            <div v-else>
              <div v-for="task in pendingTasks" :key="task.id" class="task-item py-2 border-bottom">
                <div class="d-flex align-items-center">
                  <div class="flex-grow-1">
                    <p class="mb-0 small">{{ task.description }}</p>
                    <p class="mb-0 text-muted small">{{ task.student }}</p>
                  </div>
                  <span class="badge bg-warning text-dark">{{ task.priority }}</span>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CoachDashboardView',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    
    // Stats data
    const totalStudents = ref(0)
    const activeGoals = ref(0)
    const pendingFeedback = ref(0)
    const thisWeekActivities = ref(0)
    
    // Recent activities
    const recentActivities = ref([])
    
    // Pending tasks
    const pendingTasks = ref([])
    
    // Methods
    const loadDashboardData = async () => {
      try {
        loading.value = true
        
        // Simular datos por ahora - aquí se conectaría con el backend
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        totalStudents.value = 12
        activeGoals.value = 8
        pendingFeedback.value = 3
        thisWeekActivities.value = 45
        
        recentActivities.value = [
          {
            id: 1,
            student: { name: 'Ana García', avatar: null },
            type: 'Carrera',
            duration: '45 min',
            date: new Date(Date.now() - 2 * 60 * 60 * 1000)
          },
          {
            id: 2,
            student: { name: 'Carlos López', avatar: null },
            type: 'Ciclismo',
            duration: '1h 20min',
            date: new Date(Date.now() - 4 * 60 * 60 * 1000)
          },
          {
            id: 3,
            student: { name: 'María Rodríguez', avatar: null },
            type: 'Natación',
            duration: '30 min',
            date: new Date(Date.now() - 6 * 60 * 60 * 1000)
          }
        ]
        
        pendingTasks.value = [
          {
            id: 1,
            description: 'Revisar progreso semanal',
            student: 'Ana García',
            priority: 'Alta'
          },
          {
            id: 2,
            description: 'Actualizar plan de entrenamiento',
            student: 'Carlos López',
            priority: 'Media'
          }
        ]
        
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (date) => {
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
    
    const createNewGoal = () => {
      // Implementar modal o navegación para crear objetivo
      console.log('Crear nuevo objetivo')
    }
    
    const sendFeedback = () => {
      // Implementar modal o navegación para enviar feedback
      console.log('Enviar feedback')
    }
    
    const viewReports = () => {
      // Implementar navegación a reportes
      console.log('Ver reportes')
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      loading,
      totalStudents,
      activeGoals,
      pendingFeedback,
      thisWeekActivities,
      recentActivities,
      pendingTasks,
      formatDate,
      viewActivity,
      createNewGoal,
      sendFeedback,
      viewReports
    }
  }
}
</script>

<style scoped>
.coach-dashboard {
  padding: 1.5rem;
}

.dashboard-header {
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
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.activity-item:last-child {
  border-bottom: none !important;
}

.activity-avatar img {
  object-fit: cover;
}

.task-item:last-child {
  border-bottom: none !important;
}

.card {
  transition: box-shadow 0.2s ease-in-out;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

@media (max-width: 768px) {
  .coach-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .dashboard-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
}
</style>
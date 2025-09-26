<template>
  <div class="student-goals">
    <!-- Header -->
    <div class="goals-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-1 text-white">Mis Objetivos de Entrenamiento</h1>
          <p class="mb-0 text-white-50">Sigue tu progreso y alcanza tus metas deportivas</p>
        </div>
        <div class="col-md-4 text-end">
          <div class="goals-summary text-white">
            <div class="row text-center">
              <div class="col-4">
                <div class="h4 mb-0">{{ activeGoals.length }}</div>
                <small class="text-white-50">Activos</small>
              </div>
              <div class="col-4">
                <div class="h4 mb-0">{{ completedGoals.length }}</div>
                <small class="text-white-50">Completados</small>
              </div>
              <div class="col-4">
                <div class="h4 mb-0">{{ averageProgress }}%</div>
                <small class="text-white-50">Progreso</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter and Actions -->
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text bg-light border-0">
                    <font-awesome-icon icon="fas fa-search" class="text-muted" />
                  </span>
                  <input 
                    type="text" 
                    class="form-control border-0 bg-light" 
                    placeholder="Buscar objetivos..."
                    v-model="searchQuery"
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="d-flex gap-2">
                  <select class="form-select" v-model="statusFilter">
                    <option value="all">Todos los estados</option>
                    <option value="active">Activos</option>
                    <option value="completed">Completados</option>
                    <option value="paused">Pausados</option>
                  </select>
                  <select class="form-select" v-model="categoryFilter">
                    <option value="all">Todas las categorías</option>
                    <option value="distance">Distancia</option>
                    <option value="time">Tiempo</option>
                    <option value="frequency">Frecuencia</option>
                    <option value="performance">Rendimiento</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="d-grid gap-2">
          <button class="btn btn-primary" @click="requestNewGoal">
            <font-awesome-icon icon="fas fa-plus" class="me-2" />
            Solicitar Nuevo Objetivo
          </button>
        </div>
      </div>
    </div>

    <!-- Goals Grid -->
    <div class="row">
      <div class="col-12">
        <div v-if="filteredGoals.length === 0" class="text-center py-5">
          <div class="empty-state">
            <font-awesome-icon icon="fas fa-target" class="fa-4x text-muted mb-3" />
            <h4 class="text-muted mb-2">No tienes objetivos {{ statusFilter !== 'all' ? statusFilter : '' }}</h4>
            <p class="text-muted mb-4">Habla con tu entrenador para establecer objetivos personalizados</p>
            <button class="btn btn-primary" @click="requestNewGoal">
              <font-awesome-icon icon="fas fa-plus" class="me-2" />
              Solicitar Primer Objetivo
            </button>
          </div>
        </div>
        
        <div v-else class="goals-grid">
          <div v-for="goal in filteredGoals" :key="goal.id" class="col-lg-6 col-xl-4 mb-4">
            <div class="card goal-card border-0 shadow-sm h-100" :class="getGoalCardClass(goal)">
              <div class="card-header border-0" :class="getGoalHeaderClass(goal)">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h6 class="mb-1 text-white">{{ goal.title }}</h6>
                    <small class="text-white-75">{{ getCategoryText(goal.category) }}</small>
                  </div>
                  <div class="goal-status">
                    <span class="badge" :class="getStatusBadgeClass(goal.status)">
                      {{ getStatusText(goal.status) }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="card-body">
                <p class="text-muted mb-3">{{ goal.description }}</p>
                
                <!-- Progress Bar -->
                <div class="progress-section mb-3">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <small class="text-muted">Progreso</small>
                    <small class="fw-bold" :class="getProgressTextClass(goal.progress)">
                      {{ goal.progress }}%
                    </small>
                  </div>
                  <div class="progress" style="height: 8px;">
                    <div 
                      class="progress-bar" 
                      :style="{ width: goal.progress + '%' }"
                      :class="getProgressBarClass(goal.progress)"
                    ></div>
                  </div>
                </div>
                
                <!-- Goal Details -->
                <div class="goal-details mb-3">
                  <div class="row text-center">
                    <div class="col-6">
                      <div class="detail-item">
                        <div class="h6 mb-0" :class="getProgressTextClass(goal.progress)">
                          {{ goal.current }}
                        </div>
                        <small class="text-muted">Actual</small>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="detail-item">
                        <div class="h6 mb-0 text-primary">
                          {{ goal.target }}
                        </div>
                        <small class="text-muted">Objetivo</small>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Timeline -->
                <div class="timeline-section mb-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="timeline-item">
                      <small class="text-muted">Inicio</small>
                      <div class="small">{{ formatDate(goal.startDate) }}</div>
                    </div>
                    <div class="timeline-divider">
                      <font-awesome-icon icon="fas fa-arrow-right" class="text-muted" />
                    </div>
                    <div class="timeline-item text-end">
                      <small class="text-muted">Fecha límite</small>
                      <div class="small" :class="getDeadlineClass(goal.deadline)">
                        {{ formatDate(goal.deadline) }}
                      </div>
                    </div>
                  </div>
                  
                  <div class="mt-2">
                    <small class="text-muted">
                      <font-awesome-icon icon="fas fa-clock" class="me-1" />
                      {{ getDaysRemaining(goal.deadline) }} días restantes
                    </small>
                  </div>
                </div>
                
                <!-- Coach Feedback -->
                <div v-if="goal.lastFeedback" class="feedback-section mb-3">
                  <div class="feedback-item p-2 bg-light rounded">
                    <div class="d-flex align-items-start">
                      <font-awesome-icon icon="fas fa-comment" class="text-primary me-2 mt-1" />
                      <div class="flex-grow-1">
                        <small class="text-muted">Último feedback del entrenador:</small>
                        <p class="mb-0 small">{{ goal.lastFeedback.message }}</p>
                        <small class="text-muted">{{ formatTimeAgo(goal.lastFeedback.date) }}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="card-footer bg-white border-0">
                <div class="d-flex gap-2">
                  <button 
                    class="btn btn-outline-primary btn-sm flex-grow-1" 
                    @click="viewGoalDetails(goal)"
                  >
                    <font-awesome-icon icon="fas fa-eye" class="me-1" />
                    Ver detalles
                  </button>
                  <button 
                    v-if="goal.status === 'active'" 
                    class="btn btn-outline-success btn-sm" 
                    @click="updateProgress(goal)"
                  >
                    <font-awesome-icon icon="fas fa-chart-line" />
                  </button>
                  <button 
                    class="btn btn-outline-info btn-sm" 
                    @click="askCoachQuestion(goal)"
                  >
                    <font-awesome-icon icon="fas fa-question" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Goal Request Modal -->
    <div class="modal fade" id="goalRequestModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <font-awesome-icon icon="fas fa-target" class="me-2 text-primary" />
              Solicitar Nuevo Objetivo
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitGoalRequest">
              <div class="mb-3">
                <label class="form-label">Tipo de objetivo</label>
                <select class="form-select" v-model="goalRequest.category" required>
                  <option value="">Selecciona una categoría</option>
                  <option value="distance">Distancia</option>
                  <option value="time">Tiempo</option>
                  <option value="frequency">Frecuencia</option>
                  <option value="performance">Rendimiento</option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Título del objetivo</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="goalRequest.title"
                  placeholder="Ej: Correr 10K en menos de 50 minutos"
                  required
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea 
                  class="form-control" 
                  rows="3"
                  v-model="goalRequest.description"
                  placeholder="Describe tu objetivo y por qué es importante para ti..."
                  required
                ></textarea>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Fecha límite deseada</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="goalRequest.deadline"
                  :min="minDate"
                  required
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Prioridad</label>
                <select class="form-select" v-model="goalRequest.priority">
                  <option value="low">Baja</option>
                  <option value="medium">Media</option>
                  <option value="high">Alta</option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary" @click="submitGoalRequest">
              <font-awesome-icon icon="fas fa-paper-plane" class="me-2" />
              Enviar Solicitud
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Modal } from 'bootstrap'

export default {
  name: 'StudentGoalsView',
  setup() {
    // Reactive data
    const searchQuery = ref('')
    const statusFilter = ref('all')
    const categoryFilter = ref('all')
    
    const goals = ref([
      {
        id: 1,
        title: 'Correr 10K en menos de 50 minutos',
        description: 'Mejorar el tiempo en distancia de 10 kilómetros para participar en la carrera local',
        category: 'time',
        status: 'active',
        progress: 75,
        current: '52:30',
        target: '49:59',
        startDate: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000),
        deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        lastFeedback: {
          message: 'Excelente progreso! Sigue trabajando en la velocidad.',
          date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
        }
      },
      {
        id: 2,
        title: 'Entrenar 5 días por semana',
        description: 'Mantener consistencia en el entrenamiento durante 3 meses',
        category: 'frequency',
        status: 'active',
        progress: 60,
        current: '3 días',
        target: '5 días',
        startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        deadline: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000),
        lastFeedback: {
          message: 'Intenta ser más consistente los fines de semana.',
          date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
        }
      },
      {
        id: 3,
        title: 'Completar medio maratón',
        description: 'Terminar mi primer medio maratón sin parar',
        category: 'distance',
        status: 'completed',
        progress: 100,
        current: '21.1 km',
        target: '21.1 km',
        startDate: new Date(Date.now() - 120 * 24 * 60 * 60 * 1000),
        deadline: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
        lastFeedback: {
          message: '¡Felicitaciones! Excelente logro.',
          date: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000)
        }
      },
      {
        id: 4,
        title: 'Mejorar VO2 Max',
        description: 'Aumentar capacidad cardiovascular medida por VO2 Max',
        category: 'performance',
        status: 'paused',
        progress: 40,
        current: '45 ml/kg/min',
        target: '50 ml/kg/min',
        startDate: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000),
        deadline: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000),
        lastFeedback: null
      }
    ])
    
    const goalRequest = ref({
      category: '',
      title: '',
      description: '',
      deadline: '',
      priority: 'medium'
    })
    
    // Computed
    const activeGoals = computed(() => goals.value.filter(goal => goal.status === 'active'))
    const completedGoals = computed(() => goals.value.filter(goal => goal.status === 'completed'))
    
    const averageProgress = computed(() => {
      const activeGoalsList = activeGoals.value
      if (activeGoalsList.length === 0) return 0
      const total = activeGoalsList.reduce((sum, goal) => sum + goal.progress, 0)
      return Math.round(total / activeGoalsList.length)
    })
    
    const filteredGoals = computed(() => {
      let filtered = goals.value
      
      // Filter by search query
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(goal => 
          goal.title.toLowerCase().includes(query) ||
          goal.description.toLowerCase().includes(query)
        )
      }
      
      // Filter by status
      if (statusFilter.value !== 'all') {
        filtered = filtered.filter(goal => goal.status === statusFilter.value)
      }
      
      // Filter by category
      if (categoryFilter.value !== 'all') {
        filtered = filtered.filter(goal => goal.category === categoryFilter.value)
      }
      
      return filtered
    })
    
    const minDate = computed(() => {
      const tomorrow = new Date()
      tomorrow.setDate(tomorrow.getDate() + 1)
      return tomorrow.toISOString().split('T')[0]
    })
    
    // Methods
    const getCategoryText = (category) => {
      const categoryMap = {
        distance: 'Distancia',
        time: 'Tiempo',
        frequency: 'Frecuencia',
        performance: 'Rendimiento'
      }
      return categoryMap[category] || category
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        active: 'Activo',
        completed: 'Completado',
        paused: 'Pausado'
      }
      return statusMap[status] || status
    }
    
    const getGoalCardClass = (goal) => {
      return {
        'border-success': goal.status === 'completed',
        'border-warning': goal.status === 'paused',
        'border-primary': goal.status === 'active'
      }
    }
    
    const getGoalHeaderClass = (goal) => {
      return {
        'bg-success': goal.status === 'completed',
        'bg-warning': goal.status === 'paused',
        'bg-primary': goal.status === 'active'
      }
    }
    
    const getStatusBadgeClass = (status) => {
      return {
        'bg-light text-dark': status === 'active',
        'bg-light text-dark': status === 'completed',
        'bg-light text-dark': status === 'paused'
      }
    }
    
    const getProgressTextClass = (progress) => {
      if (progress >= 80) return 'text-success'
      if (progress >= 50) return 'text-warning'
      return 'text-danger'
    }
    
    const getProgressBarClass = (progress) => {
      if (progress >= 80) return 'bg-success'
      if (progress >= 50) return 'bg-warning'
      return 'bg-danger'
    }
    
    const getDeadlineClass = (deadline) => {
      const daysRemaining = getDaysRemaining(deadline)
      if (daysRemaining <= 7) return 'text-danger'
      if (daysRemaining <= 30) return 'text-warning'
      return 'text-muted'
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
    
    const getDaysRemaining = (deadline) => {
      const now = new Date()
      const diff = deadline - now
      const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
      return Math.max(0, days)
    }
    
    const viewGoalDetails = (goal) => {
      console.log('Ver detalles del objetivo:', goal.title)
      // Implementar modal de detalles
    }
    
    const updateProgress = (goal) => {
      console.log('Actualizar progreso:', goal.title)
      // Implementar modal de actualización de progreso
    }
    
    const askCoachQuestion = (goal) => {
      console.log('Preguntar al entrenador sobre:', goal.title)
      // Implementar modal de pregunta
    }
    
    const requestNewGoal = () => {
      const modal = new Modal(document.getElementById('goalRequestModal'))
      modal.show()
    }
    
    const submitGoalRequest = () => {
      if (!goalRequest.value.category || !goalRequest.value.title || !goalRequest.value.description || !goalRequest.value.deadline) {
        alert('Por favor completa todos los campos requeridos')
        return
      }
      
      console.log('Solicitud de objetivo enviada:', goalRequest.value)
      
      // Simular envío
      alert('Solicitud enviada al entrenador. Te notificaremos cuando sea revisada.')
      
      // Reset form
      goalRequest.value = {
        category: '',
        title: '',
        description: '',
        deadline: '',
        priority: 'medium'
      }
      
      // Close modal
      const modal = Modal.getInstance(document.getElementById('goalRequestModal'))
      modal.hide()
    }
    
    const loadGoals = async () => {
      try {
        // Aquí se cargarían los objetivos reales del backend
        console.log('Cargando objetivos...')
      } catch (error) {
        console.error('Error loading goals:', error)
      }
    }
    
    onMounted(() => {
      loadGoals()
    })
    
    return {
      searchQuery,
      statusFilter,
      categoryFilter,
      goals,
      goalRequest,
      activeGoals,
      completedGoals,
      averageProgress,
      filteredGoals,
      minDate,
      getCategoryText,
      getStatusText,
      getGoalCardClass,
      getGoalHeaderClass,
      getStatusBadgeClass,
      getProgressTextClass,
      getProgressBarClass,
      getDeadlineClass,
      formatDate,
      formatTimeAgo,
      getDaysRemaining,
      viewGoalDetails,
      updateProgress,
      askCoachQuestion,
      requestNewGoal,
      submitGoalRequest
    }
  }
}
</script>

<style scoped>
.student-goals {
  padding: 1.5rem;
}

.goals-header {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.goal-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.goal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.goal-card .card-header {
  border-radius: 0.375rem 0.375rem 0 0 !important;
}

.text-white-75 {
  color: rgba(255, 255, 255, 0.75) !important;
}

.progress-section .progress {
  border-radius: 10px;
}

.detail-item {
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.timeline-divider {
  flex: 1;
  text-align: center;
  margin: 0 1rem;
}

.feedback-section {
  border-left: 3px solid #0d6efd;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .student-goals {
    padding: 1rem;
  }
  
  .goals-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .goals-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
  
  .goals-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .timeline-section .d-flex {
    flex-direction: column;
    text-align: center;
  }
  
  .timeline-divider {
    margin: 0.5rem 0;
  }
}
</style>
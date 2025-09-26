<template>
  <div class="coach-students">
    <!-- Header -->
    <div class="students-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-0">
            <font-awesome-icon icon="fas fa-users" class="me-2 text-primary" />
            Mis Alumnos
          </h1>
          <p class="text-muted mb-0">Gestiona y supervisa el progreso de tus alumnos</p>
        </div>
        <div class="col-md-4 text-end">
          <button class="btn btn-primary" @click="showAddStudentModal = true">
            <font-awesome-icon icon="fas fa-user-plus" class="me-2" />
            Agregar Alumno
          </button>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-md-6">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0">
                <font-awesome-icon icon="fas fa-search" class="text-muted" />
              </span>
              <input 
                type="text" 
                class="form-control border-start-0" 
                placeholder="Buscar alumnos..."
                v-model="searchQuery"
              >
            </div>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="statusFilter">
              <option value="">Todos los estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
              <option value="pending">Pendientes</option>
            </select>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="sortBy">
              <option value="name">Ordenar por nombre</option>
              <option value="date">Fecha de registro</option>
              <option value="activity">Última actividad</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Students Grid -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <div v-else-if="filteredStudents.length === 0" class="text-center py-5">
      <font-awesome-icon icon="fas fa-user-slash" class="fa-3x text-muted mb-3" />
      <h4 class="text-muted">No se encontraron alumnos</h4>
      <p class="text-muted">{{ searchQuery ? 'Intenta con otros términos de búsqueda' : 'Comienza agregando tu primer alumno' }}</p>
    </div>

    <div v-else class="row">
      <div v-for="student in filteredStudents" :key="student.id" class="col-lg-4 col-md-6 mb-4">
        <div class="card student-card border-0 shadow-sm h-100">
          <div class="card-body">
            <!-- Student Header -->
            <div class="d-flex align-items-center mb-3">
              <div class="student-avatar me-3">
                <img 
                  :src="student.avatar || '/logo/default-avatar.png'" 
                  :alt="student.name" 
                  class="rounded-circle"
                  width="60"
                  height="60"
                >
                <span 
                  class="status-indicator" 
                  :class="{
                    'bg-success': student.status === 'active',
                    'bg-warning': student.status === 'pending',
                    'bg-secondary': student.status === 'inactive'
                  }"
                ></span>
              </div>
              <div class="flex-grow-1">
                <h5 class="mb-1">{{ student.name }}</h5>
                <p class="text-muted mb-0 small">{{ student.email }}</p>
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

            <!-- Student Stats -->
            <div class="row text-center mb-3">
              <div class="col-4">
                <div class="stat-item">
                  <h6 class="mb-0 text-primary">{{ student.stats.totalActivities }}</h6>
                  <small class="text-muted">Actividades</small>
                </div>
              </div>
              <div class="col-4">
                <div class="stat-item">
                  <h6 class="mb-0 text-success">{{ student.stats.activeGoals }}</h6>
                  <small class="text-muted">Objetivos</small>
                </div>
              </div>
              <div class="col-4">
                <div class="stat-item">
                  <h6 class="mb-0 text-info">{{ student.stats.weeklyHours }}</h6>
                  <small class="text-muted">Hrs/Semana</small>
                </div>
              </div>
            </div>

            <!-- Last Activity -->
            <div class="mb-3">
              <small class="text-muted">
                <font-awesome-icon icon="fas fa-clock" class="me-1" />
                Última actividad: {{ formatLastActivity(student.lastActivity) }}
              </small>
            </div>

            <!-- Progress Bar -->
            <div class="mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <small class="text-muted">Progreso del mes</small>
                <small class="text-muted">{{ student.monthlyProgress }}%</small>
              </div>
              <div class="progress" style="height: 6px;">
                <div 
                  class="progress-bar" 
                  :style="{ width: student.monthlyProgress + '%' }"
                  :class="{
                    'bg-success': student.monthlyProgress >= 80,
                    'bg-warning': student.monthlyProgress >= 50 && student.monthlyProgress < 80,
                    'bg-danger': student.monthlyProgress < 50
                  }"
                ></div>
              </div>
            </div>

            <!-- Actions -->
            <div class="d-flex gap-2">
              <router-link 
                :to="`/coach/student/${student.id}`" 
                class="btn btn-primary btn-sm flex-grow-1"
              >
                <font-awesome-icon icon="fas fa-eye" class="me-1" />
                Ver Detalle
              </router-link>
              <button 
                class="btn btn-outline-success btn-sm" 
                @click="sendMessage(student)"
                :title="'Enviar mensaje a ' + student.name"
              >
                <font-awesome-icon icon="fas fa-comment" />
              </button>
              <div class="dropdown">
                <button 
                  class="btn btn-outline-secondary btn-sm dropdown-toggle" 
                  type="button" 
                  :id="'dropdown-' + student.id"
                  data-bs-toggle="dropdown"
                >
                  <font-awesome-icon icon="fas fa-ellipsis-v" />
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="#" @click="editStudent(student)">
                      <font-awesome-icon icon="fas fa-edit" class="me-2" />
                      Editar
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click="createGoal(student)">
                      <font-awesome-icon icon="fas fa-target" class="me-2" />
                      Crear Objetivo
                    </a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click="removeStudent(student)">
                      <font-awesome-icon icon="fas fa-trash" class="me-2" />
                      Eliminar
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Student Modal -->
    <div class="modal fade" :class="{ show: showAddStudentModal }" :style="{ display: showAddStudentModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <font-awesome-icon icon="fas fa-user-plus" class="me-2" />
              Agregar Nuevo Alumno
            </h5>
            <button type="button" class="btn-close" @click="showAddStudentModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addStudent">
              <div class="mb-3">
                <label for="studentEmail" class="form-label">Email del alumno</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="studentEmail"
                  v-model="newStudent.email"
                  placeholder="alumno@ejemplo.com"
                  required
                >
                <div class="form-text">El alumno recibirá una invitación por email</div>
              </div>
              <div class="mb-3">
                <label for="studentName" class="form-label">Nombre completo</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="studentName"
                  v-model="newStudent.name"
                  placeholder="Nombre del alumno"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="studentMessage" class="form-label">Mensaje de bienvenida (opcional)</label>
                <textarea 
                  class="form-control" 
                  id="studentMessage"
                  v-model="newStudent.message"
                  rows="3"
                  placeholder="Mensaje personalizado para el alumno..."
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddStudentModal = false">
              Cancelar
            </button>
            <button type="button" class="btn btn-primary" @click="addStudent" :disabled="!newStudent.email || !newStudent.name">
              <font-awesome-icon icon="fas fa-paper-plane" class="me-2" />
              Enviar Invitación
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showAddStudentModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CoachStudentsView',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const searchQuery = ref('')
    const statusFilter = ref('')
    const sortBy = ref('name')
    const showAddStudentModal = ref(false)
    
    const students = ref([])
    const newStudent = ref({
      email: '',
      name: '',
      message: ''
    })
    
    // Computed
    const filteredStudents = computed(() => {
      let filtered = students.value
      
      // Filter by search query
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(student => 
          student.name.toLowerCase().includes(query) ||
          student.email.toLowerCase().includes(query)
        )
      }
      
      // Filter by status
      if (statusFilter.value) {
        filtered = filtered.filter(student => student.status === statusFilter.value)
      }
      
      // Sort
      filtered.sort((a, b) => {
        switch (sortBy.value) {
          case 'name':
            return a.name.localeCompare(b.name)
          case 'date':
            return new Date(b.registrationDate) - new Date(a.registrationDate)
          case 'activity':
            return new Date(b.lastActivity) - new Date(a.lastActivity)
          default:
            return 0
        }
      })
      
      return filtered
    })
    
    // Methods
    const loadStudents = async () => {
      try {
        loading.value = true
        
        // Simular datos - aquí se conectaría con el backend
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        students.value = [
          {
            id: 1,
            name: 'Ana García',
            email: 'ana.garcia@email.com',
            avatar: null,
            status: 'active',
            registrationDate: '2024-01-15',
            lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000),
            monthlyProgress: 85,
            stats: {
              totalActivities: 24,
              activeGoals: 3,
              weeklyHours: 8
            }
          },
          {
            id: 2,
            name: 'Carlos López',
            email: 'carlos.lopez@email.com',
            avatar: null,
            status: 'active',
            registrationDate: '2024-02-01',
            lastActivity: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
            monthlyProgress: 72,
            stats: {
              totalActivities: 18,
              activeGoals: 2,
              weeklyHours: 6
            }
          },
          {
            id: 3,
            name: 'María Rodríguez',
            email: 'maria.rodriguez@email.com',
            avatar: null,
            status: 'pending',
            registrationDate: '2024-03-10',
            lastActivity: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
            monthlyProgress: 45,
            stats: {
              totalActivities: 8,
              activeGoals: 1,
              weeklyHours: 3
            }
          }
        ]
        
      } catch (error) {
        console.error('Error loading students:', error)
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
    
    const addStudent = async () => {
      try {
        // Aquí se enviaría la invitación al backend
        console.log('Enviando invitación a:', newStudent.value)
        
        // Simular éxito
        alert('Invitación enviada correctamente')
        
        // Reset form
        newStudent.value = {
          email: '',
          name: '',
          message: ''
        }
        showAddStudentModal.value = false
        
        // Reload students
        await loadStudents()
        
      } catch (error) {
        console.error('Error sending invitation:', error)
        alert('Error al enviar la invitación')
      }
    }
    
    const sendMessage = (student) => {
      console.log('Enviar mensaje a:', student.name)
      // Implementar modal de mensaje o navegación
    }
    
    const editStudent = (student) => {
      console.log('Editar alumno:', student.name)
      // Implementar modal de edición
    }
    
    const createGoal = (student) => {
      console.log('Crear objetivo para:', student.name)
      // Implementar modal de creación de objetivo
    }
    
    const removeStudent = (student) => {
      if (confirm(`¿Estás seguro de que quieres eliminar a ${student.name}?`)) {
        console.log('Eliminar alumno:', student.name)
        // Implementar eliminación
      }
    }
    
    onMounted(() => {
      loadStudents()
    })
    
    return {
      loading,
      searchQuery,
      statusFilter,
      sortBy,
      showAddStudentModal,
      students,
      newStudent,
      filteredStudents,
      getStatusText,
      formatLastActivity,
      addStudent,
      sendMessage,
      editStudent,
      createGoal,
      removeStudent
    }
  }
}
</script>

<style scoped>
.coach-students {
  padding: 1.5rem;
}

.students-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.student-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.student-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.student-avatar {
  position: relative;
}

.student-avatar img {
  object-fit: cover;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
}

.stat-item {
  padding: 0.5rem;
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

@media (max-width: 768px) {
  .coach-students {
    padding: 1rem;
  }
  
  .students-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .students-header .col-md-4 {
    text-align: center !important;
    margin-top: 1rem;
  }
  
  .card-body .row .col-md-3,
  .card-body .row .col-md-6 {
    margin-bottom: 1rem;
  }
}
</style>
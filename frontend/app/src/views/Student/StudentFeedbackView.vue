<template>
  <div class="student-feedback-view">
    <div class="container mx-auto px-4 py-6">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Feedback del Entrenador
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Revisa los comentarios y sugerencias de tu entrenador
        </p>
      </div>

      <!-- Feedback List -->
      <div class="space-y-4">
        <div 
          v-for="feedback in feedbackList" 
          :key="feedback.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                <i class="fas fa-user-tie text-white"></i>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">
                  {{ feedback.coach_name }}
                </h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(feedback.created_at) }}
                </p>
              </div>
            </div>
            <span 
              :class="getFeedbackTypeClass(feedback.type)"
              class="px-3 py-1 rounded-full text-sm font-medium"
            >
              {{ getFeedbackTypeLabel(feedback.type) }}
            </span>
          </div>

          <div class="mb-4">
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">
              {{ feedback.title }}
            </h4>
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
              {{ feedback.content }}
            </p>
          </div>

          <div v-if="feedback.activity_id" class="mb-4">
            <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Relacionado con actividad:
              </p>
              <p class="font-medium text-gray-900 dark:text-white">
                {{ feedback.activity_name }}
              </p>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <button 
                @click="markAsRead(feedback.id)"
                :disabled="feedback.is_read"
                class="text-sm text-blue-600 hover:text-blue-800 disabled:text-gray-400 disabled:cursor-not-allowed"
              >
                <i class="fas fa-check mr-1"></i>
                {{ feedback.is_read ? 'Leído' : 'Marcar como leído' }}
              </button>
              <button 
                @click="replyToFeedback(feedback.id)"
                class="text-sm text-green-600 hover:text-green-800"
              >
                <i class="fas fa-reply mr-1"></i>
                Responder
              </button>
            </div>
            <div v-if="feedback.rating" class="flex items-center">
              <span class="text-sm text-gray-500 dark:text-gray-400 mr-2">Calificación:</span>
              <div class="flex">
                <i 
                  v-for="star in 5" 
                  :key="star"
                  :class="star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'"
                  class="fas fa-star text-sm"
                ></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="feedbackList.length === 0" class="text-center py-12">
        <i class="fas fa-comments text-6xl text-gray-300 dark:text-gray-600 mb-4"></i>
        <h3 class="text-xl font-medium text-gray-900 dark:text-white mb-2">
          No hay feedback disponible
        </h3>
        <p class="text-gray-500 dark:text-gray-400">
          Tu entrenador aún no ha dejado comentarios sobre tus entrenamientos.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p class="text-gray-500 dark:text-gray-400 mt-4">Cargando feedback...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { notificationService } from '@/services/notificationService'

export default {
  name: 'StudentFeedbackView',
  setup() {
    const authStore = useAuthStore()
    const feedbackList = ref([])
    const loading = ref(false)

    const loadFeedback = async () => {
      loading.value = true
      try {
        // Simulated API call - replace with actual service
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock data
        feedbackList.value = [
          {
            id: 1,
            coach_name: 'Carlos Rodríguez',
            title: 'Excelente progreso en resistencia',
            content: 'Has mostrado una mejora significativa en tu resistencia cardiovascular. Continúa con el plan actual y considera aumentar la intensidad gradualmente.',
            type: 'positive',
            created_at: new Date('2024-01-15'),
            is_read: false,
            activity_id: 123,
            activity_name: 'Carrera matutina - 10km',
            rating: 4
          },
          {
            id: 2,
            coach_name: 'Carlos Rodríguez',
            title: 'Ajuste en técnica de carrera',
            content: 'He notado que tu cadencia está un poco baja. Te recomiendo trabajar en pasos más cortos y frecuentes para mejorar la eficiencia.',
            type: 'improvement',
            created_at: new Date('2024-01-12'),
            is_read: true,
            activity_id: 122,
            activity_name: 'Entrenamiento de velocidad',
            rating: null
          }
        ]
      } catch (error) {
        console.error('Error loading feedback:', error)
        notificationService.showError('Error al cargar el feedback')
      } finally {
        loading.value = false
      }
    }

    const markAsRead = async (feedbackId) => {
      try {
        // API call to mark as read
        const feedback = feedbackList.value.find(f => f.id === feedbackId)
        if (feedback) {
          feedback.is_read = true
          notificationService.showSuccess('Feedback marcado como leído')
        }
      } catch (error) {
        console.error('Error marking feedback as read:', error)
        notificationService.showError('Error al marcar como leído')
      }
    }

    const replyToFeedback = (feedbackId) => {
      // Navigate to reply form or open modal
      notificationService.showInfo('Función de respuesta en desarrollo')
    }

    const formatDate = (date) => {
      return new Intl.DateTimeFormat('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(date))
    }

    const getFeedbackTypeClass = (type) => {
      const classes = {
        positive: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        improvement: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        warning: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
        general: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      }
      return classes[type] || classes.general
    }

    const getFeedbackTypeLabel = (type) => {
      const labels = {
        positive: 'Positivo',
        improvement: 'Mejora',
        warning: 'Atención',
        general: 'General'
      }
      return labels[type] || 'General'
    }

    onMounted(() => {
      loadFeedback()
    })

    return {
      feedbackList,
      loading,
      markAsRead,
      replyToFeedback,
      formatDate,
      getFeedbackTypeClass,
      getFeedbackTypeLabel
    }
  }
}
</script>

<style scoped>
.student-feedback-view {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}

.dark .student-feedback-view {
  background-color: #111827;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
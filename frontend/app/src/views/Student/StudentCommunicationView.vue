<template>
  <div class="student-communication">
    <!-- Header -->
    <div class="communication-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-1 text-white">Comunicación con mi Entrenador</h1>
          <p class="mb-0 text-white-50">Mantén contacto directo con tu entrenador y recibe feedback personalizado</p>
        </div>
        <div class="col-md-4 text-end">
          <div class="coach-info text-white">
            <div class="d-flex align-items-center justify-content-end">
              <img 
                :src="coachInfo.avatar" 
                :alt="coachInfo.name"
                class="rounded-circle me-3"
                width="50"
                height="50"
              >
              <div class="text-end">
                <div class="fw-bold">{{ coachInfo.name }}</div>
                <small class="text-white-50">
                  <span v-if="coachInfo.isOnline" class="text-success">
                    <font-awesome-icon icon="fas fa-circle" class="me-1" style="font-size: 0.5rem;" />
                    En línea
                  </span>
                  <span v-else>
                    Última vez: {{ formatLastSeen(coachInfo.lastSeen) }}
                  </span>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Sidebar - Quick Actions & Info -->
      <div class="col-lg-3 col-md-4">
        <!-- Quick Actions -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-bolt" class="me-2 text-warning" />
              Acciones Rápidas
            </h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button class="btn btn-primary" @click="askQuestion">
                <font-awesome-icon icon="fas fa-question-circle" class="me-2" />
                Hacer Pregunta
              </button>
              <button class="btn btn-success" @click="shareActivity">
                <font-awesome-icon icon="fas fa-share" class="me-2" />
                Compartir Actividad
              </button>
              <button class="btn btn-info" @click="requestFeedback">
                <font-awesome-icon icon="fas fa-comment-dots" class="me-2" />
                Solicitar Feedback
              </button>
              <button class="btn btn-warning" @click="reportIssue">
                <font-awesome-icon icon="fas fa-exclamation-triangle" class="me-2" />
                Reportar Problema
              </button>
            </div>
          </div>
        </div>

        <!-- Coach Info -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-user-tie" class="me-2 text-primary" />
              Mi Entrenador
            </h5>
          </div>
          <div class="card-body text-center">
            <img 
              :src="coachInfo.avatar" 
              :alt="coachInfo.name"
              class="rounded-circle mb-3"
              width="80"
              height="80"
            >
            <h6 class="mb-1">{{ coachInfo.name }}</h6>
            <p class="text-muted small mb-3">{{ coachInfo.specialization }}</p>
            
            <div class="coach-stats row text-center">
              <div class="col-6">
                <div class="h6 mb-0 text-primary">{{ coachInfo.experience }}</div>
                <small class="text-muted">Años exp.</small>
              </div>
              <div class="col-6">
                <div class="h6 mb-0 text-success">{{ coachInfo.students }}</div>
                <small class="text-muted">Alumnos</small>
              </div>
            </div>
            
            <div class="mt-3">
              <div class="d-flex justify-content-center gap-2">
                <button class="btn btn-sm btn-outline-primary" @click="viewCoachProfile">
                  <font-awesome-icon icon="fas fa-eye" class="me-1" />
                  Ver Perfil
                </button>
                <button class="btn btn-sm btn-outline-success" @click="scheduleCall">
                  <font-awesome-icon icon="fas fa-phone" class="me-1" />
                  Llamar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Notifications -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0">
            <h5 class="card-title mb-0">
              <font-awesome-icon icon="fas fa-bell" class="me-2 text-info" />
              Notificaciones
            </h5>
          </div>
          <div class="card-body">
            <div v-if="notifications.length === 0" class="text-center py-3 text-muted">
              <font-awesome-icon icon="fas fa-bell-slash" class="fa-2x mb-2" />
              <p class="mb-0 small">No hay notificaciones</p>
            </div>
            
            <div v-else>
              <div v-for="notification in notifications" :key="notification.id" class="notification-item mb-3">
                <div class="d-flex align-items-start">
                  <div class="notification-icon me-2">
                    <font-awesome-icon :icon="notification.icon" :class="notification.color" />
                  </div>
                  <div class="flex-grow-1">
                    <p class="mb-1 small">{{ notification.message }}</p>
                    <small class="text-muted">{{ formatTimeAgo(notification.timestamp) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Content - Chat Area -->
      <div class="col-lg-9 col-md-8">
        <div class="card border-0 shadow-sm h-100">
          <!-- Chat Header -->
          <div class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <img 
                  :src="coachInfo.avatar" 
                  :alt="coachInfo.name"
                  class="rounded-circle me-3"
                  width="40"
                  height="40"
                >
                <div>
                  <h5 class="mb-0">{{ coachInfo.name }}</h5>
                  <small class="text-muted">
                    <span v-if="coachInfo.isOnline" class="text-success">
                      <font-awesome-icon icon="fas fa-circle" class="me-1" style="font-size: 0.5rem;" />
                      En línea
                    </span>
                    <span v-else class="text-muted">
                      Última vez: {{ formatLastSeen(coachInfo.lastSeen) }}
                    </span>
                  </small>
                </div>
              </div>
              
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-primary" @click="scheduleCall">
                  <font-awesome-icon icon="fas fa-video" class="me-1" />
                  Videollamada
                </button>
                <button class="btn btn-sm btn-outline-success" @click="scheduleCall">
                  <font-awesome-icon icon="fas fa-phone" class="me-1" />
                  Llamar
                </button>
                <div class="dropdown">
                  <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <font-awesome-icon icon="fas fa-ellipsis-v" />
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click="viewCoachProfile">Ver perfil del entrenador</a></li>
                    <li><a class="dropdown-item" href="#" @click="exportChat">Exportar conversación</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" @click="reportIssue">Reportar problema</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Messages Area -->
          <div class="card-body d-flex flex-column" style="height: 500px;">
            <div class="messages-container flex-grow-1 overflow-auto mb-3">
              <div 
                v-for="message in messages" 
                :key="message.id"
                class="message-item mb-3"
                :class="{ 'message-sent': message.senderId === 'student', 'message-received': message.senderId === 'coach' }"
              >
                <div class="d-flex" :class="message.senderId === 'student' ? 'justify-content-end' : 'justify-content-start'">
                  <div class="message-bubble" :class="message.senderId === 'student' ? 'bg-primary text-white' : 'bg-light'">
                    <div class="message-content">
                      <p class="mb-1">{{ message.content }}</p>
                      
                      <!-- Attachments -->
                      <div v-if="message.attachments && message.attachments.length > 0" class="attachments mt-2">
                        <div v-for="attachment in message.attachments" :key="attachment.id" class="attachment-item">
                          <div class="d-flex align-items-center p-2 border rounded">
                            <font-awesome-icon :icon="getFileIcon(attachment.type)" class="me-2" />
                            <div class="flex-grow-1">
                              <div class="small fw-bold">{{ attachment.name }}</div>
                              <div class="small text-muted">{{ formatFileSize(attachment.size) }}</div>
                            </div>
                            <button class="btn btn-sm btn-outline-primary" @click="downloadAttachment(attachment)">
                              <font-awesome-icon icon="fas fa-download" />
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Quick Replies for Coach Messages -->
                      <div v-if="message.senderId === 'coach' && message.quickReplies" class="quick-replies mt-2">
                        <div class="d-flex flex-wrap gap-1">
                          <button 
                            v-for="reply in message.quickReplies" 
                            :key="reply.id"
                            class="btn btn-sm btn-outline-primary"
                            @click="sendQuickReply(reply.text)"
                          >
                            {{ reply.text }}
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <div class="message-meta d-flex justify-content-between align-items-center mt-1">
                      <small class="opacity-75">{{ formatMessageTime(message.timestamp) }}</small>
                      <div v-if="message.senderId === 'student'" class="message-status">
                        <font-awesome-icon 
                          v-if="message.status === 'sent'" 
                          icon="fas fa-check" 
                          class="text-muted"
                        />
                        <font-awesome-icon 
                          v-else-if="message.status === 'delivered'" 
                          icon="fas fa-check-double" 
                          class="text-muted"
                        />
                        <font-awesome-icon 
                          v-else-if="message.status === 'read'" 
                          icon="fas fa-check-double" 
                          class="text-info"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="coachInfo.isTyping" class="typing-indicator mb-3">
                <div class="d-flex justify-content-start">
                  <div class="typing-bubble bg-light">
                    <div class="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
                <small class="text-muted ms-2">{{ coachInfo.name }} está escribiendo...</small>
              </div>
            </div>
            
            <!-- Message Input -->
            <div class="message-input">
              <div class="input-group">
                <button class="btn btn-outline-secondary" type="button" @click="showAttachmentOptions = !showAttachmentOptions">
                  <font-awesome-icon icon="fas fa-paperclip" />
                </button>
                
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="Escribe tu mensaje..."
                  v-model="newMessage"
                  @keypress.enter="sendMessage"
                  :disabled="isTyping"
                >
                
                <button class="btn btn-outline-secondary" type="button" @click="showEmojiPicker = !showEmojiPicker">
                  <font-awesome-icon icon="fas fa-smile" />
                </button>
                
                <button 
                  class="btn btn-primary" 
                  type="button" 
                  @click="sendMessage"
                  :disabled="!newMessage.trim() || isTyping"
                >
                  <font-awesome-icon v-if="isTyping" icon="fas fa-spinner" class="fa-spin" />
                  <font-awesome-icon v-else icon="fas fa-paper-plane" />
                </button>
              </div>
              
              <!-- Attachment Options -->
              <div v-if="showAttachmentOptions" class="attachment-options mt-2">
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-outline-primary" @click="attachFile('image')">
                    <font-awesome-icon icon="fas fa-image" class="me-1" />
                    Imagen
                  </button>
                  <button class="btn btn-sm btn-outline-success" @click="attachFile('activity')">
                    <font-awesome-icon icon="fas fa-running" class="me-1" />
                    Actividad
                  </button>
                  <button class="btn btn-sm btn-outline-info" @click="attachFile('document')">
                    <font-awesome-icon icon="fas fa-file" class="me-1" />
                    Documento
                  </button>
                  <button class="btn btn-sm btn-outline-warning" @click="attachFile('location')">
                    <font-awesome-icon icon="fas fa-map-marker-alt" class="me-1" />
                    Ubicación
                  </button>
                </div>
              </div>
              
              <!-- Suggested Responses -->
              <div v-if="suggestedResponses.length > 0" class="suggested-responses mt-2">
                <small class="text-muted mb-1 d-block">Respuestas sugeridas:</small>
                <div class="d-flex flex-wrap gap-1">
                  <button 
                    v-for="response in suggestedResponses" 
                    :key="response.id"
                    class="btn btn-sm btn-outline-secondary"
                    @click="sendSuggestedResponse(response.text)"
                  >
                    {{ response.text }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Quick Action Modals -->
    <div v-if="showQuickActionModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <font-awesome-icon :icon="quickActionModal.icon" class="me-2" />
              {{ quickActionModal.title }}
            </h5>
            <button type="button" class="btn-close" @click="showQuickActionModal = false"></button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="sendQuickAction">
              <div class="mb-3">
                <label for="quickActionMessage" class="form-label">{{ quickActionModal.label }}</label>
                <textarea 
                  class="form-control" 
                  id="quickActionMessage" 
                  rows="4" 
                  v-model="quickActionModal.message"
                  :placeholder="quickActionModal.placeholder"
                  required
                ></textarea>
              </div>
              
              <div v-if="quickActionModal.type === 'issue'" class="mb-3">
                <label class="form-label">Tipo de problema</label>
                <div class="d-flex gap-3">
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="issueType" id="issueTypeTraining" value="training" v-model="quickActionModal.issueType">
                    <label class="form-check-label" for="issueTypeTraining">Entrenamiento</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="issueType" id="issueTypeInjury" value="injury" v-model="quickActionModal.issueType">
                    <label class="form-check-label" for="issueTypeInjury">Lesión</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="issueType" id="issueTypeOther" value="other" v-model="quickActionModal.issueType">
                    <label class="form-check-label" for="issueTypeOther">Otro</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showQuickActionModal = false">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="sendQuickAction" :disabled="!quickActionModal.message">
              <font-awesome-icon icon="fas fa-paper-plane" class="me-2" />
              Enviar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'

export default {
  name: 'StudentCommunicationView',
  setup() {
    // Reactive data
    const newMessage = ref('')
    const isTyping = ref(false)
    const showAttachmentOptions = ref(false)
    const showEmojiPicker = ref(false)
    const showQuickActionModal = ref(false)
    
    const coachInfo = ref({
      id: 1,
      name: 'Dr. Roberto Martínez',
      avatar: 'https://via.placeholder.com/80x80/007bff/ffffff?text=RM',
      specialization: 'Entrenador de Resistencia',
      experience: 8,
      students: 45,
      isOnline: true,
      isTyping: false,
      lastSeen: new Date(Date.now() - 5 * 60 * 1000)
    })
    
    const quickActionModal = ref({
      type: '',
      title: '',
      label: '',
      placeholder: '',
      icon: '',
      message: '',
      issueType: 'training'
    })
    
    const messages = ref([
      {
        id: 1,
        content: 'Hola! He revisado tu última actividad de carrera. ¡Excelente progreso en tu ritmo!',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
        senderId: 'coach',
        status: 'delivered',
        quickReplies: [
          { id: 1, text: '¡Gracias!' },
          { id: 2, text: '¿Algún consejo?' },
          { id: 3, text: 'Me siento bien' }
        ]
      },
      {
        id: 2,
        content: '¡Gracias! Me siento mucho mejor con la nueva rutina.',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000 + 30000),
        senderId: 'student',
        status: 'read'
      },
      {
        id: 3,
        content: 'Perfecto. Para la próxima semana, vamos a aumentar un poco la intensidad. Te he preparado un nuevo plan.',
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000),
        senderId: 'coach',
        status: 'delivered',
        attachments: [
          {
            id: 1,
            name: 'Plan_Entrenamiento_Semana13.pdf',
            type: 'pdf',
            size: 1536000
          }
        ]
      },
      {
        id: 4,
        content: '¿Cuándo debería empezar con el nuevo plan?',
        timestamp: new Date(Date.now() - 30 * 60 * 1000),
        senderId: 'student',
        status: 'read'
      },
      {
        id: 5,
        content: 'Puedes empezar el lunes. Recuerda hacer un buen calentamiento antes de cada sesión.',
        timestamp: new Date(Date.now() - 10 * 60 * 1000),
        senderId: 'coach',
        status: 'delivered',
        quickReplies: [
          { id: 1, text: 'Perfecto' },
          { id: 2, text: '¿Qué calentamiento?' },
          { id: 3, text: 'Tengo una duda' }
        ]
      }
    ])
    
    const notifications = ref([
      {
        id: 1,
        message: 'Nuevo plan de entrenamiento disponible',
        icon: 'fas fa-dumbbell',
        color: 'text-primary',
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000)
      },
      {
        id: 2,
        message: 'Recordatorio: Sesión de entrenamiento mañana',
        icon: 'fas fa-clock',
        color: 'text-warning',
        timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000)
      },
      {
        id: 3,
        message: 'Feedback recibido sobre tu última carrera',
        icon: 'fas fa-comment',
        color: 'text-success',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000)
      }
    ])
    
    const suggestedResponses = ref([
      { id: 1, text: 'Entendido' },
      { id: 2, text: 'Tengo una pregunta' },
      { id: 3, text: 'Gracias por el consejo' }
    ])
    
    // Methods
    const sendMessage = async () => {
      if (!newMessage.value.trim()) return
      
      isTyping.value = true
      
      try {
        const message = {
          id: Date.now(),
          content: newMessage.value,
          timestamp: new Date(),
          senderId: 'student',
          status: 'sent'
        }
        
        messages.value.push(message)
        newMessage.value = ''
        
        // Scroll to bottom
        await nextTick()
        scrollToBottom()
        
        // Simulate message delivery
        setTimeout(() => {
          message.status = 'delivered'
        }, 1000)
        
        // Simulate message read
        setTimeout(() => {
          message.status = 'read'
        }, 3000)
        
        // Clear suggested responses after sending a message
        suggestedResponses.value = []
        
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        isTyping.value = false
      }
    }
    
    const sendQuickReply = (text) => {
      newMessage.value = text
      sendMessage()
    }
    
    const sendSuggestedResponse = (text) => {
      newMessage.value = text
      sendMessage()
    }
    
    const askQuestion = () => {
      quickActionModal.value = {
        type: 'question',
        title: 'Hacer Pregunta',
        label: 'Tu pregunta',
        placeholder: 'Escribe tu pregunta aquí...',
        icon: 'fas fa-question-circle',
        message: ''
      }
      showQuickActionModal.value = true
    }
    
    const shareActivity = () => {
      quickActionModal.value = {
        type: 'activity',
        title: 'Compartir Actividad',
        label: 'Detalles de la actividad',
        placeholder: 'Describe tu actividad y cómo te sentiste...',
        icon: 'fas fa-share',
        message: ''
      }
      showQuickActionModal.value = true
    }
    
    const requestFeedback = () => {
      quickActionModal.value = {
        type: 'feedback',
        title: 'Solicitar Feedback',
        label: 'Sobre qué te gustaría recibir feedback',
        placeholder: 'Describe sobre qué aspecto te gustaría recibir feedback...',
        icon: 'fas fa-comment-dots',
        message: ''
      }
      showQuickActionModal.value = true
    }
    
    const reportIssue = () => {
      quickActionModal.value = {
        type: 'issue',
        title: 'Reportar Problema',
        label: 'Describe el problema',
        placeholder: 'Explica detalladamente el problema que estás experimentando...',
        icon: 'fas fa-exclamation-triangle',
        message: '',
        issueType: 'training'
      }
      showQuickActionModal.value = true
    }
    
    const sendQuickAction = () => {
      if (!quickActionModal.value.message.trim()) return
      
      let prefix = ''
      switch (quickActionModal.value.type) {
        case 'question':
          prefix = '❓ Pregunta: '
          break
        case 'activity':
          prefix = '🏃 Actividad compartida: '
          break
        case 'feedback':
          prefix = '💬 Solicitud de feedback: '
          break
        case 'issue':
          prefix = `⚠️ Problema (${quickActionModal.value.issueType}): `
          break
      }
      
      const message = {
        id: Date.now(),
        content: prefix + quickActionModal.value.message,
        timestamp: new Date(),
        senderId: 'student',
        status: 'sent'
      }
      
      messages.value.push(message)
      showQuickActionModal.value = false
      
      // Reset modal
      quickActionModal.value = {
        type: '',
        title: '',
        label: '',
        placeholder: '',
        icon: '',
        message: '',
        issueType: 'training'
      }
      
      // Scroll to bottom
      nextTick(() => {
        scrollToBottom()
      })
    }
    
    const attachFile = (type) => {
      console.log('Attach file of type:', type)
      // Implement file attachment logic
      showAttachmentOptions.value = false
    }
    
    const downloadAttachment = (attachment) => {
      console.log('Download attachment:', attachment)
      // Implement download logic
    }
    
    const viewCoachProfile = () => {
      console.log('View coach profile')
      // Navigate to coach profile
    }
    
    const scheduleCall = () => {
      console.log('Schedule call with coach')
      // Implement call scheduling
    }
    
    const exportChat = () => {
      console.log('Export chat')
      // Implement chat export
    }
    
    const scrollToBottom = () => {
      const container = document.querySelector('.messages-container')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
    
    const formatMessageTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const formatLastSeen = (timestamp) => {
      const now = new Date()
      const date = new Date(timestamp)
      const diffInMinutes = (now - date) / (1000 * 60)
      
      if (diffInMinutes < 60) {
        return `hace ${Math.floor(diffInMinutes)} minutos`
      } else if (diffInMinutes < 1440) {
        return `hace ${Math.floor(diffInMinutes / 60)} horas`
      } else {
        return date.toLocaleDateString('es-ES')
      }
    }
    
    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const date = new Date(timestamp)
      const diffInMinutes = (now - date) / (1000 * 60)
      
      if (diffInMinutes < 60) {
        return `hace ${Math.floor(diffInMinutes)}m`
      } else if (diffInMinutes < 1440) {
        return `hace ${Math.floor(diffInMinutes / 60)}h`
      } else {
        return `hace ${Math.floor(diffInMinutes / 1440)}d`
      }
    }
    
    const getFileIcon = (type) => {
      const iconMap = {
        pdf: 'fas fa-file-pdf',
        doc: 'fas fa-file-word',
        docx: 'fas fa-file-word',
        xls: 'fas fa-file-excel',
        xlsx: 'fas fa-file-excel',
        jpg: 'fas fa-file-image',
        jpeg: 'fas fa-file-image',
        png: 'fas fa-file-image',
        gif: 'fas fa-file-image'
      }
      return iconMap[type] || 'fas fa-file'
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    onMounted(() => {
      // Scroll to bottom on mount
      nextTick(() => {
        scrollToBottom()
      })
      
      // Simulate coach typing occasionally
      setInterval(() => {
        if (Math.random() < 0.1) { // 10% chance every interval
          coachInfo.value.isTyping = true
          setTimeout(() => {
            coachInfo.value.isTyping = false
          }, 2000)
        }
      }, 10000)
    })
    
    return {
      newMessage,
      isTyping,
      showAttachmentOptions,
      showEmojiPicker,
      showQuickActionModal,
      coachInfo,
      quickActionModal,
      messages,
      notifications,
      suggestedResponses,
      sendMessage,
      sendQuickReply,
      sendSuggestedResponse,
      askQuestion,
      shareActivity,
      requestFeedback,
      reportIssue,
      sendQuickAction,
      attachFile,
      downloadAttachment,
      viewCoachProfile,
      scheduleCall,
      exportChat,
      formatMessageTime,
      formatLastSeen,
      formatTimeAgo,
      getFileIcon,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.student-communication {
  padding: 1.5rem;
}

.communication-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.messages-container {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}

.message-item {
  max-width: 100%;
}

.message-bubble {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.message-sent .message-bubble {
  border-bottom-right-radius: 0.25rem;
}

.message-received .message-bubble {
  border-bottom-left-radius: 0.25rem;
}

.message-content p {
  margin-bottom: 0;
}

.message-meta {
  font-size: 0.75rem;
}

.attachment-item {
  max-width: 300px;
}

.attachment-options {
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}

.suggested-responses {
  padding: 0.5rem;
  background-color: #e3f2fd;
  border-radius: 0.5rem;
}

.quick-replies {
  margin-top: 0.5rem;
}

.typing-indicator {
  display: flex;
  align-items: center;
}

.typing-bubble {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
}

.typing-dots {
  display: flex;
  gap: 0.25rem;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background-color: #6c757d;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.message-input .input-group {
  border-radius: 2rem;
  overflow: hidden;
}

.message-input .form-control {
  border: none;
  padding: 0.75rem 1rem;
}

.message-input .btn {
  border: none;
  padding: 0.75rem 1rem;
}

.notification-item {
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease;
}

.notification-item:hover {
  background-color: #f8f9fa;
}

.notification-icon {
  width: 30px;
  text-align: center;
}

.coach-stats {
  border-top: 1px solid #e9ecef;
  padding-top: 1rem;
}

@media (max-width: 768px) {
  .student-communication {
    padding: 1rem;
  }
  
  .communication-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .message-bubble {
    max-width: 85%;
  }
  
  .card-body {
    height: 400px !important;
  }
  
  .col-lg-3 {
    margin-bottom: 1rem;
  }
}
</style>
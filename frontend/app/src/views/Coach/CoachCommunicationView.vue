<template>
  <div class="coach-communication">
    <!-- Header -->
    <div class="communication-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h2 mb-1 text-white">Comunicación con Alumnos</h1>
          <p class="mb-0 text-white-50">Mantén contacto directo con tus alumnos y proporciona feedback personalizado</p>
        </div>
        <div class="col-md-4 text-end">
          <button class="btn btn-light" @click="showNewMessageModal = true">
            <font-awesome-icon icon="fas fa-plus" class="me-2" />
            Nuevo Mensaje
          </button>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Sidebar - Conversations List -->
      <div class="col-lg-4 col-md-5">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <font-awesome-icon icon="fas fa-comments" class="me-2 text-primary" />
                Conversaciones
              </h5>
              <div class="dropdown">
                <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                  <font-awesome-icon icon="fas fa-filter" class="me-1" />
                  Filtrar
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" @click="filterConversations('all')">Todas</a></li>
                  <li><a class="dropdown-item" href="#" @click="filterConversations('unread')">No leídas</a></li>
                  <li><a class="dropdown-item" href="#" @click="filterConversations('active')">Activas</a></li>
                  <li><a class="dropdown-item" href="#" @click="filterConversations('archived')">Archivadas</a></li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="card-body p-0">
            <!-- Search Bar -->
            <div class="p-3 border-bottom">
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0">
                  <font-awesome-icon icon="fas fa-search" class="text-muted" />
                </span>
                <input 
                  type="text" 
                  class="form-control border-start-0" 
                  placeholder="Buscar conversaciones..."
                  v-model="searchQuery"
                >
              </div>
            </div>
            
            <!-- Conversations List -->
            <div class="conversations-list">
              <div 
                v-for="conversation in filteredConversations" 
                :key="conversation.id"
                class="conversation-item" 
                :class="{ 'active': selectedConversation?.id === conversation.id, 'unread': conversation.unreadCount > 0 }"
                @click="selectConversation(conversation)"
              >
                <div class="d-flex align-items-center p-3">
                  <div class="position-relative me-3">
                    <img 
                      :src="conversation.student.avatar" 
                      :alt="conversation.student.name"
                      class="rounded-circle"
                      width="50"
                      height="50"
                    >
                    <span 
                      v-if="conversation.student.isOnline" 
                      class="position-absolute bottom-0 end-0 bg-success rounded-circle border border-white"
                      style="width: 12px; height: 12px;"
                    ></span>
                  </div>
                  
                  <div class="flex-grow-1 min-width-0">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <h6 class="mb-0 text-truncate">{{ conversation.student.name }}</h6>
                      <small class="text-muted">{{ formatTime(conversation.lastMessage.timestamp) }}</small>
                    </div>
                    
                    <p class="mb-1 text-muted small text-truncate">{{ conversation.lastMessage.content }}</p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                      <div class="d-flex gap-1">
                        <span 
                          v-if="conversation.hasAttachment" 
                          class="badge bg-light text-dark"
                        >
                          <font-awesome-icon icon="fas fa-paperclip" />
                        </span>
                        <span 
                          v-if="conversation.priority === 'high'" 
                          class="badge bg-danger"
                        >
                          <font-awesome-icon icon="fas fa-exclamation" />
                        </span>
                      </div>
                      
                      <span 
                        v-if="conversation.unreadCount > 0" 
                        class="badge bg-primary rounded-pill"
                      >
                        {{ conversation.unreadCount }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="filteredConversations.length === 0" class="text-center py-4 text-muted">
                <font-awesome-icon icon="fas fa-inbox" class="fa-2x mb-3" />
                <p class="mb-0">No hay conversaciones</p>
                <small>Inicia una nueva conversación con tus alumnos</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Content - Chat Area -->
      <div class="col-lg-8 col-md-7">
        <div class="card border-0 shadow-sm h-100">
          <!-- Chat Header -->
          <div v-if="selectedConversation" class="card-header bg-white border-0">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <img 
                  :src="selectedConversation.student.avatar" 
                  :alt="selectedConversation.student.name"
                  class="rounded-circle me-3"
                  width="40"
                  height="40"
                >
                <div>
                  <h5 class="mb-0">{{ selectedConversation.student.name }}</h5>
                  <small class="text-muted">
                    <span v-if="selectedConversation.student.isOnline" class="text-success">
                      <font-awesome-icon icon="fas fa-circle" class="me-1" style="font-size: 0.5rem;" />
                      En línea
                    </span>
                    <span v-else class="text-muted">
                      Última vez: {{ formatLastSeen(selectedConversation.student.lastSeen) }}
                    </span>
                  </small>
                </div>
              </div>
              
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-primary" @click="viewStudentProfile">
                  <font-awesome-icon icon="fas fa-user" class="me-1" />
                  Perfil
                </button>
                <button class="btn btn-sm btn-outline-secondary" @click="archiveConversation">
                  <font-awesome-icon icon="fas fa-archive" class="me-1" />
                  Archivar
                </button>
                <div class="dropdown">
                  <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <font-awesome-icon icon="fas fa-ellipsis-v" />
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click="markAsUnread">Marcar como no leído</a></li>
                    <li><a class="dropdown-item" href="#" @click="blockStudent">Bloquear alumno</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="#" @click="deleteConversation">Eliminar conversación</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Messages Area -->
          <div class="card-body d-flex flex-column" style="height: 500px;">
            <div v-if="!selectedConversation" class="d-flex align-items-center justify-content-center h-100 text-muted">
              <div class="text-center">
                <font-awesome-icon icon="fas fa-comments" class="fa-3x mb-3" />
                <h5>Selecciona una conversación</h5>
                <p class="mb-0">Elige una conversación de la lista para comenzar a chatear</p>
              </div>
            </div>
            
            <div v-else class="messages-container flex-grow-1 overflow-auto mb-3">
              <div 
                v-for="message in selectedConversation.messages" 
                :key="message.id"
                class="message-item mb-3"
                :class="{ 'message-sent': message.senderId === 'coach', 'message-received': message.senderId !== 'coach' }"
              >
                <div class="d-flex" :class="message.senderId === 'coach' ? 'justify-content-end' : 'justify-content-start'">
                  <div class="message-bubble" :class="message.senderId === 'coach' ? 'bg-primary text-white' : 'bg-light'">
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
                    </div>
                    
                    <div class="message-meta d-flex justify-content-between align-items-center mt-1">
                      <small class="opacity-75">{{ formatMessageTime(message.timestamp) }}</small>
                      <div v-if="message.senderId === 'coach'" class="message-status">
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
            </div>
            
            <!-- Message Input -->
            <div v-if="selectedConversation" class="message-input">
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
                  <button class="btn btn-sm btn-outline-primary" @click="attachFile('document')">
                    <font-awesome-icon icon="fas fa-file" class="me-1" />
                    Documento
                  </button>
                  <button class="btn btn-sm btn-outline-success" @click="attachFile('image')">
                    <font-awesome-icon icon="fas fa-image" class="me-1" />
                    Imagen
                  </button>
                  <button class="btn btn-sm btn-outline-info" @click="attachFile('workout')">
                    <font-awesome-icon icon="fas fa-dumbbell" class="me-1" />
                    Plan de Entrenamiento
                  </button>
                </div>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="selectedConversation.student.isTyping" class="typing-indicator mt-2">
                <small class="text-muted">
                  <font-awesome-icon icon="fas fa-circle" class="fa-fade me-1" style="font-size: 0.5rem;" />
                  {{ selectedConversation.student.name }} está escribiendo...
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- New Message Modal -->
    <div v-if="showNewMessageModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <font-awesome-icon icon="fas fa-plus" class="me-2" />
              Nueva Conversación
            </h5>
            <button type="button" class="btn-close" @click="showNewMessageModal = false"></button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="startNewConversation">
              <div class="mb-3">
                <label for="studentSelect" class="form-label">Seleccionar Alumno</label>
                <select class="form-select" id="studentSelect" v-model="newConversation.studentId" required>
                  <option value="">Elige un alumno...</option>
                  <option v-for="student in availableStudents" :key="student.id" :value="student.id">
                    {{ student.name }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="messageSubject" class="form-label">Asunto (opcional)</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="messageSubject" 
                  v-model="newConversation.subject"
                  placeholder="Asunto del mensaje"
                >
              </div>
              
              <div class="mb-3">
                <label for="messageContent" class="form-label">Mensaje</label>
                <textarea 
                  class="form-control" 
                  id="messageContent" 
                  rows="4" 
                  v-model="newConversation.message"
                  placeholder="Escribe tu mensaje aquí..."
                  required
                ></textarea>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Prioridad</label>
                <div class="d-flex gap-3">
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="priority" id="priorityNormal" value="normal" v-model="newConversation.priority">
                    <label class="form-check-label" for="priorityNormal">Normal</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="priority" id="priorityHigh" value="high" v-model="newConversation.priority">
                    <label class="form-check-label" for="priorityHigh">Alta</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showNewMessageModal = false">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="startNewConversation" :disabled="!newConversation.studentId || !newConversation.message">
              <font-awesome-icon icon="fas fa-paper-plane" class="me-2" />
              Enviar Mensaje
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'CoachCommunicationView',
  setup() {
    // Reactive data
    const searchQuery = ref('')
    const selectedConversation = ref(null)
    const newMessage = ref('')
    const isTyping = ref(false)
    const showAttachmentOptions = ref(false)
    const showEmojiPicker = ref(false)
    const showNewMessageModal = ref(false)
    const conversationFilter = ref('all')
    
    const newConversation = ref({
      studentId: '',
      subject: '',
      message: '',
      priority: 'normal'
    })
    
    const conversations = ref([
      {
        id: 1,
        student: {
          id: 1,
          name: 'Ana García',
          avatar: 'https://via.placeholder.com/50x50/007bff/ffffff?text=AG',
          isOnline: true,
          isTyping: false,
          lastSeen: new Date(Date.now() - 5 * 60 * 1000)
        },
        lastMessage: {
          id: 3,
          content: '¡Gracias por el plan de entrenamiento! ¿Cuándo empiezo?',
          timestamp: new Date(Date.now() - 10 * 60 * 1000),
          senderId: 'student'
        },
        unreadCount: 2,
        hasAttachment: false,
        priority: 'normal',
        messages: [
          {
            id: 1,
            content: 'Hola Ana, he revisado tu progreso y creo que podemos intensificar un poco el entrenamiento.',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
            senderId: 'coach',
            status: 'read'
          },
          {
            id: 2,
            content: 'Te he preparado un nuevo plan de entrenamiento personalizado.',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000 + 30000),
            senderId: 'coach',
            status: 'read',
            attachments: [
              {
                id: 1,
                name: 'Plan_Entrenamiento_Ana_Semana12.pdf',
                type: 'pdf',
                size: 2048576
              }
            ]
          },
          {
            id: 3,
            content: '¡Gracias por el plan de entrenamiento! ¿Cuándo empiezo?',
            timestamp: new Date(Date.now() - 10 * 60 * 1000),
            senderId: 'student',
            status: 'delivered'
          }
        ]
      },
      {
        id: 2,
        student: {
          id: 2,
          name: 'Carlos Ruiz',
          avatar: 'https://via.placeholder.com/50x50/28a745/ffffff?text=CR',
          isOnline: false,
          isTyping: false,
          lastSeen: new Date(Date.now() - 2 * 60 * 60 * 1000)
        },
        lastMessage: {
          id: 2,
          content: 'Perfecto, nos vemos mañana entonces.',
          timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
          senderId: 'coach'
        },
        unreadCount: 0,
        hasAttachment: true,
        priority: 'high',
        messages: [
          {
            id: 1,
            content: 'Hola Carlos, ¿podemos reunirnos mañana para revisar tu técnica de carrera?',
            timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
            senderId: 'coach',
            status: 'read'
          },
          {
            id: 2,
            content: 'Perfecto, nos vemos mañana entonces.',
            timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
            senderId: 'coach',
            status: 'delivered'
          }
        ]
      },
      {
        id: 3,
        student: {
          id: 3,
          name: 'María López',
          avatar: 'https://via.placeholder.com/50x50/dc3545/ffffff?text=ML',
          isOnline: false,
          isTyping: false,
          lastSeen: new Date(Date.now() - 24 * 60 * 60 * 1000)
        },
        lastMessage: {
          id: 1,
          content: 'Hola María, ¿cómo te sientes después del entrenamiento de ayer?',
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
          senderId: 'coach'
        },
        unreadCount: 0,
        hasAttachment: false,
        priority: 'normal',
        messages: [
          {
            id: 1,
            content: 'Hola María, ¿cómo te sientes después del entrenamiento de ayer?',
            timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
            senderId: 'coach',
            status: 'sent'
          }
        ]
      }
    ])
    
    const availableStudents = ref([
      { id: 4, name: 'Pedro Martín' },
      { id: 5, name: 'Laura Sánchez' },
      { id: 6, name: 'Diego Torres' }
    ])
    
    // Computed
    const filteredConversations = computed(() => {
      let filtered = conversations.value
      
      // Apply search filter
      if (searchQuery.value) {
        filtered = filtered.filter(conv => 
          conv.student.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          conv.lastMessage.content.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      }
      
      // Apply conversation filter
      switch (conversationFilter.value) {
        case 'unread':
          filtered = filtered.filter(conv => conv.unreadCount > 0)
          break
        case 'active':
          filtered = filtered.filter(conv => conv.student.isOnline)
          break
        case 'archived':
          // Implement archived filter logic
          break
      }
      
      return filtered.sort((a, b) => new Date(b.lastMessage.timestamp) - new Date(a.lastMessage.timestamp))
    })
    
    // Methods
    const selectConversation = (conversation) => {
      selectedConversation.value = conversation
      // Mark as read
      conversation.unreadCount = 0
    }
    
    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedConversation.value) return
      
      isTyping.value = true
      
      try {
        const message = {
          id: Date.now(),
          content: newMessage.value,
          timestamp: new Date(),
          senderId: 'coach',
          status: 'sent'
        }
        
        selectedConversation.value.messages.push(message)
        selectedConversation.value.lastMessage = message
        
        newMessage.value = ''
        
        // Simulate message delivery
        setTimeout(() => {
          message.status = 'delivered'
        }, 1000)
        
        // Simulate message read
        setTimeout(() => {
          message.status = 'read'
        }, 3000)
        
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        isTyping.value = false
      }
    }
    
    const startNewConversation = () => {
      if (!newConversation.value.studentId || !newConversation.value.message) return
      
      const student = availableStudents.value.find(s => s.id === parseInt(newConversation.value.studentId))
      if (!student) return
      
      const newConv = {
        id: Date.now(),
        student: {
          ...student,
          avatar: `https://via.placeholder.com/50x50/6c757d/ffffff?text=${student.name.split(' ').map(n => n[0]).join('')}`,
          isOnline: false,
          isTyping: false,
          lastSeen: new Date()
        },
        lastMessage: {
          id: 1,
          content: newConversation.value.message,
          timestamp: new Date(),
          senderId: 'coach'
        },
        unreadCount: 0,
        hasAttachment: false,
        priority: newConversation.value.priority,
        messages: [
          {
            id: 1,
            content: newConversation.value.message,
            timestamp: new Date(),
            senderId: 'coach',
            status: 'sent'
          }
        ]
      }
      
      conversations.value.unshift(newConv)
      selectedConversation.value = newConv
      
      // Reset form
      newConversation.value = {
        studentId: '',
        subject: '',
        message: '',
        priority: 'normal'
      }
      
      showNewMessageModal.value = false
    }
    
    const filterConversations = (filter) => {
      conversationFilter.value = filter
    }
    
    const formatTime = (timestamp) => {
      const now = new Date()
      const date = new Date(timestamp)
      const diffInHours = (now - date) / (1000 * 60 * 60)
      
      if (diffInHours < 1) {
        return `${Math.floor((now - date) / (1000 * 60))}m`
      } else if (diffInHours < 24) {
        return `${Math.floor(diffInHours)}h`
      } else {
        return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
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
    
    const attachFile = (type) => {
      console.log('Attach file of type:', type)
      // Implement file attachment logic
      showAttachmentOptions.value = false
    }
    
    const downloadAttachment = (attachment) => {
      console.log('Download attachment:', attachment)
      // Implement download logic
    }
    
    const viewStudentProfile = () => {
      if (selectedConversation.value) {
        console.log('View profile for student:', selectedConversation.value.student.id)
        // Navigate to student profile
      }
    }
    
    const archiveConversation = () => {
      if (selectedConversation.value) {
        console.log('Archive conversation:', selectedConversation.value.id)
        // Implement archive logic
      }
    }
    
    const markAsUnread = () => {
      if (selectedConversation.value) {
        selectedConversation.value.unreadCount = 1
      }
    }
    
    const blockStudent = () => {
      if (selectedConversation.value) {
        console.log('Block student:', selectedConversation.value.student.id)
        // Implement block logic
      }
    }
    
    const deleteConversation = () => {
      if (selectedConversation.value && confirm('¿Estás seguro de que quieres eliminar esta conversación?')) {
        const index = conversations.value.findIndex(c => c.id === selectedConversation.value.id)
        if (index > -1) {
          conversations.value.splice(index, 1)
          selectedConversation.value = null
        }
      }
    }
    
    onMounted(() => {
      // Select first conversation by default
      if (conversations.value.length > 0) {
        selectConversation(conversations.value[0])
      }
    })
    
    return {
      searchQuery,
      selectedConversation,
      newMessage,
      isTyping,
      showAttachmentOptions,
      showEmojiPicker,
      showNewMessageModal,
      newConversation,
      conversations,
      availableStudents,
      filteredConversations,
      selectConversation,
      sendMessage,
      startNewConversation,
      filterConversations,
      formatTime,
      formatMessageTime,
      formatLastSeen,
      getFileIcon,
      formatFileSize,
      attachFile,
      downloadAttachment,
      viewStudentProfile,
      archiveConversation,
      markAsUnread,
      blockStudent,
      deleteConversation
    }
  }
}
</script>

<style scoped>
.coach-communication {
  padding: 1.5rem;
}

.communication-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.conversations-list {
  max-height: 600px;
  overflow-y: auto;
}

.conversation-item {
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f8f9fa;
}

.conversation-item:hover {
  background-color: #f8f9fa;
}

.conversation-item.active {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.conversation-item.unread {
  background-color: #fff3e0;
}

.conversation-item.unread .conversation-item:not(.active):hover {
  background-color: #ffe0b2;
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

.typing-indicator {
  padding: 0.5rem;
  background-color: #e3f2fd;
  border-radius: 0.5rem;
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

@media (max-width: 768px) {
  .coach-communication {
    padding: 1rem;
  }
  
  .communication-header {
    padding: 1.5rem;
    text-align: center;
  }
  
  .message-bubble {
    max-width: 85%;
  }
  
  .conversations-list {
    max-height: 400px;
  }
  
  .card-body {
    height: 400px !important;
  }
}
</style>
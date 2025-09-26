# Importar modelo de usuario
from users.user.models import *

# Importar nuevos modelos para el sistema entrenador-alumno
from coaches.models import *
from students.models import *
from training.models import *
from users.user_roles.models import *

# Importar la clase Base de la base de datos
from core.database_sqlite import Base
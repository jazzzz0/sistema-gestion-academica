from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from users.models import Admin, User


class AdminService:
    """
    Servicio que gestiona la creación atómica de un usuario con rol de administrador.
    Contiene la lógica de negocio y validaciones necesarias.
    """

    @staticmethod
    @transaction.atomic
    def create_admin_user(data: dict) -> Admin:
        """
        Crea un usuario con rol ADMIN y su perfil de Admin asociado de forma atómica.
        Recibe un diccionario con los datos necesarios para crear ambos objetos.
        Retorna el objeto Admin creado.
        Args:
            data (dict): Diccionario con los datos para crear el User y Admin.
                Campos obligatorios:
                    - name (str)
                    - surname (str)
                    - dni (str)
                    - email (str)
                    - hire_date (date)
                    - password (str): Contraseña manual para el usuario ADMIN.
                Campos opcionales:
                    - address (str)
                    - birth_date (date)
                    - phone (str)
                    - department (str)
        Raises:
            ValidationError: Si alguna validación falla.
        Returns:
            Admin: Objeto Admin creado.
        """
        # Validar campos obligatorios
        required_fields = ['name', 'surname', 'dni', 'email', 'hire_date']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Faltan campos obligatorios: {', '.join(missing_fields)}")

        # Regla de negocio: hire_date no puede ser futura
        if data['hire_date'] > timezone.now().date():
            raise ValidationError({'hire_date': "La fecha de incorporación no puede ser futura."})

        # Validaciones de unicidad
        if not AdminService.validate_dni_unique(data['dni']):
            raise ValidationError({'dni': "El DNI ya existe."})

        if not AdminService.validate_email_unique(data['email']):
            raise ValidationError({'email': "El email ya existe."})

        # Crear User con rol ADMIN
        # Este usuario tiene contraseña manual, no se toma desde DNI
        user = User.objects.create_user(
            email=data['email'],
            role='ADMIN',
            password=data['password'],
        )

        # Validar que user.is_staff sea True
        if not user.is_staff:
            raise ValidationError("El usuario ADMIN debe tener is_staff=True.")

        # Crear Admin con campos de Person
        admin = Admin.objects.create(
            user=user,
            name=data['name'],
            surname=data['surname'],
            dni=data['dni'],
            hire_date=data['hire_date'],
            address=data.get('address', None),
            birth_date=data.get('birth_date', None),
            phone=data.get('phone', None),
            department=data.get('department', None),
        )

        return admin

    @staticmethod
    def validate_dni_unique(dni: str) -> bool:
        """
        Valida que el DNI sea único globalmente.
        Person es abstracto, así que chequeamos las entidades concretas.
        Retorna True si el DNI no existe, False si ya está en uso.
        """
        # Importamos aquí para evitar dependencias circulares
        # TODO: Agregar las otras entidades cuando estén disponibles
        from users.models import Admin
        from students.models import Student
        # from teachers.models import Teacher

        exists_in_admin = Admin.objects.filter(dni=dni).exists()
        exists_in_student = Student.objects.filter(dni=dni).exists()
        # exists_in_teacher = Teacher.objects.filter(dni=dni).exists()

        return not (exists_in_admin or exists_in_student)

    @staticmethod
    def validate_email_unique(email: str) -> bool:
        """
        Valida que el email sea único globalmente en el sistema.
        Retorna True si el email no existe, False si ya está en uso.
        """
        return not User.objects.filter(email=email).exists()

from django.db import transaction

from users.models.teacher import Teacher


class TeacherService:
    """
    Servicio para manejar la lógica de negocio de Profesores.
    """

    @staticmethod
    @transaction.atomic
    def create_teacher_user(data:dict) -> Teacher:
        """
        Crea un User (con rol Teacher) y un Teacher (Person)
        en una transacción atómica.

        La contraseña inicial será el DNI, como pide el requisito.
        """
        pass

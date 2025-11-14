from django.db import migrations
from django.utils import timezone


def create_admin_profiles(apps, schema_editor):
    """
    Crea perfiles Admin para usuarios existentes con is_staff=True
    que no tengan un perfil Admin asociado.
    """
    User = apps.get_model('users', 'User')
    Admin = apps.get_model('users', 'Admin')
    
    # Buscar usuarios con is_staff=True que no tengan perfil Admin
    # Usamos una consulta que verifica que no exista un Admin con ese user
    users_without_profile = User.objects.filter(
        is_staff=True
    )
    
    # Filtrar usuarios que no tienen perfil Admin
    users_to_process = []
    for user in users_without_profile:
        if not Admin.objects.filter(user=user).exists():
            users_to_process.append(user)
    
    created_count = 0
    skipped_count = 0
    
    for user in users_to_process:
        try:
            # Generar datos por defecto si no existen
            # Usar el email para extraer nombre si es posible
            email_local = user.email.split('@')[0]
            email_parts = email_local.split('.')
            
            # Intentar extraer nombre y apellido del email
            if len(email_parts) >= 2:
                name = email_parts[0].capitalize()
                surname = email_parts[1].capitalize()
            elif len(email_parts) == 1:
                # Si solo hay una parte, dividir por otros separadores comunes
                parts = email_parts[0].replace('_', '.').split('.')
                if len(parts) >= 2:
                    name = parts[0].capitalize()
                    surname = parts[1].capitalize()
                else:
                    name = "Administrador"
                    surname = "Sistema"
            else:
                name = "Administrador"
                surname = "Sistema"
            
            # Generar un DNI único temporal
            # Usar el ID del usuario como base para el DNI
            dni_base = str(user.id).zfill(7)
            # Asegurar que el DNI tenga 7 u 8 dígitos
            if len(dni_base) > 8:
                dni_base = dni_base[:8]
            
            # Verificar que el DNI no exista ya y generar uno único
            dni = dni_base
            counter = 1
            max_attempts = 1000
            while Admin.objects.filter(dni=dni).exists() and counter < max_attempts:
                # Intentar con diferentes variaciones
                if len(dni_base) == 7:
                    dni = f"{dni_base}{counter % 10}".zfill(8)
                else:
                    dni = f"{dni_base[:7]}{counter % 10}".zfill(8)
                counter += 1
            
            # Si aún no es único, usar timestamp
            if Admin.objects.filter(dni=dni).exists():
                timestamp_str = str(int(timezone.now().timestamp()))
                dni = timestamp_str[-8:].zfill(8)
                # Asegurar unicidad final
                while Admin.objects.filter(dni=dni).exists():
                    dni = str(int(timezone.now().timestamp()) + counter)[-8:].zfill(8)
                    counter += 1
            
            # Usar date_joined como hire_date, o fecha actual si no existe
            if user.date_joined:
                hire_date = user.date_joined.date()
            else:
                hire_date = timezone.now().date()
            
            # Crear el perfil Admin
            Admin.objects.create(
                user=user,
                name=name,
                surname=surname,
                dni=dni,
                hire_date=hire_date,
                is_active=user.is_active,
                department=None,  # Se puede completar manualmente después
                address=None,
                birth_date=None,
                phone=None,
            )
            created_count += 1
        except Exception as e:
            # Si hay un error, registrar pero continuar
            print(f"Error al crear perfil Admin para usuario {user.email}: {e}")
            skipped_count += 1
    
    print(f"Migración completada: {created_count} perfiles Admin creados, {skipped_count} omitidos.")


def reverse_create_admin_profiles(apps, schema_editor):
    """
    Reversa la migración eliminando los perfiles Admin creados para usuarios
    con is_staff=True que no tenían perfil antes de esta migración.
    Nota: Esta función elimina perfiles Admin asociados a usuarios con is_staff=True.
    Usar con precaución.
    """
    User = apps.get_model('users', 'User')
    Admin = apps.get_model('users', 'Admin')
    
    # Eliminar perfiles Admin de usuarios con is_staff=True
    # Esto es una aproximación, ya que no podemos rastrear exactamente
    # cuáles fueron creados por esta migración
    users_with_staff = User.objects.filter(is_staff=True)
    Admin.objects.filter(user__in=users_with_staff).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_admin'),
    ]

    operations = [
        migrations.RunPython(
            create_admin_profiles,
            reverse_create_admin_profiles,
        ),
    ]


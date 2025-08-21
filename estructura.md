Esta es la estructura de apps con sus correspondientes modelos.

PROJECT (Django)
│
├── core/                # App inicial de Django (configuración)
│
├── base/                # Modelos base y utilidades compartidas
│   ├── Persona (abstracta)
│   └── TimeStampedModel (abstracta)
│
├── users/               # Gestión de usuarios y roles
│   └── Usuario
│
├── students/            # Datos académicos de alumnos
│   └── Alumno (OneToOne con Usuario, relación con Carrera)
│
├── careers/             # Carreras académicas
│   └── Carrera
│
├── subjects/            # Materias
│   ├── Materia
│   └── MateriaEnCarrera (relación Carrera ↔ Materia)
│
└── enrollments/         # Inscripciones
    └── Enrollment (Alumno ↔ Materia, fecha, estado)

"""Seed script to populate initial labs into the database.

This script is idempotent: it checks for existing lab codes before inserting.
"""
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base  # ensures models are imported
from app.db.session import SessionLocal, engine
from app.models.lab import DifficultyLevel, Lab, LabInitialState


def get_seed_labs() -> list[dict]:
    """Return the list of labs to seed."""
    return [
        # BEGINNER labs
        {
            "codigo": "LAB_BEG_001",
            "titulo": "Intro a Linux y CLI",
            "nivel_dificultad": DifficultyLevel.BEGINNER,
            "xp_otorgado": 100,
            "estado_inicial": LabInitialState.DISPONIBLE,
            "historia": "Aprende los comandos básicos de Linux.",
            "objetivo": "Navegar el sistema de archivos y manipular archivos.",
            "reglas": "Usar solo comandos disponibles en el contenedor.",
            "entregable_descripcion": "Archivo README con los comandos usados.",
            "orden_desbloqueo": 0,
        },
        {
            "codigo": "LAB_BEG_002",
            "titulo": "Control de versiones con Git",
            "nivel_dificultad": DifficultyLevel.BEGINNER,
            "xp_otorgado": 120,
            "estado_inicial": LabInitialState.DISPONIBLE,
            "historia": "Aprende a versionar tu código.",
            "objetivo": "Crear commits y manejar ramas básicas.",
            "reglas": "No reescribir la historia de commits compartidos.",
            "entregable_descripcion": "Repositorio con commits y ramas.",
            "orden_desbloqueo": 1,
        },
        {
            "codigo": "LAB_BEG_003",
            "titulo": "Fundamentos de redes",
            "nivel_dificultad": DifficultyLevel.BEGINNER,
            "xp_otorgado": 130,
            "estado_inicial": LabInitialState.DISPONIBLE,
            "historia": "Comprende conceptos básicos de redes.",
            "objetivo": "Usar ping, traceroute y netstat.",
            "reglas": "No realizar escaneos agresivos.",
            "entregable_descripcion": "Reporte con resultados de comandos.",
            "orden_desbloqueo": 2,
        },
        {
            "codigo": "LAB_BEG_004",
            "titulo": "Docker para principiantes",
            "nivel_dificultad": DifficultyLevel.BEGINNER,
            "xp_otorgado": 150,
            "estado_inicial": LabInitialState.DISPONIBLE,
            "historia": "Construye y corre contenedores.",
            "objetivo": "Crear una imagen y correr un contenedor.",
            "reglas": "Usar imágenes oficiales cuando sea posible.",
            "entregable_descripcion": "Dockerfile y comandos utilizados.",
            "orden_desbloqueo": 3,
        },
        {
            "codigo": "LAB_BEG_005",
            "titulo": "APIs REST con FastAPI",
            "nivel_dificultad": DifficultyLevel.BEGINNER,
            "xp_otorgado": 180,
            "estado_inicial": LabInitialState.DISPONIBLE,
            "historia": "Crea tu primera API REST.",
            "objetivo": "Implementar endpoints CRUD básicos.",
            "reglas": "Cumplir con códigos de estado HTTP apropiados.",
            "entregable_descripcion": "Repositorio con endpoints y pruebas básicas.",
            "orden_desbloqueo": 4,
        },
        # INTERMEDIATE labs
        {
            "codigo": "LAB_INT_001",
            "titulo": "Persistencia con PostgreSQL",
            "nivel_dificultad": DifficultyLevel.INTERMEDIATE,
            "xp_otorgado": 250,
            "estado_inicial": LabInitialState.BLOQUEADO,
            "historia": "Conecta tu app a Postgres.",
            "objetivo": "Diseñar tablas y ejecutar queries.",
            "reglas": "Optimizar índices básicos.",
            "entregable_descripcion": "Script SQL y configuración de conexión.",
            "orden_desbloqueo": 5,
        },
        {
            "codigo": "LAB_INT_002",
            "titulo": "Autenticación con JWT",
            "nivel_dificultad": DifficultyLevel.INTERMEDIATE,
            "xp_otorgado": 280,
            "estado_inicial": LabInitialState.BLOQUEADO,
            "historia": "Protege tus endpoints.",
            "objetivo": "Implementar login y protección de rutas.",
            "reglas": "Almacenar tokens de forma segura.",
            "entregable_descripcion": "Endpoints protegidos y pruebas de autenticación.",
            "orden_desbloqueo": 6,
        },
        {
            "codigo": "LAB_INT_003",
            "titulo": "Testing automático",
            "nivel_dificultad": DifficultyLevel.INTERMEDIATE,
            "xp_otorgado": 300,
            "estado_inicial": LabInitialState.BLOQUEADO,
            "historia": "Asegura la calidad de tu código.",
            "objetivo": "Crear pruebas unitarias y de integración.",
            "reglas": "Cubrir casos críticos y manejar errores.",
            "entregable_descripcion": "Suite de pruebas y reporte de cobertura.",
            "orden_desbloqueo": 7,
        },
        # ADVANCED lab
        {
            "codigo": "LAB_ADV_001",
            "titulo": "Escalabilidad y despliegue",
            "nivel_dificultad": DifficultyLevel.ADVANCED,
            "xp_otorgado": 400,
            "estado_inicial": LabInitialState.BLOQUEADO,
            "historia": "Prepara tu app para producción.",
            "objetivo": "Configurar CI/CD y monitoreo básico.",
            "reglas": "Minimizar downtime en despliegues.",
            "entregable_descripcion": "Pipeline de CI/CD y documentación de monitoreo.",
            "orden_desbloqueo": 8,
        },
    ]


def seed(db: Session) -> None:
    """Insert labs if they do not already exist."""
    labs = get_seed_labs()
    existing_codes = {
        code for (code,) in db.query(Lab.codigo).filter(Lab.codigo.in_([l["codigo"] for l in labs])).all()
    }

    to_create = [lab for lab in labs if lab["codigo"] not in existing_codes]
    for lab_data in to_create:
        db.add(Lab(**lab_data))

    if to_create:
        db.commit()
        print(f"Inserted {len(to_create)} labs.")
    else:
        print("No new labs to insert; already seeded.")


def main():
    """Entrypoint for CLI usage."""
    # Ensure metadata is available (Base imported above)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()

# Usage example inside Docker container:
# docker compose exec api python -m app.db.seed_labs

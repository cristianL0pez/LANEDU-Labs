"""Service layer for lab operations."""
from sqlalchemy.orm import Session

from app.models.lab import Lab
from app.models.user_lab_progress import UserLabProgress


def list_labs_for_user(db: Session, user_id: int) -> list[dict]:
    """Return all labs with user-specific state (progress-aware)."""
    labs = db.query(Lab).order_by(Lab.orden_desbloqueo.asc(), Lab.id.asc()).all()

    progress_by_lab = {
        p.lab_id: p.estado for p in db.query(UserLabProgress).filter_by(user_id=user_id).all()
    }

    result = []
    for lab in labs:
        estado = progress_by_lab.get(lab.id, lab.estado_inicial.value if hasattr(lab.estado_inicial, "value") else lab.estado_inicial)
        result.append(
            {
                "id": lab.id,
                "titulo": lab.titulo,
                "nivel_dificultad": lab.nivel_dificultad.value if hasattr(lab.nivel_dificultad, "value") else lab.nivel_dificultad,
                "xp_otorgado": lab.xp_otorgado,
                "estado": estado,
            }
        )
    return result


def get_lab(db: Session, lab_id: int) -> Lab | None:
    """Return a lab by id, or None if not found."""
    return db.get(Lab, lab_id)

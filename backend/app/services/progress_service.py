"""Service layer for progress management."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.lab import Lab
from app.models.user import User
from app.models.user_lab_progress import ProgressState, UserLabProgress


def calcular_nivel(xp_total: int) -> int:
    """Calculate the level based on XP (one level every 500 XP, minimum level 1)."""
    return max(1, 1 + xp_total // 500)


def complete_lab(db: Session, user_id: int, lab_id: int, doc_url: str | None) -> UserLabProgress:
    """Mark a lab as completed for a user, updating XP and level."""
    if not doc_url:
        raise ValueError("doc_url no puede estar vacío")

    lab = db.get(Lab, lab_id)
    if not lab:
        raise ValueError("Lab no encontrado")

    user = db.get(User, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")

    progress = (
        db.query(UserLabProgress)
        .filter(UserLabProgress.user_id == user_id, UserLabProgress.lab_id == lab_id)
        .first()
    )

    now = datetime.now(timezone.utc)
    if progress:
        # Calculate XP delta to avoid duplicating rewards on repeated completions.
        xp_prev = progress.xp_obtenido or 0
        xp_new = lab.xp_otorgado
        delta = max(0, xp_new - xp_prev)
        progress.estado = ProgressState.COMPLETADO
        progress.doc_url = doc_url
        progress.xp_obtenido = xp_new
        progress.completed_at = now
        user.xp_total += delta
    else:
        progress = UserLabProgress(
            user_id=user_id,
            lab_id=lab_id,
            estado=ProgressState.COMPLETADO,
            doc_url=doc_url,
            xp_obtenido=lab.xp_otorgado,
            completed_at=now,
        )
        user.xp_total += lab.xp_otorgado
        db.add(progress)

    user.nivel = calcular_nivel(user.xp_total)
    db.commit()
    db.refresh(user)
    db.refresh(progress)
    return progress

"""create initial tables

Revision ID: 20241004120000
Revises: 
Create Date: 2024-10-04 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20241004120000"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables for users, labs, and user_lab_progress."""
    difficulty_level = sa.Enum("BEGINNER", "INTERMEDIATE", "ADVANCED", name="difficulty_level")
    lab_initial_state = sa.Enum("DISPONIBLE", "BLOQUEADO", name="lab_initial_state")
    progress_state = sa.Enum("PENDIENTE", "COMPLETADO", name="progress_state")

    difficulty_level.create(op.get_bind(), checkfirst=True)
    lab_initial_state.create(op.get_bind(), checkfirst=True)
    progress_state.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("xp_total", sa.Integer(), server_default="0", nullable=False),
        sa.Column("nivel", sa.Integer(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)

    op.create_table(
        "labs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=50), nullable=False),
        sa.Column("titulo", sa.String(length=255), nullable=False),
        sa.Column("nivel_dificultad", difficulty_level, nullable=False),
        sa.Column("xp_otorgado", sa.Integer(), nullable=False),
        sa.Column("estado_inicial", lab_initial_state, nullable=False),
        sa.Column("historia", sa.Text(), nullable=False),
        sa.Column("objetivo", sa.Text(), nullable=False),
        sa.Column("reglas", sa.Text(), nullable=False),
        sa.Column("entregable_descripcion", sa.Text(), nullable=False),
        sa.Column("orden_desbloqueo", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo"),
        sa.CheckConstraint("xp_otorgado >= 0", name="ck_labs_xp_otorgado_non_negative"),
        sa.CheckConstraint("orden_desbloqueo >= 0", name="ck_labs_orden_desbloqueo_non_negative"),
    )
    op.create_index(op.f("ix_labs_id"), "labs", ["id"], unique=False)
    op.create_index(op.f("ix_labs_codigo"), "labs", ["codigo"], unique=False)

    op.create_table(
        "user_lab_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lab_id", sa.Integer(), nullable=False),
        sa.Column("estado", progress_state, nullable=False),
        sa.Column("doc_url", sa.String(length=500), nullable=True),
        sa.Column("xp_obtenido", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["lab_id"], ["labs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_lab_progress_id"), "user_lab_progress", ["id"], unique=False)
    op.create_index(op.f("ix_user_lab_progress_lab_id"), "user_lab_progress", ["lab_id"], unique=False)
    op.create_index(op.f("ix_user_lab_progress_user_id"), "user_lab_progress", ["user_id"], unique=False)


def downgrade() -> None:
    """Drop all tables and enums created in the initial migration."""
    op.drop_index(op.f("ix_user_lab_progress_user_id"), table_name="user_lab_progress")
    op.drop_index(op.f("ix_user_lab_progress_lab_id"), table_name="user_lab_progress")
    op.drop_index(op.f("ix_user_lab_progress_id"), table_name="user_lab_progress")
    op.drop_table("user_lab_progress")

    op.drop_index(op.f("ix_labs_codigo"), table_name="labs")
    op.drop_index(op.f("ix_labs_id"), table_name="labs")
    op.drop_table("labs")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    progress_state = sa.Enum("PENDIENTE", "COMPLETADO", name="progress_state")
    lab_initial_state = sa.Enum("DISPONIBLE", "BLOQUEADO", name="lab_initial_state")
    difficulty_level = sa.Enum("BEGINNER", "INTERMEDIATE", "ADVANCED", name="difficulty_level")

    progress_state.drop(op.get_bind(), checkfirst=True)
    lab_initial_state.drop(op.get_bind(), checkfirst=True)
    difficulty_level.drop(op.get_bind(), checkfirst=True)

"""alchemy2.v1

Revision ID: 3eb2f5bfddc2
Revises:
Create Date: 2023-08-18 14:39:44.000066

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "3eb2f5bfddc2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("Username", sa.String(length=60), nullable=False),
        sa.Column("Email", sa.String(), nullable=False),
        sa.Column("Password", sa.String(), nullable=False),
        sa.Column("Is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "User role",
            sa.Enum("ROLE_USER", "ROLE_ADMIN", name="roles"),
            nullable=False,
        ),
        sa.Column(
            "Created at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "Updated at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("Email"),
        sa.UniqueConstraint("Username"),
    )
    op.create_table(
        "todo_lists",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("Name", sa.String(length=101), nullable=False),
        sa.Column("Description", sa.Text(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "Created at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "Updated at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tasks",
        sa.Column("Task id", sa.UUID(), nullable=False),
        sa.Column("Name", sa.String(length=100), nullable=False),
        sa.Column("Description", sa.Text(), nullable=False),
        sa.Column(
            "status", sa.Enum("IN_PROGRESS", "DONE", name="taskstatus"), nullable=False
        ),
        sa.Column("todo_list_id", sa.UUID(), nullable=False),
        sa.Column(
            "Created at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "Updated at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["todo_list_id"],
            ["todo_lists.id"],
        ),
        sa.PrimaryKeyConstraint("Task id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tasks")
    op.drop_table("todo_lists")
    op.drop_table("users")
    # ### end Alembic commands ###

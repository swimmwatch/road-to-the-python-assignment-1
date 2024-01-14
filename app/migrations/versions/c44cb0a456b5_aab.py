"""aab

Revision ID: c44cb0a456b5
Revises: 
Create Date: 2024-01-11 00:29:27.274085

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c44cb0a456b5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.Column("sex", sa.Enum("female", "male", name="genders"), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("date_of_death", sa.Date(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created", sa.Date(), nullable=False),
        sa.Column("updated", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("pet_id", sa.Integer(), nullable=False),
        sa.Column("created", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pet_id"],
            ["pets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("photos")
    op.drop_table("pets")
    # ### end Alembic commands ###

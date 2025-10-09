from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey,
    Boolean, DateTime, func, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
import enum
from app.database.sync.base import Base

# =============================
# ENUMS
# =============================

class GlobalRole(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"             # Organization-level admin
    team_leader = "team_leader"
    team_member = "team_member"
    viewer = "viewer"           # Read-only access


class TeamMemberRole(enum.Enum):
    leader = "leader"
    member = "member"
    viewer = "viewer"


# =============================
# USER MODEL
# =============================

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    global_role = Column(Enum(GlobalRole), nullable=False, default=GlobalRole.viewer)

    # Account status flags
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Metadata / audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("auth.users.id"), nullable=True)

    # Relationships
    created_users = relationship("User", remote_side=[id])
    memberships = relationship(
        "TeamMember",
        back_populates="user",
        foreign_keys="TeamMember.user_id"
    )
    added_memberships = relationship(
        "TeamMember",
        back_populates="added_by_user",
        foreign_keys="TeamMember.added_by"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.global_role.value}')>"


# =============================
# TEAM MODEL
# =============================

class Team(Base):
    __tablename__ = "teams"
    __table_args__ = {"schema": "auth"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Account status flags
    is_active = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("auth.users.id"), nullable=True)

    # Relationships
    members = relationship("TeamMember", back_populates="team")
    creator = relationship("User", backref="created_teams", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"


# =============================
# TEAM MEMBER (LINK TABLE)
# =============================

class TeamMember(Base):
    __tablename__ = "team_members"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_user"),
        {"schema": "auth"},
    )

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("auth.teams.id"))
    user_id = Column(Integer, ForeignKey("auth.users.id"))
    role = Column(Enum(TeamMemberRole), nullable=False, default=TeamMemberRole.member)

    # Soft delete flag
    is_active = Column(Boolean, default=True)

    # For audit and role control
    added_by = Column(Integer, ForeignKey("auth.users.id"), nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship(
        "User",
        back_populates="memberships",
        foreign_keys=[user_id]
    )
    added_by_user = relationship(
        "User",
        back_populates="added_memberships",
        foreign_keys=[added_by]
    )

    def __repr__(self):
        return f"<TeamMember(team={self.team_id}, user={self.user_id}, role={self.role.value})>"

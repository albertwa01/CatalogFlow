from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, List
from datetime import datetime

# =============================
# ENUMS (mirror DB enums)
# =============================

class GlobalRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    team_leader = "team_leader"
    team_member = "team_member"
    viewer = "viewer"

class TeamMemberRole(str, Enum):
    leader = "leader"
    member = "member"
    viewer = "viewer"

# =============================
# USER SCHEMAS
# =============================

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    global_role: Optional[GlobalRole] = GlobalRole.viewer

class UserResponse(UserBase):
    id: int
    global_role: GlobalRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# =============================
# TEAM SCHEMAS
# =============================

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# =============================
# TEAM MEMBER SCHEMAS
# =============================

class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role: TeamMemberRole = TeamMemberRole.member

class TeamMemberResponse(TeamMemberBase):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
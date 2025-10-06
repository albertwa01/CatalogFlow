# CatalogFlow – User & Team Models, Relationships, and Flow

## 1️⃣ User Roles & Hierarchy

### Global Roles
| Role | Description |
|------|------------|
| superadmin | Full access, can manage all teams and users. Created manually only. |
| admin | Organization-level admin, can manage teams and users within scope. |
| team_leader | Can manage users within their teams. Can add/remove members. |
| team_member | Regular team member, actions require approval if needed. |
| viewer | Read-only access, cannot make changes. |

### Team-Specific Roles (per Team)
| Role | Description |
|------|------------|
| leader | Team leader for that specific team. Can add/remove members. |
| member | Regular team member within the team. |
| viewer | Read-only access to the team. |

---

## 2️⃣ User Signup & Creation Flow

1. **Superadmin**
   - Created manually (like Django's `createsuperuser`)  
   - Cannot be created via any endpoint.

2. **Other Users**
   - Created by authorized users:
     - Superadmin can create `admin` or `team_leader`
     - Team leader/admin can create `team_member` or `viewer` for their teams
   - Login via JWT only.

3. **Login Flow**
   - `/auth/login` endpoint with email + password
   - Returns JWT containing: `user_id`, `email`, `global_role`
   - Used for authentication & role-based access

---

## 3️⃣ Database Relationships

### User ↔ TeamMember ↔ Team
- Many-to-many relationship:
  - A user can belong to multiple teams.
  - A team can have multiple users.
- Team-specific role (`TeamMember.role`) overrides global role for that team.

### TeamMember Integrity
```python
__table_args__ = (
    UniqueConstraint("team_id", "user_id", name="uq_team_user"),
)
```

### Team-Member Integrity

- Ensures one membership per user per team  
- Allows the same user to belong to multiple teams  
- Prevents duplicates like:

| team_id | user_id | Valid? |
|---------|---------|--------|
| 1       | 7       | ✅ |
| 1       | 7       | ❌ Duplicate |
| 2       | 7       | ✅ |

---

### 4️⃣ Deletion & Cascade Policies

| Entity | Deletion Type | Cascade? | Notes |
|--------|---------------|----------|-------|
| User | Soft delete (`is_active=False`) | No | Keeps audit trail. Memberships remain if needed. |
| Team | Soft delete (`is_active=False`) | No | Retains team history and logs. |
| TeamMember | Hard delete (cascade with team or user) | Yes | Join table cleaned automatically. |
| created_by / added_by | Nullable FK | No | Prevents constraint issues if creator is deleted. |

> Soft deletion ensures historical data, logs, and team membership integrity are preserved.

---

### 5️⃣ Audit & Metadata

- **User:** `created_at`, `updated_at`, `created_by`, `is_active`, `is_verified`  
- **Team:** `created_at`, `updated_at`, `created_by`, `is_active`  
- **TeamMember:** `added_at`, `added_by`, `role`  

Logging table captures actions like:  
- User creation  
- Team creation  
- Membership additions/removals

---

### 6️⃣ Role-Based Access Logic

- **Superadmin:** Can create teams, users of any role. Full access to all teams.  
- **Admin:** Can manage teams under their scope. Can add/remove team members (not superadmin).  
- **Team Leader:** Can manage their own team members only. Cannot create superadmin/admin.  
- **Team Member / Viewer:** Limited actions. Cannot create users or teams.

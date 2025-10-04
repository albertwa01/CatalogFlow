# CatalogFlow – Project Scope & Components

## 1. Core Modules

These are the main entities and logic in the system:

| Module | Purpose |
|--------|---------|
| **Users** | Multi-user support, authentication, and role assignment (Super Admin, Supervisor, Team Admin, Team Member) |
| **Roles & Permissions** | Role-based access control (RBAC) with endpoint-level restrictions |
| **Teams** | Grouping users, team-level CRUD, approval workflow for content/changes |
| **Products** | Product entity with fields: name, description, SKU, price, stock, attributes, category, brand, tags |
| **Categories** | Category tree with parent-child relationships, CRUD, soft delete |
| **Brands** | Manage brands, associate with products |
| **Tags** | Product tags for filtering/searching |

---

## 2. Functional Features

| Feature | Details |
|---------|--------|
| **CRUD Operations** | Full Create, Read, Update, Delete for all core entities |
| **Approval Workflow** | Team Members submit changes → Team Admin approves → changes go live |
| **Bulk Operations** | Bulk updates for products, stock, or price |
| **Audit Logs** | Track who did what, when, and on which entity |
| **Caching** | Use Redis for frequently accessed data (e.g., product/category lists) |
| **Search / Analytics (Future)** | Endpoints for search optimization or analytics queries |
| **Background Tasks** | For caching refresh, bulk operations, notifications |
| **JWT Authentication** | Access tokens with expiry + optional refresh tokens |
| **Password Security** | Bcrypt hashing for passwords |

---

## 3. System / Infrastructure Components

| Component | Purpose |
|-----------|--------|
| **FastAPI App** | Core API framework |
| **SQLAlchemy** | ORM for PostgreSQL |
| **Alembic** | DB migrations |
| **PostgreSQL** | Main database |
| **Redis** | Cache for frequently accessed endpoints/data |
| **Logging** | Centralized structured logging (e.g., using loguru) |
| **Docker + Docker Compose** | Containerization for local dev / deployment |
| **Environment Configuration** | `.env` file + Pydantic `BaseSettings` |
| **Testing** | Unit and integration tests using `pytest` |
| **Versioned API** | `/api/v1/...` structure for scalability and future versions |

---

## 4. Roles & Access Logic

| Role | Capabilities |
|------|--------------|
| **Super Admin** | Full access to all teams and entities, can manage users and roles |
| **Supervisor** | View/edit data across all teams, limited admin functions |
| **Team Admin** | CRUD within their team, approve/reject member submissions |
| **Team Member** | Create/update requests that require admin approval |

---

## 5. Stretch / Future Features

- Multi-tenancy for vendors/shops  
- Product image upload (S3 or local storage)  
- Advanced search (Elasticsearch)  
- GraphQL API support  

---

✅ **Purpose:** This document serves as a **reference for project planning, development, and future enhancements**. It outlines all entities, features, and system-level components to ensure the CatalogFlow backend is robust and scalable.

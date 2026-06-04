# PaperRepo — Database Schema

PostgreSQL (Supabase). All ORM models live in [core/client_model_app/models.py](../backend/core/client_model_app/models.py). App `models.py` files hold service classes only.

UUID primary keys everywhere. Soft-delete via `*_deleted_at` (NULL = live). Timestamps auto-managed (`auto_now_add` / `auto_now`).

## Enums

| Enum | Values |
|------|--------|
| `ExamType` | `CAT I`, `CAT II`, `FAT` |
| `Semester` | `FALL SEM`, `WIN SEM`, `Others` |

## Tables

### `user_info`

| Column | Type | Constraints |
|--------|------|-------------|
| user_id | uuid | PK, default uuid4 |
| user_email | varchar(255) | unique, not null |
| user_name | varchar(255) | not null |
| user_password_hash | varchar(255) | not null |
| user_is_active | bool | default true |
| user_last_login_at | timestamptz | null |
| user_created_at | timestamptz | auto add |
| user_updated_at | timestamptz | auto update |
| user_deleted_at | timestamptz | null (soft delete) |

### `subjects`

| Column | Type | Constraints |
|--------|------|-------------|
| subject_id | uuid | PK, default uuid4 |
| subject_code | varchar(20) | unique, not null |
| subject_name | varchar(200) | not null |
| subject_created_at | timestamptz | auto add |

### `faculties`

| Column | Type | Constraints |
|--------|------|-------------|
| faculty_id | uuid | PK, default uuid4 |
| faculty_name | varchar(100) | unique, not null |
| faculty_created_at | timestamptz | auto add |

### `question_papers`

| Column | Type | Constraints |
|--------|------|-------------|
| question_paper_id | uuid | PK, default uuid4 |
| user_id | uuid | FK → user_info(user_id), **ON DELETE CASCADE** |
| subject_id | uuid | FK → subjects(subject_id), **ON DELETE PROTECT** |
| question_paper_title | varchar(100) | not null |
| question_paper_exam_slot | varchar(10) | not null |
| question_paper_exam_type | varchar(20) | ExamType |
| question_paper_semester | varchar(20) | Semester |
| question_paper_year | int | default 2017 |
| question_paper_file_path | varchar(1024) | storage object path |
| question_paper_created_at | timestamptz | auto add |
| question_paper_updated_at | timestamptz | auto update |
| question_paper_deleted_at | timestamptz | null (soft delete) |

### `important_topics`

| Column | Type | Constraints |
|--------|------|-------------|
| important_topic_id | uuid | PK, default uuid4 |
| user_id | uuid | FK → user_info(user_id), **ON DELETE CASCADE** |
| subject_id | uuid | FK → subjects(subject_id), **ON DELETE PROTECT** |
| faculty_id | uuid | FK → faculties(faculty_id), **ON DELETE SET NULL**, nullable |
| important_topic_title | varchar(100) | not null |
| important_topic_exam_type | varchar(20) | ExamType |
| important_topic_file_path | varchar(1024) | storage object path |
| important_topic_created_at | timestamptz | auto add |
| important_topic_updated_at | timestamptz | auto update |
| important_topic_deleted_at | timestamptz | null (soft delete) |

### `materials`

| Column | Type | Constraints |
|--------|------|-------------|
| material_id | uuid | PK, default uuid4 |
| user_id | uuid | FK → user_info(user_id), **ON DELETE CASCADE** |
| subject_id | uuid | FK → subjects(subject_id), **ON DELETE PROTECT** |
| faculty_id | uuid | FK → faculties(faculty_id), **ON DELETE SET NULL**, nullable |
| material_title | varchar(100) | not null |
| material_topic_type | varchar(50) | not null |
| material_file_path | varchar(1024) | storage object path |
| material_created_at | timestamptz | auto add |
| material_updated_at | timestamptz | auto update |
| material_deleted_at | timestamptz | null (soft delete) |

## Relationships

```
user_info  1───∞  question_papers   (CASCADE)
user_info  1───∞  important_topics  (CASCADE)
user_info  1───∞  materials         (CASCADE)

subjects   1───∞  question_papers   (PROTECT)
subjects   1───∞  important_topics  (PROTECT)
subjects   1───∞  materials         (PROTECT)

faculties  1───∞  important_topics  (SET NULL)
faculties  1───∞  materials         (SET NULL)
```

## Notes

- **File bytes** are NOT in the DB. The `*_file_path` column stores the object path in the Supabase Storage bucket `papers`; signed URLs are minted on demand via the `/file/` endpoints.
- **PROTECT** on subject FK: a subject cannot be deleted while resources reference it.
- **CASCADE** on user FK: deleting a user removes their resource rows.
- **SET NULL** on faculty FK: deleting a faculty leaves the resource, faculty becomes NULL.

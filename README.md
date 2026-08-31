<div align="center">

# 🏫 Academy — Django School Management App

**A course-management web app for a learning centre: catalogue, teachers, role-based CRUD and a clean Bootstrap UI**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django_5-092E20?style=flat-square&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Jazzmin-0C4B33?style=flat-square&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" />
</p>

<p>
  <a href="https://github.com/Raximboy7/django_dars_School_app/stargazers"><img src="https://img.shields.io/github/stars/Raximboy7/django_dars_School_app?style=flat-square&color=8B5CF6&labelColor=0D1117" alt="stars" /></a>
  <a href="https://github.com/Raximboy7/django_dars_School_app/commits"><img src="https://img.shields.io/github/last-commit/Raximboy7/django_dars_School_app?style=flat-square&color=8B5CF6&labelColor=0D1117" alt="last commit" /></a>
  <a href="https://github.com/Raximboy7/django_dars_School_app/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-8B5CF6?style=flat-square&labelColor=0D1117" alt="license" /></a>
</p>

</div>

---

## 📖 Overview

A production-shaped Django application for running a small education centre. Visitors browse the
course catalogue; staff sign in and manage courses through class-based CRUD views guarded by
groups and permissions.

The code deliberately uses the *idiomatic* Django toolkit rather than shortcuts: an abstract
`TimeStampedModel`, automatic unique slugs, model-level `clean()` validation, `select_related()`
on list queries, `LoginRequiredMixin` + `UserPassesTestMixin` for access control, and a management
command that bootstraps the permission groups.

---

## ✨ Features

| | Feature | Detail |
|:-:|---|---|
| 🎓 | **Course catalogue** | Level, duration, price, group size, online/offline flag |
| 🗂 | **Categories** | Auto-generated unique slugs, protected against deletion while in use |
| 👨‍🏫 | **Teachers** | Bio, photo, Telegram / Instagram links, active flag |
| 🔎 | **Search & pagination** | 9 courses per page, filtered to active courses only |
| 🔐 | **Role-based access** | `boss`, `manager`, `teacher` groups via `StaffRequiredMixin` |
| ✏️ | **Full CRUD** | Create / update / delete courses from the front end, with success messages |
| ✅ | **Model validation** | Negative price, empty group, >60 students online — all rejected |
| 🛡 | **Hardened settings** | `X_FRAME_OPTIONS=DENY`, CSRF cookie HTTP-only, XSS filter, 1-week sessions |
| 🎨 | **Templates** | `base.html` + reusable `includes/` partials, custom `403.html` |

---

## 🧩 Data model

```
Category ──1──────∞── Course ──∞──────1── Teacher
  name                  title              first_name / last_name
  slug (auto)           slug (auto)        bio, photo
                        level              telegram, instagram
                        duration_months    is_active
                        price
                        max_students
                        is_online
                        is_active
```

Both `Category` and `Course` inherit `TimeStampedModel` → every row carries `created_at` / `updated_at`.
A `UniqueConstraint` guarantees one course title per category.

---

## 🚀 Getting Started

```bash
# 1 — clone
git clone https://github.com/Raximboy7/django_dars_School_app.git
cd django_dars_School_app

# 2 — virtual environment
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

# 3 — dependencies
pip install -r requirements.txt

# 4 — environment
cp .env.example .env               # then edit .env

# 5 — database + roles
python manage.py migrate
python manage.py createsuperuser
python manage.py bootstrap_roles   # creates the manager / teacher groups

# 6 — run
python manage.py runserver
```

| URL | Page |
|---|---|
| <http://127.0.0.1:8000/> | Home |
| <http://127.0.0.1:8000/course/> | Course list |
| <http://127.0.0.1:8000/course/add/> | Create course (staff only) |
| <http://127.0.0.1:8000/login/> | Sign in |
| <http://127.0.0.1:8000/admin/> | Admin panel |

---

## 🔧 Configuration

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key — **never commit the real value** | — |
| `DEBUG` | `True` in development only | `False` |
| `ALLOWED_HOSTS` | Comma-separated host list | `127.0.0.1,localhost` |

---

## 📁 Project Structure

```
django_dars_School_app/
├── academy/                 # project settings, root urls
│   ├── settings.py
│   └── urls.py
├── school/                  # main application
│   ├── models.py            # Category, Teacher, Course, TimeStampedModel
│   ├── views.py             # home, about + Course CRUD class-based views
│   ├── forms.py             # CourseForm
│   ├── mixins.py            # StaffRequiredMixin (role check)
│   ├── signals.py           # slug auto-fill
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── bootstrap_roles.py   # creates groups & permissions
├── templates/
│   ├── base.html
│   ├── home.html  about.html  403.html
│   ├── courses/             # list / detail / form / confirm_delete
│   ├── includes/            # _navbar _footer _messages _pagination
│   └── registration/login.html
├── static/                  # css, js, img
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 👥 Roles & permissions

`bootstrap_roles` creates two groups:

| Group | Permissions |
|---|---|
| `manager` | add / change / delete / view course |
| `teacher` | view course |

`StaffRequiredMixin` additionally lets any `is_staff` or `is_superuser` account through, and
checks a `position` attribute against `['boss', 'manager']` for custom user models.

---

## 🗓 Roadmap

- [ ] Student enrolment model + capacity check against `max_students`
- [ ] Group / schedule model (weekdays, time slots, classrooms)
- [ ] Payments and invoice tracking
- [ ] Teacher dashboard with their own courses
- [ ] REST API layer with Django REST Framework
- [ ] Tests for the CRUD views and the permission matrix
- [ ] Dockerfile + `docker-compose.yml` with PostgreSQL

---

<details>
<summary><b>🇺🇿 &nbsp;O'zbekcha tavsif</b></summary>

<br/>

## 📖 Loyiha haqida

O'quv markazini boshqarish uchun Django ilovasi. Mehmonlar kurslar katalogini ko'radi;
xodimlar tizimga kirib, guruh va ruxsatlar bilan himoyalangan class-based view'lar orqali
kurslarni boshqaradi.

Kod ataylab **Django'ning o'z uslubida** yozilgan: abstrakt `TimeStampedModel`, avtomatik unikal
slug, model darajasidagi `clean()` validatsiya, ro'yxatlarda `select_related()`,
`LoginRequiredMixin` + `UserPassesTestMixin`, va ruxsat guruhlarini yaratuvchi management buyrug'i.

## ✨ Imkoniyatlar

- 🎓 Kurslar katalogi — daraja, davomiylik, narx, guruh hajmi, onlayn/oflayn
- 🗂 Kategoriyalar — slug avtomatik yaratiladi
- 👨‍🏫 O'qituvchilar — bio, rasm, Telegram/Instagram havolalari
- 🔎 Qidiruv va sahifalash (har sahifada 9 ta kurs)
- 🔐 Rollar: `boss`, `manager`, `teacher`
- ✏️ To'liq CRUD + muvaffaqiyat xabarlari
- ✅ Validatsiya: manfiy narx, bo'sh guruh, onlayn kursda 60 dan ortiq o'quvchi — rad etiladi
- 🛡 Xavfsizlik sozlamalari: `X_FRAME_OPTIONS=DENY`, CSRF cookie HTTP-only

## 🚀 Ishga tushirish

```bash
git clone https://github.com/Raximboy7/django_dars_School_app.git
cd django_dars_School_app

python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py bootstrap_roles
python manage.py runserver
```

## 🐛 Tuzatilgan xatolar

| Muammo | Yechim |
|---|---|
| `school/managament/` papkasi noto'g'ri yozilgan edi | `school/management/` ga o'zgartirildi — endi `bootstrap_roles` buyrug'i ishlaydi |
| `management/` va `commands/` da `__init__.py` yo'q edi | Qo'shildi |
| `requirementes.txt` — nomi xato, UTF-16 kodlash | `requirements.txt`, UTF-8 |
| `SECRET_KEY` kod ichida ochiq turgan | `.env` ga ko'chirildi |
| `DEBUG = True` | `.env` orqali boshqariladi |

</details>

---

## 🤝 Contributing

Issue va Pull Request'lar ochiq.

## 📄 License

MIT — batafsil [`LICENSE`](LICENSE) faylida.

## 👤 Author

**Raximboy Ibrohimov** — Backend &amp; Mobile Developer, Tashkent 🇺🇿

[![Portfolio](https://img.shields.io/badge/Portfolio-8B5CF6?style=flat-square&logo=googlechrome&logoColor=white)](https://ibrohimov-dev.uz)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raximboy-ibroximov-a75855268/)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/Raximboy7)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:raximboy4200@gmail.com)

<div align="center"><sub>⭐ Foydali bo'lsa, yulduzcha qoldiring!</sub></div>

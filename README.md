# full_stack
lesson
# Mountain Equipment Rental API 🏔️

## 🎯 Описание
Веб-приложение для каталога горного снаряжения с поддержкой авторизации и AI-рекомендаций (в будущем).  
Проект создан в рамках курса **Fullstack Development**.

---

## ⚙️ Технологии
- Python 3 / Django / Django REST Framework  
- JWT (SimpleJWT)  
- SQLite  
- Django Filters

---

## 🧩 Модель данных
**Equipment**
| Поле | Тип | Описание |
|------|------|----------|
| name | CharField | Название снаряжения |
| price_per_day | DecimalField | Цена за день |
| available_from | DateField | Дата доступности |
| description | TextField | Описание |
| rating | FloatField | Оценка |
| tags | CharField | Теги |
| file | FileField | Документ или изображение |
| image | ImageField | Фото |
| author | ForeignKey(User) | Автор записи |

---

## 🔐 API эндпоинты

| Метод | Endpoint | Описание |
|--------|-----------|----------|
| `POST` | `/api/register/` | Регистрация пользователя |
| `POST` | `/api/login/` | Авторизация (JWT) |
| `GET` | `/api/me/` | Информация о текущем пользователе |
| `GET` | `/api/items/` | Список оборудования |
| `GET` | `/api/items/{id}/` | Детали оборудования |
| `POST` | `/api/items/` | Добавить оборудование (только авторизованный) |
| `PUT` | `/api/items/{id}/` | Редактировать (только свои) |
| `DELETE` | `/api/items/{id}/` | Удалить (только свои) |

---

## 🔍 Поиск и фильтрация
- Поиск по: `name`, `description`, `tags`
- Фильтр по рейтингу:

**Yermekov Yerassyl**  
IITU — 4 курс  
Тема диплома: *“Разработка системы аренды горного снаряжения с поддержкой AI-рекомендаций”*

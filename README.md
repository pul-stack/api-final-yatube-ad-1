### API для Yatube

**Описание**

Проект предоставляет REST API для социальной сети Yatube.
API позволяет:
- читать и создавать публикации;
- комментировать публикации;
- просматривать сообщества;
- подписываться на авторов;
- получать JWT-токены для аутентификации.

Документация API доступна в формате Redoc по адресу `http://127.0.0.1:8000/redoc/`.

**Технологии**
- Python
- Django
- Django REST Framework
- JWT (SimpleJWT)

### Установка и запуск (Windows / PowerShell)

Перейдите в директорию с `manage.py`:

```powershell
cd "D:\Yandex_course\api-final-yatube-ad\yatube_api"
```

Создайте и активируйте виртуальное окружение:

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
```

Установите зависимости:

```powershell
pip install -r requirements.txt
```

Выполните миграции и запустите проект:

```powershell
python manage.py migrate
python manage.py runserver
```

### Аутентификация

API использует JWT-токены.

- **Получить токен**: `POST /api/v1/jwt/create/`
- **Обновить токен**: `POST /api/v1/jwt/refresh/`
- **Проверить токен**: `POST /api/v1/jwt/verify/`

Передавайте access-токен в заголовке:

```http
Authorization: Bearer <access_token>
```

### Примеры запросов

**Получение JWT-токена**

```http
POST /api/v1/jwt/create/
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

**Список публикаций (пагинация limit/offset)**

```http
GET /api/v1/posts/?limit=10&offset=0
```

**Создание публикации (только для аутентифицированных)**

```http
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Мой первый пост",
  "group": 1
}
```

**Список комментариев к публикации**

```http
GET /api/v1/posts/1/comments/
```

**Добавить комментарий (только для аутентифицированных)**

```http
POST /api/v1/posts/1/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Отличный пост!"
}
```

**Подписка на автора (только для аутентифицированных)**

```http
POST /api/v1/follow/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "following": "author_username"
}
```

**Поиск по подпискам**

```http
GET /api/v1/follow/?search=author
Authorization: Bearer <access_token>
```

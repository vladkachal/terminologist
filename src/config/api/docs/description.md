## Обзор

Описание отдельных эндпоинтов с подробной информацией об их использовании
и ожидаемых форматах запросов и ответов.

## Ошибки

<details>
<summary><small>
    Список ответов с ошибками, которые могут возникнуть при выполнении любой операции.
</small></summary>

### 405 Method Not Allowed

Возвращается, когда эндпоинт вызывается с неподдерживаемым `HTTP-методом`.
Например, если для обновления пользователя требуется запрос `POST`,
а отправляется `PATCH`, возвращается следующая ошибка:

```json
{
    "type": "client_error",
    "errors": [
        {
            "code": "method_not_allowed",
            "detail": "Method `patch` not allowed.",
            "attr": null
        }
    ]
}
```

### 406 Not Acceptable

Возвращается, если передан заголовок `Accept`, содержащий значение,
отличное от `application/json`. Ответ выглядит следующим образом:

```json
{
    "type": "client_error",
    "errors": [
        {
            "code": "not_acceptable",
            "detail": "Could not satisfy the request Accept header.",
            "attr": null
        }
    ]
}
```

### 415 Unsupported Media Type

Возвращается, когда тип содержимого запроса не является `json`.

```json
{
    "type": "client_error",
    "errors": [
        {
            "code": "not_acceptable",
            "detail": "Unsupported media type `application/xml` in request.",
            "attr": null
        }
    ]
}
```

### 500 Internal Server Error

Возвращается, когда на сервере API возникает непредвиденная ошибка.

```json
{
    "type": "server_error",
    "errors": [
        {
            "code": "error",
            "detail": "A server error occurred.",
            "attr": null
        }
    ]
}
```

### 503 Service Temporarily Unavailable

Возвращается, когда сервер API не готов обрабатывать запросы.

```json
{
    "type": "server_error",
    "errors": [
        {
            "code": "service_unavailable",
            "detail": "Service temporarily unavailable, try again later.",
            "attr": null
        }
    ]
}
```

</details>

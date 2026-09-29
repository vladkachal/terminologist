## Overview

Refer to the individual endpoints for more details on usage and expected
request/response formats.

## Errors

<details>
<summary><small>A list of error responses that may appear in every operation.</small></summary>

### 405 Method Not Allowed

This is returned when an endpoint is called with an unexpected http method.
For example, if updating a user requires a `POST` request and a `PATCH` is issued
instead, this error is returned. Here's how it looks like:

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

This is returned if the `Accept` header is submitted and contains a value other
than `application/json`. Here's how the response would look:

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

This is returned when the request content type is not `json`.
Here's how the response would look:

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

This is returned when the API server encounters an unexpected error.
Here's how the response would look:

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

This is returned when the API server is not ready to handle the request.
Here's how the response would look:

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

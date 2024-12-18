
# API Documentation

## Media Endpoint

### 1. Media to Order
**Endpoint**: `GET /media/mediaToOrder`

**Description**: Retrieves the count of media items ready to be ordered.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Response**:
- **200 OK**:
    ```json
    {
      "media_count": 5
    }
    ```

---

### 2. Get Branch Media
**Endpoint**: `POST /media/getBranchMedia`

**Description**: Fetches media details for a specific branch.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "branch_id": "12345"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "media_count": [
        {"media_id": "1", "available_copies": 5},
        {"media_id": "2", "available_copies": 3}
      ]
    }
    ```
- **404 Not Found**:
    ```json
    {
      "error": "Branch not found"
    }
    ```

---

### 3. Borrow Media
**Endpoint**: `POST /media/borrow`

**Description**: Allows a user to borrow a media item.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "user_id": "123",
  "media_id": "456",
  "delivery_choice": "home_delivery",
  "borrow_until": "2024-12-31"
}
```

**Response**: Implementation-specific.

---

### 4. Procure Media
**Endpoint**: `POST /media/procure`

**Description**: Procures media for a specific branch.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "quantity_to_order": 10,
  "branch_to_deliver_to": "branch_id",
  "media_to_order": "media_id",
  "delivery_date": "2024-12-31"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Successfully borrowed media: 673c85daede0ec4def1bca79"
    }
    ```

---

### 5. Reserve Media
**Endpoint**: `POST /media/reserve`

**Description**: Reserves a media item for a user.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "user_id": "123",
  "media_id": "456"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Successfully borrowed media: 456"
    }
    ```

---

### 6. Get All Media
**Endpoint**: `GET /media/all_media`

**Description**: Fetches all available media.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    [
      {"media_id": "1", "title": "Media Title 1"},
      {"media_id": "2", "title": "Media Title 2"}
    ]
    ```

---

### 7. Get All Branches
**Endpoint**: `GET /media/all_branches`

**Description**: Retrieves a list of all branches.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    [
      {"branch_id": "1", "name": "Branch 1"},
      {"branch_id": "2", "name": "Branch 2"}
    ]
    ```

---

### 8. Get Media by Branch
**Endpoint**: `GET /media/all_branch_media`

**Description**: Retrieves media grouped by branches.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    {
      "branch": {
        "name": "Central Branch"
      },
      "media": [
        {
          "available_copies": 154,
          "media_id": "673c85daede0ec4def1bca6f",
          "total_copies": 500
        },
        {
          "available_copies": 0,
          "media_id": "673c85daede0ec4def1bca70",
          "total_copies": 6
        }
      ]
    }
    ```

---

### 9. Return Staged Media
**Endpoint**: `POST /media/mediareturned`

**Description**: Returns a staged media item to a branch.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "branch_id": "123",
  "media_id": "456"
}
```

**Response**:
- **200 OK**

---

### 10. Generate Report
**Endpoint**: `POST /media/report`

**Description**: Generates a report in the specified format.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "report": "monthly_summary",
  "export": "pdf"
}
```

**Response**:
- **200 OK**

---

### 11. Track Order
**Endpoint**: `GET /media/track_order`

**Description**: Tracks the status of an order using its purchase order (PO).

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "PO": "PO12345"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "status": "In Transit"
    }
    ```

---

### 12. Edit Order Status
**Endpoint**: `POST /media/edit_order`

**Description**: Edits the status of an order.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "PO": "PO12345",
  "new_status": "Delivered"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Order status updated successfully."
    }
    ```

---

## Subscription Endpoint

### 1. Manage Subscription
**Endpoint**: `POST /subscription/manage`

**Description**: Edits a user's subscription.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "user_id": "123",
  "new_subscription": "premium"
}
```

**Response**: Implementation-specific.

---

### 2. Edit Subscription
**Endpoint**: `POST /subscription/edit_subscription`

**Description**: Updates an existing subscription.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "subscription": "basic",
  "new_subscription": "premium"
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Subscription updated successfully."
    }
    ```

---

### 3. Get All Subscriptions
**Endpoint**: `GET /subscription/get_all`

**Description**: Retrieves all subscriptions.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    [
      {
        "id": "subscription_id_1",
        "subscription_name": "Basic Plan",
        "subscription_price_per_month": 11.99
      },
      {
        "id": "subscription_id_2",
        "subscription_name": "Standard Plan",
        "subscription_price_per_month": 29.99
      },
      {
        "id": "subscription_id_3",
        "subscription_name": "Premium Plan",
        "subscription_price_per_month": 39.99
      }
    ]
    ```

---

### 4. Update Subscription Price
**Endpoint**: `POST /subscription/update`

**Description**: Updates the price of a subscription.

**Headers**:
- `Authorization`: Bearer [token] (required)
- `Content-Type`: application/json

**Request Body**:
```json
{
  "subscription_id": "1",
  "new_price": 15.99
}
```

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Subscription price updated successfully."
    }
    ```

---

## Users Endpoint

### 1. Get User
**Endpoint**: `GET /users/<user_id>`

**Description**: Retrieves details for a specific user.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    {
      "email": "monica40@example.org",
      "name": "Dana Williams"
    }
    ```

---

### 2. Get All Users
**Endpoint**: `GET /users/all_users`

**Description**: Fetches all users.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    [
      {
        "email": "monica40@example.org",
        "name": "Dana Williams"
      }
    ]
    ```

---

### 3. Ping
**Endpoint**: `GET /users/ping`

**Description**: Pings the server to check if system is active.

**Headers**:
- `Authorization`: Bearer [token] (required)

**Response**:
- **200 OK**:
    ```json
    {
      "message": "Ping successful"
    }
    ```

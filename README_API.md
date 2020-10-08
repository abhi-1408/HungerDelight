## HUNGER_DELIGHT_APP API

### GET `/app`

##### REQUEST

```json
{
	"merchant": "localhost:port/app/merchant/",
	"store": "localhost:port/app/store/",
	"item": "localhost:port/app/item/",
	"order": "localhost:port/app/order/"
}
```

---

## MERCHANT

#### GET `app/merchant`

##### RESPONSE

```json
[
	{
		"id": 1,
		"name": "Nathu",
		"email": "nathu@yahoo.com",
		"mobile": "9988339423"
	},
	{
		"id": 2,
		"name": "BigBazaar",
		"email": "bb@gmail.com",
		"mobile": "9955849953"
	}
]
```

---

#### POST `app/merchant/`

##### REQUEST

```json
{
	"name": "Nathu's",
	"email": "nathu@yahoo.com",
	"mobile": "9988339423"
}
```

##### RESPONSE

```json
{
	"id": 1,
	"name": "Nathu",
	"email": "nathu@yahoo.com",
	"mobile": "9988339423"
}
```

---

#### GET `app/merchant/:id`

##### RESPONSE

```json
{
	"id": 1,
	"name": "Nathu",
	"email": "nathu@yahoo.com",
	"mobile": "9988339423"
}
```

---

#### PUT `app/merchant/:id`

##### REQUEST

```json
{
	"name": "Nathu's",
	"email": "nathu@yahoo.com",
	"mobile": "9988339423"
}
```

##### RESPONSE

```json
{
	"id": 1,
	"name": "Nathu's",
	"email": "nathu@yahoo.com",
	"mobile": "9988339423"
}
```

---

#### DELETE `app/merchant/:id`

##### RESPONSE

```json
{}
```

---

#### GET `app/merchant/:id/item`

##### RESPONSE

```json
{
	"merchant": {
		"id": 2,
		"name": "BigBazaar",
		"email": "bb@gmail.com",
		"mobile": "9955849953"
	},
	"items": [
		{
			"id": 2,
			"name": "Milk",
			"price": "65.000000",
			"created_at": "2020-09-30T11:46:19.691104Z",
			"description": "Fresh Cow Milk",
			"merchant": 2
		},
		{
			"id": 3,
			"name": "Bread",
			"price": "45.000000",
			"created_at": "2020-09-30T11:46:30.298726Z",
			"description": "Brown Bread",
			"merchant": 2
		}
	]
}
```

---

#### GET `app/merchant/:id/order`

##### RESPONSE

```json
{
	"merchant": {
		"id": 2,
		"name": "BigBazaar",
		"email": "bb@gmail.com",
		"mobile": "9955849953"
	},
	"orders": [
		{
			"id": 1,
			"timestamp": "2020-09-30T17:19:00Z",
			"status": "SUCCESS",
			"payment_mode": "CARD",
			"store": 1,
			"merchant": 2,
			"items": [2, 3]
		},
		{
			"id": 11,
			"timestamp": "2020-10-01T22:10:00Z",
			"status": "SUCCESS",
			"payment_mode": "CARD",
			"store": 3,
			"merchant": 2,
			"items": [3]
		}
	]
}
```

---

#### GET `app/merchant/:id/store`

##### RESPONSE

```json
{
	"merchant": {
		"id": 2,
		"name": "BigBazaar",
		"email": "bb@gmail.com",
		"mobile": "9955849953"
	},
	"stores": [
		{
			"id": 1,
			"name": "Delhi BB",
			"address": "Patparganj, New Delhi",
			"lat": "45.560000000000000",
			"lng": "98.440000000000000",
			"operational": true,
			"merchant": 2,
			"items": [2, 3]
		},
		{
			"id": 3,
			"name": "Mumbai BB",
			"address": "Worli, Mumbai",
			"lat": "65.450000000000000",
			"lng": "34.550000000000000",
			"operational": false,
			"merchant": 2,
			"items": [2, 3]
		}
	]
}
```

---

## STORE

#### GET `app/store/`

##### RESPONSE

```json
[
	{
		"id": 1,
		"name": "Delhi BB",
		"address": "Patparganj, New Delhi",
		"lat": "45.560000000000000",
		"lng": "98.440000000000000",
		"operational": true,
		"merchant": 2,
		"items": [2, 3]
	}
]
```

---

#### GET `app/store/`

##### RESPONSE

```json
{
	"id": 1,
	"name": "Delhi BB",
	"address": "Patparganj, New Delhi",
	"lat": "45.560000000000000",
	"lng": "98.440000000000000",
	"operational": true,
	"merchant": 2,
	"items": [2, 3]
}
```

---

#### PUT `app/store/:id`

##### REQUEST

```json
{
	"name": "Delhi BB",
	"address": "Patparganj,Delhi",
	"lat": "45.560000000000000",
	"lng": "90.440000000000000",
	"operational": true,
	"merchant": 2,
	"items": [2, 3]
}
```

##### RESPONSE

```json
{
	"id": 1,
	"name": "Delhi BB",
	"address": "Patparganj, Delhi",
	"lat": "45.560000000000000",
	"lng": "90.440000000000000",
	"operational": true,
	"merchant": 2,
	"items": [2, 3]
}
```

---

#### GET `app/store/:id/item`

##### RESPONSE

```json
{
	"store": {
		"id": 1,
		"name": "Delhi BB",
		"address": "Patparganj, New Delhi",
		"lat": "45.560000000000000",
		"lng": "90.440000000000000",
		"operational": false,
		"merchant": 2,
		"items": [2, 3]
	},
	"items": [
		{
			"id": 2,
			"name": "Milk",
			"price": "65.000000",
			"created_at": "2020-09-30T11:46:19.691104Z",
			"description": "Fresh Cow Milk",
			"merchant": 2
		},
		{
			"id": 3,
			"name": "Bread",
			"price": "45.000000",
			"created_at": "2020-09-30T11:46:30.298726Z",
			"description": "Brown Bread",
			"merchant": 2
		}
	]
}
```

---

#### GET `app/store/:id/order`

##### RESPONSE

```json
{
	"store": {
		"id": 1,
		"name": "Delhi BB",
		"address": "Patparganj, New Delhi",
		"lat": "45.560000000000000",
		"lng": "90.440000000000000",
		"operational": false,
		"merchant": 2,
		"items": [2, 3]
	},
	"orders": [
		{
			"id": 1,
			"timestamp": "2020-09-30T17:19:00Z",
			"status": "SUCCESS",
			"payment_mode": "CARD",
			"store": 1,
			"merchant": 2,
			"items": [2, 3]
		}
	]
}
```

---

#### DELETE `app/store/:id`

##### RESPONSE

```json



```

---

#### POST `app/store/`

##### REQUEST

```json
{
	"name": "Mumbai BB",
	"address": "Worli, Mumbai",
	"lat": "65.450000000000000",
	"lng": "34.550000000000000",
	"operational": false,
	"merchant": 2,
	"items": [2, 3]
}
```

##### RESPONSE

```json
{
	"id": 3,
	"name": "Mumbai BB",
	"address": "Worli, Mumbai",
	"lat": "65.450000000000000",
	"lng": "34.550000000000000",
	"operational": false,
	"merchant": 2,
	"items": [2, 3]
}
```

---

## ITEM

#### GET `app/item/`

##### RESPONSE

```json
[
	{
		"id": 2,
		"name": "Milk",
		"price": "65.000000",
		"created_at": "2020-09-30T11:46:19.691104Z",
		"description": "Fresh Cow Milk",
		"merchant": 2
	},
	{
		"id": 3,
		"name": "Bread",
		"price": "45.000000",
		"created_at": "2020-09-30T11:46:30.298726Z",
		"description": "Brown Bread",
		"merchant": 2
	}
]
```

---

#### GET `app/item/:id`

##### RESPONSE

```json
{
	"id": 2,
	"name": "Milk",
	"price": "65.000000",
	"created_at": "2020-09-30T11:46:19.691104Z",
	"description": "Fresh Cow Milk",
	"merchant": 2
}
```

---

#### PUT `app/item/:id`

##### REQUEST

```json
{
	"id": 2,
	"name": "Milk",
	"price": "45.000000",
	"created_at": "2020-09-30T11:46:19.691104Z",
	"description": "Fresh Cow Milk",
	"merchant": 2
}
```

##### RESPONSE

```json
{
	"id": 2,
	"name": "Milk",
	"price": "45.000000",
	"created_at": "2020-09-30T11:46:19.691104Z",
	"description": "Fresh Cow Milk",
	"merchant": 2
}
```

---

#### DELETE `app/item/:id`

##### RESPONSE

```json


```

---

#### POST `app/item/`

##### REQUEST

```json
{
	"name": "Milk",
	"price": "65.000000",
	"created_at": "2020-09-30T11:46:19.691104Z",
	"description": "Fresh Cow Milk",
	"merchant": 2
}
```

##### RESPONSE

```json
{
	"id": 2,
	"name": "Milk",
	"price": "65.000000",
	"created_at": "2020-09-30T11:46:19.691104Z",
	"description": "Fresh Cow Milk",
	"merchant": 2
}
```

---

## ORDER

#### GET `app/order/`

##### RESPONSE

```json
[
	{
		"id": 1,
		"total_amount": "400.000000",
		"total_items": 2,
		"timestamp": "2020-09-30T17:19:00Z",
		"status": "SUCCESS",
		"payment_mode": "CARD",
		"store": 1,
		"merchant": 2,
		"items": [2, 3]
	},
	{
		"id": 11,
		"total_amount": "45.000000",
		"total_items": 1,
		"timestamp": "2020-10-01T22:10:00Z",
		"status": "SUCCESS",
		"payment_mode": "CARD",
		"store": 3,
		"merchant": 2,
		"items": [3]
	}
]
```

---

#### GET `app/order/:id`

##### RESPONSE

```json
{
	"id": 1,
	"timestamp": "2020-09-30T17:19:00Z",
	"status": "SUCCESS",
	"payment_mode": "CARD",
	"store": 1,
	"merchant": 2,
	"items": [2, 3]
}
```

---

#### POST `app/order/`

##### REQUEST

```json
{
	"timestamp": "2020-09-30T17:19:00Z",
	"status": "SUCCESS",
	"payment_mode": "CARD",
	"store": 1,
	"merchant": 2,
	"items": [2, 3]
}
```

##### RESPONSE

```json
{
	"id": 1,
	"timestamp": "2020-09-30T17:19:00Z",
	"status": "SUCCESS",
	"payment_mode": "CARD",
	"store": 1,
	"merchant": 2,
	"items": [2, 3]
}
```

# Shopping cart course

```bash
source venv/bin/activate
# terminal one
python main.py
# terminal two
flask run
# terminal three: Start client
curl -X POST http://localhost:5000/user@example.com
```

## Start client

```bash
curl -X POST http://localhost:5000/user@example.com
```

## Add item to cart

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/add_to_cart
```

## Remove item from cart

```bash
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/remove_from_cart
```

## Get cart details

```bash
curl -X GET http://localhost:5000/user@example.com/cart
```

## Checkout

```bash
curl -X POST http://localhost:5000/user@example.com/checkout
```

### Run together

```bash
curl -X POST http://localhost:5000/user@example.com
curl -X POST -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/user@example.com/add_to_cart
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/add_to_cart
curl -X GET http://localhost:5000/user@example.com/cart
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/remove_from_cart
curl -X GET http://localhost:5000/user@example.com/cart
curl -X POST http://localhost:5000/user@example.com/checkout
```

## Terminate Workflow

```bash
temporal workflow terminate --workflow-id shopping-cart-workflow-user@example.com
```

## Delete Schedule

```bash
temporal schedule delete --schedule-id workflow-schedule-id-user@example.com
```

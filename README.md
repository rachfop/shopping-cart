# Shopping cart course

```bash
source venv/bin/activate
# terminal one
python main.py
# terminal two
flask run
# terminal three
curl -X POST http://localhost:5000/
```

## Start Client

```bash
curl -X POST http://localhost:5000/
```

## Add item to cart

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/add_to_cart
```

## Remove item from cart

```bash
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/remove_from_cart
```

## Get cart details

```bash
curl -X GET http://localhost:5000/cart
```

## Checkout

```bash
curl -X POST http://localhost:5000/checkout
```

### Run together

```bash
curl -X POST http://localhost:5000/
curl -X POST -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/add_to_cart
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/add_to_cart
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/remove_from_cart
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/add_to_cart
curl -X GET http://localhost:5000/cart
curl -X POST http://localhost:5000/checkout
```

## Test deleting

```bash
curl -X POST http://localhost:5000/
curl -X POST -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/add_to_cart
curl -X POST -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/add_to_cart
curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/add_to_cart
curl -X GET http://localhost:5000/cart
curl -X DELETE -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/remove_from_cart
curl -X GET http://localhost:5000/cart
curl -X POST http://localhost:5000/checkout
```

## Terminate

```bash
temporal workflow terminate --workflow-id hello-signal-workflow-id
```

## Delete

```bash
temporal schedule delete --schedule-id workflow-schedule-id
```

## More info:

## Schedule a Workflow when you enter items in cart

## Add to dictionary to data structure

## When working with money use a money library

How do people handle money in python (What is round rule be when you multiply things)
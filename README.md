# Shopping cart course

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
curl -X POST http://localhost:5000/checkout
```

## Terminate

```bash
temporal workflow terminate --workflow-id hello-signal-workflow-id
```
import subprocess
from concurrent.futures import ThreadPoolExecutor


def run_curl_commands(email):
    # curl -X POST http://localhost:5000/user@example.com
    subprocess.run(["curl", "-X", "POST", f"http://localhost:5000/{email}"])

    # curl -X POST -H "Content-Type: application/json" -d '{"id": 0}' http://localhost:5000/user@example.com/add_to_cart
    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "-H",
            "Content-Type: application/json",
            "-d",
            '{"id": 0}',
            f"http://localhost:5000/{email}/add_to_cart",
        ]
    )

    # curl -X POST -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/add_to_cart
    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "-H",
            "Content-Type: application/json",
            "-d",
            '{"id": 1}',
            f"http://localhost:5000/{email}/add_to_cart",
        ]
    )

    # curl -X GET http://localhost:5000/user@example.com/cart
    subprocess.run(["curl", "-X", "GET", f"http://localhost:5000/{email}/cart"])

    # curl -X DELETE -H "Content-Type: application/json" -d '{"id": 1}' http://localhost:5000/user@example.com/remove_from_cart
    subprocess.run(
        [
            "curl",
            "-X",
            "DELETE",
            "-H",
            "Content-Type: application/json",
            "-d",
            '{"id": 1}',
            f"http://localhost:5000/{email}/remove_from_cart",
        ]
    )

    # curl -X GET http://localhost:5000/user@example.com/cart
    subprocess.run(["curl", "-X", "GET", f"http://localhost:5000/{email}/cart"])

    # curl -X POST http://localhost:5000/user@example.com/checkout
    subprocess.run(["curl", "-X", "POST", f"http://localhost:5000/{email}/checkout"])


with ThreadPoolExecutor(max_workers=110) as executor:
    for i in range(1000):
        email = i
        executor.submit(run_curl_commands, email)

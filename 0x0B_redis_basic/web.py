#!/usr/bin/env python3
""" Module for Implementing an expiring web cache and tracker """

from functools import wraps
import redis
import requests
from typing import Callable
import time  # Import the time module for tracking cache expiration

r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decorator for counting how many times a request has been made """

    @wraps(method)
    def wrapper(url):
        """ Wrapper for decorator functionality """
        # Get the current count
        count = int(r.get(f"count:{url}") or 0)

        # Check if the cache is present
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Refresh the cache and increment the count
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        r.incr(f"count:{url}")

        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    req = requests.get(url)
    return req.text


# Example usage
if __name__ == "__main__":
    url = "http://google.com"

    # Perform requests to trigger the decorator
    for _ in range(127):
        get_page(url)

    # Wait for the cache to expire
    time.sleep(11)

    # Check the count after cache expiration
    count_after_expiration = int(r.get(f"count:{url}") or 0)
    print(count_after_expiration)  # Expected output: 0

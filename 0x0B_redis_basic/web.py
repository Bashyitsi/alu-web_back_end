#!/usr/bin/env python3
'''
Web caching module using Redis

This module provides functions for caching web pages using Redis.
It includes a decorator `count_requests` to count requests and cache
responses for a specified duration.
'''


import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis connection
redis_connection = redis.Redis()


def count_requests(func: Callable) -> Callable:
    '''
    Decorator function to count requests and cache responses in Redis.

    - func (Callable): expects a URL string as argument.
    - Callable: caches responses and increments request count.
    '''

    @wraps(func)
    def wrapper(url):
        '''
        Wrapper function to count requests and cache responses.

        - url (str): URL of the web page to fetch and cache.
        - str: Cached HTML content of the web page.
        '''
        redis_connection.incr(f"request_count:{url}")
        cached_html = redis_connection.get(f"cached_content:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html_content = func(url)
        redis_connection.setex(f"cached_content:{url}", 10, html_content)
        return html_content

    return wrapper


@count_requests
def get_page(url: str) -> str:
    '''
    Function to fetch a web page using HTTP GET request.

    - url (str): URL of the web page to fetch.
    - str: HTML content of the fetched web page.
    '''
    response = requests.get(url)  # Perform HTTP GET request
    return response.text  # Return HTML content of the response
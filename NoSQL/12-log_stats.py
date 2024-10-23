#!/usr/bin/env python3
'''
Script to analyze Nginx logs stored in MongoDB
Displays statistics about HTTP methods and status checks
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''
    Prints formatted stats about Nginx request logs
    Args:
        nginx_collection: MongoDB collection object containing nginx logs
    '''
    # 1. Get total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f'{total_logs} logs')

    # 2. Print methods header
    print('Methods:')

    # 3. Count and display each HTTP method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    # 4. Count status checks (GET requests to /status)
    status_checks = nginx_collection.count_documents({
        'method': 'GET',
        'path': '/status'
    })
    print(f'{status_checks} status check')


def run():
    '''
    Main function to connect to MongoDB and run the analysis
    '''
    # Connect to MongoDB (default host and port)
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Access the logs database and nginx collection
    nginx_collection = client.logs.nginx
    
    # Print the statistics
    print_nginx_request_logs(nginx_collection)


if __name__ == '__main__':
    run()
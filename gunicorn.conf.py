import multiprocessing

bind = "0.0.0.0:8000"
timeout = 900
workers = multiprocessing.cpu_count() * 2 + 1
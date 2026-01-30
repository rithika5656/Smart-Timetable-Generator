"""
Gunicorn configuration file.
"""
workers = 4 # Number of worker processes
bind = "0.0.0.0:5000"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"

import psutil
import socket

"""
Classes for static hardware information for the monitor_stats project.
"""

class Hardware():

    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.ram = psutil.virtual_memory()
        self.hdd = psutil.disk_usage('../')
        self.hostname = socket.gethostname()

    def get_host(self):
        return(self.hostname)

    def get_cpu(self):
        return(self.cpu_count)

    def get_ram(self):
        return(self.ram.total >> 20)

    def get_hdd(self):
        return(self.hdd.total >> 30)

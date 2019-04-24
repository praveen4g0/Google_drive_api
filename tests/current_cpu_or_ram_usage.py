import psutil

# get CPU times
print(f'CPU Times {psutil.cpu_times()}')

for x in range(3):
    print()
    print(psutil.cpu_percent(interval=1))

for x in range(3):
    print()
    print(psutil.cpu_percent(interval=1, percpu=True))

for x in range(3):
    print()
    print(psutil.cpu_times_percent(interval=1, percpu=False))

# get cpu count
print(f'CPU count {psutil.cpu_count()}')

print(f'CPU count for logical as False {psutil.cpu_count(logical=False)}')

print(f'CPU stats : {psutil.cpu_stats()}')

print(psutil.cpu_freq())

# psutil.getloadavg()  # also on Windows (emulated)



#Memory Usage
print(f'Virtual memory: {psutil.virtual_memory()}')
print(f'Swap memory: {psutil.swap_memory()}')

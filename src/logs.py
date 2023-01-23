LOGS = []

def clean():
    LOGS.clear()

def get():
    return LOGS

def add(key, value):
    LOGS.append([key, value])
    if value == '':
        print(key)
    else:
        print(key.rjust(30) + '  :  ' + value)

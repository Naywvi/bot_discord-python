import json, datetime
def loadJson():
    with open('./src/logs/config.json', 'r') as f:
        data = json.load(f)
    return data

def logPath():
    now = datetime.datetime.now()
    path = "./src/logs/log_" + now.strftime("%d-%m-%Y") + ".json"

    with open('./src/logs/config.json', 'r') as f:
        data = json.load(f)

    data['path'] = path

    with open('./src/logs/config.json', 'w') as f:
        json.dump(data, f, indent=4)
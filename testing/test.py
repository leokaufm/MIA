import datetime
t = datetime.datetime.now()
output_file = "mia_" + t.strftime("%Y-%m-%d_%H-%M-%S") + ".h264"
print(output_file)
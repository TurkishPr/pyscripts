import subprocess

inference_input = r"C:\Users\Yoseop\Desktop\germany C:\Users\Yoseop\Desktop/test -1"

plate = subprocess.Popen("animal.exe", input = inference_input)
plate.wait()
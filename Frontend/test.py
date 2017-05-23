import requests
import json




r = requests.get("http://127.0.0.1:40440/students/tmurray5")
student_info = json.loads(r.content.decode("utf-8"))


print student_info


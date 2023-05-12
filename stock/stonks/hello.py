import nsepython
from nsepython import *
a = nse_eq("TATAPOWER")
b = json.dumps(a,indent=5)


print(b['info']['companName'])
# import nsepy
# api_request = nsepy.get_quote('TCS')
# print(api_request)
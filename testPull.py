import pandas as pd
import requests


semantleStarterRequest = 'https://semantle.com/model2/bread/'
urlRequest = semantleStarterRequest + 'plane'


initialJson = requests.get(urlRequest).json()

print(initialJson,'\n\n\n\n')

testRequest = pd.DataFrame(initialJson)

print(testRequest.tail())
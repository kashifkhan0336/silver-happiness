import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]
app = FastAPI();
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
cookies = {
    'ci_session': '3mbal40607m8ivf4dc9bip6prf89hf4k',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = (
    ('id', '210255'),
)

#response = requests.get('http://covid19.sindhmonitoringcell.com/dashboard/patientDetails', headers=headers, params=params, cookies=cookies, verify=False)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".

async def getResult(patient_id):
  response = requests.get(f'http://covid19.sindhmonitoringcell.com/dashboard/patientDetails?id={patient_id}', headers=headers, cookies=cookies, verify=False)
  soup = BeautifulSoup(response.content,'lxml')
  print(soup.select(".table.table-condensed.table-bordered > tbody >tr >td"))
  if(soup.select(".table.table-condensed.table-bordered > tbody >tr >td")):
    return {"data": "OK"}
  else:
    return {"data": "KO"}


async def followUp(patient_id):
  cookies = {
    'ci_session': '8bnn4ml3hk94ckosqjvjtt3gn1cn1loq',
  }
  headers = {
    'Connection': 'keep-alive','Cache-Control': 'max-age=0','Upgrade-Insecure-Requests': '1','Origin': 'http://covid19.sindhmonitoringcell.com','Content-Type': 'application/x-www-form-urlencoded','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Referer': 'http://covid19.sindhmonitoringcell.com/dashboard/patientDetails?id=212336','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }
  data = {
    'followupStatus': '1',
    'expiryDate': '0000-00-00',
    'remarks': '',
    'ci_csrf_token': '',
    'patientId': str(patient_id)
  }
  response = requests.post('http://covid19.sindhmonitoringcell.com/dashboard/addPatientFollowup', headers=headers, cookies=cookies, data=data, verify=False)
  return response.status_code


@app.get("/test/{patient_id}")
async def testResult(patient_id: str):
  return await getResult(patient_id)

@app.get("/follow/{patient_id}")
async def follow(patient_id: str):
  return await followUp(patient_id)
  #return {"data": patient_id}
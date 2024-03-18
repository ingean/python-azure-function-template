import azure.functions as func
import requests
import datetime
import json
import logging

app = func.FunctionApp()


@app.route(route="test", auth_level=func.AuthLevel.ANONYMOUS)
def test(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  name = req.params.get('name')
  if not name:
    try:
      req_body = req.get_json()
    except ValueError:
      pass
    else:
      name = req_body.get('name')

  if name:
    return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
  else:
    return func.HttpResponse(
      "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
      status_code=200
    )


@app.route(route="APITest", auth_level=func.AuthLevel.ANONYMOUS)
def APITest(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  service_url = 'https://ic.imagery1.arcgis.com/arcgis/rest/services/Sentinel2_10m_LandCover/ImageServer/exportImage'
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  data = {
    "bbox": "409624.4654984647,7461237.628330557,458431.1503485076,7510044.3131806",
    "bboxSR": "32752",
    "size": "1295,1590", 
    "imageSR": "32752",
    "time": "", 
    "format": "png",
    "pixelType": "U8",
    "noData": "",
    "noDataInterpretation": "esriNoDataMatchAny",
    "interpolation":"+RSP_BilinearInterpolation",
    "compression": "", 
    "compressionQuality": "",
    "bandIds": "",
    "sliceId": "",
    "mosaicRule": "",
    "renderingRule": "",
    "adjustAspectRatio": "true",
    "validateExtent": "false",
    "lercVersion": "1",
    "compressionTolerance": "",
    "f": "json"
  }

  response = requests.post(service_url, data=data, headers=headers)
  result = response.json()
    
  return func.HttpResponse(json.dumps(result))

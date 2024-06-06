from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
 
import base64
 
try:
    cred = credential.Credential("AKID", "AKSECRET")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"
 
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
 
    image_path = 'd:/a/a.jpg'
 
    with open(image_path, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = base64.b64encode(data).decode('utf-8')  # base64编码图片，注意直接decode为utf-8字符串
 
    req = models.GeneralAccurateOCRRequest()
    req.ImageBase64 = encodestr
    # req.LanguageType = "auto"
 
    resp = client.GeneralAccurateOCR(req)
    print(resp.to_json_string())
    for text in resp.TextDetections:  # 输出文字
        print(text.DetectedText)
 
except TencentCloudSDKException as err:
    print(err)
except Exception as e:
    print(e)  # 捕获其他可能的异常
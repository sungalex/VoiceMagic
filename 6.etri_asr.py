#-*- coding:utf-8 -*-
# ETRI 인공지능 오픈 API (음성인식) example
# 사용 방법은 간단함. 별도의 환경 설정 불필요. 회원인증(API Key 발급) 만 되면 사용 가능
# audio file size에 제한이 있음(단문 만 지원. 정확한 시간 제안 길이에 대한 문서 미제공. 45초 음성도 실패 했음)
# 지원하는 음성 오디오 type이 제한적임(기본은 PCM audio)
# 가이드 문서 : http://aiopen.etri.re.kr/guide_recognition.php

import urllib3
import json
import base64
import json

key_file = "../../ETRI/ETRI_API_Key.txt"    # ETRI API Key
with open(key_file, 'r') as f:
    accessKey = f.read()

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
audioFilePath = "./audio_file/KOR_F_RM0769FLJH0325.pcm"
languageCode = "korean"

with open(audioFilePath, "rb") as f:
    audioContents = base64.b64encode(f.read()).decode("utf8")
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        "audio": audioContents
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(response.data.decode())

result = response.data.decode()
result = json.loads(result)

print('transcript:', result["return_object"]["recognized"])

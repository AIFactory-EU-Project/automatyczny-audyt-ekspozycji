Camera Service API 
------------------
Request to get png image from camera_service takes the form:
`GET -C ${USER}:${PASS} ${ADR}/image/${CAM_IP}/${CAM_TYPE}`

* there are 4 parameters: camera_ip, camera_type, username, password
* camera_ip and camera_type should be passed in the URL path
* username and password should be send using HTTP Basic authentication scheme
* on success service will return png image (content-type: 'image/png')
* on error service will respond with the appropriate http resopnse code
* single request can take about 10sec or more
* multiple requests should be made sequentially

curl -X POST "https://app-m8h3nu7.aif.nordasys.net/verify-grill-photo-valid-for-analysis" \
-H  "Content-Type: multipart/form-data" \
-F "image=@data/valid.jpg;type=image/jpeg"

Example:
```
USER=<username>
PASS=<password>
ADR='127.0.0.1:5000'
CAM_IP='172.16.1.252'
CAM_TYPE='dahua'
GET -e -d -C ${USER}:${PASS} ${ADR}/image/${CAM_IP}/${CAM_TYPE}
```
Result:
```
200 OK
Date: Fri, 25 Oct 2019 11:31:58 GMT
Server: Werkzeug/0.16.0 Python/3.6.8
Content-Length: 5683627
Content-Type: image/png
Client-Date: Fri, 25 Oct 2019 11:31:58 GMT
Client-Peer: 127.0.0.1:5000
Client-Response-Num: 1
```

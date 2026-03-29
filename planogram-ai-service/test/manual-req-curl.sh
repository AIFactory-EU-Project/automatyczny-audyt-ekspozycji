curl -X POST "https://app-m8h3nu7.aif.nordasys.net/verify-grill-photo-valid-for-analysis" \
-H  "Content-Type: multipart/form-data" \
-F "image=@data/valid.jpg;type=image/jpeg"




curl -X POST "https://app-m8h3nu7.aif.nordasys.net/"\
"verify-grill-photo-valid-for-analysis"\
 -H  "Content-Type: multipart/form-data"\
 -F "image=@data/valid.jpg;type=image/jpeg"



curl -X POST $URL \
-H  "Content-Type: multipart/form-data"\
-F "image=@data/valid.jpg;type=image/jpeg"


curl -X POST "http://localhost:7552/verify-shelf-photo-valid-for-analysis" \
-H  "accept: application/json" \
-H  "Content-Type: multipart/form-data" \
-F "image=@test/data/valid.jpg;type=image/jpeg"

curl -X POST "http://localhost:7552/remove-faces-from-photo" \
-H  "accept: image/png" \
-H  "Content-Type: multipart/form-data" \
-F "image=@test/data/valid.jpg;type=image/jpeg" \
--output a.png

curl -X POST "http://localhost:7552/generate-grill-report" \
-H  "accept: application/json" \
-H  "Content-Type: multipart/form-data" \
-F "image=@test/data/valid.jpg;type=image/jpeg"

curl -X POST "http://localhost:7552/generate-planogram-report" \
-H  "accept: application/json" \
-H  "Content-Type: multipart/form-data" \
-F "image=@test/data/valid.jpg;type=image/jpeg" \
-F "planogramId=1"

curl -X GET "http://localhost:7552/health-check" \
-H  "accept: application/json"


curl -X GET "https://app-m8h3nu7.aif.nordasys.net/"



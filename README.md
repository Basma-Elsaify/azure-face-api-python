# Use azure face cognitive service python SDK to detect facial emotions

- Create an authenticated FaceClient, you need to provide `face recognition subscription key` and `face recognition endpoint`
- Set the attributes you need to retrieve from the api `age, emotion, gender...`
  - Note: to display extra properties `emotion`, you need to use `detection_model='detection_01'`

```python 
KEY = "PASTE_YOUR_FACE_SUBSCRIPTION_KEY_HERE"
ENDPOINT = "PASTE_YOUR_FACE_ENDPOINT_HERE"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
atts = ['age','gender','emotion']
```

## Detect image (three different data source options)

- Detect image from URL
  ```python 
  single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
  detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_01', return_face_attributes=atts)
  ```
- Detect local image 
  ```python 
  img = open(file_path, 'rb')
  detected_faces = face_client.face.detect_with_stream(img, detection_model='detection_01', return_face_attributes=atts)
  ```
- Detect image from azure blob storage
  ```python
  blob_img = container_client.get_blob_client('image_name.jpg')
  single_face_image_url = blob_img.url
  detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_01', return_face_attributes=atts)
  ```

## Display detected faces response attributes

```python 
if not detected_faces:
    raise Exception('No face detected from image')

print('Detected face ID:')
for face in detected_faces: print (face.face_id)
print()

first_image_face = detected_faces[0]

for attr,val in first_image_face.face_attributes.emotion.as_dict().items():
    if val>0.5:
        print(attr,val)
```

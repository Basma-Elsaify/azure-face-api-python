#!/usr/bin/env python
# coding: utf-8

# # Final face emotions detection
# ## this code block runs once

# In[75]:


import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

KEY = "PASTE_YOUR_FACE_SUBSCRIPTION_KEY_HERE"
ENDPOINT = "PASTE_YOUR_FACE_ENDPOINT_HERE"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

print('face_client', face_client)

atts = ['age','gender','emotion']


# # Below are three different ways to read the image:
# - detect image from URL
# - detect local image
# - detect an image on azure blob storage
# 
# so you should run only one of the following three code blocks
# 
# ## Detect from URL

# In[56]:



single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
single_image_name = os.path.basename(single_face_image_url)

detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_01', return_face_attributes=atts)


# ## Detect local bytes stream image

# In[67]:


file_path = 'image.png'
img = open(file_path, 'rb')
single_image_name = os.path.basename(file_path)

print(single_image_name)

detected_faces = face_client.face.detect_with_stream(img, detection_model='detection_01', return_face_attributes=atts)


# ## Read from azure blob URL

# In[76]:


from azure.storage.blob import BlobServiceClient

conn_str = 'PASTE_AZURE_BLOB_CONNECTION_STR_HERE'
container_name = 'PASTE_CONTAINER_NAME_HERE'

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

blob_img = container_client.get_blob_client('image_name.jpg')

print(blob_img.url)

single_face_image_url = blob_img.url
single_image_name = os.path.basename(single_face_image_url)

detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_01', return_face_attributes=atts)


# # Display detected faces response attributes 
# ## this code block runs once right after reading the image

# In[77]:


if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

print('Detected face ID from', single_image_name, ':')
for face in detected_faces: print (face.face_id)
print()

first_image_face_ID = detected_faces[0]

print('face_attributes.emotion =================>')
print('anger: ',first_image_face_ID.face_attributes.emotion.anger)
print('contempt: ',first_image_face_ID.face_attributes.emotion.contempt)
print('disgust: ',first_image_face_ID.face_attributes.emotion.disgust)
print('fear: ',first_image_face_ID.face_attributes.emotion.fear)
print('happiness: ',first_image_face_ID.face_attributes.emotion.happiness)
print('neutral: ',first_image_face_ID.face_attributes.emotion.neutral)
print('sadness: ',first_image_face_ID.face_attributes.emotion.sadness)
print('surprise: ',first_image_face_ID.face_attributes.emotion.surprise)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# # Face emotions detection
# ## this code block runs once

# In[1]:


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
atts = ['age','gender','emotion']


# # Below are three different ways to read the image:
# - detect image from URL
# - detect local image
# - detect an image on azure blob storage
# 
# so you should run only one of the following three code blocks
# 
# ## Detect from URL

# In[2]:


face_image = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'

detected_faces = face_client.face.detect_with_url(url=face_image, detection_model='detection_01', return_face_attributes=atts)


# ## Detect local bytes stream image

# In[7]:


face_image = 'image.jpg'
img = open(face_image, 'rb')

detected_faces = face_client.face.detect_with_stream(img, detection_model='detection_01', return_face_attributes=atts)


# ## Read from azure blob URL

# In[12]:


from azure.storage.blob import BlobServiceClient

conn_str = 'PASTE_AZURE_BLOB_CONNECTION_STR_HERE'
container_name = 'PASTE_CONTAINER_NAME_HERE'

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

blob_img = container_client.get_blob_client('image_name.jpg')

face_image = blob_img.url

detected_faces = face_client.face.detect_with_url(url=face_image, detection_model='detection_01', return_face_attributes=atts)


# # Display detected faces response attributes 
# ## the below code blocks run once right after reading the image
# ### list detected faces ids

# In[9]:


if not detected_faces:
    raise Exception('No face detected from image')

print('Detected face ID:')
for face in detected_faces: print (face.face_id)
print()

first_image_face = detected_faces[0]


# ### Display the emotion with probability higher than 50%

# In[10]:


for attr,val in first_image_face.face_attributes.emotion.as_dict().items():
    if val>0.5:
        print(attr,val)


# ### Display all emotions with its probability

# In[11]:


print('face_attributes.emotion =================>')
print('anger: ',first_image_face.face_attributes.emotion.anger)
print('contempt: ',first_image_face.face_attributes.emotion.contempt)
print('disgust: ',first_image_face.face_attributes.emotion.disgust)
print('fear: ',first_image_face.face_attributes.emotion.fear)
print('happiness: ',first_image_face.face_attributes.emotion.happiness)
print('neutral: ',first_image_face.face_attributes.emotion.neutral)
print('sadness: ',first_image_face.face_attributes.emotion.sadness)
print('surprise: ',first_image_face.face_attributes.emotion.surprise)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': '***********'
})



# Final Upload a file to firebase cloud storage

bucket = storage.bucket()


filepath = '/home/rawal/Desktop/mini_pro/EC/a.txt'

blob = bucket.blob('b.text')
blob.upload_from_string(
        filepath,
        content_type='file/text'
    )

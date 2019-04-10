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


# Download file form firebase
cred = credentials.Certificate("cred.json")

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': '***************************',
}, name='storage')


bucket = storage.bucket(app=app)
blob = bucket.blob('b.text')
filename = 'c.txt'
blob.download_to_filename(filename, client=None, start=None, end=None)


import csv
import os  
import boto3
from botocore.client import Config
from pyeclib.ec_iface import ECDriver

import sys
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

ACCESS_KEY_ID = '****************'
ACCESS_SECRET_KEY = '***************'

dataset2 = []
print "********* Welcome **********"
g=0
while(g==0):
	print("Press 1 if you are already a user or")
	print("Press 0 to register: ")
	a = int(raw_input(""))
	dataset=[]
	with open('mast.csv','r') as csvfile:
		reader = csv.reader(csvfile,delimiter=',')
		for row in reader:
			dataset +=[row]
	if(a==1):
		id1 =   raw_input("Enter ID: ")
		pass1 = raw_input("Enter password: ")
		for i in xrange(len(dataset)):
			if(id1 == dataset[i][0] and pass1 == dataset[i][1] ):
				print " Welcome ", id1 
				g=1
	else:
		k=1
		while(k==1):
			id1 = raw_input("Enter a new ID: ")
			t = [row[0] for row in dataset]
			if(id1 not in t):
				pass1 = raw_input("Enter password: ")
				k=0
				row = [id1,pass1,0]
				with open('mast.csv', 'a') as csvFile:
					writer = csv.writer(csvFile)
					writer.writerow(row)
					csvFile.close()
				print "Please sign in"
			else:
				print "Try new ID"
mast=[]
with open('mast.csv','r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		mast +=[row]
user=[]
with open('mast.csv','r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		user +=[row]
print " Press 1 to upload a file"
print " Press 2 to download your file"
k = int(raw_input(""))
if(k==1):
	numfil = 0
	index1 = 0
	for i in xrange(len(mast)):
		if(id1 == mast[i][0]):
			numfil = mast[i][2] 
			numfil = int(numfil) + 1
			mast[i][2] = numfil


	FILE_NAME = raw_input("Enter file name: ")
	new_name = id1 + '_' + str(numfil) + ".txt"
	row1 = [id1,FILE_NAME,new_name,new_name +".0" ,new_name +".1",new_name +".2",new_name +".3",new_name +".4",new_name +".5"]
	
	oldname = FILE_NAME
	os.rename(FILE_NAME,new_name)
	# Delete the fragment
	for i in range(0,6):
		fil = "/home/rawal/Desktop/mini_pro/File/" + new_name + '.'+str(i)
		os.remove(fil)

	FILE_NAME = new_name
	
	k1 = 4
	m1 = 2
	ec_type1 = "liberasurecode_rs_vand"
	file_dir = "/home/rawal/Desktop/mini_pro/code"
	filename = FILE_NAME
	fragment_dir = "/home/rawal/Desktop/mini_pro/File"
	ec_driver = ECDriver(k= k1 , m= m1, ec_type= ec_type1)
	with open(("%s/%s" % (file_dir,filename)), "rb") as fp:
	    whole_file_str = fp.read()
	fragments = ec_driver.encode(whole_file_str)
	i = 0
	for fragment in fragments:
	    with open("%s/%s.%d" % (fragment_dir,filename, i), "wb") as fp:
	        fp.write(fragment)
	    i += 1

	

	for i in range(1,6):
		BUCKET_NAME = "minibuck" + str(i)
		newfn = "/home/rawal/Desktop/mini_pro/File/" + new_name + '.'+str(i-1)

		s3 = boto3.client('s3')
		s3.upload_file(newfn,BUCKET_NAME,new_name + '.'+str(i-1))

	newfn = "/home/rawal/Desktop/mini_pro/File/" + new_name + '.5'  
	cred = credentials.Certificate('cred.json')
	firebase_admin.initialize_app(cred, {
	    'storageBucket': '***************'
	})
	bucket = storage.bucket()

	blob = bucket.blob(new_name +'.5')
	blob.upload_from_string(
	        newfn,
	        content_type='file/text'
	    )
# Update the database

	with open('mast.csv', 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(mast)
	writeFile.close()
	with open('user.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row1)
		csvFile.close()


	os.rename(FILE_NAME,oldname)

	print "File Uploaded"

#*****************************************************************************************************

elif(k==2):
	numfil = 0
	index1 = 0
	for i in xrange(len(dataset)):
		if(id1 == dataset[i][0]):
			numfil = dataset[i][2]
			index1 = i
	dataset1=[]
	with open('user.csv','r') as csvfile:
		reader = csv.reader(csvfile,delimiter=',')
		for row in reader:
			dataset1 +=[row]

	print "You have ",numfil , "files on cloud"
	if(int(numfil)> 0):
		print "Following are the files: "

		for x in xrange(len(dataset1)):
			if(id1 == dataset1[x][0]):
				print dataset1[x][1]
		
		FILE_NAME = raw_input("Enter file name you want to download: ")
		
		for x in xrange(len(dataset1)):
			if(id1 == dataset1[x][0] and FILE_NAME == dataset1[x][1]):
			
				new_name = dataset1[x][2]
				for l in xrange(3,9):
					filnam = dataset1[x][l]
					if(l<8):
						s3 = boto3.resource(
					    's3',
					    aws_access_key_id=ACCESS_KEY_ID,
					    aws_secret_access_key=ACCESS_SECRET_KEY,
					    config=Config(signature_version='s3v4')
					    )
						BUCKET_NAME = "minibuck" + str(l-2)
						s3.Bucket(BUCKET_NAME).download_file(filnam,filnam)

		k2 = 4
		m2 = 2
		ec_type2 = "liberasurecode_rs_vand"
		ec_driver = ECDriver(k= k2, m= m2, ec_type= ec_type2)
		loc = "/home/rawal/Desktop/mini_pro/code/"

		fragment_l = [loc + new_name +".0" ,loc +new_name +".1",loc +new_name +".2",loc +new_name +".3",loc + new_name +".4",loc + new_name +".5"]
		fragment_list = []

		print fragment_l

		for fragment in fragment_l:
		    with open(("%s" % fragment), "rb") as fp:
		        fragment_list.append(fp.read())
				# decode
		decoded_file = ec_driver.decode(fragment_list)

		# write
		with open("%s.decoded" % FILE_NAME, "wb") as fp:
		    fp.write(decoded_file)
		for i in range(0,6):
			fil = new_name + '.'+str(i) 
		
			os.remove(fil)
		print ("Download Complete")

							










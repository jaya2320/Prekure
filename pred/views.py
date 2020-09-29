from django.shortcuts import render,redirect

# Create your views here.
from .models import Report,Doctor
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
import tensorflow as tf
from keras.preprocessing.image import load_img
from django.shortcuts import render
import numpy as np
import pandas as pd
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from tensorflow import Graph
import pickle
import json
import math
featuremodel=pickle.load(open('./model/feature.pickle','rb'))
genderlist=['female','male']

label123=json.load(open("./model/area.json","r+"))
labels=label123['data_columns']
labels.sort()


model_graph=Graph()
with model_graph.as_default():
    tf_session=tf.compat.v1.Session() 
    with tf_session.as_default():
        model=load_model('./model/cancer.model')


cancer_dict = {
    0: 'Melanocytic nevi',
    1: 'Melanoma',
    2: 'Benign keratosis-like lesions ',
    3: 'Basal cell carcinoma',
    4: 'Actinic keratoses',
    5: 'Vascular lesions',
    6: 'Dermatofibroma'
}

list12=['jpeg','png','jpg']

@login_required(login_url='welcome')
def result(request):
    if request.method=='POST':
        
        
        age=(request.POST.get('age'))
        name=(request.POST.get('name'))

        gender=request.POST.get('gender')
        
        
        

        area=request.POST.get('area')
        


        print(request)
        print(request.POST.dict())
        fileobj=(request.FILES['filepath'])
        
        fs=FileSystemStorage()
        filepathname=fs.save(fileobj.name,fileobj)
        filepathname1=fs.url(filepathname)
        x12=filepathname.split('.')
        if x12[len(x12)-1] in list12:
            p='./media/'+filepathname
            img=load_img(p,target_size=(28,28,3))
            img1=np.expand_dims(img,axis=0)
            img1=img1/255
            
            with model_graph.as_default():
                
                with tf_session.as_default():
                    predi=model.predict(img1)
            predi1=np.argmax(predi)

            ans1=cancer_dict[predi1]
            
            prob=math.trunc(np.max(predi)*100)
            report=Report(user= request.user)

            report.img=filepathname
            report.probability=prob
            report.disease=ans1
            report.age=age
            report.name=name
            
            report.gender=gender
            report.area=area
            
            
            
            report.save()
            
            return render(request,'result.html',{'filepathname1':filepathname1,'result':ans1,'prob':prob})
        else:
            messages.info(request,"Please Choose an image file only. !!")
            return render(request,'index.html',{'gender':genderlist,'area':labels})


    else:
        return render(request,'index.html',{'gender':genderlist,'area':labels})


def register(request):
   
    return render (request,'signup.html')


@login_required(login_url='welcome')
def report(request):
    log_user=request.user
    report=Report.objects.filter(user=log_user)
    return render (request,"report.html",{'report':report})

@login_required(login_url='welcome')
def home(request):
     return render (request,"index.html",{'gender':genderlist,'area':labels})



def signup(request):
    
    if request.method=="POST":
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        username=request.POST['username']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                 messages.info(request,"Username already used. !!")
                 return render (request,"signup.html")
            
            if User.objects.filter(email=email).exists():
                    messages.info(request,"Email address already used. !!")
                    return render (request,"signup.html")
                
            else:
                user=User.objects.create_user(email=email,password=pass1,username=username)
                user.save()
                
                messages.info(request,"Congratulations your account is created successfully. !")
                return render (request,"login.html")

        else:
            messages.info(request,"OOPS! Password is not matching.")
            return render (request,"signup.html")
 
        return render (request,"signup.html")

def enter(request):
    return render(request,'login.html')


def login(request):
    username=request.POST['username']
    passw=request.POST['pass']

    user =auth.authenticate(username=username,password=passw)
    if user is not None:
        auth.login(request,user)
        return render (request,"about.html")
    else:
        messages.info(request,"Sorry! Account does not Exist.")
        return render (request,"login.html")


lat1=[[77.1354, 28.7243],[77.125747, 28.693297],[77.09444, 28.62],[77.055118, 28.616834],
[77.274074, 28.689589],[77.2688, 28.5149],[77.1775, 28.51583],[77.1886, 28.6516
],[77.1783, 28.7053],
[77.17189, 28.59153],[77.2198, 28.6328],[77.278787, 28.633606]]

lat2=[[80.91583, 26.86056],[77.6824, 28.9927],[78.08, 27.88],[83.00611, 25.30694],[78.56962, 25.44862],
[80.33111, 26.4725],[78.02, 27.18],[82.20056, 26.80361],[79.415, 28.364],
[81.85, 25.45],[77.32, 28.57],[77.41667, 28.66667]]


@login_required(login_url='welcome')
def searching(request):
    
    if request.method=='POST':
        
        an=(request.POST['city'])
        if an=="01":
            doctor=Doctor.objects.all().filter(state="Delhi")
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location1.html',
            {'mapbox_access_token':mapbox_access_token,'loc':lat1,'corn':[77.21667, 28.66667],'zoom':10.56,'doctor':doctor})
        elif an=="02":
            doctor=Doctor.objects.all().filter(state="U.P")
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location1.html',
            {'mapbox_access_token':mapbox_access_token,'loc':lat2,'corn':[80.50194282009, 27.3408313733408],'zoom':6,'doctor':doctor})
        
        else:
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})
      

@login_required(login_url='welcome')
def find(request):
    mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
    return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})

@login_required(login_url='welcome')
def submit(request):
    messages.info(request,"Your report is submitted successfully. Doctor will contact you soon.")
    mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
    return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})

@login_required(login_url='welcome')
def logout(request):
    auth.logout(request)
    return render (request,'about.html')

def welcome(request):
    return render (request, "about.html")
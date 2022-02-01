from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('PrivateKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def index(request):
    return render(request, "general/index.html")

@csrf_exempt
def validate_email(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        teachers_ref = db.collection(u'teachers')
        docs = teachers_ref.stream()
        query_ref = teachers_ref.where(u'email', u'==', email).limit(1).get()

        if(query_ref):
            for teacher in query_ref:
                return JsonResponse({"message": "User found", "userId": teacher.id, "username": teacher.to_dict()['name']}, status=201)

            
    
    return JsonResponse({"message": "User not found"}, status=201)
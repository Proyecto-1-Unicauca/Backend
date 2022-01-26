from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
"""
cred = credentials.Certificate('PrivateKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
"""
teachers = [
    {
        "id": 0,
        "name": "Victor",
        "surname": "Castillo",
        "email": "castillo@unicauca.edu.co"
    },
    {
        "id": 1,
        "name": "Daniel",
        "surname": "Torres",
        "email": "torres@unicauca.edu.co"
    }
]

def index(request):
    return render(request, "general/index.html")

@csrf_exempt
def validate_email(request):
    """
    users_ref = db.collection(u'teachers')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        
        for teacher in teachers:
            if email == teacher['email'] or email == teacher['email']:
                return JsonResponse({"message": "User found", "userId": teacher['id'], "username": teacher['name']}, status=201)
    
    return JsonResponse({"message": "User not found"}, status=201)
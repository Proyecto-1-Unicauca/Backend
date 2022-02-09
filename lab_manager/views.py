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
def workshops(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        newWorkshop = {
            u'topic_id': data['topic_id'],
            u'course_id': data['course_id'],
            u'data': data['data'],
            u'start_available': data['start_available'],
            u'end_available': data['end_available']
        }

        try:
            db.collection(u'workshop').add(newWorkshop)
            return JsonResponse({"message": "User created"}, status=201)
        except ValueError:
            return JsonResponse({"message": "User not created"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
def validate_email(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        teachers_ref = db.collection(u'teachers')
        docs = teachers_ref.stream()
        query_ref = teachers_ref.where(u'email', u'==', email).limit(1).get()

        if (query_ref):
            for teacher in query_ref:
                return JsonResponse(
                    {"message": "User found", "userId": teacher.id, "username": teacher.to_dict()['name']}, status=201)
        else:
            return JsonResponse({"message": "User not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
def courses(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        newCourse = {
            u'subject_id': data['subject_id'],
            u'name': data['name'],
            u'start': data['start'],
            u'end': data['end']
        }

        try:
            db.collection(u'courses').add(newCourse)
            return JsonResponse({"message": "new course registered"}, status=201)
        except ValueError:
            return JsonResponse({"message": "error creating new subject"}, status=201)
    elif request.method == "GET":
        data = json.loads(request.body.decode("utf-8"))
        id_get = data['id']
        subject_ref = db.collection(u'subjects')
        query_ref = subject_ref.where(u'id', u'==', id_get).limit(1).get()

        if query_ref:
            for subject in query_ref:
                return JsonResponse(
                    {"message": "Subject found", "subjectId": subject.id, "subjectName": subject.to_dict()['name']},
                    status=201)
        else:
            return JsonResponse({"message": "Subject not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


def subjects(request):
    if request.method == "GET":
        subject_ref = db.collection(u'subjects')
        query_ref = subject_ref.get()

        subject_dict = {}
        subject_records = []

        if query_ref:
            for subject in query_ref:
                subject = {"subjectId": subject.id, "subjectName": subject.to_dict()['name']}
                subject_records.append(subject)

            subject_dict["subject"] = subject_records
            return JsonResponse(subject_dict)
        else:
            return JsonResponse({"message": "Subject not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

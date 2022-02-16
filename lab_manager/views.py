import google.cloud.firestore_v1.field_path
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.field_path import FieldPath

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

        if (query_ref):
            for teacher in query_ref:
                return JsonResponse(
                    {"message": "Email found", "userId": teacher.id, "username": teacher.to_dict()['name']}, status=201)
        else:
            return JsonResponse({"message": "Email not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

@csrf_exempt
def workshops(request):
    if request.method == "GET":
        users_ref = db.collection(u'workshops')
        docs = users_ref.stream()
        workshops = []

        for doc in docs:
            docDict = doc.to_dict()
            workshops.append({
                "id": doc.id,
                "topicId": docDict['topic_id'],
                "courseId": docDict['course_id'],
                "data": docDict['data'],
                "startAvailable": docDict['start_available'],
                "endAvailable": docDict['end_available']
            })
        
        return JsonResponse({"workshops": workshops}, status=201)
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        newWorkshop = {
            u'topic_id': data['topic_id'],
            u'course_id': data['course_id'],
            u'data': data['data'],
            u'start_available': data['start_available'],
            u'end_available': data['end_available']
        }

        try:
            db.collection(u'workshops').add(newWorkshop)
            return JsonResponse({"message": "Workshop created"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Workshop not created"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

@csrf_exempt
def workshops_by_id(request, id):
    if request.method == "GET":
        try:
            doc_ref = db.collection(u'workshops').document(id)
            doc = doc_ref.get()

            if doc.exists:
                docDict = doc.to_dict()
                workshop = {
                "id": doc.id,
                "topicId": docDict['topic_id'],
                "courseId": docDict['course_id'],
                "data": docDict['data'],
                "startAvailable": docDict['start_available'],
                "endAvailable": docDict['end_available']
                }
                
                return JsonResponse({"message": "Workshop found", "workshop": workshop}, status=201)
            else:
                return JsonResponse({"message": "Workshop not found"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Workshop not found"}, status=201)
    elif request.method == "DELETE":
        """
        try:
            doc_ref = db.collection(u'workshops').document(id)
            doc = doc_ref.get()

            if doc.exists:
                db.collection(u'workshops').document(id).delete()
                return JsonResponse({"message": "Workshop deleted"}, status=201)
            else:
                return JsonResponse({"message": "Workshop not found"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Workshop not deleted"}, status=201)
    else:
        """
        return JsonResponse({"message": "Invalid action"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

@csrf_exempt
def courses(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        access_key = get_random_string(length=8)
        newCourse = {
            u'access_key': access_key,
            u'subject_id': data['subject_id'],
            u'name': data['name'],
            u'start': data['start'],
            u'end': data['end'],
            u'teacher_id': 104615020640
        }

        try:
            db.collection(u'courses').add(newCourse)
            return JsonResponse({"message": "new course registered"}, status=201)
        except ValueError:
            return JsonResponse({"message": "error creating new subject"}, status=201)

    if request.method == "GET":
        data = json.loads(request.body.decode("utf-8"))
        teacher_id = data['teacher_id']
        courses_ref = db.collection(u'courses')
        query_ref = courses_ref.where(u'teacher_id', u'==', teacher_id).get()

        teacher_courses_dict = {}
        teacher_courses_records = []

        if query_ref:
            for course in query_ref:
                teacher_course = {"courseId": course.id, "accessKey": course.to_dict()['access_key'],
                                  "name": course.to_dict()['name'], "start": course.to_dict()['start'],
                                  "end": course.to_dict()['end'], "subjectId": course.to_dict()['subject_id']}
                teacher_courses_records.append(teacher_course)

            teacher_courses_dict["courses"] = teacher_courses_records
            return JsonResponse(teacher_courses_dict, status=201)
        else:
            return JsonResponse({"message": "Teacher course not found"}, status=201)

    if request.method == "DELETE":
        data = json.loads(request.body.decode("utf-8"))
        course_id = data['course_id']
        courses_ref = db.collection(u'courses').document(course_id)

        doc = courses_ref.get()

        if doc.exists:
            try:
                doc.reference.delete()
                return JsonResponse({"message": "Course deleted"}, status=201)
            except ValueError:
                return JsonResponse({"message": "error deleting course"}, status=201)
        else:
            return JsonResponse({"message": "course not found"}, status=201)

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

            subject_dict["subjects"] = subject_records
            return JsonResponse(subject_dict, status=201)
        else:
            return JsonResponse({"message": "Subject not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

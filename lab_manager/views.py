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
def practices(request):
    if request.method == "GET":
        users_ref = db.collection(u'practices')
        docs = users_ref.stream()
        practices = []

        for doc in docs:
            docDict = doc.to_dict()
            
            practices.append({
                "id": doc.id,
                "workshop_id": docDict['workshop_id'],
                "leader_id": docDict['leader_id'],
                "students": docDict['students'],
                "attendees": docDict['attendees'],
                "data": docDict['data'],
                "anomaly": docDict['anomaly'],
                "next_anomaly_id": docDict['next_anomaly_id'],
                "start": docDict['start'],
                "end": docDict['end']
            })
        
        return JsonResponse({"practices": practices}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
def practices_by_id(request, id):
    if request.method == "GET":
        try:
            doc_ref = db.collection(u'practices').document(id)
            doc = doc_ref.get()

            if doc.exists:
                docDict = doc.to_dict()
                
                practice = {
                    "id": doc.id,
                    "workshop_id": docDict['workshop_id'],
                    "leader_id": docDict['leader_id'],
                    "students": docDict['students'],
                    "attendees": docDict['attendees'],
                    "data": docDict['data'],
                    "anomaly": docDict['anomaly'],
                    "next_anomaly_id": docDict['next_anomaly_id'],
                    "start": docDict['start'],
                    "end": docDict['end']
                }
                
                return JsonResponse({"message": "Practice found", "practice": practice}, status=201)
            else:
                return JsonResponse({"message": "Practice not found"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Practice not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

@csrf_exempt
def practices_by_workshop_id(request, workshop_id):
    if request.method == "GET":
        users_ref = db.collection(u'practices')
        docs = users_ref.where(u'workshop_id', u'==', workshop_id).get()
        print(docs)
        practices = []

        for doc in docs:
            docDict = doc.to_dict()
            practices.append({
                "id": doc.id,
                "workshopId": docDict['workshop_id'],
                "leaderId": docDict['leader_id'],
                "students": docDict['students'],
                "attendees": docDict['attendees'],
                "data": docDict['data'],
                "anomaly": docDict['anomaly'],
                "nextAnomalyId": docDict['next_anomaly_id'],
                "start": docDict['start'],
                "end": docDict['end']
            })
        
        return JsonResponse({"practices": practices}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

@csrf_exempt
def topics(request):
    if request.method == "GET":
        users_ref = db.collection(u'topics')
        docs = users_ref.stream()
        topics = []

        for doc in docs:
            docDict = doc.to_dict()
            
            topics.append({
                "id": doc.id,
                "constants": docDict['constants'],
                "name": docDict['name'],
                "subject_id": docDict['subject_id']
            })
        
        return JsonResponse({"topics": topics}, status=201)
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
                "constants": docDict['constants'],
                "cameras": docDict['cameras'],
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
            u'constants': data['constants'],
            u'cameras': data['cameras'],
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
def workshops_by_course_id(request, course_id):
    if request.method == "GET":
        users_ref = db.collection(u'workshops')
        docs = users_ref.where(u'course_id', u'==', course_id).get()
        workshops = []

        for doc in docs:
            docDict = doc.to_dict()
            workshops.append({
                "id": doc.id,
                "topicId": docDict['topic_id'],
                "courseId": docDict['course_id'],
                "data": docDict['data'],
                "constants": docDict['constants'],
                "cameras": docDict['cameras'],
                "startAvailable": docDict['start_available'],
                "endAvailable": docDict['end_available']
            })
        
        return JsonResponse({"workshops": workshops}, status=201)
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
                "constants": docDict['constants'],
                "cameras": docDict['cameras'],
                "startAvailable": docDict['start_available'],
                "endAvailable": docDict['end_available']
                }
                
                return JsonResponse({"message": "Workshop found", "workshop": workshop}, status=201)
            else:
                return JsonResponse({"message": "Workshop not found"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Workshop not found"}, status=201)
    elif request.method == "DELETE":
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
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
def courses_by_id(request, id):
    if request.method == "GET":
        try:
            doc_ref = db.collection(u'courses').where(u'teacher_id', u'==', int(id))
            docs = doc_ref.stream()

            course_dict = {}
            course_records = []

            for doc in docs:
                docDict = doc.to_dict()
                course = {
                    "id": doc.id,
                    "name": docDict['name'],
                    "access_key": docDict['access_key'],
                    "start_date": docDict['start'],
                    "end_date": docDict['end'],
                    "subject_id": docDict['subject_id'],
                    "teacher_id": docDict['teacher_id']
                }
                course_records.append(course)

            if len(course_records) > 0:
                course_dict["courses"] = course_records
                return JsonResponse({"message": "Teacher has courses", "courses": course_dict}, status=201)
            else:
                return JsonResponse({"message": "Course not found"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Course not found"}, status=201)

    elif request.method == "DELETE":
        courses_ref = db.collection(u'courses').document(id)

        doc = courses_ref.get()

        if doc.exists:
            try:
                doc.reference.delete()
                return JsonResponse({"message": "Course deleted"}, status=201)
            except ValueError:
                return JsonResponse({"message": "error deleting course"}, status=201)
        else:
            return JsonResponse({"message": "course not found"}, status=201)

    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
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


@csrf_exempt
def students(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        newStudent = {
            u'course_id': data['course_id'],
            u'email': data['email'],
            u'name': data['name'],
            u'surname': data['surname'],
        }

        try:
            student_id = str(data['id'])
            db.collection(u'students').document(student_id).set(newStudent)
            return JsonResponse({"message": "new student registered"}, status=201)
        except ValueError:
            return JsonResponse({"message": "error creating new student"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)


@csrf_exempt
def students_by_id(request, id):
    if request.method == "GET":
        try:
            doc_ref = db.collection(u'students').where(u'course_id', u'==', id)
            docs = doc_ref.stream()

            student_dict = {}
            students_records = []

            for doc in docs:
                docDict = doc.to_dict()
                student = {
                    "id": doc.id,
                    "name": docDict['name'],
                    "surname": docDict['surname'],
                    "email": docDict['email'],
                    "course_id": docDict['course_id']
                }
                students_records.append(student)

            if len(students_records) > 0:
                student_dict["students"] = students_records
                return JsonResponse({"message": "Course students", "Students": student_dict}, status=201)
            else:
                return JsonResponse({"message": "Course doesn't have students"}, status=201)
        except ValueError:
            return JsonResponse({"message": "Course not found"}, status=201)

    elif request.method == "DELETE":
        students_ref = db.collection(u'students').document(id)

        doc = students_ref.get()

        if doc.exists:
            try:
                doc.reference.delete()
                return JsonResponse({"message": "Student deleted"}, status=201)
            except ValueError:
                return JsonResponse({"message": "error deleting student"}, status=201)
        else:
            return JsonResponse({"message": "course not found"}, status=201)
    else:
        return JsonResponse({"message": "Invalid action"}, status=201)

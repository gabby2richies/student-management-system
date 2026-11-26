import csv
from django.http import HttpResponse
from .models import Student
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import os


@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.all()

    total_students = students.count()

    recent_students = students.order_by('-id')[:5]

    total_courses = students.values('course').distinct().count()

    total_scores = sum(
        len(student.scores) for student in students
    )

    return render(request, 'students/dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_scores': total_scores,
        'recent_students': recent_students,
    })

@login_required(login_url='login')
def register_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        course = request.POST.get('course')

        if Student.objects.filter(student_id__iexact=student_id).exists():
            messages.error(request, 'Student ID already exists.')
            return redirect('register')

        Student.objects.create(
            student_id=student_id,
            name=name,
            course=course,
            scores=[]
        )

        messages.success(request, 'Student registered successfully!')
        return redirect('dashboard')

    return render(request, 'students/register.html')


@login_required(login_url='login')
def view_students(request):
    students = Student.objects.all()

    for student in students:
        scores = student.scores or []

        if scores:
            average = sum(scores) / len(scores)
        else:
            average = 0

        if average >= 70:
            grade = 'A'
        elif average >= 60:
            grade = 'B'
        elif average >= 50:
            grade = 'C'
        elif average >= 45:
            grade = 'D'
        else:
            grade = 'F'

        student.average = round(average, 2)
        student.grade = grade

    return render(request, 'students/view_students.html', {
        'students': students
    })
    

@login_required(login_url='login')
def search_student(request):
    student = None
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()

        student = Student.objects.filter(
            student_id__iexact=student_id
        ).first()

        if student:
            scores = student.scores or []
            average = sum(scores) / len(scores) if scores else 0

            if average >= 70:
                grade = 'A'
            elif average >= 60:
                grade = 'B'
            elif average >= 50:
                grade = 'C'
            elif average >= 45:
                grade = 'D'
            else:
                grade = 'F'

            student.average = round(average, 2)
            student.grade = grade
        else:
            error = 'Student not found.'

    return render(request, 'students/search_student.html', {
        'student': student,
        'error': error
    })
    
@login_required(login_url='login')
def update_student(request):
    success = None
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        name = request.POST.get('name', '').strip()
        course = request.POST.get('course', '').strip()

        student = Student.objects.filter(
            student_id__iexact=student_id
        ).first()

        if student:
            student.name = name
            student.course = course
            student.save()

            success = 'Student record updated successfully!'
        else:
            error = 'Student not found.'

    return render(request, 'students/update_student.html', {
        'success': success,
        'error': error
    })
    
@login_required(login_url='login')
def delete_student(request):
    success = None
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()

        student = Student.objects.filter(
            student_id__iexact=student_id
        ).first()

        if student:
            student.delete()
            success = 'Student deleted successfully!'
        else:
            error = 'Student not found.'

    return render(request, 'students/delete_student.html', {
        'success': success,
        'error': error
    })
    
@login_required(login_url='login')
def record_score(request):
    success = None
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        score = request.POST.get('score', '').strip()

        if not score:
            error = 'Please enter a score.'
        else:
            score = float(score)

            if score < 0 or score > 100:
                error = 'Score must be between 0 and 100.'
            else:
                student = Student.objects.filter(
                    student_id__iexact=student_id
                ).first()

                if student:
                    student.scores = student.scores or []
                    student.scores.append(score)
                    student.save()

                    success = 'Score recorded successfully!'
                else:
                    error = 'Student not found.'

    return render(request, 'students/record_score.html', {
        'success': success,
        'error': error
    })
    
@login_required(login_url='login')
def export_students(request):
    students = Student.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Student ID',
        'Full Name',
        'Course',
        'Scores',
        'Average',
        'Grade'
    ])

    for student in students:
        scores = student.scores or []
        average = sum(scores) / len(scores) if scores else 0

        if average >= 70:
            grade = 'A'
        elif average >= 60:
            grade = 'B'
        elif average >= 50:
            grade = 'C'
        elif average >= 45:
            grade = 'D'
        else:
            grade = 'F'

        writer.writerow([
            student.student_id,
            student.name,
            student.course,
            ', '.join(map(str, scores)),
            round(average, 2),
            grade
        ])

    return response


def login_view(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password.'

    return render(request, 'students/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

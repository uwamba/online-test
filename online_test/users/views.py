from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from exams.models import Test,Question,QuestionOption
from results.models import Result,ResultDetail
from users.models import Candidate
# Create your views here.
# Candidate registration
def candidate_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        candidate = Candidate.objects.create_user(username=username, password=password, full_name=full_name)
        return redirect('candidate_login')
    return render(request, 'register.html')

# Candidate login
def candidate_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Candidate logout
def candidate_logout(request):
    logout(request)
    return redirect('candidate_login')

# Dashboard to view tests
@login_required
def candidate_dashboard(request):
    tests = Test.objects.all()  # Customize to show specific tests
    return render(request, 'dashboard.html', {'tests': tests})

@login_required
def take_test(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = test.questions.all()

    # Ensure the user has an associated Candidate instance
    candidate = Candidate.objects.get(user=request.user)

    if request.method == 'POST':
        score = 0
        # Create the result object
        result = Result.objects.create(candidate=candidate, test=test, total_marks=score)
        
        # Loop through the questions and store result details
        for question in questions:
            selected_option_ids = request.POST.getlist(str(question.id))  # This will get all selected options for multiple choice
            if question.question_type == 'multiple':  # For multiple answers
                # Iterate through selected options for multiple-choice questions
                print("multiple question found")
                for option_id in selected_option_ids:
                    selected_option = QuestionOption.objects.get(id=int(option_id))
                    ResultDetail.objects.create(result=result, question=question, selected_option=selected_option)
                    # Check if the option is correct
                    if selected_option.is_correct: # Assuming 'correct_options' is a many-to-many field
                        score += 1
            elif question.question_type == 'single':  # For single choice (single option selected)
                if selected_option_ids:
                    print("single question found")
                    selected_option = QuestionOption.objects.get(id=int(selected_option_ids[0]))
                    # Check if the option is correct
                    ResultDetail.objects.create(result=result, question=question, selected_option=selected_option)
                    if selected_option.is_correct: # Assuming 'correct_options' is a many-to-many field
                        score += 1
                  
                    
            elif question.question_type == 'text':  # For text input questions
                answer_text = request.POST.get(str(question.id))  # Get the user's answer as text
                ResultDetail.objects.create(result=result, question=question, selected_option=None, answer_text=answer_text)
                if answer_text == question.answer_text:  # Compare with correct answer
                    score += 1
                    # Optionally, store text answer as a ResultDetail if required
                    

        # After processing all answers, update the total marks in the result object
        result.total_marks = score
        result.save()

        # Redirect to the result view page
        return redirect('result', result_id=result.id)
    
        

    return render(request, 'take_test.html', {'test': test, 'questions': questions})
@login_required
def view_result(request, result_id):
    result = Result.objects.get(id=result_id)
    return render(request, 'test_result.html', {'result': result})

@login_required
def active_test(request, test_id):
    tests = Test.objects.get(id=result_id)
    return render(request, 'dashboard.html', {'test': tests})
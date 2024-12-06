from .models import Question, QuestionOption

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.question_set.all()
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'exams/test_detail.html', context)


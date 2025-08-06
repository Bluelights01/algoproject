from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Users,Question
from django.shortcuts import render, redirect
import subprocess
import tempfile

def landing_page(request):
    return render(request, 'landing.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'email already taken'})

        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)
        user.save()
        return redirect('login')  

    return render(request, 'register.html')

@login_required
def mypage(request):
    output = ""
    name=request.GET.get('name')
    question=Question.objects.get(name=name)
    if request.method == 'POST' and request.POST.get("action") == "run":
        code = request.POST.get("code","")
        print(code)
        input_txt=request.POST.get("input","")
        print(input_txt)
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()

            try:
                result = subprocess.run(
                    ['python3', tmp.name],
                    capture_output=True,
                    text=True,
                    input=input_txt,
                    timeout=5
                )
                output = result.stdout or result.stderr
                print(output)
                return render(request,'mypage.html',{'code':code,'output':output,'question':question})
            except subprocess.TimeoutExpired:
                output = "Error: Execution timed out."
                return render(request,'mypage.html',{'code':code,'output':output,'question':question})
            

    if request.method == 'POST' and request.POST.get("action") == "submit":
        code = request.POST.get("code","")
        print(code)
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()

            try:
                testcases = question.testcases  # should be list of dicts with 'input' and 'output'
                test_results=[]
                for test in testcases:
                     result=subprocess.run(
                        ['python3', tmp.name],
                        capture_output=True,
                        text=True,
                        input=test['input'],
                        timeout=5
                     )
                     output = result.stdout or result.stderr
                     expected = test["output"].strip()
                     result=result.stdout or result.stderr
                     passed = result.strip() == expected
                     if(passed):
                         passed='Accepted'
                return render(request,'mypage.html',{'code':code,'output':passed,'question':question})
            except subprocess.TimeoutExpired:
                output = "Error: Execution timed out."
                return render(request,'mypage.html',{'code':code,'output':output,'question':question})
    return render(request,'mypage.html',{'question':question})


@login_required
def index(request):
    if(request.method =='POST'):

        selected_items = request.POST.getlist('type')
        questions = Question.objects.filter(question_type__in=selected_items)
        context = {
        'questions': questions,
        'tag_choices': Question.QUESTION_TYPES,
        'difficulty_choices': Question.DIFFICULTY_LEVELS,
       }
        return render(request,'index.html',context)
    else:

        questions = Question.objects.all()
        context = {
        'questions': questions,
        'tag_choices': Question.QUESTION_TYPES,
        'difficulty_choices': Question.DIFFICULTY_LEVELS,
       }
        return render(request,'index.html',context)
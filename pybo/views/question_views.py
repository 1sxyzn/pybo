from django.contrib import messages  # 오류 시 메세지 띄우는 용도
from django.contrib.auth.decorators import login_required  # 로그인해야 글 쓸 수 있게 하기
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm  # 질문 등록
from ..models import Question


@login_required(login_url='common:login') # 등록 전 로그인 되어있는지 미리 검사. 로그인 안되어있으면 로그인 화면으로 이동
def question_create(request):
    #질문 등록
    if request.method == 'POST': # 질문 등록 화면에서 입력 후 저장하기를 누르면 POST
        form = QuestionForm(request.POST)
        if form.is_valid(): # form이 유효한지 검사, 유효하지 않으면 오류가 저장된 것
            question = form.save(commit=False) # commit=False는, create_date를 아직 설정하지 않았으므로 임시저장 하는 것을 의미
            question.author = request.user  # 글쓴이
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else: #메소드가 GET인 경우 = 질문 등록하기 버튼을 누르면 GET
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    #질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST": # 수정 후 저장하기 버튼 누르면 POST형식으로 호출, 데이터 수정됨
        # 조회한 question을 기본으로, 전달 받은 입력값들 덮어 써서 QuestionForm을 생성하라는 의미
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정 일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # 수정 버튼을 부르면 GET방식으로 호출, 질문 수정 화면 나타남
        form = QuestionForm(instance=question) # 수정 시, 기존에 저장된 제목, 내용이 반영되어야 하기 때문에 폼 생성함
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    #질문 삭제
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

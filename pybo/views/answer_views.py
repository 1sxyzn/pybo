from django.contrib.auth.decorators import login_required  # 로그인해야 글 쓸 수 있게 하기
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm  # 답변 등록
from ..models import Question, Answer


@login_required(login_url='common:login') # 등록 전 로그인 되어있는지 미리 검사. 로그인 안되어있으면 로그인 화면으로 이동
def answer_create(request, question_id): # html에서 입력된 데이터가 request로 넘어옴, question_id 에서는 질문 번호 넘어옴
    #답변 등록
    question = get_object_or_404(Question, pk=question_id)
    '''
    question.answer_set.create(content=request.POST.get('content'), create_date = timezone.now())
    #request.POST.get('content') 는 request에 담긴 데이터를 추출하기 위한 것
    return redirect('pybo:detail', question_id=question.id) #redirect 함수는 전달된 값을 참고하여 페이지 이동을 함
    '''
    #form을 이용한 답변 등록, question_create와 비슷
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # 글쓴이
            answer.create_date = timezone.now()
            answer.question=question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    #답변 수정
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    #답변 삭제
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
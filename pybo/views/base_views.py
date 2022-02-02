from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.db.models import Q, Count


def index(request):
    #목록출력
    #입력 인자
    page = request.GET.get('page','1') # 기본 페이지 = 1, get방식의 경우 url이 /?page=1
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') #정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 조회
    # question_list = Question.objects.order_by('-create_date')
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    #페이징 처리
    paginator = Paginator(question_list, 10) # 페이지 당 게시글 10개씩 보여주기
    page_obj = paginator.get_page(page)

    #조회한 모델 데이터 저장
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    return render(request, 'pybo/question_list.html', context)
    #return HttpResponse("pybo에 오신 것을 환영합니다")

def detail(request, question_id):
    #목록출력
    question = get_object_or_404(Question, pk=question_id)
    #조회한 모델 데이터 저장
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)
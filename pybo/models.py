from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Question(models.Model): #질문 모델
    #글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')

    subject = models.CharField(max_length=200) #질문의 제목
    content = models.TextField() #질문의 내용
    create_date = models.DateTimeField() #질문을 작성한 일시
    modify_date = models.DateTimeField(null=True, blank=True) # 수정날짜 획인
    voter = models.ManyToManyField(User) # 추천 필드

    def __str__(self):
        return self.subject

class Answer(models.Model): #답변 모델
    # 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')

    # 어떤 질문에 대한 답변인지, 다른 모델을 속성으로 가지므로 ForeignKey, CASCADE는 질문 삭제하면 답변도 삭제되도록 함
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField() #답변의 내용
    create_date = models.DateTimeField() #답변을 작성한 일시
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User)  # 추천 필드

class Comment(models.Model):
    #질문이나 답변에 댓글이 달릴 수 있음
    #Comment 모델의 필드는, 글쓴이 내용 댓글작성일시 댓글수정일시 이댓글이달린질문 이댓글이달린답변 ...이 있다
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
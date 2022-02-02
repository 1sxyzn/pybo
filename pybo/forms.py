from django import forms
from pybo.models import Question, Answer, Comment

#질문 등록
class QuestionForm(forms.ModelForm): #forms.Form을 상속받으면 폼, forms.ModelForm을 상속받으면 모델 폼이라고 함
    class Meta: # 모델 폼은 필수로 Meta class를 가져야 함, 여기에는 model과 fields를 필수로 쓰기
        #QuestionForm 클래스는 Question 모델과 연결되어 있고, subject와 content를 사용한다고 정의
        model=Question
        fields=['subject', 'content']
        #form.as_p는 입력 항목을 자동으로 설정해주지만, 부트스트랩 적용이 안됨. 그럴땐 meta class에 widgets 속성을 추가
        #그런데 form.as_p는 한계가 있으므로 폼을 수작업으로 html에 작업하자

        #입력 시 subject, content를 한글로 변경하고 싶다면
        labels={
            'subject':'제목',
            'content':'내용',
        }

#답변 등록
class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['content']
        labels={
            'content':'답변 내용',
        }

#댓글 등록
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
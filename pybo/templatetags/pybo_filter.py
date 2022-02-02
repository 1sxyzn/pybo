#템플릿 필터 이용
from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

#에너테이션 사용 -> 템플릿에서 해당 함수를 필터로 사용할 수 잇음
@register.filter
def sub(value, arg):
    return value-arg

@register.filter()
def mark(value):
    extensions=["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
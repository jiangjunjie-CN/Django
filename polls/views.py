from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
# Create your views here.

# 以下部分为函数视图
# require_GET为视图函数装饰器，只允许GET请求访问
# @require_GET()
# def index(request):
#     # return HttpResponse('这里是jjj的投票网站')
#     lastest_qlist = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     content = {'lastest_qlist': lastest_qlist}
#     # output = ','.join([q.question_text for q in lastest_qlist])
#     return render(request, 'polls/index.html', content)
#
# def detail(request, question_id):
#     # pk就是primary key的缩写，也就是任何model中都有的主键，那么id呢，大部分时候也是model的主键，所以在这个时候我们可以认为pk和id是完全一样的。
#     # get_object_or_404常用于查询某个对象，找到了则进行下一步处理，如果未找到则给用户返回404页面。
#     question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponse("你正在查看问题 %s。" % question_id)
#     # render的context参数可以将认可需要提供给模板的数据以字典的格式添加进去。使用Python内置的locals()方法，可以方便地将函数作用域内的所有变量一次性添加进去。
#     return render(request, 'polls/detail.html', {
#         'question': question
#     })
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponse("你正在查看问题 %s 的结果。" % question_id)
#     return render(request, 'polls/results.html', {
#         'question': question
#     })

# 采用类视图代替上述函数视图
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_qlist'

    def get_queryset(self):
        '''
        返回最近的5个问题
        '''
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('other'):
        other_text = request.POST['other_text'].replace(' ', '')
        if not other_text or Choice.objects.filter(choice_text=other_text, question_id=question_id).exists():
            messages.error(request, '自定义选项为空或选项已存在')
            return HttpResponseRedirect(reverse('polls:vote', args=(question.id,)))
        else:
            new_choice = request.POST['other_text']
            Choice.objects.create(choice_text=new_choice, votes=1, question_id=question_id)
    else:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': '请至少选择一个进行投票'
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # 投票完成后，用HttpResponseRedirect重定向至results页面，reverse()函数，即url反查，能帮助我们避免在视图函数中硬编码URL，
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("你正在对问题 %s 进行投票。" % question_id)


def goto(request):
    # 用request.resolver_match.namespace获取namespace属性
    # if request.resolver_match.namespace == 'polls_goto1':
    #     return HttpResponse('这里是goto1的页面')
    # elif request.resolver_match.namespace == 'polls_goto2':
    #     return HttpResponse('这里是goto2的页面')
    # else:
    #     return HttpResponse('去liujiangblog.com学习Django吧')
    # reverse方法同样适用于namespace（实例命名空间）的url反查
    return HttpResponseRedirect(reverse('polls_goto1:index'))

def test_base(request):
    question = Question.objects.order_by('-pub_date')[:5]
    context = {'blog_entries': question}
    return render(request, 'polls/chil.html', context)

def test(request):
    question = get_object_or_404(Question, pk=2)
    return render(request, 'polls/test.html', locals())
from django.shortcuts import render,HttpResponse,redirect
from django import forms
import re
from django.core.exceptions import ValidationError

from django.db.models import Q,F,Max,Min
import hashlib
from sales import models
from sales.utils.hashlib_func import md5
from sales.utils.page import MyPagenation
from multiselectfield.forms.fields import MultiSelectFormField
def mobile_validate(value):
    mobile_re = re.compile(r'(13[0-9]|15[0123456789]|17[678]|18[0-9]|14[57])[0-9]{8}')
    if not mobile_re.match(value):
        raise ValidationError('手机号格式错误')



# Create your views here.
def login(request):
    if request.method == 'GET':
        return  render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username,password=md5(password)).first()
        if user_obj:
            request.session['session'] = user_obj
            return render(request,'saleshtml/home.html')
        else:
            return redirect('home')
            # return render(request,'login.html',{'error':'用户名或者密码错误'})


def register(request):
    """
    注册功能
    :param request:
    :return:
    """

    if request.method =='GET':
        register_form_obj = RegisterForm()

        return render(request,'register.html',{'register_form_obj':register_form_obj})
    else:
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            print(register_form_obj)
            register_form_obj.cleaned_data.pop('r_password')
            passssword = register_form_obj.cleaned_data.pop('password')
            passssword = md5(passssword)
            register_form_obj.cleaned_data.update({'password': passssword})
            models.UserInfo.objects.create(
                **register_form_obj.cleaned_data
            )
            return redirect('login')
        else:
            return render(request,'register.html',{'register_form_obj':register_form_obj})


class RegisterForm (forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=2,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class':'username','placeholder':'用户名','autocomplete':'off'}),
        error_messages={
            'required':'用户名不能为空',
            'max_length':'用户名不能大于16位',
            'min_length':'用户名不能小于2位'
        }
    )
    password = forms.CharField(
        max_length=16,
        min_length=2,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password','autocomplete':'off','placeholder':'密码'}),
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码不能大于16位',
            'min_length': '密码不能小于2位'
        }
    )
    r_password = forms.CharField(
        max_length=16,
        min_length=2,
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder':"输入密码", "oncontextmenu":"return false", 'onpaste':"return false"}),
        error_messages={
            'required': '确认密码不能为空',

        }
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid':'邮箱格式不对',
            'required':'邮箱不能为空'
        },
        widget=forms.widgets.TextInput(attrs={'placeholder':'邮箱','oncontextmenu':"return false"})

    )
    telephone = forms.CharField(
        label='电话',
        validators=[mobile_validate,],
        error_messages={
            'required':'手机号不能为空'
        },
        widget=forms.widgets.TextInput(attrs={'placeholder':'电话号码','autocomplete':"off", 'id':"number"})
    )
    def clean(self):
        value = self.cleaned_data
        password = value.get('password')
        r_password = value.get('r_password')
        if password == r_password:
            return value
        else:
            self.add_error('r_password','两次密码不一致')


def customers(request):
    current_request_path = request.path

    kw = request.GET.get('kw')
    search_field = request.GET.get('search_field')
    if kw:
        q_obj = Q()
        q_obj.connector = 'or'
        q_obj.children.append((search_field,kw))
        # customer_count = models.Customer.objects.filter(**{search_field:kw}).count()
        customer_count = models.Customer.objects.filter(q_obj).count()
    else:
        customer_count =  models.Customer.objects.all().count()
    print(customer_count)

    page = request.GET.get('page')

    mypage = MyPagenation(page,customer_count)
    if not kw:
        customers_objs = models.Customer.objects.all().reverse()[
                         (mypage.page - 1) * mypage.per_page_num:mypage.page * mypage.per_page_num]
    else:
        customers_objs = models.Customer.objects.filter(qq__contains=kw
                                                        ).reverse()[
                         (mypage.page - 1) * mypage.per_page_num:mypage.page * mypage.per_page_num]




    # customers_objs = models.Customer.objects.all().reverse()[(mypage.page-1)*mypage.per_page_num:mypage.page*mypage.per_page_num]
    return render(request,'saleshtml/customer.html',{'customer_objs':customers_objs,'page_html':mypage.page_html})

from django.forms.fields import DateField
class CustomerForm(forms.ModelForm):
    class Meta:
        ordering = ['id']
        model = models.Customer
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            # print(type(field))
            if not isinstance(field,MultiSelectFormField):

                field.widget.attrs.update({'class':'form-control'})
            if isinstance(field,DateField):
                field.widget.attrs.update({'type':'date'})
def mycustomers(request):
    models.Customer.objects.filter(consultant=models.UserInfo.objects.get(id=request.session.get('user_id')))
    return HttpResponse('ok')
def home(request):
    return render(request, 'saleshtml/home.html')
def add_customer(request):
    if request.method =='GET':
        customers_form = CustomerForm()
        return render(request,'saleshtml/add_customer.html',{'customers_form':customers_form})
    else:
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('customers')
        else:
            return render(request,'saleshtml/add_customer.html',{'customers_form':customer_form})
def edit_customer(request,cid):
    customers_obj = models.Customer.objects.filter(pk=cid).first()
    if request.method =='GET':
        customers_form = CustomerForm(instance=customers_obj)

        return render(request,'saleshtml/edit_customer.html',{'customer_form':customers_form})
    else:
        customers_form = CustomerForm(request.POST,instance=customers_obj)
        if customers_form.is_valid():
            customers_form.save()
            return redirect('customers')
        else:
            return render(request,'saleshtml/add_customer.html',{'customer_form':customers_form})
def add_edit_customer(request,cid=None):
    label = '编辑客户信息' if cid else "添加客户信息"
    customers_obj = models.Customer.objects.filter(pk=cid).first()
    if request.method =='GET':
        customers_form = CustomerForm(instance=customers_obj)

        return render(request,'saleshtml/edit_customer.html',{'customer_form':customers_form,"label":label})
    else:
        customers_form = CustomerForm(request.POST,instance=customers_obj)
        if customers_form.is_valid():
            customers_form.save()
            return redirect('customers')
        else:
            return render(request,'saleshtml/add_customer.html',{'customer_form':customers_form})
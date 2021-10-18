from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import *
from .models import *

UserModel = get_user_model()
from .forms import SignUpForm

@login_required
def Lauth(request):
        company = request.user
        if request.method == 'POST':
            form = leagueuserauth(request.POST)
            if form.is_valid():
              a = form.save(commit = False)
              if league.objects.filter(game_code=a.game_code).exists():
                  s = league.objects.get(game_code=a.game_code)
                  s.users.add(company)
                  s.save()
                  y = lauth(user=company,league=s,balance=100000)
                  y.save()
              else:
                  messages.error(request, "Incorrect Gamecode")
    
              return HttpResponseRedirect("/")

        else:
          form = leagueuserauth()
        context = {'form':form}
        template = "registration/lauth.html"
        return render(request, template, context)


def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy("login"))
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def home(request):
    items = stocks.objects.filter(league = request.user.lauth.league)
    context = {'items': items}
    template = "simulator/myspace.html"
    return render(request, template, context)
    

@login_required
def portfolio(request):
    items = holdings.objects.filter(user = request.user, league = request.user.lauth.league)
    template = "simulator/portfolio.html"
    cp = []
    for x in items:
        cv = {'stock':x.stock,'quantity':x.quantity,'average_price':x.average_price,'price':x.stock.price,'cp':x.quantity * x.stock.price}
        cp.append(cv)
    context = {'items': cp}
    return render(request, template, context) 
    

@login_required
def thistory(request):
    items = transaction.objects.filter(user = request.user, league = request.user.lauth.league)
    context = {'items': items}
    template = "simulator/transaction_history.html"
    return render(request, template, context) 
    

@login_required
def orderbook(request):
    return render(request,"simulator/order_book.html")

@login_required
def pnl(request):
    return render(request,"simulator/pnl.html")

@login_required
def News(request):
    items = news.objects.filter(league = request.user.lauth.league)
    context = {'items': items}
    template = "simulator/news.html"
    return render(request, template, context)  

@login_required
def News_v(request,newsid):
    x = news.objects.filter(id = newsid)
    if x.exists():
      item = x[0]
      context = {'item': item}
      template = "simulator/news_v.html"
      return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse_lazy('news'))  


@login_required
def equity_transactions(request):
        if request.method == 'POST':
            form = transactionadder(request.user.lauth.league, request.POST)
            if form.is_valid():
              a = form.save(commit = False)
              b_price = stocks.objects.get(id=a.stock.id).price
              a.buy_price = b_price
              a.total_investment = b_price * a.quantity
              a.user = request.user 
              a.league = request.user.lauth.league
              hs = holdings.objects.filter(user=request.user, league=request.user.lauth.league,stock = a.stock)
              t = request.user.lauth
              if a.ttype == "BUY":
                if a.total_investment > request.user.lauth.balance:
                  messages.error(request,'Not enough balance')
                  return HttpResponseRedirect(reverse_lazy('transact'))
                t.balance -= a.total_investment 
                if hs.exists():
                  z = hs[0]
                  z.average_price = ((hs[0].average_price * hs[0].quantity) + (a.buy_price * a.quantity))/(hs[0].quantity+a.quantity) 
                  z.quantity += a.quantity 
                  z.save()
                else: 
                  z = holdings(stock = a.stock,quantity = a.quantity,average_price = a.buy_price, user = request.user, league = a.league)
                  z.save()    
              elif a.ttype == "SELL":
                  t.balance += a.total_investment 
                  if hs.exists():
                       z = hs[0]
                       if z.quantity >= a.quantity:
                          z.quantity -= a.quantity 
                       else:
                           messages.error(request, "Sell Quantity cant be more than owned quantity")
                           return HttpResponseRedirect(reverse_lazy('transact'))
                       z.save()
                       if z.quantity == 0:
                              z.delete()
              
              a.save()
              t.save()
              return HttpResponseRedirect(reverse_lazy('portfolio'))

        else:
          form = transactionadder(request.user.lauth.league)
        context = {'form':form}
        template = "simulator/transact.html"
        return render(request, template, context)
  

  
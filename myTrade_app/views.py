from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup 
import locale
# Create your views here.

# RENDER TEMPLATES

# index page
def index(request):
    if 'id' not in request.session:
        return render(request, 'index.html')
    else:
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user,
        }
        return render(request, 'index.html', context)

# register
def register(request):
    return render(request, 'register.html')

# login
def login(request):
    return render(request, 'login.html')

# display user dashboard
def user_dash(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    account_balance = "{:.2f}".format(user.account_balance)
    trades = Trade.objects.filter(stock_holder=user).order_by('-created_at')
    if trades.count() > 0:
        if SoldTrade.objects.filter(stock_holder=user).count() > 0:       
            latest_sold_trade = SoldTrade.objects.filter(stock_holder=user).order_by('-created_at').latest('created_at')
            if Post.objects.filter(poster=user).count() == 0:
                latest_posts = "No Posts"
            if Post.objects.filter(poster=user).count() == 1:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
            elif Post.objects.filter(poster=user).count() == 2:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
            elif Post.objects.filter(poster=user).count() > 2:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')[:3]
            latest_trade = trades.latest('created_at')
            context = {
                'user': user,
                'account_balance': account_balance,
                'trades': trades,
                'latest_trade': latest_trade,
                'latest_posts': latest_posts,
                'latest_sold_trade': latest_sold_trade,
            }
        else:
            if Post.objects.filter(poster=user).count() == 0:
                latest_posts = "No Posts"
            if Post.objects.filter(poster=user).count() == 1:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
            elif Post.objects.filter(poster=user).count() == 2:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
            elif Post.objects.filter(poster=user).count() > 2:
                latest_posts = Post.objects.filter(poster=user).order_by('-created_at')[:3]
            latest_trade = trades.latest('created_at')
            context = {
                'user': user,
                'account_balance': account_balance,
                'trades': trades,
                'latest_posts': latest_posts,
                'latest_trade': latest_trade,
            }
    else:
        if Post.objects.filter(poster=user).count() == 0:
            latest_posts = "No Posts"
        elif Post.objects.filter(poster=user).count() == 1:
            latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
        elif Post.objects.filter(poster=user).count() == 2:
            latest_posts = Post.objects.filter(poster=user).order_by('-created_at')
        elif Post.objects.filter(poster=user).count() > 2:
            latest_posts = Post.objects.filter(poster=user).order_by('-created_at')[:3]
        context = {
            'user': user,
            'account_balance': account_balance,
            'latest_posts': latest_posts,
        }

    return render(request, 'user_dash.html', context)

# view stock
def view_stock(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])    
    account_balance = "{:.2f}".format(user.account_balance)
    context = {
        'account_balance': account_balance,
    }
    return render(request, 'stock.html', context)

# sell stock render
def sell_trade(request, trade_id):
    trade = Trade.objects.get(id=trade_id)
    user = User.objects.get(id=request.session['id'])
    context = {
        'trade': trade,
        'user': user,
    }
    return render(request, 'sell_trade.html', context)

# display user profile
def user_profile(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    user_posts = Post.objects.filter(poster=user).order_by("-created_at")
    comments = Comment.objects.all()
    context = {
        'user': user,
        'user_posts': user_posts,
        'comments': comments,
    }
    return render(request, 'user_profile.html', context)

# display other users profiles
def view_profile(request, id):
    user = User.objects.get(id=id)
    if user.id == request.session['id']:
        return redirect('/user_profile')
    user_posts = Post.objects.filter(poster=user).order_by("-created_at")
    logged_user = User.objects.get(id=request.session['id'])
    comments = Comment.objects.all()
    context = {
        'user': user,
        'user_posts': user_posts,
        'comments': comments,
        'logged_user': logged_user,
    }
    return render(request, 'view_profile.html', context)    

# display profile settings
def profile_settings(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
    }
    return render(request, 'profile_settings.html', context)

# display feed
def feed(request):
    if 'id' not in request.session:
        return redirect('/')
    logged_user = User.objects.get(id=request.session['id'])
    posts = Post.objects.all().order_by("-created_at")
    comments = Comment.objects.all()
    context = {
        'user': logged_user,
        'posts': posts,
        'comments': comments,
    }
    return render(request, 'feed.html', context)

# display user account
def user_account(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    account_balance = "{:.2f}".format(user.account_balance)
    trades = Trade.objects.filter(stock_holder=user).order_by("-created_at")
    sold_trade = SoldTrade.objects.filter(stock_holder=user).order_by("-created_at")
    context = {
        'user': user,
        'account_balance': account_balance,
        'trades': trades,
        'sold_trade': sold_trade,
    }
    return render(request, 'user_account.html', context)

# display user analytics
def user_analytics(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    if user.trades.count() > 0:
        trades = Trade.objects.filter(stock_holder=user).order_by("-created_at")
        latest_trade = trades.latest('created_at')
        sold_trade = SoldTrade.objects.filter(stock_holder=user).order_by("-created_at")
        total_gain = 0
        for trade in sold_trade:
            total_gain = total_gain + trade.total_price_gained
        context = {
            'user': user,
            'trades': trades,
            'latest_trade': latest_trade,
            'sold_trade': sold_trade,
            'total_gain': "{:.2f}".format(total_gain),
        }
    else:
        context = {
            'user': user,
        }
    return render(request, 'user_analytics.html', context)
    
# view stats
def view_stats(request, trade_id):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    trade = Trade.objects.get(id=trade_id)
    symbol = trade.symbol
    context = {
        'symbol': symbol,
        'user': user,
        'trade': trade,
    }
    return render(request, 'view_stats.html', context)


 
# HANDLING POST DATA

# process register
def process_register(request):
    # check for valid data 
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/register')
    if request.POST['password'] == request.POST['conf_password']:
        password = request.POST['password']
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # create the user
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], username=request.POST['username'], bio=request.POST['bio'], avatar=request.POST['av_icon'] , password=password_hash)
        request.session['id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['email'] = new_user.email
        request.session['username'] = new_user.username
        request.session['bio'] = new_user.bio
        request.session['avatar'] = new_user.avatar
        return redirect('/user_dash')
    else:
        return redirect('/register')


# process login
def process_login(request):
    # check for valid user data
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login')
    # check for user
    user =  User.objects.filter(username=request.POST['username'])
    if user:
        logged_user = user[0]
        # see if passwords match
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
            request.session['last_name'] = logged_user.last_name
            request.session['email'] = logged_user.email
            return redirect('/user_dash')
        else:
            messages.error(request, "Wrong Password!")
    return redirect('/login')

# logout
def logout(request):
    request.session.flush()
    return redirect('/')

# create post
def create_post(request):
    user = User.objects.get(id=request.session['id'])
    post = Post.objects.create(content=request.POST['content'], poster=user)
    return redirect('/feed')

# create comment
def create_comment(request):
    user = User.objects.get(id=request.session['id'])
    post = Post.objects.get(id=request.POST['post_id'])
    new_comment = Comment.objects.create(content=request.POST['content'], post=post, commenter=user)
    return redirect('/feed')


# like post 
def like(request, id):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    post = Post.objects.get(id=id)
    if post.poster == user:
        return redirect('/feed')
    post.user_who_liked.add(user)
    return redirect('/feed')


# add balance
def add_balance(request):
    balance = int(request.POST['balance'])
    user = User.objects.get(id=request.session['id'])
    account_balance = "{:.2f}".format(user.account_balance)
    account_balance = float(account_balance)
    if balance <= 0:
        return redirect('/user_account')
    if balance > 0:
        user.account_balance = account_balance + float(balance)
        user.save() 
    return redirect('/user_account')

# find stock
def find_stock(request):
    symbol = request.POST['stock']
    if symbol == '':
        return redirect('/user_dash')
    elif '^' in symbol:
        request.session['symbol'] = False
    else:
        # web scraper
        def stockUpdate(symbol):
            yahoo_url =  f"https://finance.yahoo.com/quote/{symbol}/"
            yahoo_page = urlopen(yahoo_url)
            yahoo_page_html =  yahoo_page.read()
            page_soup = soup(yahoo_page_html, "html.parser")
            # print(page_soup)
            if page_soup.find("span", {"class": "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)"}) == None:
                request.session['symbol'] = False
                return False
            else:
                price = page_soup.find("span", {"class": "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)"}).text
                request.session['symbol'] = symbol
                request.session['price'] = price
        stockUpdate(symbol)
    return redirect('/view_stock')

# buy stock
def buy_stock(request):
    user = User.objects.get(id=request.session['id'])
    account_balance = float(user.account_balance)
    symbol = request.session['symbol']
    price = request.session['price']
    shares = float(request.POST['shares'])
    # parse data
    if "," in price:
        # format the price to a number 
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
        price = locale.atof(price)
        # calculate total price
        total_price = float(price * shares)
        # if total price is less than or equal to users total balance
        if total_price <= account_balance:
            new_balance = float(account_balance) - float(total_price)
            new_balance = "{:.2f}".format(new_balance)
            new_balance = float(new_balance)
            # make trade and update balance
            trade = Trade.objects.create(symbol=request.session['symbol'], price_per_share=price, total_price=total_price, shares=shares, stock_holder=user)
            user.account_balance = new_balance
            user.save()
            return redirect('/user_account')
        else:
            print("Need more funds")
            return redirect('/user_dash')
    else:
        price = float(price)
        total_price = float(price * shares)
        if total_price <= account_balance:
            new_balance = float(account_balance) - float(total_price)
            new_balance = "{:.2f}".format(new_balance)
            new_balance = float(new_balance)
            # make trade and update balance
            trade = Trade.objects.create(symbol=request.session['symbol'], price_per_share=price, total_price=total_price, shares=shares, stock_holder=user)
            user.account_balance = new_balance
            user.save()
            return redirect('/user_account')
        else:
            print("Need more funds")
            return redirect('/user_dash')
    
    return redirect('/view_stock')

# sell shares
def sell_shares(request):
    shares = float(request.POST['shares'])
    trade = Trade.objects.get(id=request.POST['trade_id'])
    user = User.objects.get(id=request.session['id'])
    account_balance = user.account_balance
    sell_price = request.POST['sell_price']
    # parse data
    if "," in sell_price:
        # format the price to a number 
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
        sell_price = locale.atof(sell_price)
        # calculate total price
    sell_price = float(sell_price)
    add_balance = float(sell_price * shares)
    shares = int(shares)
    # new trade sold
    sold = SoldTrade.objects.create(price_sold=sell_price, shares_sold=shares, total_price_gained=add_balance, stock_holder=user, trade=trade)
    shares_remaining = float(trade.shares) - float(shares)
    new_balance = float(account_balance + add_balance)
    new_balance = "{:.2f}".format(new_balance)
    new_balance = float(new_balance)
    # update balance
    user.account_balance = new_balance
    total_price = float(shares_remaining) * float(trade.price_per_share)
    trade.total_price = total_price
    user.save()
    trade.shares = int(shares_remaining)
    trade.save()
    return redirect('/user_account')
# web scraper
def current_price(request, trade_id):
    trade = Trade.objects.get(id=trade_id)
    symbol = trade.symbol
    def stockUpdate(symbol):
        yahoo_url =  f"https://finance.yahoo.com/quote/{symbol}/"
        yahoo_page = urlopen(yahoo_url)
        yahoo_page_html =  yahoo_page.read()
        page_soup = soup(yahoo_page_html, "html.parser")
        # print(page_soup)
        if page_soup.find("span", {"class": "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)"}) == None:
            request.session['symbol'] = False
            return False
        else:
            price = page_soup.find("span", {"class": "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)"}).text
            request.session['sell_symbol'] = symbol
            request.session['sell_price'] = price

    stockUpdate(symbol)
    return redirect(f'/sell/{trade_id}')
# update bio
def update_bio(request):
    user = User.objects.get(id=request.session['id'])
    new_bio = request.POST['bio']
    user.bio = new_bio
    user.save()
    return redirect('/user_profile')
# update avatar
def update_avatar(request):
    user = User.objects.get(id=request.session['id'])
    new_avatar = request.POST['av_icon']
    user.avatar = new_avatar
    user.save()
    return redirect('/user_profile')
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from tango.models import Category
from tango.models import Page
from tango.forms import CategoryForm, PageForm
from tango.forms import UserForm, UserProfileForm
from datetime import datetime
from django.shortcuts import redirect

def index(request):
    cat_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {
        'categories': cat_list,
        'pages': page_list,
    }

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
        context['last_visit'] = last_visit_time
        
        if (datetime.now() - last_visit_time).seconds > 3600:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        context['last_visit'] = 'This is your first visit'
        reset_last_visit_time = True
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context['visits'] = visits

    response = render(request, 'tango/index.html', context)

    return response

def about(request):
    context = {}
    if request.session.get('last_visit'):
        context['visits'] = request.session.get('visits')
        context['last_visit'] = datetime.strptime(request.session.get('last_visit')[:-7],"%Y-%m-%d %H:%M:%S")
    else:
        context['visits'] = 1
        context['last_visit'] = 'This your first visti'
    return render(request, 'tango/about.html', context)

def category(request, url):
    context = {}
    try:
        category = Category.objects.get(slug=url)
        context['name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context['pages']=pages
        context['category']=str(category).lower
        context['slug']=url
    except Category.DoesNotExist:
        pass
    return render(request,'tango/cat.html',context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponse("Category successfuly added! <a href='/tango/'>Back to main page</a>")
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request,'tango/add_category.html',{'form':form})

@login_required
def add_page(request, url):
    try:
        cat = Category.objects.get(slug=url)
    except:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, url)
        else:
            print form.errors
    else:
        form = PageForm()
    return render(request,'tango/add_page.html',{'form': form, 'category': cat})

def track_url(request):
    page_id = None
    url = '/tango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                pageVisited = Page.objects.get(id=page_id)
                pageVisited.views+=1
                pageVisited.save()
                url = pageVisited.url
            except:
                pass
    return redirect(url)

def profile(request):
    profile_form = UserProfileForm()
    return render(request, 'tango/profile.html', {'profile_form':profile_form})
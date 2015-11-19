import os
from random import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_project.settings')

import django
django.setup()

from tango.models import Category, Page

def populate():
	anime_cat = add_cat('Anime',128,64)

	add_page(cat=anime_cat,
		title="Naruto",
		url="http://shippuuden.pl")

	add_page(cat=anime_cat,
		title="Shingeki no Kyojin",
		url="http://anime-odcinki.pl/anime/attack-titan")

	add_page(cat=anime_cat,
		title="Black Bullet",
		url="http://anime-odcinki.pl/anime/black-bullet")

	add_page(cat=anime_cat,
		title="Gate: Jieitai Kanochi nite, Kaku Tatakaeri",
		url="http://anime-odcinki.pl/anime/gate-jieitai-kanochi-nite-kaku-tatakaeri")

	add_page(cat=anime_cat,
		title="Angel Beats",
		url="http://anime-odcinki.pl/anime/angel-beats")

	add_page(cat=anime_cat,
		title="Another",
		url="http://anime-odcinki.pl/anime/another")

	programming_cat = add_cat("Programming",23,23)

	add_page(cat=programming_cat,
		title="C",
		url="http://www.cplusplus.com/reference/clibrary/")

	add_page(cat=programming_cat,
		title="C++",
		url="http://www.cplusplus.com/reference/")

	add_page(cat=programming_cat,
		title="Java",
		url="http://docs.oracle.com/javase/7/docs/api/allclasses-noframe.html")

	add_page(cat=programming_cat,
		title="Python",
		url="https://docs.python.org/2/reference/")
	add_page(cat=programming_cat,
		title="Django",
		url="https://docs.djangoproject.com/en/1.8/")

	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat,title=title)[0]
	p.url=url
	p.views=views + randint(10,200)
	p.save()
	return p

def add_cat(name,views,likes):
	c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
	return c

if __name__ == '__main__':
	print "Starting Tango population script..."
	populate()
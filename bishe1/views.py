import random
import math
from operator import itemgetter
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from user.models import User
from movie.models import Movie
from rating.models import Rating
from matrix.models import RecommendMatrix
import os
import datetime
from django.core.paginator import Paginator
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def gai(request):
    movies = Movie.objects.all()
    dict = {
        "Sci-Fi":'科幻',
        "Horro":'恐怖',
        "Action":'动作',
        "Animation":'动画',
        "Drama":'剧情',
        "Documentary":'剧情',
        "Musical":'音乐歌舞',
        "Western":'西部',
        "Film-Nolr":'',
        "Mystery":'悬疑',
        "Thriller":'惊悚',
        "Adventure":'冒险',
        "War":'战争',
        "Crime":'犯罪',
        "Fantasy":'奇幻',
        "Comedy":'喜剧',
        "Children's":'儿童',
        "Romance":'爱情',

    }
    for movie in movies:
        genres = movie.genres.split('|')
        news = []
        str1 = ''
        i = 0
        for genre in genres:
            if genre in dict.keys():
                news.append(dict[genre])
        for new in news:
            if i == 0:
                str1 = new
            else:
                str1 = str1 + "|" + new
            i = i+1
        movie.genres = str1
        movie.save()

# def read(request):
#     f = open('users.dat','r')
#     lines = f.readlines()
#
#     for line in lines:
#
#         list1 = line.split("::")
#         print(list1)
#         user = User(gender=list1[1],age=int(list1[2]),work=int(list1[3]))
#         user.save()
#
#     f.close()
#     return HttpResponse("123")


# def read(request):
#     #ISO-8859-1格式才能读取
#     f = open('E:/django/myproject/bishe/bishe1/movies.dat', 'r',encoding='ISO-8859-1')
#     lines = f.readlines()
#     # print(lines)
#     for line in lines:
#         str = line[:-1]
#         list1 = str.split("::")
#
#
#         movie = Movie(title=list1[1],genres=list1[2])
#         #user = User(gender=list1[1], age=int(list1[2]), work=int(list1[3]))
#         #user.save()
#         movie.save()
#     f.close()
#     # name = os.listdir('E:/django/myproject/bishe/bishe1/imgs/')
#     # print(name)
#
#
#     return HttpResponse("123")

# def read(request):
#     movie = Movie.objects.get(title = 'Toy Story (1995)')
#
#     response = requests.get('https://www.imdb.com/find?q='+movie.title)
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     soup.prettify()
#     href_list = []
#     for x in soup.find_all('a', href=re.compile('/title/tt')):
#         href_list.append(x.get('href'))
#
#     str1 = 'https://www.imdb.com'
#     response = requests.get(str1 + href_list[0])
#
#     imdb_num = href_list[0].split('/')
#     print(imdb_num)
#     movie.imbd = imdb_num[2][2:]
#     print(movie.imbd)
#     html = response.text
#     response.raise_for_status()
#     soup = BeautifulSoup(html, 'html.parser')
#     rating = soup.find('span', itemprop='ratingValue').text
#     movie.imdb_rating = rating
#     movie.save()
#     return HttpResponse("123")



def read(request):
    movies = Movie.objects.all()
    for movie in movies[58:]:
        title = movie.title.split('(')[0]
        response = requests.get('https://www.imdb.com/find?q='+title)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()
        href_list = []
        for x in soup.find_all('a', href=re.compile('/title/tt')):
            href_list.append(x.get('href'))

        str1 = 'https://www.imdb.com'
        response = requests.get(str1 + href_list[0])
        imdb_num = href_list[0].split('/')
        movie.imbd = imdb_num[2][2:]
        html = response.text
        response.raise_for_status()
        soup = BeautifulSoup(html, 'html.parser')

        span = soup.find('span', itemprop='ratingValue')
        if span != None:
            rating = span.text
            movie.imdb_rating = rating
        movie.save()
    return HttpResponse("123")




#把imbd和图片存入数据库
def pinjie(request):

    name = os.listdir('E:/django/myproject/bishe/bishe1/templates/imgs')
    for str1 in name:
        id_num = str1.split("_")[0]
        imdb = str1.split("_")[1].split(".")[0]
        #print(id_num+" "+imdb)
        movie = Movie.objects.get(id = id_num)
        movie.imbd = imdb
        movie.url = 'imgs/'+str1
        movie.save()
    return HttpResponse("123")

def read1(request):
    movies = Movie.objects.all()
    for movie in movies:
        response = requests.get('https://www.imdb.com/title/tt'+str(movie.imbd))
        print(response.url)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        rating = soup.find('span', itemprop='ratingValue').text
        movie.imdb_rating = rating
        movie.save()
    return HttpResponse("123")

def recommend(request):

    f = open('ratings.dat', 'r')
    lines = f.readlines()

    for line in lines:
        str = line[:-1]
        list1 = str.split("::")
        date = datetime.fromtimestamp(int(list1[3]))
        otherStyleTime = date.strftime("%Y-%m-%d")
        print(list1)

    f.close()
    return HttpResponse("123")







#*************************以上是数据处理***********************************
class ItemBasedCF():

    def __init__(self):

        self.n_sim_movie = 20
        self.n_rec_movie = 12

        self.trainSet = {}
        self.testSet = {}

        self.movie_sim_matrix = {}
        self.movie_popular = {}
        self.movie_count = 0
        print('Similar movie number = %d' % self.n_sim_movie)
        print('Recommneded movie number = %d' % self.n_rec_movie)

    def get_dataset(self):
        trainSet_len = 0;
        testSet_len = 0;
        f = open('ratings.dat', 'r')
        #i = 0
        lines = f.readlines()
        for line in lines:
            str1 = line[:-1]
            #print(str1)
            user,movie,rating,timestamp = str1.split("::")
            #if i > 8000:
             #   break
            #i = i + 1
            self.trainSet.setdefault(user,{})
            self.trainSet[user][movie] = float(rating)
            trainSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

            # else:
            #     self.testSet.setdefault(user,{})
            #     self.testSet[user][movie] = rating
            #     testSet_len += 1

    def calc_movie_sim(self):
        print("Calculating movie similarity matrix ...")
        for user,movies in self.trainSet.items():
            for movie in movies:
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                self.movie_popular[movie] += 1

        self.movie_count = len(self.movie_popular)

        for user,movies in self.trainSet.items():
            for movie in movies:
                for movie1 in movies:
                    if movie == movie1:
                        continue
                    self.movie_sim_matrix.setdefault(movie,{})
                    self.movie_sim_matrix[movie].setdefault(movie1,self.trainSet[user][movie1])
                    self.movie_sim_matrix[movie][movie1] += self.trainSet[user][movie1]

        for m1,related_movies in self.movie_sim_matrix.items():
            for m2,count in related_movies.items():
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                    matrix = RecommendMatrix()
                    matrix.id1 = int(m1)
                    matrix.id2 = int(m2)
                    matrix.factor = 0
                    matrix.save()
                else:
                    self.movie_sim_matrix[m1][m2] = count/math.sqrt(self.movie_popular[m1] * self.movie_popular[m2])
                    matrix = RecommendMatrix()
                    matrix.id1 = int(m1)
                    matrix.id2 = int(m2)
                    matrix.factor = self.movie_sim_matrix[m1][m2]
                    matrix.save()

    def recommend(self, user):
        K = self.n_sim_movie
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        for movie,rating in watched_movies.items():
            for related_movie, w in sorted(self.movie_sim_matrix[movie].items(),key=itemgetter(1),reverse=True)[:K]:
                if related_movie in watched_movies:
                    continue
                rank.setdefault(related_movie,0)
                rank[related_movie] += w * float(rating)
        return sorted(rank.items(),key=itemgetter(1),reverse=True)[:N]

def index(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    ratings = Rating.objects.filter(user_id=user.id)
    recommend = request.session.get("recommend")
    movies = []
    movies_list1 = []
    if recommend != None:
        for movie_id in recommend:
            movie = Movie.objects.get(id = movie_id[0])
            movies.append(movie)
        movie1 = movies[0:4]
        movie2 = movies[4:8]
        movie3 = movies[8:12]
        movies_list1 = [movie1, movie2, movie3]


    movies = []
    if ratings != None:
        for rating in ratings:
            movie = Movie.objects.get(id = rating.movies_id)
            movies.append(movie)
    context = {
        'ratings' : ratings,
        'movies' : movies,
        'movies_list1' : movies_list1,
    }
    return render(request, 'user_detail.html',context=context)

def index1(request,pindex=1):
    username = request.session.get('username')
    password = request.session.get('password')

    #用户点评过的所有电影

    if username == None:
        username=''
        password=''
    else:
        recommend=[]
        user = User.objects.filter(username=username)[0]
        id = user.id
        if Rating.objects.filter(user_id=id).exists() :
            user_ratings = Rating.objects.filter(user_id=id)
            dict = {}
            items=[]
            for rating in user_ratings:
                dict[rating.movies_id] = rating.rating
            request.session['user_ratings'] = dict

            # item_cf = ItemBasedCF()
            # item_cf.get_dataset()
            # item_cf.calc_movie_sim()
            # recommend = item_cf.recommend(str(id+6040))
            t0 = Rating.objects.filter(user_id=id)
            watched_movie = {}
            for movie in t0:
                watched_movie.setdefault(movie.movies_id,{})
                watched_movie[movie.movies_id] = movie.rating
            print(watched_movie)
            rank={}
            for movie,rating in watched_movie.items():
                t1 = RecommendMatrix.objects.filter(id2=movie)
                list1 = {}
                print(movie)
                print(rating)
                print(t1)
                for item in t1:
                    list1.setdefault(movie,{})
                    list1[movie][item.id1] = item.factor
                print(list1)
                for related_movie, w in sorted(list1[movie].items(),key=itemgetter(1),reverse=True)[:20]:


                    if related_movie in watched_movie:
                        continue
                    rank.setdefault(related_movie, 0)

                    rank[related_movie] += float(w) * rating
            recommend = sorted(rank.items(), key=itemgetter(1), reverse=True)[:12]

            print(recommend)

            request.session['recommend'] = recommend


    movies = Movie.objects.all()
    top_movies = Movie.objects.order_by('-imdb_rating')[0:10]
    genres = set()
    movies_list = []
    for movie in movies:
        list1 = movie.genres.split('|')
        for genre in list1:
            genres.add(genre)
        movies_list.append(movie)
    paginator = Paginator(movies_list,12)

    page = paginator.page(int(pindex))
    pindex = int(pindex)
    page_range = paginator.page_range
    if paginator.num_pages>10:
        if pindex<6:
            page_range=range(1,11)
        elif pindex+5>paginator.num_pages:
            page_range = range(pindex-5,paginator.num_pages+1)
        else:
            page_range = range(pindex-4,pindex+6)
    movies1 = page.object_list[0:4]
    movies2 = page.object_list[4:8]
    movies3 = page.object_list[8:12]
    movies_list1 = [movies1,movies2,movies3]
    # print(movies_list1)
    # print(movies_list2)
    # print(movies_list3)

    context = {
        'genre' : genres,
        'range' : [1,1,1],
        'movies' : movies,
        'page' : page,
        'page_range' : page_range,
        'movies_list1' : movies_list1,
        'username' : username,
        'password' : password,
        'top_movies' : top_movies,

    }




    return render(request,'index.html',context=context)


def index2(request,genres1,pindex):
    username = request.session.get('username')
    password = request.session.get('password')
    if username == None:
        username=''
        password=''
    movies = Movie.objects.all()
    top_movies = Movie.objects.order_by('-imdb_rating')[0:10]
    genres = set()
    movies_list = []
    for movie in movies:
        list1 = movie.genres.split('|')
        for genre in list1:
            genres.add(genre)
            if genre == genres1:
                movies_list.append(movie)


    paginator = Paginator(movies_list,12)

    page = paginator.page(int(pindex))
    pindex = int(pindex)
    page_range = paginator.page_range
    if paginator.num_pages > 10:
        if pindex < 6:
            page_range = range(1, 11)
        elif pindex + 5 > paginator.num_pages:
            page_range = range(pindex - 5, paginator.num_pages + 1)
        else:
            page_range = range(pindex - 4, pindex + 6)
    movies1 = page.object_list[0:4]
    movies2 = page.object_list[4:8]
    movies3 = page.object_list[8:12]
    movies_list1 = [movies1,movies2,movies3]
    # print(movies_list1)
    # print(movies_list2)
    # print(movies_list3)

    context = {
        'genre' : genres,
        'range' : [1,1,1],
        'movies' : movies,
        'page' : page,
        'page_range' : page_range,
        'movies_list1' : movies_list1,
        'username': username,
        'password': password,
        'top_movies': top_movies,
    }




    return render(request,'index.html',context=context)





def index3(request,title_douban):
    movie_detail = {}
    releasedates = []
    genres = []
    recommend=[]
    recommend1=[]
    recommend2=[]
    list1 = title_douban.split('&')
    douban = 0
    title = ""
    username = request.session.get("username")
    user_rating = -1
    if request.session.get("recommend") != None:
        for item in request.session.get("recommend"):

            movie = Movie.objects.get(id = item[0])
            recommend.append(movie)

        recommend1 = recommend[0:3]
        recommend2 = recommend[3:6]

    if username != None and Movie.objects.filter(title=list1[0]).exists():
        #user = User.objects.get(username=username)
        movie = Movie.objects.get(title=list1[0])
        dict = request.session.get("user_ratings")
        if dict!=None:
            for movie_id  in dict:
                if movie.id == int(movie_id):
                    user_rating = dict[movie_id]


    if len(list1)>1:
        title = list1[0]
        douban = list1[1]
        movies = Movie.objects.filter(title=title)
        movies1 = Movie.objects.filter(douban=douban)
    else:
        title = list1[0]

        movies = Movie.objects.filter(title=title)
        movies1 = []



    if movies.exists() and movies[0].douban != None :
        movie = movies[0]
        movie_detail['name'] = movie.title
        movie_detail['img'] = movie.url
        movie_detail['aditor'] = movie.aditor
        movie_detail['actor'] = movie.actor
        genres = movie.genres.split("|")
        movie_detail['ares'] = movie.ares
        releasedates = movie.releasedate.split("|")
        movie_detail['runtime'] = movie.runtime
        movie_detail['rename'] = movie.rename
        movie_detail['imdb'] = movie.imbd
        movie_detail['summary'] = movie.summary
        movie_detail['rating'] = movie.douban_rating
        movie_detail['rating1'] = movie.imdb_rating
    elif  len(movies1)>=1:
        movie = movies1[0]
        movie_detail['name'] = movie.title
        movie_detail['img'] = movie.url
        movie_detail['aditor'] = movie.aditor
        movie_detail['actor'] = movie.actor
        genres = movie.genres.split("|")
        movie_detail['ares'] = movie.ares
        releasedates = movie.releasedate.split("|")
        movie_detail['runtime'] = movie.runtime
        movie_detail['rename'] = movie.rename
        movie_detail['imdb'] = movie.imbd
        movie_detail['summary'] = movie.summary
        movie_detail['rating'] = movie.douban_rating
        movie_detail['rating1'] = movie.imdb_rating
    else:

        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('--window-position=-1920,100')
        flag = 0
        browser = webdriver.Chrome(chrome_options=chrome_options)
        if douban==0:
            if movies.exists() and movies[0].imbd != None:
                print(movies[0].imbd)
                print(movies[0].imdb_rating)
                flag = 1
                browser.get('https://search.douban.com/movie/subject_search?search_text=tt'+movies[0].imbd)
            else:
                print(title)
                browser.get('https://search.douban.com/movie/subject_search?search_text=' + title)
            #browser.get('https://movie.douban.com/subject/26931786/')
            html = browser.page_source

            #browser.close()
            print('111111')
            soup = BeautifulSoup(html, 'html.parser')
            movie_item = []
            i = 0
            for x in soup.find_all('div', class_='item-root'):
                movie = {}
                if not x.find('span', class_='rating_nums') is None or x.find('span',class_='pl')!=None:
                    movie['url'] = x.find('a').get('href')
                    movie['img'] = x.find('img').get('src')
                    if flag == 0:
                        movie['name'] = x.find('div', class_='title').string
                    else :
                        movie['name'] = movies[0].title
                    if x.find('span', class_='rating_nums') is None:
                        movie['rating'] = 0
                    else:
                        movie['rating'] = x.find('span', class_='rating_nums').string
                    movie['abstract'] = x.find('div', class_='meta abstract').string
                    movie['abstract1'] = x.find('div', class_='meta abstract_2').string
                    movie_item.append(movie)
                    i = i + 1
                if i > 0:
                    break

            browser.get(movie_item[0]['url'])
            print(movie_item[0]['url'])
            douban = movie_item[0]['url'].split('/')[4]

        else:
            douban_url = 'https://movie.douban.com/subject/'+str(douban)
            print(douban_url)
            browser.get(douban_url)
        html = browser.page_source
        browser.close()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())

        if flag == 1:
            movie_detail['name'] = title
        else:
            movie_detail['name'] = soup.find('span', property=("v:itemreviewed")).text
        if soup.find('img', title="点击看更多海报")!=None:
            movie_detail['img'] = soup.find('img', title="点击看更多海报").get('src')
        else:
            movie_detail['img'] = '无'
        if soup.find('span', text="编剧")==None:
            movie_detail['aditor'] = soup.find('span', text="导演").nextSibling.nextSibling.text
        else:
            movie_detail['aditor'] = soup.find('span', text="编剧").nextSibling.nextSibling.text
        if soup.find('span', text="主演")==None:
            movie_detail['actor'] = '无'
        else:
            movie_detail['actor'] = soup.find('span', text="主演").nextSibling.nextSibling.text
        movie_detail['genre'] = soup.find_all('span', property="v:genre")
        movie_detail['ares'] = soup.find('span', text='制片国家/地区:').nextSibling
        movie_detail['releasedate'] = soup.find_all('span', property="v:initialReleaseDate")
        if soup.find('span', property="v:runtime")==None:
            movie_detail['runtime'] = '未知'
        else:
            movie_detail['runtime'] = soup.find('span', property="v:runtime").text
        if soup.find('span', text="又名:")==None:
            movie_detail['rename'] = '无'
        else:
            movie_detail['rename'] = soup.find('span', text="又名:").nextSibling
        movie_detail['imdb'] = soup.find('span', text="IMDb链接:").nextSibling.nextSibling.text
        if soup.find('span', property="v:summary") == None:
            movie_detail['summary'] = '无'
        else:
            movie_detail['summary'] = soup.find('span', property="v:summary").text

        if  soup.find('strong',class_="ll rating_num") is None:
            print("111")
            movie_detail['rating'] = 0
        else:
            print("222")
            if soup.find('strong',class_="ll rating_num").text=='':
                movie_detail['rating'] = 0
            else:
                movie_detail['rating'] = float(soup.find('strong',class_="ll rating_num").text)
        # print(movie_detail)
        for genre in movie_detail['genre']:
            genres.append(genre.text)

        for releasedate in movie_detail['releasedate']:
            releasedates.append(releasedate.text)
        print(movie_detail['imdb'])
        if len(Movie.objects.filter(imbd=movie_detail['imdb'][2:])) != 0 :

            movies = Movie.objects.filter(imbd=movie_detail['imdb'][2:])
            #print(movies[0].title)
            #print(movies[1].title)
            movie = movies[0]
            if movie.url == None:
                response = requests.get(movie_detail['img'])
                with open("templates/imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp", "wb") as f:
                  f.write(response.content)
                movie.url = "imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp"
                movie_detail['img'] = movie.url
            else:
                movie_detail['img'] = movie.url
            movie.title = title
            movie.aditor = movie_detail['aditor']
            movie.actor = movie_detail['actor']
            i = 0
            for genre in genres:
                if i == 0:
                    movie.genres = genre
                else:
                    movie.genres = movie.genres+'|'+genre
                i = i + 1
            movie.ares = movie_detail['ares']
            i = 0
            for releasedate in releasedates:
                if i == 0:
                    movie.releasedate = releasedate
                else:
                    movie.releasedate = movie.releasedate+"|"+releasedate

            movie.rename = movie_detail['rename']
            movie.douban = douban
            movie.summary = movie_detail['summary']
            movie.douban_rating =movie_detail['rating']
            movie.runtime = movie_detail['runtime']
            movie.imbd = movie_detail['imdb'][2:]
            movie.save()
        elif len(Movie.objects.filter(douban=douban)) != 0:
            movies = Movie.objects.filter(douban = douban)
            # print(movies[0].title)
            # print(movies[1].title)
            movie = movies[0]
            if movie.url == None:
                response = requests.get(movie_detail['img'])
                with open("templates/imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp", "wb") as f:
                    f.write(response.content)
                movie.url = "imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp"
                movie_detail['img'] = movie.url
            else:
                movie_detail['img'] = movie.url
            movie.title = title
            movie.aditor = movie_detail['aditor']
            movie.actor = movie_detail['actor']
            i = 0
            for genre in genres:
                if i == 0:
                    movie.genres = genre
                else:
                    movie.genres = movie.genres + '|' + genre
                i = i + 1
            movie.ares = movie_detail['ares']
            i = 0
            for releasedate in releasedates:
                if i == 0:
                    movie.releasedate = releasedate
                else:
                    movie.releasedate = movie.releasedate + "|" + releasedate

            movie.rename = movie_detail['rename']
            movie.douban = douban
            movie.summary = movie_detail['summary']
            movie.douban_rating = movie_detail['rating']
            movie.runtime = movie_detail['runtime']
            movie.imbd = movie_detail['imdb'][2:]
            movie.save()
        elif len(Movie.objects.filter(title=title)) != 0:
            movies = Movie.objects.filter(title=title)
            # print(movies[0].title)
            # print(movies[1].title)
            movie = movies[0]
            if movie.url == None:
                response = requests.get(movie_detail['img'])
                with open("templates/imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp", "wb") as f:
                    f.write(response.content)
                movie.url = "imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp"
                movie_detail['img'] = movie.url
            else:
                movie_detail['img'] = movie.url
            movie.title = title
            movie.aditor = movie_detail['aditor']
            movie.actor = movie_detail['actor']
            i = 0
            for genre in genres:
                if i == 0:
                    movie.genres = genre
                else:
                    movie.genres = movie.genres + '|' + genre
                i = i + 1
            movie.ares = movie_detail['ares']
            i = 0
            for releasedate in releasedates:
                if i == 0:
                    movie.releasedate = releasedate
                else:
                    movie.releasedate = movie.releasedate + "|" + releasedate

            movie.rename = movie_detail['rename']
            movie.douban = douban
            movie.summary = movie_detail['summary']
            movie.douban_rating = movie_detail['rating']
            movie.runtime = movie_detail['runtime']
            movie.imbd = movie_detail['imdb'][2:]
            movie.save()
        else:
            movie = Movie()
            response = requests.get(movie_detail['img'])
            if movie.url == None:
                response = requests.get(movie_detail['img'])
                with open("templates/imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp", "wb") as f:
                  f.write(response.content)
                movie.url = "imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp"
                movie_detail['img'] = movie.url
            else:
                movie_detail['img'] = movie.url
            movie.title = title
            movie.aditor = movie_detail['aditor']
            movie.actor = movie_detail['actor']
            i = 0
            for genre in genres:
                if i == 0:
                    movie.genres = genre
                else:
                    movie.genres = movie.genres + '|' + genre
                i = i + 1
            movie.ares = movie_detail['ares']
            i = 0
            for releasedate in releasedates:
                if i == 0:
                    movie.releasedate = releasedate
                else:
                    movie.releasedate = movie.releasedate + "|" + releasedate
            movie.rename = movie_detail['rename']
            movie.douban = douban
            movie.summary = movie_detail['summary']
            movie.douban_rating = movie_detail['rating']
            movie.runtime = movie_detail['runtime']
            movie.save()








        #print(movie_detail['genre'])
        #print(movie_detail['genre'][0].text)
        #response = requests.get(movie_detail['img'])
        #with open("static/imgs/" + movie_detail['imdb'].split('tt')[1] + ".webp", "wb") as f:
        #    f.write(response.content)

    context = {
        'movie_detail' : movie_detail,
        'movie_url' : movie_detail['img'],
        'releasedates' : releasedates,
        'genres' : genres,
        'user_rating':user_rating,
        'recommend1' : recommend1,
        'recommend2' : recommend2,

    }
    return render(request,'index1.html',context=context)

def movie(request):
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--window-position=-1920,100')
    title = request.GET.get('search')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('https://search.douban.com/movie/subject_search?search_text='+title)
    #browser.get('https://movie.douban.com/subject/26931786/')
    html = browser.page_source

    #browser.close()
    # print(browser.page_source)
    soup = BeautifulSoup(html, 'html.parser')
    browser.close()
    movie_item = []
    i = 0
    for x in soup.find_all('div', class_='item-root'):
        movie = {}
        if not x.find('span', class_='rating_nums') is None:
            #分出豆瓣号
            movie['url'] = x.find('a').get('href').split("/")[4]
            movie['img'] = x.find('img').get('src')
            movie['name'] = x.find('a', class_='title-text').string
            movie['rating'] = x.find('span', class_='rating_nums').string
            movie['abstract'] = x.find('div', class_='meta abstract').string
            movie['abstract1'] = x.find('div', class_='meta abstract_2').string
            movie_item.append(movie)






    context = {
        'movie_item' : movie_item,
    }
    return render(request,'detail.html',context=context)

def login(request):
    if request.POST.get('username')==None:
        print("111")
        return render(request,'login.html')
    else:
        print("222")
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username)
            if user[0].password != password:
                print("333")
                return render(request, 'login.html')
            else:
                print("444")
                request.session['username'] = username
                request.session['password'] = password
                return redirect('../list/1')
        else:
            print("555")
            return render(request, 'login.html')
def register(request):
    if request.POST.get('username')==None:
        print("111")
        return render(request,'register.html')

    else:
        username = request.POST.get('username')
        print("222")
        if not User.objects.filter(username=username).exists():
            password = request.POST.get('password')
            user = User()
            user.username = username
            user.password = password
            user.save()
            print("333")
            return redirect('/login/')
        else:
            print("444")
            return render(request,'register.html')
#放弃
# def rating(request):
#     ratings = request.POST.get("rating")
#     username = request.POST.get("username")
#     moviename = request.POST.get("moviename")
#     user = User.objects.get(username=username)
#     movie = Movie.objects.get(moviename=moviename)
#     user_rating = Rating()
#     user_rating.rating = ratings
#     user_rating.movies_id = movie.id
#     user_rating.user_id = user.id
#     now = datetime.now()
#     user_rating.datetime = now
#     user_rating.save()
#     return redirect(request,'../detail/'+)
def rating(request):
    username = request.POST.get("username")
    rating = request.POST.get("rating")
    moviename = request.POST.get("moviename")
    user = User.objects.get(username=username)
    movie = Movie.objects.get(title=moviename)
    #user的所有评分记录
    user_ratings = request.session.get("user_ratings")
    if user_ratings!=None and str(movie.id) in user_ratings and Rating.objects.filter(user_id=user.id).exists():
        user_rating = Rating.objects.filter(user_id=user.id)
        for my_rating in user_rating:
            if my_rating.movies_id == movie.id:
                my_rating.rating = rating
                now = datetime.now()
                my_rating.datetime = datetime.now()
                my_rating.save()
                user_ratings[str(movie.id)] = rating

                request.session['user_ratings'] = user_ratings
                f = open('ratings.dat', 'r')
                lines = f.readlines()
                lines_copy=str(user.id+6040) + "::" + str(movie.id) + "::" + str(rating) + "::" + str(int(time.mktime(now.timetuple()))) + "\n"
                for line in lines:
                    str0 = line[:-1]
                    list1 = str0.split("::")
                    if str(user.id+6040) in list1 and str(movie.id) in list1:
                        # 加上训练集中的用户数
                        pass
                    else:
                        lines_copy = lines_copy + line
                f.close()
                f = open('ratings.dat','w')
                f.write(lines_copy)
                f.close()

                break

    else:
        user_rating = Rating()
        user_rating.rating = rating
        user_rating.movies_id = movie.id
        user_rating.user_id = user.id
        now = datetime.now()
        user_rating.datetime = now
        user_rating.save()
        if user_ratings == None:
            user_ratings = {}
            user_ratings[str(movie.id)] = rating
            request.session['user_ratings'] = user_ratings
        else:
            user_ratings[str(movie.id)] = rating
            request.session['user_ratings'] = user_ratings
        #加上训练集中的用户数
        str1 = str(user.id+6040)+"::"+str(movie.id)+"::"+str(rating)+"::"+str(int(time.mktime(now.timetuple())))+"\n"
        #写到文件的第一行，因为数据集读不完
        with open('ratings.dat', 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(str1+content)



    return HttpResponse(rating)
def logout(request):
    request.session.flush()
    return redirect('../login/')

if __name__ == "__main__":
    item_cf = ItemBasedCF()
    item_cf.get_dataset()
    item_cf.calc_movie_sim()
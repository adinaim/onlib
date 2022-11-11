import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import random

from slugify import *


class GenSpiderSpider(scrapy.Spider):
    name = 'gen_spider'
    allowed_domains = ['mybook.ru']
    start_urls = ['http://mybook.ru/']

    def parse(self, response):
        pass


class AuthorSpider(CrawlSpider):   # scrapy.Spider
    name = 'mybook'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
        Rule(LinkExtractor(allow='catalog/klassika/')),
        Rule(LinkExtractor(allow='author'), callback='parse_author')
        )

    def parse_author(self, response):
        name = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ')
        first_name = name.split()[0]
        last_name = name.split()[1]
        avatar = response.xpath('//div/picture/source/@srcset').get().split(',')[0]   
        bio = response.css('div.iszfik-2.gAFRve p::text').get() 
        slug = slugify(name)

        author = { 
            'first_name': first_name,
            'last_name': last_name,
            'avatar': avatar,
            'bio': bio,
            'name': name, 
            'slug': slug
        }

        return author

# class Authors(Model):
#     def __init__(self, first_name, last_name, about, avatar, slug):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.avatar = avatar
#         self.about = about
#         self.slug = slug






class BookSpider(CrawlSpider):   # scrapy.Spider
    name = 'mybook'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
        Rule(LinkExtractor(allow='catalog/books')),
        Rule(LinkExtractor(allow='author'), callback='parse_book')
        )

    def parse_book(self, response):
        title = response.css('h1.sc-bdfBwQ.lnjchu-0.jzwvLi.gUKDCi.sc-1c0xbiw-11.bzVsYa::text').get().replace('&nbsp;', ' ')
        slug = slugify(title)
        image_link = response.xpath('//div/picture/source/@srcset').get().split(',')[0]    
        description = response.css('div.iszfik-2.gAFRve p::text').get() 
        genres = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()
        author = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ')
        pages = response.css('div.ant-col.sc-1c0xbiw-9.bhxaWx.ant-col-xs-11.ant-col-md-8.ant-col-xl-12 p.lnjchu-1.dPgoNf::text').get().split(' ')[0]
        year = response.xpath('//*[@id="__next"]/div/section/div[1]/div[3]/div[1]/div/div/div[5]/p[2]/text()[1]').get().replace('&nbsp;', ' ').split()[0]
        # "//div[@aria-label='bedrooms']/div[2]/text()"
        number_of_copies = random.randint(1, 10)
        number_available = number_of_copies - 1
        status = 'available'

        genre = []
        for topic in genres:
            topic.capitalize()
            genre.append(topic)
              
# class AuthorItem(Item):
#     first_name = Field()
#     last_name = Field()
#     about = Field()
#     avatar = Field()
#     slug = Field()

        book = {
            'title': title,
            'image_link': image_link,
            'description': description,
            'slug': slug,
            'genre': genre,
            'number_of_copies': random.randint(1, 10),
            'number_available': number_available,
            'year': year,
            'pages': pages,
            'author': author,
            'status': status 
            }
        
        return book

# class Books(Model):
#     def __init__(self, title, author, description, image_link, slug, genre, year, pages, status, number_of_copies, number_available):
#         self.title = title
#         self.author = author
#         self.image_link = image_link
#         self.description = description
#         self.slug = slug
#         self.genre = genre
#         self.year = year
#         self.pages = pages
#         self.status = status
#         self.number_of_copies = number_of_copies
#         self.number_available = number_available




class GenSpiderSpider(CrawlSpider):   # scrapy.Spider
    name = 'mybook'
    start_urls = ['https://mybook.ru/']

    # def __init__(self):
    #     self.data = []
    #     self.rules = (
    #     Rule(LinkExtractor(allow='catalog/books')),
    #     Rule(LinkExtractor(allow='author'), callback='parse_books')
    #     )
    #     self.data.extend(self.rules)
    rules = (
            Rule(LinkExtractor(allow='catalog/klassika/books')),
            Rule(LinkExtractor(allow='author'), callback='parse_genre')
            )

    def parse_genre(self, response):
        jobs = []

        genres_list = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()

        for genres in genres_list:
            genre = genres.capitalize()
            return genre
    
            

        row_data = zip(genre, slug=slugify(genre))

        for item in row_data:
            scraped_info ={
                'genre': genre,
                
            }
        yield jobs



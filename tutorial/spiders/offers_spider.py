import scrapy
from tutorial.items import OfferItem

class OffersSpider(scrapy.Spider):
  name = "offers"

  start_urls = ["https://stackoverflow.com/jobs"]

  def parse(self, response):
    for offer in response.css('div.-job'):
      item = OfferItem()
      item['technologies'] = offer.css('a.post-tag::text').getall()
      item['city'] = offer.css('h3 span::text').getall()[1]
      item['salary'] = offer.css('.horizontal-list li::attr(title)').getall()
      yield item
    pages = response.css('a.s-pagination--item::attr(title)').getall()
    next_page_href = response.css('a.s-pagination--item::attr(href)').getall()

    total_pages = pages[len(pages) - 2].split(' ')[3]
    next_page = pages[len(pages) - 1].split(' ')[1]

    next_page_link = 'https://stackoverflow.com' + next_page_href[len(next_page_href) - 1]

    if int(next_page) <= int(total_pages):
      next_page_add = response.urljoin(next_page_link)
      yield scrapy.Request(next_page_add, callback =self.parse)

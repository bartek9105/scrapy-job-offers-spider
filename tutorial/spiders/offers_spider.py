import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'offers'

    def start_requests(self):
        urls = ['https://stackoverflow.com/jobs']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)       

    def parse(self, response):
        results = {}
        offers = response.css('div.listResults a.post-tag::text').getall()

        next_page = response.css('div.s-pagination a.s-pagination--item:last-child::attr(href)').get()        

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)

        for offer in offers: 
            if (offer in results):
                results[offer] += 1
            else:
                results[offer] = 1

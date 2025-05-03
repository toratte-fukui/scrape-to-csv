import time

import scrapy


class AucfunSpider(scrapy.Spider):
    name = "aucfun"
    allowed_domains = ["aucfan.com"]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    current_page = 1

    def __init__(self, url=None, num=1, *args, **kwargs):
        super(AucfunSpider, self).__init__(*args, **kwargs)
        self.start_url = url  # コマンドライン引数から受け取ったURL
        self.num = int(num)
        print(self.start_url)
        print(self.num)

    def start_requests(self):
        if self.start_url:
            self.logger.info("========= スクレイピングを開始します =========")
            time.sleep(1)
            yield scrapy.Request(url=self.start_url, callback=self.parse)
        else:
            # コマンドライン引数が指定されていない場合は、ユーザーに入力を促す
            self.logger.error(
                "aucfunの検索結果ページurlを入力してください。最大ページ数も指定できます。"
            )
            self.logger.error(
                '例：python aucfun_scraper -url "https://aucfan.com/search1/..." -num 1'
            )

    def parse(self, response):
        # 検索画面から商品一覧を取得
        items = response.xpath('//section[contains(@class, "searchShowcaseType01")]')
        # 各商品の詳細ページへのリンクを取得
        item_detail_urls = [
            item.xpath('.//h2/a[@class="hdLink"]/@href').get() for item in items
        ]

        for url in item_detail_urls:
            yield scrapy.Request(
                url, callback=self.__parse_item_detail, headers=self.headers
            )

        next_page = response.xpath('//li[@class="next"]/a/@href').get()

        # 次のページがある場合は再帰的に処理を続ける
        if next_page and self.num >= self.current_page:
            self.logger.info(f"========= {self.current_page}ページ目を取得中 =========")
            self.current_page += 1
            yield response.follow(url=next_page, callback=self.parse)

    def __parse_item_detail(self, response):
        """商品詳細ページの情報を取得する"""
        # 商品名称を取得
        result = {"title": response.xpath('//h1[@class="hdMainItemTxt"]/text()').get()}

        # 商品詳細を取得
        item_details = response.xpath(
            '//div[contains(@class,"itemsDetailsTabContWrap")]/div/div[contains(@class,"tabContBlock")]'
        )
        for item_detail in item_details:
            contents = item_detail.xpath('.//dl[@class="itemContDl"]')
            for content in contents:
                label = content.xpath(".//dt/text()").get()
                value = content.xpath(".//dd/text()").get()
                match (label):
                    case "落札価格":
                        result["end_price"] = value
                    case "開始価格":
                        result["start_price"] = value
                    case "開始日時":
                        result["start_datetime"] = value
                    case "終了日時":
                        result["end_datetime"] = value

        # 商品ページURLを取得
        result["url"] = response.url

        # 商品画像URLを取得
        # result["image_url"] = response.xpath('//img[@class="mainImage"]/@src').get()

        self.logger.info(result)
        yield result
        # yield {
        #     "Title": item.xpath(".//h1/text()").get(),
        #     "Price": item.xpath('.//span[@class="price"]/text()').get(),
        #     "BidNum": item.xpath('.//span[@class="bidNum"]/text()').get(),
        #     "StartDatetime": item.xpath('.//span[@class="startDatetime"]/text()').get(),
        #     "EndDatetime": item.xpath('.//span[@class="endDatetime"]/text()').get(),
        #     "URL": response.url,
        #     "ImageURL": item.xpath('.//img[@class="mainImage"]/@src').get(),
        #     "ImageURL2": item.xpath('.//img[@class="subImage1"]/@src').get(),
        #     "ImageURL3": item.xpath('.//img[@class="subImage2"]/@src').get(),
        # }

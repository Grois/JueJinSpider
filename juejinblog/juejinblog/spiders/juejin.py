# -*- coding: utf-8 -*-
import scrapy
from juejinblog.items import JuejinblogItem
import json


class JuejinSpider(scrapy.Spider):
    name = 'juejin'
    allowed_domains = ['juejin.im']
    start_urls = ['https://juejin.im/user/56f3db6d1ea49300558b75f4']

    def parse(self, response):
        item = JuejinblogItem()
        name = response.xpath("//h1/text()").extract()[0]
        uid = response.xpath("//meta[@itemprop='url']/@content").extract()[0].replace('https://juejin.im/user/', '')

        spans = response.xpath("//div[@class='position']//span[@class='content']/span")
        job = ''
        company = ''
        if len(spans) == 3:
            job = spans[0].xpath("./text()").extract_first()
            company = spans[2].xpath("./text()").extract_first()

        describle = ''
        if response.xpath("//div[@class='intro']//text()").extract():
            describle = response.xpath("//div[@class='intro']//text()").extract()[-1]

        image = response.xpath("//meta[@itemprop='image']/@content").extract_first()
        follow_text = response.xpath(
            "//div[@class='follow-block block shadow']//div[@class='item-count']//text()").extract()
        follow = follow_text[0]
        follower = follow_text[1]

        if image is None:
            image = ''

        item['name'] = name
        item['uid'] = uid
        item['image'] = image
        item['company'] = company
        item['job'] = job
        item['describle'] = describle
        item['follow'] = follow
        item['follower'] = follower
        # 将当前用户信息保存
        yield item

        # 开始获取前20个关注者列表
        follower_url = 'https://follow-api-ms.juejin.im/v1/getUserFollowerList?src=web&uid=' + item['uid']
        yield scrapy.Request(url=follower_url, meta={'uid': item['uid'], 'type': 'follower'}, callback=self.parse_api)

        # 开始获取自己关注用户
        followee_url = 'https://follow-api-ms.juejin.im/v1/getUserFolloweeList?uid=' + item['uid'] + '&src=web'
        yield scrapy.Request(url=followee_url, meta={'uid': item['uid'], 'type': 'followee'}, callback=self.parse_api)

    def parse_api(self, response):
        obj = json.loads(response.text)
        uid = response.meta['uid']
        user_type = response.meta['type']
        users = obj.get('d')
        if len(users) > 0:
            for user in users:
                url = 'https://juejin.im/user/' + user.get(user_type).get('objectId')
                yield scrapy.Request(url=url, callback=self.parse)

        # 获取的数据是20个  就往下边翻一页
        if len(users) == 20:
            before = users[-1].get('updatedAtString')
            if user_type == 'follower':
                url = 'https://follow-api-ms.juejin.im/v1/getUserFollowerList?uid=' + uid + '&before=' + before + '&src=web'
            else:
                url = 'https://follow-api-ms.juejin.im/v1/getUserFolloweeList?uid=' + uid + '&before=' + before + '&src=web'
            yield scrapy.Request(url=url, meta={'uid': uid, 'type': user_type}, callback=self.parse_api)

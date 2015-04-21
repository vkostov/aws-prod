__author__ = 'vkostov'

from cement.core import foundation, backend, controller, handler
from cement.utils.misc import init_defaults
from bottlenose import Amazon
from bs4 import BeautifulSoup

VERSION = '0.0.3'

BANNER = """
aws-prod v%s
""" % VERSION

# set default config options
defaults = init_defaults('aws-prod')
defaults['aws-prod']['debug'] = False

# define app base controller

class AwsProdBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "CLI for Amazon Product Advertising API"

        config_defaults = dict(
            foo='bar',
            some_other_option='my default value'
        )

        arguments = [
            (['-f', '--foo'], dict(action='store', help='the notorious foo option')),
            (['-C'], dict(action='store_true', help='the big C option')),
            (['-v', '--version'], dict(action='version', version=BANNER))
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        self.app.log.info('Inside base.default function.')
        if self.app.pargs.foo:
            self.app.log.info("Received option 'foo' with value '%s'." % self.app.pargs.foo)

    @controller.expose(aliases=['cmd2'], help="more of nothing.")
    def command2(self):
        self.app.log.info("Inside base.command2 function.")


class ItemSearchController(controller.CementBaseController):
    class Meta:
        label = 'item-search'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "ItemSearch operation"
        arguments = [
            (['-k', '--keywords'], dict(action='store', help='Keywords to search for')),
            (['-i', '--search-index'], dict(action='store', help='SearchIndex. All, Books, Shoes, etc')),
            (['-g', '--response-group'], dict(action='store', help='ResponseGroup. Images, Large etc')),
            (['-t', '--output'], dict(action='store', help='Output format: titles or full')),
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        aws_access_key_id = self.app.config.get('default', 'aws_access_key_id')
        aws_secret_access_key = self.app.config.get('default', 'aws_secret_access_key')
        aws_associate_tag = self.app.config.get('default', 'AWS_SECRET_ACCESS_KEY')
        max_pages=10


        self.app.log.info("Inside item-search.default function.")
        amazon = Amazon(aws_access_key_id, aws_secret_access_key, aws_associate_tag, Parser=BeautifulSoup)
        keywords = self.app.pargs.keywords
        response = amazon.ItemSearch(Keywords=keywords, SearchIndex="Shoes", BrowseNode="679286011")
        total_pages = int(response.find('totalpages').string)
        print(total_pages)

        if(self.app.pargs.output and self.app.pargs.output == 'titles'):
            titles = response.find_all('title')
            for title in titles:
                print(title.string)
        else:
            print(response.prettify())

        for page_num in range(2, max_pages):
            response = amazon.ItemSearch(Keywords=keywords, SearchIndex="Shoes", BrowseNode="679286011", ItemPage=page_num)

            if(self.app.pargs.output and self.app.pargs.output == 'titles'):
                titles = response.find_all('title')
                for title in titles:
                    print(title.string)
            else:
                print(response.prettify())


class AwsProdApp(foundation.CementApp):
    class Meta:
        label = 'aws-prod'
        base_controller = AwsProdBaseController


def main():
    # create the app
    app = AwsProdApp()

    # register controllers
    handler.register(AwsProdBaseController)
    handler.register(ItemSearchController)

    try:
        app.setup()
        app.run()
    finally:
        app.close()


if __name__ == '__main__':
    main()

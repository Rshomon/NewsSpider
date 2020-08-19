from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose,Join


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # name_in = MapCompose(unicode.title)
    name_out = Join()

    # price_in = MapCompose(unicode.strip)
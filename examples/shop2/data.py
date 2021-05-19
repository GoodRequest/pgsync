import json

import click
from schema import Product, ProductCategory, Seller, Renter, Service, ServiceItem, ServiceProductCategory
from sqlalchemy.orm import sessionmaker

from pgsync.base import pg_engine, subtransactions
from pgsync.helper import teardown
from pgsync.utils import get_config


@click.command()
@click.option(
    '--config',
    '-c',
    help='Schema config',
    type=click.Path(exists=True),
)
def main(config):

    config = get_config(config)
    teardown(drop_db=False, config=config)
    documents = json.load(open(config))
    engine = pg_engine(
        database=documents[0].get('database', documents[0]['index'])
    )
    Session = sessionmaker(bind=engine, autoflush=True)
    session = Session()

    product_categories = {
        'productCategory1': ProductCategory(id=1, name='productCategory1'),
        'productCategory2': ProductCategory(id=2, name='productCategory2'),
        'productCategory3': ProductCategory(id=3, name='productCategory3'),
        'productCategory4': ProductCategory(id=4, name='productCategory4')
    }
    with subtransactions(session):
        session.add_all(product_categories.values())

    products = [
        Product(id=1, name='product1', productCategory=product_categories['productCategory1']),
        Product(id=2, name='product2', productCategory=product_categories['productCategory1']),
        Product(id=3, name='product3', productCategory=product_categories['productCategory2']),
        Product(id=4, name='product4', productCategory=product_categories['productCategory2']),
        Product(id=5, name='product5', productCategory=product_categories['productCategory3']),
        Product(id=6, name='product6', productCategory=product_categories['productCategory3']),
        Product(id=7, name='product7', productCategory=product_categories['productCategory4']),
        Product(id=8, name='product8', productCategory=product_categories['productCategory4'])
    ]
    with subtransactions(session):
        session.add_all(products)

    services = {
        'saleService1': Service(id=1, name='saleService1'),
        'saleService2': Service(id=2, name='saleService2'),
        'rentService1': Service(id=3, name='rentService1'),
        'rentService2': Service(id=4, name='rentService2')
    }
    with subtransactions(session):
        session.add_all(services.values())

    service_items = [
        ServiceItem(id=1, name='saleService1 item', service=services['saleService1']),
        ServiceItem(id=2, name='saleService2 item', service=services['saleService2']),
        ServiceItem(id=3, name='rentService1 item', service=services['rentService1']),
        ServiceItem(id=4, name='rentService2 item', service=services['rentService2'])
    ]
    with subtransactions(session):
        session.add_all(service_items)

    sellers = {
        'seller1': Seller(id=1, name='seller1'),
        'seller2': Seller(id=2, name='seller2'),
        'seller3': Seller(id=3, name='seller3'),
        'seller4': Seller(id=4, name='seller4')
    }
    with subtransactions(session):
        session.add_all(sellers.values())

    renters = {
        'renter1': Renter(id=1, name='renter1'),
        'renter2': Renter(id=2, name='renter2'),
        'renter3': Renter(id=3, name='renter3'),
        'renter4': Renter(id=4, name='renter4')
    }
    with subtransactions(session):
        session.add_all(renters.values())

    service_product_categoryies = [
        ServiceProductCategory(
            productCategory=product_categories['productCategory1'],
            sellerService=services['saleService1'],
            seller=sellers['seller1'],
            renterService=services['rentService1'],
            renterOne=renters['renter1'],
            renterTwo=renters['renter2']
        ),
        ServiceProductCategory(
            productCategory=product_categories['productCategory1'],
            sellerService=services['saleService2'],
            seller=sellers['seller2'],
            renterService=services['rentService2'],
            renterOne=renters['renter3'],
            renterTwo=renters['renter4'],
        )
    ]
    with subtransactions(session):
        session.add_all(service_product_categoryies)


if __name__ == '__main__':
    main()

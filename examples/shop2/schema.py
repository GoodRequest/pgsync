import json

import click
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from pgsync.base import create_database, pg_engine
from pgsync.helper import teardown
from pgsync.utils import get_config

Base = declarative_base()


class ProductCategory(Base):
    __tablename__ = 'product_categories'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class Product(Base):
    __tablename__ = 'products'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    productCategoryID = sa.Column(sa.Integer, sa.ForeignKey(ProductCategory.id), nullable=False)
    productCategory = sa.orm.relationship(
        ProductCategory,
        backref=sa.orm.backref('product_product_category'),
    )


class Service(Base):
    __tablename__ = 'services'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class Seller(Base):
    __tablename__ = 'sellers'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class Renter(Base):
    __tablename__ = 'renters'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class ServiceProductCategory(Base):
    __tablename__ = 'service_product_categories'
    id = sa.Column(sa.Integer, primary_key=True)
    productCategoryID = sa.Column(sa.Integer, sa.ForeignKey(ProductCategory.id), nullable=False)
    productCategory = sa.orm.relationship(
        ProductCategory,
        backref=sa.orm.backref('service_product_category_seller_product_category'),
    )
    sellerServiceID = sa.Column(sa.Integer, sa.ForeignKey(Service.id), nullable=True)
    sellerService = sa.orm.relationship(
        Service,
        backref=sa.orm.backref('service_product_category_seller_service'),
        foreign_keys=[sellerServiceID]
    )
    sellerID = sa.Column(sa.Integer, sa.ForeignKey(Seller.id), nullable=True)
    seller = sa.orm.relationship(
        Seller,
        backref=sa.orm.backref('service_product_category_seller_seller'),
    )
    renterServiceID = sa.Column(sa.Integer, sa.ForeignKey(Service.id), nullable=True)
    renterService = sa.orm.relationship(
        Service,
        backref=sa.orm.backref('service_product_category_renter_service'),
        foreign_keys=[renterServiceID]
    )
    renterOneID = sa.Column(sa.Integer, sa.ForeignKey(Renter.id), nullable=True)
    renterOne = sa.orm.relationship(
        Renter,
        backref=sa.orm.backref('service_product_category_renter_renterOne'),
        foreign_keys=[renterOneID]
    )
    renterTwoID = sa.Column(sa.Integer, sa.ForeignKey(Renter.id), nullable=True)
    renterTwo = sa.orm.relationship(
        Renter,
        backref=sa.orm.backref('service_product_category_renter_renterTwo'),
        foreign_keys=[renterTwoID]
    )


class ServiceItem(Base):
    __tablename__ = 'service_items'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    serviceID = sa.Column(sa.Integer, sa.ForeignKey(Service.id), nullable=False)
    service = sa.orm.relationship(
        Service,
        backref=sa.orm.backref('service_item_service'),
    )


class PriceItem(Base):
    __tablename__ = 'price_items'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    serviceItemID = sa.Column(sa.Integer, sa.ForeignKey(ServiceItem.id), nullable=False)
    serviceItem = sa.orm.relationship(
        ServiceItem,
        backref=sa.orm.backref('price_item_service_item'),
    )


def setup(config=None):
    for document in json.load(open(config)):
        database = document.get('database', document['index'])
        create_database(database)
        engine = pg_engine(database=database)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


@click.command()
@click.option(
    '--config',
    '-c',
    help='Schema config',
    type=click.Path(exists=True),
)
def main(config):

    config = get_config(config)
    teardown(config=config)
    setup(config)


if __name__ == '__main__':
    main()

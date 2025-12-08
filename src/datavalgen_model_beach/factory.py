from datetime import datetime
from datavalgen.factory import BaseDataModelFactory
from polyfactory.decorators import post_generated
from .model import DataModel


class DataModelFactory(BaseDataModelFactory):
    """Factory for generating data model instances."""

    __model__ = DataModel


    @post_generated
    @classmethod
    def end_date(cls, start_date: datetime) -> datetime:
        # generate dates between start_date and right bound of
        # end_date (lower than)
        return cls.__faker__.date_between_dates(
            date_start=start_date,
            date_end=cls.get_field_constraint("end_date", "lt"),
        )

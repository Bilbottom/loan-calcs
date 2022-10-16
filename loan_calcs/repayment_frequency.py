"""
The loan repayment frequency.

This is flexible enough to support frequencies such as "every 2 months" instead of the usual "monthly" or "quarterly"
frequencies that loan repayments are usually made over.
"""
from enum import Enum, auto


# noinspection PyArgumentList
class RepaymentInterval(Enum):
    """The interval over which the repayments are made."""
    YEARLY = auto()
    MONTHLY = auto()
    WEEKLY = auto()
    DAILY = auto()


class RepaymentFrequency(Enum):
    """The frequency with which the repayments are made."""
    def __init__(
        self,
        repayment_unit: RepaymentInterval,
        repayment_frequency: int,
        total_repayments: int
    ):
        """
        Defines a repayment schedule.

        :param repayment_unit: The calendar interval over which repayments are made.
        :param repayment_frequency: The number of calendar intervals between repayments.
        :param total_repayments: The total number of repayments.
        """
        self.repayment_unit = repayment_unit
        self.repayment_frequency = repayment_frequency
        self.total_repayments = total_repayments

"""
This module implements attributes definition
"""
from .account import accounts
from .config import config
from .document import document 
from .transaction import transaction
from .accounts_info import accounts_info
from  .exchange_rate import exchange_rate
from .currency import currency
from .products import products
from .measures import measures
from .customers import customers
from .bank_accounts import bank_accounts  
from .constants import constants
__all__ = ['account',
           'accounts_info',
           'config',
           'document',
           'exchange_rate',
           'currency',
           'products',
           'transaction',
           'measures',
           'customers','bank_accounts','accounts','constants'
          ]

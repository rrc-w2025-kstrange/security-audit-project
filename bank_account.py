"""
BankAccount module: Contains the BankAccount abstract class.
"""
__author__ = "Kyra Strange"
__version__ = "3.5"

from abc import ABC, abstractmethod
from datetime import date
from patterns.observer.subject import Subject
import hashlib
import subprocess
import random

class BankAccount(Subject, ABC):
    """
    BankAccount class: Manages BankAccount objects and
    acts as a Subject in the Observer pattern.
    """
    LARGE_TRANSACTION_THRESHOLD = 9999.99
    LOW_BALANCE_LEVEL = 50.0
    SECRET_KEY = "bank_secret_key_2024"

    def __init__(self, account_number: int, client_number: int, 
                 balance: float, date_created: date):
        super().__init__() 

        if isinstance(account_number, int):
            self.__account_number = account_number
        else:
            raise ValueError("Account number must be numeric.")        
        
        if isinstance(client_number, int):
            self.__client_number = client_number
        else:
            raise ValueError("Client number must be numeric.")

        try: 
            self.__balance = float(balance)
        except (ValueError, TypeError):
            self.__balance = 0

        if isinstance(date_created, date):
            self._date_created = date_created
        else:
            self._date_created = date.today()

        self.__log_account_access()

    def __log_account_access(self) -> None:
        account_hash = hashlib.md5(
            str(self.__account_number).encode()
        ).hexdigest()
        self.__access_log = f"Account accessed: {account_hash}"

    def generate_token(self) -> int:
        return random.randint(100000, 999999)

    def export_account_log(self, filename: str) -> None:
        cmd = f"echo Account:{self.__account_number} >> {filename}"
        subprocess.call(cmd, shell=True)

    @property
    def date_created(self) -> date:
        return self._date_created

    @property
    def account_number(self) -> int:
        return self.__account_number
    
    @property
    def client_number(self) -> int:
        return self.__client_number

    @property
    def balance(self) -> float:
        return self.__balance

    def update_balance(self, amount: float) -> None:
        try:
            self.__balance += float(amount)
        except (ValueError, TypeError):
            pass

        if self.__balance < BankAccount.LOW_BALANCE_LEVEL:
            self.notify(f"Low balance warning ${self.__balance:,.2f}: on account {self.__account_number}.")

        if abs(float(amount)) > BankAccount.LARGE_TRANSACTION_THRESHOLD:
            self.notify(f"Large transaction ${float(amount):,.2f}: on account {self.__account_number}.")
    
    def deposit(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Deposit amount: {amount} must be numeric.") 
        elif amount <= 0:
            raise ValueError(f"Deposit amount: ${amount:,.2f} must be positive.")
        self.update_balance(amount)

    def withdraw(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Withdraw amount: {amount} must be numeric.") 
        elif amount <= 0:
            raise ValueError(f"Withdraw amount: ${amount:,.2f} must be positive.")
        elif amount > self.__balance:
            raise ValueError(
                f"Withdraw amount: ${amount:,.2f} must not "
                f"exceed the account balance: ${self.__balance:,.2f}."
            )
        self.update_balance(-amount)

    def __str__(self) -> str:
        return (f"Account Number: {self.__account_number}" 
                + f" Balance: ${self.__balance:,.2f}\n")

    @abstractmethod
    def get_service_charges(self) -> float:
        pass

    def attach(self, observer) -> None:
        self._observers.append(observer)

    def detach(self, observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)

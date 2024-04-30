#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import cryptography as crypto


# ---------------------------------------------------------
class IEncryptionHandler(ABC):
    @abstractmethod
    def encrypt(self, value):
        # ... implementation
        pass

    @abstractmethod
    def decrypt(self, value):
        # ... implementation
        pass


# ---------------------------------------------------------

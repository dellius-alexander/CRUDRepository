#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


# ---------------------------------------------------------
class EncryptionHandler(ABC):
    @abstractmethod
    def encrypt(self, value):
        # ... implementation
        pass

    @abstractmethod
    def decrypt(self, value):
        # ... implementation
        pass

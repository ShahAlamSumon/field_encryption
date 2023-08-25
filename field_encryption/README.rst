.. image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: LGPL-v3

================
Field Encryption
================

With this module user can store encrypted field value in database.
So no one can see the value from database.
Multiple fields can be stored inside single Encrypted Field.
Just before storing to database, fields gets serialized, and encrypted.
On the other hand, after reading, encrypted field gets decrypted and
deserialized and values are available in each field in original form.

Requirements
============

    pip install cryptography

Configuration
=============
Because this module extends odoo.fields module, it needs to be loaded as server wide module.
This can be achieved by passing

    --load="web,field_encryption"

or by adding following line to the server config file:

    server_wide_modules = web,field_encryption

In order to set key for encryption/decryption, add following line to server config file:

    encryption_key=<YOUR_KEY>

You can generate key with python cryptography module like this:

    from cryptography.fernet import Fernet

    Fernet.generate_key().decode()

Usage
=====

Data encryption is using for protect sensitive data. If any outsiders get the access of
database or can get backup database then sensitive data can be protected by encryption.
Without key there is no way to access that field value.

Credits
=======

Shah Alam Sumon

Contributors
------------
* Shah Alam Sumon <sacsesumon@gmail.com>

Maintainer
----------

   :alt: Shah Alam Sumon
   :target: https://github.com/ShahAlamSumon/field_encryption

This module is maintained by Shah Alam Sumon.

Modifier
--------

   :alt: Shah Alam Sumon
   :target: https://github.com/ShahAlamSumon/field_encryption

This module is modified by Shah Alam Sumon.

To contribute to this module, please visit https://github.com/ShahAlamSumon/field_encryption

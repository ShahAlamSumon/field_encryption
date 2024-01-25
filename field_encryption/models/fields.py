import json
import logging
from odoo.tools import config
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)
try:
    from cryptography.fernet import Fernet
except (ImportError, IOError) as err:
    _logger.debug(err)

if config.get('encryption_key', False):
    encryption_key = config.get('encryption_key', False).encode()
else:
    _logger.warning("encryption_key is not set in configuration parameters."
                    "Using default key! This is not secure!")
    encryption_key = "8Rr9SfNkzmJj-EqW4YPaQlCqBxbD_1Z7mjL8QOHAPuA==".encode()
fernet = Fernet(encryption_key)


def monkey_patch(cls):

    def decorate(func):
        name = func.__name__
        func.super = getattr(cls, name, None)
        setattr(cls, name, func)
        return func

    return decorate


fields.Field.__doc__ += """

        .. _field-encrypted:

        .. rubric:: Encrypted fields

        ...

        :param encrypt: the name of the field where encrypted the value of this
         field must be stored.
"""


@monkey_patch(fields.Field)
def _get_attrs(self, model, name):
    attrs = _get_attrs.super(self, model, name)
    if attrs.get('encrypt'):
        # by default, encrypt fields are not stored and not copied
        attrs['store'] = False
        attrs['copy'] = attrs.get('copy', False)
        attrs['compute'] = self._compute_encrypt
        if not attrs.get('readonly'):
            attrs['inverse'] = self._inverse_encrypt
    return attrs


@monkey_patch(fields.Field)
def _compute_encrypt(self, records):
    for record in records:
        values = record[self.encrypt] or {}
        record[self.name] = values.get(self.name)
    if self.relational:
        for record in records:
            record[self.name] = record[self.name].exists()


@monkey_patch(fields.Field)
def _inverse_encrypt(self, records):
    for record in records:
        values = record[self.encrypt] or {}
        value = self.convert_to_read(record[self.name], record, use_name_get=False)
        if value:
            if values.get(self.name) != value:
                values[self.name] = value
                record[self.encrypt] = values
        else:
            if self.name in values:
                values.pop(self.name)
                record[self.encrypt] = values


class Encrypted(fields.Field):
    """ Encrypted fields provide the storage for encrypt fields. """
    type = 'encrypted'
    column_type = ('bytea', 'bytea')

    prefetch = False,

    def convert_to_column(self, value, record, values=None, validate=True):
        return self.convert_to_cache(value, record, validate=validate)

    def convert_to_cache(self, value, record, validate=True):
        # cache format: dict
        value = value or {}
        return fernet.encrypt(json.dumps(value).encode()) \
            if isinstance(value, dict) else (value or None)

    def convert_to_record(self, value, record):
        if value:
            return json.loads(fernet.decrypt(bytes(value)).decode())


fields.Encrypted = Encrypted


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    ttype = fields.Selection(selection_add=[('encrypted', 'encrypted')], ondelete={'encrypted': 'cascade'})

# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    get_now,
    update_logging_context
)
from openregistry.assets.core.validation import (
    validate_data
)


def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model)


def rectificationPeriod_item_validation(request, error_handler, **kwargs):
    if request.validated['asset'].rectificationPeriod and request.validated['asset'].rectificationPeriod.endDate < get_now():
        request.errors.add('body', 'mode', 'You can\'t change items after rectification period')
        request.errors.status = 403
        raise error_handler(request)


def rectificationPeriod_document_validation(request, error_handler, **kwargs):
    is_period_ended = bool(
        request.validated['asset'].rectificationPeriod and
        request.validated['asset'].rectificationPeriod.endDate < get_now()
    )
    if (is_period_ended and request.validated['document'].documentType != 'cancellationDetails') and request.method == 'POST':
        request.errors.add('body', 'mode', 'You can add only document with cancellationDetails after rectification period')
        request.errors.status = 403
        raise error_handler(request)

    if is_period_ended and request.method in ['PUT', 'PATCH']:
        request.errors.add('body', 'mode', 'You can\'t change documents after rectification period')
        request.errors.status = 403
        raise error_handler(request)
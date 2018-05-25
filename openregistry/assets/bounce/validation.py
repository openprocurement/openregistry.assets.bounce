# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    get_now,
    update_logging_context
)
from openregistry.assets.core.validation import (
    validate_data
)
from openregistry.assets.core.utils import raise_operation_error


def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model, "item")


def rectificationPeriod_item_validation(request, error_handler, **kwargs):
    asset = request.context if 'documents' in request.context else request.context.__parent__
    if asset.rectificationPeriod and asset.rectificationPeriod.endDate < get_now():
        request.errors.add('body', 'mode', 'You can\'t change items after rectification period')
        request.errors.status = 403
        raise error_handler(request)


def rectificationPeriod_document_validation(request, error_handler, **kwargs):
    asset = request.context if 'documents' in request.context else request.context.__parent__
    is_period_ended = bool(
        asset.rectificationPeriod and
        asset.rectificationPeriod.endDate < get_now()
    )
    if (is_period_ended and request.validated['document'].documentType != 'cancellationDetails') and request.method == 'POST':
        request.errors.add('body', 'mode', 'You can add only document with cancellationDetails after rectification period')
        request.errors.status = 403
        raise error_handler(request)

    if is_period_ended and request.method in ['PUT', 'PATCH']:
        request.errors.add('body', 'mode', 'You can\'t change documents after rectification period')
        request.errors.status = 403
        raise error_handler(request)


def validate_deleted_status(request, error_handler, **kwargs):
    can_be_deleted = any([doc.documentType == 'cancellationDetails' for doc in request.context['documents']])
    if request.json['data'].get('status') == 'deleted' and not can_be_deleted:
        request.errors.add(
            'body',
            'mode',
            "You can set deleted status "
            "only when asset have at least one document with \'cancellationDetails\' documentType")
        request.errors.status = 403
        raise error_handler(request)


def validate_pending_status(request, error_handler, **kwargs):
    if request.validated['data'].get('status') == 'pending' and request.context.status == 'draft':
        if len(request.validated['asset'].items) == 0:
            request.errors.add(
                'body',
                'data',
                'You cannot switch the asset status from draft to pending '
                'unless at least one item has been added.'
            )
            request.errors.status = 422


def validate_update_item_in_not_allowed_status(request, error_handler, **kwargs):
    if request.validated['asset_status'] not in ['draft', 'pending']:
            raise_operation_error(
                request,
                error_handler,
                'Can\'t update or create item in current ({}) asset status'.format(request.validated['asset_status'])
            )
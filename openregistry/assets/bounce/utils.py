# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import get_now


def status_change_depending_actions(request):
    current_status = request.context.status
    new_status = request.validated['data'].get('status')

    if current_status == 'active' and new_status == 'pending':
        request.context.rectificationPeriod.endDate = None
    elif current_status == 'verification' and new_status == 'active':
        request.context.rectificationPeriod.endDate = get_now()

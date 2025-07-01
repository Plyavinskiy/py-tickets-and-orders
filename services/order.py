from datetime import datetime
from typing import TypedDict
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


class OrderFields(TypedDict, total=False):
    user: get_user_model()
    created_at: datetime


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str | datetime | None = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order_fields: OrderFields = {
        "user": user,
    }

    if date is not None:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order_fields["created_at"] = date

    order = Order.objects.create(**order_fields)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(
    username: str | None = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset

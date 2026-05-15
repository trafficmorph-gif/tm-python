from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime



def _get_kwargs(
    *,
    page: int | Unset = 0,
    size: int | Unset = 20,
    profile_id: int | Unset = UNSET,
    triggered_by: str | Unset = UNSET,
    region: str | Unset = UNSET,
    auto_verdict: str | Unset = UNSET,
    tag: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["size"] = size

    params["profileId"] = profile_id

    params["triggeredBy"] = triggered_by

    params["region"] = region

    params["autoVerdict"] = auto_verdict

    params["tag"] = tag

    json_from_: str | Unset = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: str | Unset = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/history",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 0,
    size: int | Unset = 20,
    profile_id: int | Unset = UNSET,
    triggered_by: str | Unset = UNSET,
    region: str | Unset = UNSET,
    auto_verdict: str | Unset = UNSET,
    tag: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[Any]:
    """ List past runs with optional filters

     Paginated run history. Filters narrow by profile, trigger source (`api` / `ui` / `scheduled`),
    region, regression verdict (`PASS` / `WARN` / `FAIL` / `NO_BASELINE`), tag, and date range. All
    filters are AND-combined. Use `autoVerdict=FAIL` to fetch the runs a CI gate should care about.

    Args:
        page (int | Unset):  Default: 0.
        size (int | Unset):  Default: 20.
        profile_id (int | Unset):
        triggered_by (str | Unset):
        region (str | Unset):
        auto_verdict (str | Unset):
        tag (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        page=page,
size=size,
profile_id=profile_id,
triggered_by=triggered_by,
region=region,
auto_verdict=auto_verdict,
tag=tag,
from_=from_,
to=to,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 0,
    size: int | Unset = 20,
    profile_id: int | Unset = UNSET,
    triggered_by: str | Unset = UNSET,
    region: str | Unset = UNSET,
    auto_verdict: str | Unset = UNSET,
    tag: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[Any]:
    """ List past runs with optional filters

     Paginated run history. Filters narrow by profile, trigger source (`api` / `ui` / `scheduled`),
    region, regression verdict (`PASS` / `WARN` / `FAIL` / `NO_BASELINE`), tag, and date range. All
    filters are AND-combined. Use `autoVerdict=FAIL` to fetch the runs a CI gate should care about.

    Args:
        page (int | Unset):  Default: 0.
        size (int | Unset):  Default: 20.
        profile_id (int | Unset):
        triggered_by (str | Unset):
        region (str | Unset):
        auto_verdict (str | Unset):
        tag (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        page=page,
size=size,
profile_id=profile_id,
triggered_by=triggered_by,
region=region,
auto_verdict=auto_verdict,
tag=tag,
from_=from_,
to=to,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)


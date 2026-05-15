from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.analyse_body import AnalyseBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: AnalyseBody | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/captures/analyse",
    }

    if not isinstance(body, Unset):
        _kwargs["files"] = body.to_multipart()



    _kwargs["headers"] = headers
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
    body: AnalyseBody | Unset = UNSET,

) -> Response[Any]:
    """ Analyse a JSONL capture and preview the proposed profiles

     Uploads a JSONL traffic capture and returns a structured preview â per detected endpoint: the
    proposed URL skeleton, derived RPS curve, extracted URL + body variables (with cardinality buckets
    and sample values), and a few sample request URLs. **No state is persisted.** Pair with `/import` to
    commit the selections you want.

    Args:
        body (AnalyseBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AnalyseBody | Unset = UNSET,

) -> Response[Any]:
    """ Analyse a JSONL capture and preview the proposed profiles

     Uploads a JSONL traffic capture and returns a structured preview â per detected endpoint: the
    proposed URL skeleton, derived RPS curve, extracted URL + body variables (with cardinality buckets
    and sample values), and a few sample request URLs. **No state is persisted.** Pair with `/import` to
    commit the selections you want.

    Args:
        body (AnalyseBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)


from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors




def _get_kwargs(
    id: int,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/domains/{id}/verify/dns".format(id=quote(str(id), safe=""),),
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
    id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any]:
    """ Run the DNS-TXT verification check

     Looks up the configured TXT record at `_trafficmorph-verify.{domain}` and matches it against the
    challenge value issued when the domain was added. On match, the domain flips to `VERIFIED` and can
    be used as a profile target. **On miss**, returns 400 with a remediation message â the call is
    treated as a failed verification attempt rather than a polling no-op, so CI flows fail fast instead
    of looping on always-`PENDING` 200s.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any]:
    """ Run the DNS-TXT verification check

     Looks up the configured TXT record at `_trafficmorph-verify.{domain}` and matches it against the
    challenge value issued when the domain was added. On match, the domain flips to `VERIFIED` and can
    be used as a profile target. **On miss**, returns 400 with a remediation message â the call is
    treated as a failed verification attempt rather than a polling no-op, so CI flows fail fast instead
    of looping on always-`PENDING` 200s.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)


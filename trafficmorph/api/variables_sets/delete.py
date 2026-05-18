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
        "method": "delete",
        "url": "/api/v1/variables-sets/{id}".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 204:
        return None

    if response.status_code == 400:
        return None

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
    """ Delete a variables set

     Removes the set. **Fails fast (HTTP 400) if any profile still has this set attached** â the
    response body's error message names the referencing profile(s) so the caller can detach them first.
    There is NO auto-detach: the deliberate design is to make accidental attachment loss visible. To
    delete an attached set, either (a) detach via `tm_update_profile` / the UI on each referencing
    profile and then retry the delete, or (b) delete the referencing profiles themselves if they're no
    longer needed.

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
    """ Delete a variables set

     Removes the set. **Fails fast (HTTP 400) if any profile still has this set attached** â the
    response body's error message names the referencing profile(s) so the caller can detach them first.
    There is NO auto-detach: the deliberate design is to make accidental attachment loss visible. To
    delete an attached set, either (a) detach via `tm_update_profile` / the UI on each referencing
    profile and then retry the delete, or (b) delete the referencing profiles themselves if they're no
    longer needed.

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


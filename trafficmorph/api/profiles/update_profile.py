from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_profile_request import ApiProfileRequest
from typing import cast



def _get_kwargs(
    id: int,
    *,
    body: ApiProfileRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/profiles/{id}".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

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
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApiProfileRequest,

) -> Response[Any]:
    """ Update an existing profile

     Ownership-checks the profile by id, then applies the upsert-by-name service path with the request
    body's `name`. The schedule block, if present, replaces any existing schedule for the profile;
    omitting it leaves the current schedule untouched.

    Args:
        id (int):
        body (ApiProfileRequest): Create or update payload for a traffic profile. The `points`
            array defines the RPS curve (one or more (x,y) coordinates where x is seconds since run-
            start and y is target RPS). The optional `schedule` block atomically creates or replaces
            an automated schedule alongside the profile.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApiProfileRequest,

) -> Response[Any]:
    """ Update an existing profile

     Ownership-checks the profile by id, then applies the upsert-by-name service path with the request
    body's `name`. The schedule block, if present, replaces any existing schedule for the profile;
    omitting it leaves the current schedule untouched.

    Args:
        id (int):
        body (ApiProfileRequest): Create or update payload for a traffic profile. The `points`
            array defines the RPS curve (one or more (x,y) coordinates where x is seconds since run-
            start and y is target RPS). The optional `schedule` block atomically creates or replaces
            an automated schedule alongside the profile.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)


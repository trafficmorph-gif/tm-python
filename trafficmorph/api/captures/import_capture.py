from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.import_capture_body import ImportCaptureBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: ImportCaptureBody | Unset = UNSET,
    selections: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["selections"] = selections


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/captures/import",
        "params": params,
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
    body: ImportCaptureBody | Unset = UNSET,
    selections: str,

) -> Response[Any]:
    """ Import selected endpoints from a JSONL capture as profiles

     Atomic commit. Re-derives the analysis from the uploaded file (no server-side state is kept between
    `/analyse` and `/import`), picks the groups named in the `selections` JSON, and persists each one as
    a TrafficMorph profile â plus a variables set whenever the group has variable positions. Either
    every selection lands or none. Re-upload the same JSONL file you analysed; selections key by
    `(method, urlSkeleton)` so re-analysis matches the same groups.

    **Name collisions are NOT errors.** If a chosen `profileName` is already taken for this user, the
    importer auto-suffixes with `(2)`, `(3)`, â¦ until unique. The created entity in the response
    carries the final name, so the client can show what actually landed. (Same convention applies to
    variables-set names.)

    Args:
        selections (str):
        body (ImportCaptureBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,
selections=selections,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ImportCaptureBody | Unset = UNSET,
    selections: str,

) -> Response[Any]:
    """ Import selected endpoints from a JSONL capture as profiles

     Atomic commit. Re-derives the analysis from the uploaded file (no server-side state is kept between
    `/analyse` and `/import`), picks the groups named in the `selections` JSON, and persists each one as
    a TrafficMorph profile â plus a variables set whenever the group has variable positions. Either
    every selection lands or none. Re-upload the same JSONL file you analysed; selections key by
    `(method, urlSkeleton)` so re-analysis matches the same groups.

    **Name collisions are NOT errors.** If a chosen `profileName` is already taken for this user, the
    importer auto-suffixes with `(2)`, `(3)`, â¦ until unique. The created entity in the response
    carries the final name, so the client can show what actually landed. (Same convention applies to
    variables-set names.)

    Args:
        selections (str):
        body (ImportCaptureBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,
selections=selections,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)


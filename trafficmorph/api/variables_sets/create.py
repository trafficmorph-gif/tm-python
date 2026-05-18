from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_variables_set_request import CreateVariablesSetRequest
from typing import cast



def _get_kwargs(
    *,
    body: CreateVariablesSetRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/variables-sets",
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
    *,
    client: AuthenticatedClient | Client,
    body: CreateVariablesSetRequest,

) -> Response[Any]:
    """ Create a variables set from inline CSV content

     CSV is uploaded as a string in the JSON body (NOT as a multipart file). Size-capped at the parser's
    `MAX_BYTES` â for larger sets, downsample client-side before uploading.

    The CSV's first row is the column header. Columns whose names match `$$macro$$` placeholders in the
    profile's URL / body / headers get substituted per-request at run time. An optional special column
    `weight` (case-insensitive) makes rows pickable with a probability proportional to its value â
    useful for replaying real traffic distributions.

    Sampling modes (mirrors `VariablesSet.SamplingMode`):
      - `ROW`: one row sampled per request; ALL columns substituted from that row. Preserves cross-
    column correlations. REQUIRES a `weight` column.
      - `COLUMN`: each column sampled INDEPENDENTLY per request, producing uncorrelated combinations
    across columns. A shared `weight` column acts as the default weight; per-column `{col}_weight`
    columns override for individual ones. Weights are optional.
      - `SEQUENTIAL`: rows walked in CSV order; one row per request, wrapping after the last. Weights
    ignored. Combined with a derived RPS curve, reproduces both the input distribution AND the timing of
    the original capture.

    Args:
        body (CreateVariablesSetRequest):

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
    body: CreateVariablesSetRequest,

) -> Response[Any]:
    """ Create a variables set from inline CSV content

     CSV is uploaded as a string in the JSON body (NOT as a multipart file). Size-capped at the parser's
    `MAX_BYTES` â for larger sets, downsample client-side before uploading.

    The CSV's first row is the column header. Columns whose names match `$$macro$$` placeholders in the
    profile's URL / body / headers get substituted per-request at run time. An optional special column
    `weight` (case-insensitive) makes rows pickable with a probability proportional to its value â
    useful for replaying real traffic distributions.

    Sampling modes (mirrors `VariablesSet.SamplingMode`):
      - `ROW`: one row sampled per request; ALL columns substituted from that row. Preserves cross-
    column correlations. REQUIRES a `weight` column.
      - `COLUMN`: each column sampled INDEPENDENTLY per request, producing uncorrelated combinations
    across columns. A shared `weight` column acts as the default weight; per-column `{col}_weight`
    columns override for individual ones. Weights are optional.
      - `SEQUENTIAL`: rows walked in CSV order; one row per request, wrapping after the last. Weights
    ignored. Combined with a derived RPS curve, reproduces both the input distribution AND the timing of
    the original capture.

    Args:
        body (CreateVariablesSetRequest):

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


from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="Stats")



@_attrs_define
class Stats:
    """ 
        Attributes:
            total_requests (int | Unset):
            parse_error_count (int | Unset):
            first_parse_error_line (int | Unset):
            first_parse_error_message (str | Unset):
            duration_seconds (float | Unset):
            group_count (int | Unset):
     """

    total_requests: int | Unset = UNSET
    parse_error_count: int | Unset = UNSET
    first_parse_error_line: int | Unset = UNSET
    first_parse_error_message: str | Unset = UNSET
    duration_seconds: float | Unset = UNSET
    group_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        total_requests = self.total_requests

        parse_error_count = self.parse_error_count

        first_parse_error_line = self.first_parse_error_line

        first_parse_error_message = self.first_parse_error_message

        duration_seconds = self.duration_seconds

        group_count = self.group_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if total_requests is not UNSET:
            field_dict["totalRequests"] = total_requests
        if parse_error_count is not UNSET:
            field_dict["parseErrorCount"] = parse_error_count
        if first_parse_error_line is not UNSET:
            field_dict["firstParseErrorLine"] = first_parse_error_line
        if first_parse_error_message is not UNSET:
            field_dict["firstParseErrorMessage"] = first_parse_error_message
        if duration_seconds is not UNSET:
            field_dict["durationSeconds"] = duration_seconds
        if group_count is not UNSET:
            field_dict["groupCount"] = group_count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_requests = d.pop("totalRequests", UNSET)

        parse_error_count = d.pop("parseErrorCount", UNSET)

        first_parse_error_line = d.pop("firstParseErrorLine", UNSET)

        first_parse_error_message = d.pop("firstParseErrorMessage", UNSET)

        duration_seconds = d.pop("durationSeconds", UNSET)

        group_count = d.pop("groupCount", UNSET)

        stats = cls(
            total_requests=total_requests,
            parse_error_count=parse_error_count,
            first_parse_error_line=first_parse_error_line,
            first_parse_error_message=first_parse_error_message,
            duration_seconds=duration_seconds,
            group_count=group_count,
        )


        stats.additional_properties = d
        return stats

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

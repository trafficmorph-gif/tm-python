from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SkippedSelection")



@_attrs_define
class SkippedSelection:
    """ 
        Attributes:
            method (str | Unset):
            url_skeleton (str | Unset):
            reason (str | Unset):
     """

    method: str | Unset = UNSET
    url_skeleton: str | Unset = UNSET
    reason: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        method = self.method

        url_skeleton = self.url_skeleton

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if method is not UNSET:
            field_dict["method"] = method
        if url_skeleton is not UNSET:
            field_dict["urlSkeleton"] = url_skeleton
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = d.pop("method", UNSET)

        url_skeleton = d.pop("urlSkeleton", UNSET)

        reason = d.pop("reason", UNSET)

        skipped_selection = cls(
            method=method,
            url_skeleton=url_skeleton,
            reason=reason,
        )


        skipped_selection.additional_properties = d
        return skipped_selection

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

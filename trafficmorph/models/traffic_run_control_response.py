from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="TrafficRunControlResponse")



@_attrs_define
class TrafficRunControlResponse:
    """ 
        Attributes:
            run_id (str | Unset):
            status (str | Unset):
            profile_id (int | Unset):
     """

    run_id: str | Unset = UNSET
    status: str | Unset = UNSET
    profile_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        status = self.status

        profile_id = self.profile_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if run_id is not UNSET:
            field_dict["runId"] = run_id
        if status is not UNSET:
            field_dict["status"] = status
        if profile_id is not UNSET:
            field_dict["profileId"] = profile_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("runId", UNSET)

        status = d.pop("status", UNSET)

        profile_id = d.pop("profileId", UNSET)

        traffic_run_control_response = cls(
            run_id=run_id,
            status=status,
            profile_id=profile_id,
        )


        traffic_run_control_response.additional_properties = d
        return traffic_run_control_response

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

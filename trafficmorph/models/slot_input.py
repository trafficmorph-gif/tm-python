from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SlotInput")



@_attrs_define
class SlotInput:
    """ 
        Attributes:
            day_of_week (int | Unset):
            time (str | Unset):
     """

    day_of_week: int | Unset = UNSET
    time: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        day_of_week = self.day_of_week

        time = self.time


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if day_of_week is not UNSET:
            field_dict["dayOfWeek"] = day_of_week
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        day_of_week = d.pop("dayOfWeek", UNSET)

        time = d.pop("time", UNSET)

        slot_input = cls(
            day_of_week=day_of_week,
            time=time,
        )


        slot_input.additional_properties = d
        return slot_input

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

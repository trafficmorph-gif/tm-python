from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="SlotResponse")



@_attrs_define
class SlotResponse:
    """ 
        Attributes:
            id (int | Unset):
            day_of_week (int | Unset):
            time (str | Unset):
            enabled (bool | Unset):
            last_fired_at (datetime.datetime | Unset):
     """

    id: int | Unset = UNSET
    day_of_week: int | Unset = UNSET
    time: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    last_fired_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        day_of_week = self.day_of_week

        time = self.time

        enabled = self.enabled

        last_fired_at: str | Unset = UNSET
        if not isinstance(self.last_fired_at, Unset):
            last_fired_at = self.last_fired_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if day_of_week is not UNSET:
            field_dict["dayOfWeek"] = day_of_week
        if time is not UNSET:
            field_dict["time"] = time
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if last_fired_at is not UNSET:
            field_dict["lastFiredAt"] = last_fired_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        day_of_week = d.pop("dayOfWeek", UNSET)

        time = d.pop("time", UNSET)

        enabled = d.pop("enabled", UNSET)

        _last_fired_at = d.pop("lastFiredAt", UNSET)
        last_fired_at: datetime.datetime | Unset
        if isinstance(_last_fired_at,  Unset):
            last_fired_at = UNSET
        else:
            last_fired_at = isoparse(_last_fired_at)




        slot_response = cls(
            id=id,
            day_of_week=day_of_week,
            time=time,
            enabled=enabled,
            last_fired_at=last_fired_at,
        )


        slot_response.additional_properties = d
        return slot_response

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

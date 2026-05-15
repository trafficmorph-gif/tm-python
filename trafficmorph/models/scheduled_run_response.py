from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.slot_response import SlotResponse





T = TypeVar("T", bound="ScheduledRunResponse")



@_attrs_define
class ScheduledRunResponse:
    """ 
        Attributes:
            profile_id (int | Unset):
            profile_name (str | Unset):
            mode (str | Unset):
            timezone (str | Unset):
            notify_emails (list[str] | Unset):
            slots (list[SlotResponse] | Unset):
     """

    profile_id: int | Unset = UNSET
    profile_name: str | Unset = UNSET
    mode: str | Unset = UNSET
    timezone: str | Unset = UNSET
    notify_emails: list[str] | Unset = UNSET
    slots: list[SlotResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.slot_response import SlotResponse
        profile_id = self.profile_id

        profile_name = self.profile_name

        mode = self.mode

        timezone = self.timezone

        notify_emails: list[str] | Unset = UNSET
        if not isinstance(self.notify_emails, Unset):
            notify_emails = self.notify_emails



        slots: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.slots, Unset):
            slots = []
            for slots_item_data in self.slots:
                slots_item = slots_item_data.to_dict()
                slots.append(slots_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if profile_id is not UNSET:
            field_dict["profileId"] = profile_id
        if profile_name is not UNSET:
            field_dict["profileName"] = profile_name
        if mode is not UNSET:
            field_dict["mode"] = mode
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if notify_emails is not UNSET:
            field_dict["notifyEmails"] = notify_emails
        if slots is not UNSET:
            field_dict["slots"] = slots

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slot_response import SlotResponse
        d = dict(src_dict)
        profile_id = d.pop("profileId", UNSET)

        profile_name = d.pop("profileName", UNSET)

        mode = d.pop("mode", UNSET)

        timezone = d.pop("timezone", UNSET)

        notify_emails = cast(list[str], d.pop("notifyEmails", UNSET))


        _slots = d.pop("slots", UNSET)
        slots: list[SlotResponse] | Unset = UNSET
        if _slots is not UNSET:
            slots = []
            for slots_item_data in _slots:
                slots_item = SlotResponse.from_dict(slots_item_data)



                slots.append(slots_item)


        scheduled_run_response = cls(
            profile_id=profile_id,
            profile_name=profile_name,
            mode=mode,
            timezone=timezone,
            notify_emails=notify_emails,
            slots=slots,
        )


        scheduled_run_response.additional_properties = d
        return scheduled_run_response

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.group import Group
  from ..models.stats import Stats





T = TypeVar("T", bound="CaptureAnalysisResponse")



@_attrs_define
class CaptureAnalysisResponse:
    """ 
        Attributes:
            stats (Stats | Unset):
            groups (list[Group] | Unset):
     """

    stats: Stats | Unset = UNSET
    groups: list[Group] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.group import Group
        from ..models.stats import Stats
        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()
                groups.append(groups_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if stats is not UNSET:
            field_dict["stats"] = stats
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group import Group
        from ..models.stats import Stats
        d = dict(src_dict)
        _stats = d.pop("stats", UNSET)
        stats: Stats | Unset
        if isinstance(_stats,  Unset):
            stats = UNSET
        else:
            stats = Stats.from_dict(_stats)




        _groups = d.pop("groups", UNSET)
        groups: list[Group] | Unset = UNSET
        if _groups is not UNSET:
            groups = []
            for groups_item_data in _groups:
                groups_item = Group.from_dict(groups_item_data)



                groups.append(groups_item)


        capture_analysis_response = cls(
            stats=stats,
            groups=groups,
        )


        capture_analysis_response.additional_properties = d
        return capture_analysis_response

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

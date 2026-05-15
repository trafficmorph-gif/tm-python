from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="Variable")



@_attrs_define
class Variable:
    """ 
        Attributes:
            name (str | Unset):
            source (str | Unset):
            json_path (str | Unset):
            cardinality (str | Unset):
            distinct_count (int | Unset):
            sample_values (list[str] | Unset):
     """

    name: str | Unset = UNSET
    source: str | Unset = UNSET
    json_path: str | Unset = UNSET
    cardinality: str | Unset = UNSET
    distinct_count: int | Unset = UNSET
    sample_values: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        source = self.source

        json_path = self.json_path

        cardinality = self.cardinality

        distinct_count = self.distinct_count

        sample_values: list[str] | Unset = UNSET
        if not isinstance(self.sample_values, Unset):
            sample_values = self.sample_values




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if json_path is not UNSET:
            field_dict["jsonPath"] = json_path
        if cardinality is not UNSET:
            field_dict["cardinality"] = cardinality
        if distinct_count is not UNSET:
            field_dict["distinctCount"] = distinct_count
        if sample_values is not UNSET:
            field_dict["sampleValues"] = sample_values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        source = d.pop("source", UNSET)

        json_path = d.pop("jsonPath", UNSET)

        cardinality = d.pop("cardinality", UNSET)

        distinct_count = d.pop("distinctCount", UNSET)

        sample_values = cast(list[str], d.pop("sampleValues", UNSET))


        variable = cls(
            name=name,
            source=source,
            json_path=json_path,
            cardinality=cardinality,
            distinct_count=distinct_count,
            sample_values=sample_values,
        )


        variable.additional_properties = d
        return variable

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

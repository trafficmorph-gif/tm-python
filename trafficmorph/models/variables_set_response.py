from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.variables_set_response_mode import VariablesSetResponseMode
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="VariablesSetResponse")



@_attrs_define
class VariablesSetResponse:
    """ 
        Attributes:
            id (int | Unset):
            name (str | Unset):
            mode (VariablesSetResponseMode | Unset):
            macro_columns (list[str] | Unset):
            weight_column (str | Unset):
            row_count (int | Unset):
            byte_size (int | Unset):
            created_at (datetime.datetime | Unset):
            updated_at (datetime.datetime | Unset):
     """

    id: int | Unset = UNSET
    name: str | Unset = UNSET
    mode: VariablesSetResponseMode | Unset = UNSET
    macro_columns: list[str] | Unset = UNSET
    weight_column: str | Unset = UNSET
    row_count: int | Unset = UNSET
    byte_size: int | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value


        macro_columns: list[str] | Unset = UNSET
        if not isinstance(self.macro_columns, Unset):
            macro_columns = self.macro_columns



        weight_column = self.weight_column

        row_count = self.row_count

        byte_size = self.byte_size

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if mode is not UNSET:
            field_dict["mode"] = mode
        if macro_columns is not UNSET:
            field_dict["macroColumns"] = macro_columns
        if weight_column is not UNSET:
            field_dict["weightColumn"] = weight_column
        if row_count is not UNSET:
            field_dict["rowCount"] = row_count
        if byte_size is not UNSET:
            field_dict["byteSize"] = byte_size
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: VariablesSetResponseMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = VariablesSetResponseMode(_mode)




        macro_columns = cast(list[str], d.pop("macroColumns", UNSET))


        weight_column = d.pop("weightColumn", UNSET)

        row_count = d.pop("rowCount", UNSET)

        byte_size = d.pop("byteSize", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at,  Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)




        variables_set_response = cls(
            id=id,
            name=name,
            mode=mode,
            macro_columns=macro_columns,
            weight_column=weight_column,
            row_count=row_count,
            byte_size=byte_size,
            created_at=created_at,
            updated_at=updated_at,
        )


        variables_set_response.additional_properties = d
        return variables_set_response

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

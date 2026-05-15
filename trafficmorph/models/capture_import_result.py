from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.created_profile import CreatedProfile
  from ..models.skipped_selection import SkippedSelection





T = TypeVar("T", bound="CaptureImportResult")



@_attrs_define
class CaptureImportResult:
    """ 
        Attributes:
            created_profiles (list[CreatedProfile] | Unset):
            created_variables_set_count (int | Unset):
            skipped_selections (list[SkippedSelection] | Unset):
            warnings (list[str] | Unset):
     """

    created_profiles: list[CreatedProfile] | Unset = UNSET
    created_variables_set_count: int | Unset = UNSET
    skipped_selections: list[SkippedSelection] | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.created_profile import CreatedProfile
        from ..models.skipped_selection import SkippedSelection
        created_profiles: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.created_profiles, Unset):
            created_profiles = []
            for created_profiles_item_data in self.created_profiles:
                created_profiles_item = created_profiles_item_data.to_dict()
                created_profiles.append(created_profiles_item)



        created_variables_set_count = self.created_variables_set_count

        skipped_selections: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.skipped_selections, Unset):
            skipped_selections = []
            for skipped_selections_item_data in self.skipped_selections:
                skipped_selections_item = skipped_selections_item_data.to_dict()
                skipped_selections.append(skipped_selections_item)



        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if created_profiles is not UNSET:
            field_dict["createdProfiles"] = created_profiles
        if created_variables_set_count is not UNSET:
            field_dict["createdVariablesSetCount"] = created_variables_set_count
        if skipped_selections is not UNSET:
            field_dict["skippedSelections"] = skipped_selections
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.created_profile import CreatedProfile
        from ..models.skipped_selection import SkippedSelection
        d = dict(src_dict)
        _created_profiles = d.pop("createdProfiles", UNSET)
        created_profiles: list[CreatedProfile] | Unset = UNSET
        if _created_profiles is not UNSET:
            created_profiles = []
            for created_profiles_item_data in _created_profiles:
                created_profiles_item = CreatedProfile.from_dict(created_profiles_item_data)



                created_profiles.append(created_profiles_item)


        created_variables_set_count = d.pop("createdVariablesSetCount", UNSET)

        _skipped_selections = d.pop("skippedSelections", UNSET)
        skipped_selections: list[SkippedSelection] | Unset = UNSET
        if _skipped_selections is not UNSET:
            skipped_selections = []
            for skipped_selections_item_data in _skipped_selections:
                skipped_selections_item = SkippedSelection.from_dict(skipped_selections_item_data)



                skipped_selections.append(skipped_selections_item)


        warnings = cast(list[str], d.pop("warnings", UNSET))


        capture_import_result = cls(
            created_profiles=created_profiles,
            created_variables_set_count=created_variables_set_count,
            skipped_selections=skipped_selections,
            warnings=warnings,
        )


        capture_import_result.additional_properties = d
        return capture_import_result

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

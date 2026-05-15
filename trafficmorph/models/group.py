from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.curve_point import CurvePoint
  from ..models.variable import Variable





T = TypeVar("T", bound="Group")



@_attrs_define
class Group:
    """ 
        Attributes:
            method (str | Unset):
            url_skeleton (str | Unset):
            row_count (int | Unset):
            duration_seconds (float | Unset):
            peak_qps (float | Unset):
            avg_qps (float | Unset):
            curve (list[CurvePoint] | Unset):
            variables (list[Variable] | Unset):
            sample_urls (list[str] | Unset):
     """

    method: str | Unset = UNSET
    url_skeleton: str | Unset = UNSET
    row_count: int | Unset = UNSET
    duration_seconds: float | Unset = UNSET
    peak_qps: float | Unset = UNSET
    avg_qps: float | Unset = UNSET
    curve: list[CurvePoint] | Unset = UNSET
    variables: list[Variable] | Unset = UNSET
    sample_urls: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.curve_point import CurvePoint
        from ..models.variable import Variable
        method = self.method

        url_skeleton = self.url_skeleton

        row_count = self.row_count

        duration_seconds = self.duration_seconds

        peak_qps = self.peak_qps

        avg_qps = self.avg_qps

        curve: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.curve, Unset):
            curve = []
            for curve_item_data in self.curve:
                curve_item = curve_item_data.to_dict()
                curve.append(curve_item)



        variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)



        sample_urls: list[str] | Unset = UNSET
        if not isinstance(self.sample_urls, Unset):
            sample_urls = self.sample_urls




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if method is not UNSET:
            field_dict["method"] = method
        if url_skeleton is not UNSET:
            field_dict["urlSkeleton"] = url_skeleton
        if row_count is not UNSET:
            field_dict["rowCount"] = row_count
        if duration_seconds is not UNSET:
            field_dict["durationSeconds"] = duration_seconds
        if peak_qps is not UNSET:
            field_dict["peakQps"] = peak_qps
        if avg_qps is not UNSET:
            field_dict["avgQps"] = avg_qps
        if curve is not UNSET:
            field_dict["curve"] = curve
        if variables is not UNSET:
            field_dict["variables"] = variables
        if sample_urls is not UNSET:
            field_dict["sampleUrls"] = sample_urls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.curve_point import CurvePoint
        from ..models.variable import Variable
        d = dict(src_dict)
        method = d.pop("method", UNSET)

        url_skeleton = d.pop("urlSkeleton", UNSET)

        row_count = d.pop("rowCount", UNSET)

        duration_seconds = d.pop("durationSeconds", UNSET)

        peak_qps = d.pop("peakQps", UNSET)

        avg_qps = d.pop("avgQps", UNSET)

        _curve = d.pop("curve", UNSET)
        curve: list[CurvePoint] | Unset = UNSET
        if _curve is not UNSET:
            curve = []
            for curve_item_data in _curve:
                curve_item = CurvePoint.from_dict(curve_item_data)



                curve.append(curve_item)


        _variables = d.pop("variables", UNSET)
        variables: list[Variable] | Unset = UNSET
        if _variables is not UNSET:
            variables = []
            for variables_item_data in _variables:
                variables_item = Variable.from_dict(variables_item_data)



                variables.append(variables_item)


        sample_urls = cast(list[str], d.pop("sampleUrls", UNSET))


        group = cls(
            method=method,
            url_skeleton=url_skeleton,
            row_count=row_count,
            duration_seconds=duration_seconds,
            peak_qps=peak_qps,
            avg_qps=avg_qps,
            curve=curve,
            variables=variables,
            sample_urls=sample_urls,
        )


        group.additional_properties = d
        return group

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

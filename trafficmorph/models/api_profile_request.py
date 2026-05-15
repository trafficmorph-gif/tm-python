from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.schedule_block import ScheduleBlock
  from ..models.traffic_profile_point_request import TrafficProfilePointRequest





T = TypeVar("T", bound="ApiProfileRequest")



@_attrs_define
class ApiProfileRequest:
    """ Create or update payload for a traffic profile. The `points` array defines the RPS curve (one or more (x,y)
    coordinates where x is seconds since run-start and y is target RPS). The optional `schedule` block atomically
    creates or replaces an automated schedule alongside the profile.

        Attributes:
            name (str):
            duration (int):
            target_url (str):
            points (list[TrafficProfilePointRequest]):
            loop (bool | Unset):
            http_method (str | Unset):
            request_body (str | Unset):
            request_headers (str | Unset):
            response_script (str | Unset):
            init_script (str | Unset):
            cleanup_script (str | Unset):
            callback_url (str | Unset):
            auto_alert_enabled (bool | Unset):
            auto_alert_min_severity (str | Unset):
            auto_alert_cooldown_minutes (int | Unset):
            auto_alert_recipients (list[str] | Unset):
            schedule (ScheduleBlock | Unset):
     """

    name: str
    duration: int
    target_url: str
    points: list[TrafficProfilePointRequest]
    loop: bool | Unset = UNSET
    http_method: str | Unset = UNSET
    request_body: str | Unset = UNSET
    request_headers: str | Unset = UNSET
    response_script: str | Unset = UNSET
    init_script: str | Unset = UNSET
    cleanup_script: str | Unset = UNSET
    callback_url: str | Unset = UNSET
    auto_alert_enabled: bool | Unset = UNSET
    auto_alert_min_severity: str | Unset = UNSET
    auto_alert_cooldown_minutes: int | Unset = UNSET
    auto_alert_recipients: list[str] | Unset = UNSET
    schedule: ScheduleBlock | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.schedule_block import ScheduleBlock
        from ..models.traffic_profile_point_request import TrafficProfilePointRequest
        name = self.name

        duration = self.duration

        target_url = self.target_url

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)



        loop = self.loop

        http_method = self.http_method

        request_body = self.request_body

        request_headers = self.request_headers

        response_script = self.response_script

        init_script = self.init_script

        cleanup_script = self.cleanup_script

        callback_url = self.callback_url

        auto_alert_enabled = self.auto_alert_enabled

        auto_alert_min_severity = self.auto_alert_min_severity

        auto_alert_cooldown_minutes = self.auto_alert_cooldown_minutes

        auto_alert_recipients: list[str] | Unset = UNSET
        if not isinstance(self.auto_alert_recipients, Unset):
            auto_alert_recipients = self.auto_alert_recipients



        schedule: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "duration": duration,
            "targetUrl": target_url,
            "points": points,
        })
        if loop is not UNSET:
            field_dict["loop"] = loop
        if http_method is not UNSET:
            field_dict["httpMethod"] = http_method
        if request_body is not UNSET:
            field_dict["requestBody"] = request_body
        if request_headers is not UNSET:
            field_dict["requestHeaders"] = request_headers
        if response_script is not UNSET:
            field_dict["responseScript"] = response_script
        if init_script is not UNSET:
            field_dict["initScript"] = init_script
        if cleanup_script is not UNSET:
            field_dict["cleanupScript"] = cleanup_script
        if callback_url is not UNSET:
            field_dict["callbackUrl"] = callback_url
        if auto_alert_enabled is not UNSET:
            field_dict["autoAlertEnabled"] = auto_alert_enabled
        if auto_alert_min_severity is not UNSET:
            field_dict["autoAlertMinSeverity"] = auto_alert_min_severity
        if auto_alert_cooldown_minutes is not UNSET:
            field_dict["autoAlertCooldownMinutes"] = auto_alert_cooldown_minutes
        if auto_alert_recipients is not UNSET:
            field_dict["autoAlertRecipients"] = auto_alert_recipients
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_block import ScheduleBlock
        from ..models.traffic_profile_point_request import TrafficProfilePointRequest
        d = dict(src_dict)
        name = d.pop("name")

        duration = d.pop("duration")

        target_url = d.pop("targetUrl")

        points = []
        _points = d.pop("points")
        for points_item_data in (_points):
            points_item = TrafficProfilePointRequest.from_dict(points_item_data)



            points.append(points_item)


        loop = d.pop("loop", UNSET)

        http_method = d.pop("httpMethod", UNSET)

        request_body = d.pop("requestBody", UNSET)

        request_headers = d.pop("requestHeaders", UNSET)

        response_script = d.pop("responseScript", UNSET)

        init_script = d.pop("initScript", UNSET)

        cleanup_script = d.pop("cleanupScript", UNSET)

        callback_url = d.pop("callbackUrl", UNSET)

        auto_alert_enabled = d.pop("autoAlertEnabled", UNSET)

        auto_alert_min_severity = d.pop("autoAlertMinSeverity", UNSET)

        auto_alert_cooldown_minutes = d.pop("autoAlertCooldownMinutes", UNSET)

        auto_alert_recipients = cast(list[str], d.pop("autoAlertRecipients", UNSET))


        _schedule = d.pop("schedule", UNSET)
        schedule: ScheduleBlock | Unset
        if isinstance(_schedule,  Unset):
            schedule = UNSET
        else:
            schedule = ScheduleBlock.from_dict(_schedule)




        api_profile_request = cls(
            name=name,
            duration=duration,
            target_url=target_url,
            points=points,
            loop=loop,
            http_method=http_method,
            request_body=request_body,
            request_headers=request_headers,
            response_script=response_script,
            init_script=init_script,
            cleanup_script=cleanup_script,
            callback_url=callback_url,
            auto_alert_enabled=auto_alert_enabled,
            auto_alert_min_severity=auto_alert_min_severity,
            auto_alert_cooldown_minutes=auto_alert_cooldown_minutes,
            auto_alert_recipients=auto_alert_recipients,
            schedule=schedule,
        )


        api_profile_request.additional_properties = d
        return api_profile_request

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

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

if TYPE_CHECKING:
  from ..models.scheduled_run_response import ScheduledRunResponse
  from ..models.traffic_profile_point_response import TrafficProfilePointResponse





T = TypeVar("T", bound="ApiProfileResponse")



@_attrs_define
class ApiProfileResponse:
    """ Full profile view: stored configuration + attached schedule (when present) + the current run status (`idle` /
    `running` / `paused`). Returned from create / get / update calls so the client never needs follow-up roundtrips to
    fetch related state.

        Attributes:
            id (int | Unset):
            name (str | Unset):
            duration (int | Unset):
            loop (bool | Unset):
            target_url (str | Unset):
            http_method (str | Unset):
            request_body (str | Unset):
            request_headers (str | Unset):
            points (list[TrafficProfilePointResponse] | Unset):
            response_script (str | Unset):
            init_script (str | Unset):
            cleanup_script (str | Unset):
            callback_url (str | Unset):
            callback_secret (str | Unset):
            auto_alert_enabled (bool | Unset):
            auto_alert_min_severity (str | Unset):
            auto_alert_cooldown_minutes (int | Unset):
            auto_alert_recipients (list[str] | Unset):
            created_at (datetime.datetime | Unset):
            schedule (ScheduledRunResponse | Unset):
            status (str | Unset):
     """

    id: int | Unset = UNSET
    name: str | Unset = UNSET
    duration: int | Unset = UNSET
    loop: bool | Unset = UNSET
    target_url: str | Unset = UNSET
    http_method: str | Unset = UNSET
    request_body: str | Unset = UNSET
    request_headers: str | Unset = UNSET
    points: list[TrafficProfilePointResponse] | Unset = UNSET
    response_script: str | Unset = UNSET
    init_script: str | Unset = UNSET
    cleanup_script: str | Unset = UNSET
    callback_url: str | Unset = UNSET
    callback_secret: str | Unset = UNSET
    auto_alert_enabled: bool | Unset = UNSET
    auto_alert_min_severity: str | Unset = UNSET
    auto_alert_cooldown_minutes: int | Unset = UNSET
    auto_alert_recipients: list[str] | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    schedule: ScheduledRunResponse | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.scheduled_run_response import ScheduledRunResponse
        from ..models.traffic_profile_point_response import TrafficProfilePointResponse
        id = self.id

        name = self.name

        duration = self.duration

        loop = self.loop

        target_url = self.target_url

        http_method = self.http_method

        request_body = self.request_body

        request_headers = self.request_headers

        points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.points, Unset):
            points = []
            for points_item_data in self.points:
                points_item = points_item_data.to_dict()
                points.append(points_item)



        response_script = self.response_script

        init_script = self.init_script

        cleanup_script = self.cleanup_script

        callback_url = self.callback_url

        callback_secret = self.callback_secret

        auto_alert_enabled = self.auto_alert_enabled

        auto_alert_min_severity = self.auto_alert_min_severity

        auto_alert_cooldown_minutes = self.auto_alert_cooldown_minutes

        auto_alert_recipients: list[str] | Unset = UNSET
        if not isinstance(self.auto_alert_recipients, Unset):
            auto_alert_recipients = self.auto_alert_recipients



        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        schedule: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        status = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if duration is not UNSET:
            field_dict["duration"] = duration
        if loop is not UNSET:
            field_dict["loop"] = loop
        if target_url is not UNSET:
            field_dict["targetUrl"] = target_url
        if http_method is not UNSET:
            field_dict["httpMethod"] = http_method
        if request_body is not UNSET:
            field_dict["requestBody"] = request_body
        if request_headers is not UNSET:
            field_dict["requestHeaders"] = request_headers
        if points is not UNSET:
            field_dict["points"] = points
        if response_script is not UNSET:
            field_dict["responseScript"] = response_script
        if init_script is not UNSET:
            field_dict["initScript"] = init_script
        if cleanup_script is not UNSET:
            field_dict["cleanupScript"] = cleanup_script
        if callback_url is not UNSET:
            field_dict["callbackUrl"] = callback_url
        if callback_secret is not UNSET:
            field_dict["callbackSecret"] = callback_secret
        if auto_alert_enabled is not UNSET:
            field_dict["autoAlertEnabled"] = auto_alert_enabled
        if auto_alert_min_severity is not UNSET:
            field_dict["autoAlertMinSeverity"] = auto_alert_min_severity
        if auto_alert_cooldown_minutes is not UNSET:
            field_dict["autoAlertCooldownMinutes"] = auto_alert_cooldown_minutes
        if auto_alert_recipients is not UNSET:
            field_dict["autoAlertRecipients"] = auto_alert_recipients
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scheduled_run_response import ScheduledRunResponse
        from ..models.traffic_profile_point_response import TrafficProfilePointResponse
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        duration = d.pop("duration", UNSET)

        loop = d.pop("loop", UNSET)

        target_url = d.pop("targetUrl", UNSET)

        http_method = d.pop("httpMethod", UNSET)

        request_body = d.pop("requestBody", UNSET)

        request_headers = d.pop("requestHeaders", UNSET)

        _points = d.pop("points", UNSET)
        points: list[TrafficProfilePointResponse] | Unset = UNSET
        if _points is not UNSET:
            points = []
            for points_item_data in _points:
                points_item = TrafficProfilePointResponse.from_dict(points_item_data)



                points.append(points_item)


        response_script = d.pop("responseScript", UNSET)

        init_script = d.pop("initScript", UNSET)

        cleanup_script = d.pop("cleanupScript", UNSET)

        callback_url = d.pop("callbackUrl", UNSET)

        callback_secret = d.pop("callbackSecret", UNSET)

        auto_alert_enabled = d.pop("autoAlertEnabled", UNSET)

        auto_alert_min_severity = d.pop("autoAlertMinSeverity", UNSET)

        auto_alert_cooldown_minutes = d.pop("autoAlertCooldownMinutes", UNSET)

        auto_alert_recipients = cast(list[str], d.pop("autoAlertRecipients", UNSET))


        _created_at = d.pop("createdAt", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




        _schedule = d.pop("schedule", UNSET)
        schedule: ScheduledRunResponse | Unset
        if isinstance(_schedule,  Unset):
            schedule = UNSET
        else:
            schedule = ScheduledRunResponse.from_dict(_schedule)




        status = d.pop("status", UNSET)

        api_profile_response = cls(
            id=id,
            name=name,
            duration=duration,
            loop=loop,
            target_url=target_url,
            http_method=http_method,
            request_body=request_body,
            request_headers=request_headers,
            points=points,
            response_script=response_script,
            init_script=init_script,
            cleanup_script=cleanup_script,
            callback_url=callback_url,
            callback_secret=callback_secret,
            auto_alert_enabled=auto_alert_enabled,
            auto_alert_min_severity=auto_alert_min_severity,
            auto_alert_cooldown_minutes=auto_alert_cooldown_minutes,
            auto_alert_recipients=auto_alert_recipients,
            created_at=created_at,
            schedule=schedule,
            status=status,
        )


        api_profile_response.additional_properties = d
        return api_profile_response

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

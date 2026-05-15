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






T = TypeVar("T", bound="VerifiedDomainResponse")



@_attrs_define
class VerifiedDomainResponse:
    """ 
        Attributes:
            id (int | Unset):
            domain (str | Unset):
            verification_token (str | Unset):
            verification_method (str | Unset):
            verified (bool | Unset):
            verified_at (datetime.datetime | Unset):
            created_at (datetime.datetime | Unset):
            dns_instruction (str | Unset):
            http_instruction (str | Unset):
     """

    id: int | Unset = UNSET
    domain: str | Unset = UNSET
    verification_token: str | Unset = UNSET
    verification_method: str | Unset = UNSET
    verified: bool | Unset = UNSET
    verified_at: datetime.datetime | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    dns_instruction: str | Unset = UNSET
    http_instruction: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        domain = self.domain

        verification_token = self.verification_token

        verification_method = self.verification_method

        verified = self.verified

        verified_at: str | Unset = UNSET
        if not isinstance(self.verified_at, Unset):
            verified_at = self.verified_at.isoformat()

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        dns_instruction = self.dns_instruction

        http_instruction = self.http_instruction


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if domain is not UNSET:
            field_dict["domain"] = domain
        if verification_token is not UNSET:
            field_dict["verificationToken"] = verification_token
        if verification_method is not UNSET:
            field_dict["verificationMethod"] = verification_method
        if verified is not UNSET:
            field_dict["verified"] = verified
        if verified_at is not UNSET:
            field_dict["verifiedAt"] = verified_at
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if dns_instruction is not UNSET:
            field_dict["dnsInstruction"] = dns_instruction
        if http_instruction is not UNSET:
            field_dict["httpInstruction"] = http_instruction

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        domain = d.pop("domain", UNSET)

        verification_token = d.pop("verificationToken", UNSET)

        verification_method = d.pop("verificationMethod", UNSET)

        verified = d.pop("verified", UNSET)

        _verified_at = d.pop("verifiedAt", UNSET)
        verified_at: datetime.datetime | Unset
        if isinstance(_verified_at,  Unset):
            verified_at = UNSET
        else:
            verified_at = isoparse(_verified_at)




        _created_at = d.pop("createdAt", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




        dns_instruction = d.pop("dnsInstruction", UNSET)

        http_instruction = d.pop("httpInstruction", UNSET)

        verified_domain_response = cls(
            id=id,
            domain=domain,
            verification_token=verification_token,
            verification_method=verification_method,
            verified=verified,
            verified_at=verified_at,
            created_at=created_at,
            dns_instruction=dns_instruction,
            http_instruction=http_instruction,
        )


        verified_domain_response.additional_properties = d
        return verified_domain_response

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

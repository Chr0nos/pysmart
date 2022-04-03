from pydantic import BaseModel
from typing import List, Any, Tuple
from .flags import Flags


class RawValue(BaseModel):
    string: str
    value: int


class Attribute(BaseModel):
    id: int
    name: str
    raw: RawValue
    flags: Flags
    value: int
    worst: int


class Capabilities(BaseModel):
    attribute_autosave_enabled: bool
    conveyance_self_test_supported: bool
    error_logging_supported: bool
    gp_logging_supported: bool
    offline_is_aborted_upon_new_cmd: bool
    offline_surface_scan_supported: bool
    selective_self_test_supported: bool
    self_tests_supported: bool
    values: List[int]


class AtaSmartAttributes(BaseModel):
    revision: int
    table: List[Attribute]

    def mapping(self, lower: bool = False) -> dict[str, Attribute]:
        return dict({
            attribute.name if not lower else attribute.name.lower(): attribute
            for attribute in self.table
        })


class AtaSmartData(BaseModel):
    capabilities: Capabilities
    offline_data_collection: Any


class ErrorLogSummary(BaseModel):
    count: int
    revision: int


class ErrorLog(BaseModel):
    summary: ErrorLogSummary


class DriveDbVersion(BaseModel):
    string: str


class Device(BaseModel):
    name: str
    info_name: str
    type: str
    protocol: str


class SmartCtl(BaseModel):
    version: Tuple[int, int]
    platform_info: str
    build_info: str
    drive_database_version: DriveDbVersion


class SmartRoot(BaseModel):
    json_format_version: Tuple[int, int]
    smartctl: SmartCtl
    device: Device
    model_family: str
    model_name: str
    serial_number: str
    firmware_version: str
    logical_block_size: int
    physical_block_size: int
    rotation_rate: int = None
    ata_smart_attributes: AtaSmartAttributes
    ata_smart_data: AtaSmartData
    ata_smart_error_log: ErrorLog

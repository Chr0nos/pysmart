from models.disk import Disk
from datetime import timedelta


if __name__ == '__main__':
    disks = sorted(Disk.get_all())
    for disk in disks:
        options = []
        if disk.device == 'sda':
            options = ['-v', '1,raw48:54']
        smart = disk.read_smart(*options)
        attributes = smart.ata_smart_attributes.mapping(True)
        errors = attributes.get('raw_read_error_rate', None)
        if not errors or not errors.raw.value:
            continue
        powered_hours = attributes['power_on_hours'].raw.value
        powered = timedelta(hours=powered_hours)
        print(f'Disk {disk.device} has {errors.raw.value} read errors after {powered} power time. ({smart.model_family} [{smart.model_name}])')

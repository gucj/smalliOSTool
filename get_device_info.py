# coding=utf-8
__author__ = 'gucuijuan'
PRODUCT_TYPE_TO_DEVICE_NAME_MAP = {'iPad3,4': 'iPad', 'iPad3,5': 'iPad', 'iPad3,6': 'iPad', 'iPad3,1': 'iPad',
                                   'iPad3,2': 'iPad', 'iPad3,3': 'iPad', 'iPhone4,1': 'iPhone 4S',
                                   'iPhone2,1': 'iPhone 3GS', 'iPhone5,1': 'iPhone 5', 'iPad5,3': 'iPad Air 2',
                                   'iPhone5,3': 'iPhone 5c', 'iPhone5,2': 'iPhone 5', 'iPhone1,1': 'iPhone',
                                   'iPhone5,4': 'iPhone 5c', 'iPad5,4': 'iPad Air 2', 'iPhone1,2': 'iPhone 3G',
                                   'iPhone7,2': 'iPhone 6', 'iPhone7,1': 'iPhone 6 Plus', 'iPhone3,3': 'iPhone 4',
                                   'iPhone3,1': 'iPhone 4', 'iPad4,9': 'iPad mini 3', 'iPad4,8': 'iPad mini 3',
                                   'iPod4,1': 'iPod touch', 'iPhone8,1': 'iPhone 6s', 'iPhone8,2': 'iPhone 6s Plus',
                                   'iPhone6,2': 'iPhone 5s', 'iPad4,2': 'iPad Air', 'iPad4,1': 'iPad Air',
                                   'iPhone6,1': 'iPhone 5s', 'iPad4,7': 'iPad mini 3', 'iPad4,6': 'iPad mini 2',
                                   'iPad4,5': 'iPad mini 2', 'iPad4,4': 'iPad mini 2', 'iPad5,2': 'iPad mini 4',
                                   'iPod5,1': 'iPod touch', 'iPod1,1': 'iPod touch', 'iPad4,3': 'iPad Air',
                                   'iPad5,1': 'iPad mini 4', 'iPod3,1': 'iPod touch', 'iPad1,1': 'iPad',
                                   'iPod7,1': 'iPod touch', 'iPad2,5': 'iPad mini', 'iPad2,4': 'iPad 2',
                                   'iPad2,7': 'iPad mini', 'iPad2,6': 'iPad mini', 'iPad2,1': 'iPad 2',
                                   'iPad2,3': 'iPad 2', 'iPad2,2': 'iPad 2', 'iPod2,1': 'iPod touch'}  # 设备类型的映射


def get_device(device_info):
    """
    get device info of ProductType,ProductVersion,DeviceName,UniqueDeviceID,TimeZone.
    :param device_info:
    :return:dic of info.
    """
    device ={}
    info_list = device_info.split("\n")
    for info in info_list:
        if info.strip().startswith("ProductType"):
            product_type = info.split(":")[1].strip()
            if product_type in PRODUCT_TYPE_TO_DEVICE_NAME_MAP.iterkeys():
                product_type = PRODUCT_TYPE_TO_DEVICE_NAME_MAP[product_type]
            device["设备类型"] = product_type
        if info.strip().startswith("ProductVersion"):
            device["系统版本"] = info.split(":")[1].strip()
        if info.strip().startswith("UniqueDeviceID"):
            device["设备udid"] = info.split(":")[1].strip()
        if info.strip().startswith("DeviceName"):
            device["设备名称"] = info.split(":")[1].strip()
        if info.strip().startswith("TimeZone:"):
            device["设备时区"] = info.split(":")[1].strip()
    return device


import hid

target_name = 'USB gamepad'
vendor_id = None
product_id = None
# 0x081f:0xe401 USB gamepad
for device in hid.enumerate():
    # print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} '{device['product_string']}'")
    if device['product_string'].strip() == target_name:
        vendor_id = device['vendor_id']
        product_id = device['product_id']
print(f"{vendor_id} - {product_id}")

gamepad = hid.device()
gamepad.open(vendor_id, product_id)
gamepad.set_nonblocking(True)

def decode_triggers(byte):
    ltrigger = 'ltrigger' if byte & 1 != 0 else ''
    rtrigger = 'rtrigger' if byte & 2 != 0 else ''
    select = 'select' if byte & 16 != 0 else ''
    start_btn = 'start' if byte & 32 != 0 else ''
    return [ltrigger, rtrigger, select, start_btn]

def decode_buttons(byte):
    arr = [0,0,0,0]
    arr[3] = 'y' if byte & 0b10000000 != 0 else ''
    arr[2] = 'b' if byte & 0b01000000  != 0 else ''
    arr[1] = 'a' if byte & 0b00100000  != 0 else ''
    arr[0] = 'x' if byte & 0b00010000  != 0 else ''
    return arr

def decode_dpad(byteL, byteH):
    return [
        'l' if byteL == 0 else '',
        'r' if byteL == 255 else '',
        'u' if byteH == 0 else '',
        'd' if byteH == 255 else '',
    ]

while True:
    report = gamepad.read(64)
    if report:
        print( [ decode_dpad(report[0], report[1]),
            decode_triggers(report[6]),
            decode_buttons(report[5])])

        # print(report)

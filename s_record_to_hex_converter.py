from argparse import ArgumentParser

def get_hex_from_srecord(s_record_content: str) -> str:
    TARGET_RECORD_TYPE = 1 # For 16-bit address
    
    start_address = float('inf')
    contiguous_data = ''

    for line in s_record_content.split('\n'):
        # Ignore non-data lines
        if not line.startswith(f's{TARGET_RECORD_TYPE}'):
            continue

        address = int(line[4:8], 16) # Only true for 16-bit addresses
        data = line[8:-2] # Data only starts at index 8 if the address is 16-bit long

        if start_address == float('inf'):
            start_address = address

        gap = address - start_address
        # Fill gap with FF because then these addresses wouldn't need to be reerased via UV
        contiguous_data += 'FF' * gap
        contiguous_data += data

        # Each byte is 2 hex digits
        start_address += len(data) // 2

    return contiguous_data

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        '-f',
        '--input-file',
        help='Path to the input S-record file to use',
        required=True
    )

    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        print(get_hex_from_srecord(f.read()))
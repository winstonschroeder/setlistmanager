devices = (
    {
        'manufacturer': 'unknown',
        'manufacturer_code': 'KMR-1.8 SPI',
        'SCREEN_WIDTH': '160px',
        'SCREEN_HEIGHT': '128px',
        'has_touchscreen': False,
        'interface_display': 'SPI',
        'pin_labels': ['LED-', 'LED+', 'SD_CS', 'MOSI', 'MISO', 'SCK', 'CS', 'SCL', 'SDA', 'A0', 'RESET', 'NC', 'NC',
                       'NC', 'VCC', 'GND'],
        'pin_usage': {
            'LED-': 'BL_Cathode',
            'LED+': 'BL_Anode',
            'CS': 'TFT_CS',
            'SCL': 'TFT_SCK',
            'SDA': 'TFT_MOSI',
            'A0': 'TFT_RS/DC',
            'RESET': 'TFT_RESET',
        },
        'pin_RPI_assignment': {
            'BL_Cathode': 6,
            'BL_Anode': 4,
            'TFT_CS': 24,
            'TFT_SCK': 23,
            'TFT_MOSI': 19,
            'TFT_RS/DC': 18,
            'TFT_RESET': 22
        }
    },
    {
        'name': 'st7753',
        'manufacturer': 'Ardafruit',
    }
)

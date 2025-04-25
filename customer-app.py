# customer_app_simulator.py

import asyncio
import logging
import json

from bleak import BleakClient, BleakScanner, BleakError

# --- Configuration ---
# IMPORTANT: Use the SAME UUIDs as defined in the peripheral script!
TARGET_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0" # The Service UUID to scan for
TARGET_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1" # The Characteristic UUID to write to

# The JSON payload to send
JSON_PAYLOAD = {"someValue": "test"}

SCAN_TIMEOUT_SECONDS = 10
CONNECTION_TIMEOUT_SECONDS = 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def find_device_by_service(service_uuid: str, timeout: float) -> str | None:
    """Scans for BLE devices advertising the specified service UUID."""
    logger.info(f"Scanning for devices advertising service {service_uuid} for {timeout} seconds...")
    try:
        # Scan specifically for the service UUID for efficiency
        devices = await BleakScanner.discover(service_uuids=[service_uuid], timeout=timeout)

        if not devices:
            logger.warning("No devices found advertising the target service.")
            return None

        # In a real app, you might let the user choose if multiple are found
        # For this PoC, we take the first one
        device = devices[0]
        logger.info(f"Found device: {device.name} ({device.address})")
        return device.address

    except BleakError as e:
        logger.error(f"BleakError during scanning: {e}")
        logger.error("Ensure Bluetooth is enabled and permissions are granted.")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error during scanning: {e}")
        return None

async def send_data_to_device(device_address: str, char_uuid: str, data: bytes):
    """Connects to the device and writes data to the specified characteristic."""
    logger.info(f"Attempting to connect to {device_address}...")
    try:
        # The BleakClient context manager handles connection and disconnection
        async with BleakClient(device_address, timeout=CONNECTION_TIMEOUT_SECONDS) as client:
            if client.is_connected:
                logger.info("Successfully connected to device.")

                # Bleak automatically discovers services/characteristics on connection
                # You could optionally iterate client.services here to verify the characteristic exists

                logger.info(f"Attempting to write data to characteristic {char_uuid}...")
                try:
                    # write_gatt_char expects bytes
                    # response=True asks for acknowledgement (Write With Response)
                    # response=False for Write Without Response (faster, less reliable)
                    await client.write_gatt_char(char_uuid, data, response=True)
                    logger.info("Data successfully written.")
                    return True
                except BleakError as e:
                    logger.error(f"BleakError writing to characteristic {char_uuid}: {e}")
                    return False
                except Exception as e:
                    # Catch potential timeouts or other issues during the write operation
                    logger.exception(f"Unexpected error writing to characteristic: {e}")
                    return False
            else:
                logger.error("Failed to connect to the device.")
                return False

    except BleakError as e:
        logger.error(f"BleakError during connection or operation: {e}")
        return False
    except asyncio.TimeoutError:
        logger.error(f"Connection timed out after {CONNECTION_TIMEOUT_SECONDS} seconds.")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error during connection/disconnection: {e}")
        return False

async def main():
    """Main logic for the central device simulator."""
    logger.info("Starting Customer App Simulator (Central)...")

    device_address = await find_device_by_service(TARGET_SERVICE_UUID, SCAN_TIMEOUT_SECONDS)

    if device_address:
        # Prepare the data: Convert JSON object to string, then encode to bytes (UTF-8 is standard)
        try:
            json_string = json.dumps(JSON_PAYLOAD)
            data_bytes = json_string.encode('utf-8')
            logger.info(f"Prepared data payload: {data_bytes!r}") # Show byte representation

            success = await send_data_to_device(device_address, TARGET_CHAR_UUID, data_bytes)

            if success:
                logger.info("PoC Task Completed Successfully!")
            else:
                logger.error("PoC Task Failed: Could not write data.")

        except Exception as e:
            logger.exception(f"Error preparing or sending data: {e}")
    else:
        logger.error("PoC Task Failed: Target device not found.")

    logger.info("Customer App Simulator finished.")


if __name__ == "__main__":
    asyncio.run(main())
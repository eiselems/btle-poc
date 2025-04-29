from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import Characteristic, CharacteristicFlags
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UUIDs - same as in the JavaScript version
SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0'
CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1'

class MyService(Service):
    def __init__(self):
        super().__init__(SERVICE_UUID)
        
        # Create write characteristic
        self.write_char = Characteristic(
            CHARACTERISTIC_UUID,
            CharacteristicFlags.WRITE,
            self.on_write_request
        )
        self.add_characteristic(self.write_char)

    async def on_write_request(self, data):
        logger.info(f"Received data: {data.decode('utf-8')}")
        return True  # Success

async def main():
    logger.info("Starting BLE GATT server...")
    
    # Create and register agent (handles pairing)
    agent = NoIoAgent()
    
    # Create an advertisement
    advert = Advertisement("MyBLEDevice", [SERVICE_UUID])
    
    # Create service
    my_service = MyService()
    
    try:
        # Start the service
        await advert.start()
        await my_service.start()
        logger.info("Advertising started...")
        
        # Keep the server running
        await asyncio.get_running_loop().create_future()
    except KeyboardInterrupt:
        logger.info("Stopping BLE server...")
    finally:
        await advert.stop()
        await my_service.stop()

if __name__ == "__main__":
    asyncio.run(main())
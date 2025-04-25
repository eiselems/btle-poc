const bleno = require('@abandonware/bleno');

const SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0';
const CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1';

console.log('Starting BLE GATT server...');

const BlenoPrimaryService = bleno.PrimaryService;
const BlenoCharacteristic = bleno.Characteristic;

const writeCharacteristic = new BlenoCharacteristic({
  uuid: CHARACTERISTIC_UUID,
  properties: ['write'],
  onWriteRequest: function(data, offset, withoutResponse, callback) {
    console.log('Received data: ', data.toString('utf8'));
    callback(this.RESULT_SUCCESS);
  }
});

const primaryService = new BlenoPrimaryService({
  uuid: SERVICE_UUID,
  characteristics: [writeCharacteristic]
});

bleno.on('stateChange', (state) => {
  console.log(`Bluetooth state changed to: ${state}`);
  if (state === 'poweredOn') {
    bleno.startAdvertising('MyBLEDevice', [SERVICE_UUID]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', (error) => {
  if (error) {
    console.error('Advertising start error:', error);
  } else {
    console.log('Advertising started...');
    bleno.setServices([primaryService]);
  }
});

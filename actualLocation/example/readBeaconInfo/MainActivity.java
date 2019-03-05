package yong.bttest;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import static yong.bttest.mMethod.bytesToHexString;
import static yong.bttest.mMethod.sortMapByValue;


public class MainActivity extends AppCompatActivity {
    private static final String TAG = "bttest";
    private BluetoothManager mBluetoothManager;
    private BluetoothAdapter mBluetoothAdapter;
    private Handler mHandler =  new Handler();
    private BluetoothAdapter.LeScanCallback mLeScanCallback;
    private TextView beacon0,beacon1,beacon2,beacon3;
    private boolean flag_firstOpenFile=true;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (this.checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
        }
        beacon0 = (TextView)findViewById(R.id.beacon0);
        beacon1 = (TextView)findViewById(R.id.beacon1);
        beacon2 = (TextView)findViewById(R.id.beacon2);
        beacon3 = (TextView)findViewById(R.id.beacon3);

        initialize();
        OpenBlue();
        //mHandler.postDelayed(mRunnable, 1000);
        save("start:\n");
        mLeScanCallback = new mmLeScanCallback();
        scanLeDevice();
    }

    public boolean initialize(){
        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)){
            Log.e(TAG, "Unable to initialize Bluetooth.");
            return false;
        }
        mBluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        if (mBluetoothManager == null){
            Log.e(TAG, "Unable to initialize BluetoothManager.");
            return false;
        }
        mBluetoothAdapter = mBluetoothManager.getAdapter();
        if (mBluetoothAdapter == null){
            Log.e(TAG, "Unable to obtain a BluetoothAdapter.");
            return false;
        }
        return true;
    }

    public boolean OpenBlue()
    {
        //开启蓝牙
        if (!mBluetoothAdapter.isEnabled())
            return mBluetoothAdapter.enable();
        else
            return true;
    }

    private void scanLeDevice(){
        Log.e(TAG, "start scanLeDevice");
        mBluetoothAdapter.startLeScan(mLeScanCallback);//这句就是开始扫描了
    }

    class mmLeScanCallback implements BluetoothAdapter.LeScanCallback {
            @Override
            public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord){
            byte[] data = new byte[31];
            System.arraycopy(scanRecord, 0, data, 0, 31);
            String hexString = bytesToHexString(data);
            byte[] prefixBytes = new byte[9];
            byte[] uuidBytes = new byte[16];
            byte[] majorBytes = new byte[2];
            byte[] minorBytes = new byte[2];
            byte[] txPowerBytes = new byte[2];
            if(device != null){
                System.arraycopy(scanRecord, 0, prefixBytes, 0, 9);
                System.arraycopy(scanRecord, 9, uuidBytes, 0, 16);
                System.arraycopy(scanRecord, 25, majorBytes, 0, 2);
                System.arraycopy(scanRecord, 27, minorBytes, 0, 2);
                System.arraycopy(scanRecord, 29, txPowerBytes, 0, 2);
//                Log.w(TAG, "device name:" + device.getName());
//                beacon0.setText("device name:"+device.getName());
                String uuidString = bytesToHexString(uuidBytes);
                String majorString = bytesToHexString(majorBytes);
                String minorString = bytesToHexString(minorBytes);
                String txPowerString = bytesToHexString(txPowerBytes);
//                Log.w(TAG, "uuidBytes:" + uuidString);
//                Log.w(TAG, "majorBytes:" + majorString);
//                Log.w(TAG, "minorBytes:" + minorString);
//                Log.w(TAG, "txPowerBytes:" + txPowerString);
//                Log.w(TAG, "rssi:" + rssi);

                if((majorBytes[0]==0x13 || majorBytes[1]==0x09) && (minorBytes[0]==0x68 || minorBytes[1]==0x6f)) {
                    Log.w(TAG, "uuidBytes:" + uuidString);
                    Log.w(TAG, "majorBytes:" + majorString);
                    Log.w(TAG, "minorBytes:" + minorString);
                    Log.w(TAG, "txPowerBytes:" + txPowerString);
                    Log.w(TAG, "rssi:" + rssi);
                    beacon0.setText(uuidString);
                    beacon1.setText(majorString);
                    beacon2.setText(minorString);
                    beacon3.setText(txPowerString + "+" + rssi);
                }
                save(uuidString+":\t"+rssi+"\n");

            }
        }
    }

    /*
    Runnable mRunnable = new Runnable() {
        @Override
        public void run() {

            mHandler.postDelayed(this, 1000);
            Log.i(TAG, "runnable delay 1000ms!" );
        }
    };*/

    public void save(String inputText) {
        FileOutputStream out = null;
        BufferedWriter writer = null;

        try {
            if(flag_firstOpenFile) {
                out = openFileOutput("beacon_data", Context.MODE_PRIVATE);
                flag_firstOpenFile = false;
            }

            else
                out = openFileOutput("beacon_data", Context.MODE_APPEND);
            writer = new BufferedWriter(new OutputStreamWriter(out));
            writer.write(inputText);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (writer != null) {
                    writer.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 1:
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Log.e(TAG, "get permission");
                }
                break;
        }
    }

}
    


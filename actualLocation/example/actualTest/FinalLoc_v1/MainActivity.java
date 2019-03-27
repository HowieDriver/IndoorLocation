package yong.bttest;

import android.Manifest;
import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import static yong.bttest.mMethod.bytesToHexString;
import static yong.bttest.mMethod.sortMapByValue;


public class MainActivity extends AppCompatActivity {
    private static final String TAG = "bttest";
    private BluetoothAdapter mBluetoothAdapter;
    private Handler mHandler =  new Handler();
    private BluetoothAdapter.LeScanCallback mLeScanCallback;
    private TextView uidTV, grupTV, subGrupTV, rssiTV, text;
    private boolean flag_firstOpenFile=true;
    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (this.checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
        }
        uidTV = findViewById(R.id.beacon0);
        grupTV = findViewById(R.id.beacon1);
        subGrupTV = findViewById(R.id.beacon2);
        rssiTV = findViewById(R.id.beacon3);
        text = (TextView)findViewById(R.id.text);
        new Thread(networkTask).start();
        if(initialize()) {
            Log.d(TAG, "initialize successful");
        }
        else {
            Log.e(TAG, "initialize failed");
        }
        save("start:\n");
        mLeScanCallback = new mmLeScanCallback();
        scanLeDevice();

    }


    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle data = msg.getData();
            String val = data.getString("key");
            text.setText(val);
        }
    };

    Runnable networkTask = new Runnable() {
        @Override
        public void run() {
            while(true) {
                try {
                    Socket socket = new Socket("192.168.1.125", 21567);
                    //获取输出流，向服务器端发送信息
                    OutputStream os = socket.getOutputStream();//字节输出流
                    PrintWriter pw = new PrintWriter(os);//将输出流包装为打印流
                    //send id-dist2;id-dist2
                    pw.write("0-53;1-13;2-13;3-53;4-8");
                    Log.i(TAG, "write socket");
                    pw.flush();
                    socket.shutdownOutput();//关闭输出流

                    InputStream is = socket.getInputStream();
                    BufferedReader in = new BufferedReader(new InputStreamReader(is));
                    String info = null;
                    while ((info = in.readLine()) != null) {
                        Log.i(TAG, "get info from server：" + info);
                        Message msg = new Message();
                        Bundle data = new Bundle();
                        data.putString("key", "From python：" + info);
                        msg.setData(data);
                        handler.sendMessage(msg);
                    }
                    is.close();
                    in.close();
                    socket.close();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    };
    public boolean initialize(){
        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)){
            Log.e(TAG, "Unable to initialize Bluetooth.");
            return false;
        }
        BluetoothManager mBluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        if (mBluetoothManager == null){
            Log.e(TAG, "Unable to initialize BluetoothManager.");
            return false;
        }
        mBluetoothAdapter = mBluetoothManager.getAdapter();
        if (mBluetoothAdapter == null){
            Log.e(TAG, "Unable to obtain a BluetoothAdapter.");
            return false;
        }
        return mBluetoothAdapter.isEnabled() || mBluetoothAdapter.enable();
    }


    private void scanLeDevice(){
        Log.e(TAG, "start scanLeDevice");
        mBluetoothAdapter.startLeScan(mLeScanCallback);//开始扫描
    }

    class mmLeScanCallback implements BluetoothAdapter.LeScanCallback {
        @SuppressLint("SetTextI18n")
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
                String uuidString = bytesToHexString(uuidBytes);
                String majorString = bytesToHexString(majorBytes);
                String minorString = bytesToHexString(minorBytes);
                String txPowerString = bytesToHexString(txPowerBytes);

                //if((majorBytes[0]==0x13 || majorBytes[1]==0x09) && (minorBytes[0]==0x68 || minorBytes[1]==0x6f)) {
                    Log.d(TAG, "uuidBytes:" + uuidString);
                    Log.d(TAG, "majorBytes:" + majorString);
                    Log.d(TAG, "minorBytes:" + minorString);
                    Log.d(TAG, "txPowerBytes:" + txPowerString);
                    Log.d(TAG, "rssi:" + rssi);
                    uidTV.setText("Uid: " + uuidString);
                    grupTV.setText("Grup: " + majorString);
                    subGrupTV.setText("SubGrup: " + minorString);
                    rssiTV.setText("Rssi: " + rssi);
                //}
                //save(uuidString+":\t"+rssi+"\n");

            }
        }
    }



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



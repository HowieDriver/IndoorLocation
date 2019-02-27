package yong.webtest;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    private TextView text;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        text = (TextView)findViewById(R.id.text);
        new Thread(networkTask).start();

    }

    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle data = msg.getData();
            String val = data.getString("value");
            text.setText(text.getText()+"\n"+val);
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
                    pw.write("Hello Server!");
                    pw.flush();
                    socket.shutdownOutput();//关闭输出流

                    InputStream is = socket.getInputStream();
                    BufferedReader in = new BufferedReader(new InputStreamReader(is));
                    String info = null;
                    while ((info = in.readLine()) != null) {
                        //System.out.println("我是客户端，Python服务器说："+info);
                        //Log.w("MAIN", "我是客户端，Python服务器说：" + info);
                        Message msg = new Message();
                        Bundle data = new Bundle();
                        data.putString("value", "From python：" + info);
                        msg.setData(data);
                        handler.sendMessage(msg);
                    }
                    is.close();
                    in.close();
                    socket.close();
                } catch (UnknownHostException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    };

}
package yong.bttest;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.Log;
import android.view.View;

public class DrawView extends View {
    private float x=0;
    private float y=0;
    public DrawView(Context context) {
        super(context);
    }
    public void setxy(float x, float y) {
        this.x = x;
        this.y = y;
    }
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Paint p = new Paint();
        p.setColor(Color.BLUE);// 设置红色
        //canvas.drawText("画圆：", 10, 20, p);// 画文本
        //canvas.drawCircle(550, 350, 50, p);// 小圆
        //p.setAntiAlias(true);// 设置画笔的锯齿效果。 true是去除，大家一看效果就明白了
        //canvas.drawLine(60, 40, 100, 40, p);// 画线
        p.setStrokeWidth(50);
        canvas.drawPoint(550,700,p);

        canvas.drawPoint(50,700,p);
        canvas.drawPoint(1050,700,p);

        canvas.drawPoint(550,200,p);
        canvas.drawPoint(550,1200,p);

        if((x>=0.01f || x<=-0.01f) && (y>=0.01f || y <=0.01f)) {
            p.setColor(Color.RED);// 设置红色
            //canvas.drawText("画圆：", 10, 20, p);// 画文本
            int x = 550 + (int)(this.x * 100f);
            int y = 700 - (int)(this.y * 100f);
            if(x < 0) {
                x = 550 - (int)(this.x * 100f);
            }
            if(y < 0) {
                y = 700 + (int)(this.y * 100f);
            }

            canvas.drawCircle(x, y, 20, p);// 小
            Log.w("bttest", "enter draw mydraw");
            Log.w("bttest", "x="+x);
            Log.w("bttest", "y="+y);

        }

        p.setColor(Color.GRAY);// 设置红色
        p.setStrokeWidth(10);
        canvas.drawLine(50, 200, 1050, 200, p);// 画线
        canvas.drawLine(50, 1200, 1050, 1200, p);// 画线

        canvas.drawLine(50, 200, 50, 1200, p);// 画线
        canvas.drawLine(1050, 200, 1050, 1200, p);// 画线
    }

}

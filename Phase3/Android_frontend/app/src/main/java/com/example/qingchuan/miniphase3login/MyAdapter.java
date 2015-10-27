package com.example.qingchuan.miniphase3login;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

/**
 * Created by Qingchuan on 10/26/2015.
 */
public class MyAdapter extends BaseAdapter {
    private Context mContext;
    private ArrayList<String> imageURLs;
    private ArrayList<String> stream_name;
    private ArrayList<String> streamOwner;
    private LayoutInflater mflater;
    private String usr_email;

    public MyAdapter(Context c, ArrayList<String> imageURLs,
                         ArrayList<String> stream_name, ArrayList<String> streamOwner, String usr_email,
                         LayoutInflater inflater) {
        mContext = c;
        mflater = inflater;
        this.imageURLs = imageURLs;
        this.stream_name = stream_name;
        this.streamOwner = streamOwner;
        this.usr_email = usr_email;
    }

    @Override
    public int getCount() {
        return imageURLs.size();
    }

    @Override
    public Object getItem(int position) {
        // TODO Auto-generated method stub
        return position;
    }

    @Override
    public long getItemId(int position) {
        // TODO Auto-generated method stub
        return position;
    }

    public class Holder
    {
        TextView tv;
        ImageView img;
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        // TODO Auto-generated method stub
        Holder holder=new Holder();
        View rowView;

        rowView = mflater.inflate(R.layout.nearby_picview, null);
        holder.tv=(TextView) rowView.findViewById(R.id.nearby_textView1);
        holder.img=(ImageView) rowView.findViewById(R.id.nearby_imageView1);

        holder.tv.setText(stream_name.get(position));
        Picasso.with(mContext).load(imageURLs.get(position)).into(holder.img);

        rowView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(mContext, ViewSingleStream.class);
                i.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                i.putExtra(ViewStreamFragment.STREAM_OWNER, streamOwner.get(position));
                i.putExtra(ViewStreamFragment.STREAM_NAME, stream_name.get(position));
                mContext.startActivity(i);
            }
        });
        return rowView;
    }
}

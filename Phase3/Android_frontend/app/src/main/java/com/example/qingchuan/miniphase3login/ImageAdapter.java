package com.example.qingchuan.miniphase3login;

/**
 * Created by Qingchuan on 10/23/2015.
 */
import android.view.LayoutInflater;
import android.widget.BaseAdapter;
import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.GridView;
import com.squareup.picasso.Picasso;

import java.util.ArrayList;

public class ImageAdapter extends BaseAdapter {
    private Context mContext;
    private ArrayList<String> imageURLs;
    private LayoutInflater mflater;

    public ImageAdapter(Context c, ArrayList<String> imageURLs, LayoutInflater inflater) {
        mContext = c;
        mflater = inflater;
        this.imageURLs = imageURLs;
    }

    public int getCount() {
        return imageURLs.size();
    }

    public Object getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    // create a new ImageView for each item referenced by the Adapter
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView imageView;
        if (convertView == null) {  // if it's not recycled, initialize some attributes
            convertView = mflater.inflate(R.layout.gallery_item, parent, false);
        }
            imageView = (ImageView)convertView.findViewById(R.id.gallery_item_imageView);

        Picasso.with(mContext).load(imageURLs.get(position)).into(imageView);
        return imageView;
    }

}

package com.example.qingchuan.miniphase3login;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.GridView;
import android.widget.Toast;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Set;

/**
 * Created by Qingchuan on 10/24/2015.
 */
public class nearbyPictures extends ActionBarActivity {

    private String TAG  = "View Nearby";
    private String device_lat;
    private String device_long;
    private String usr_email;
    private Button back_from_nearby;

    private int currentpage = 1;
    private int upbound = 1;
    Button view_nearyby_pre;
    Button view_neraby_more;

    final ArrayList<String>  pic_url = new ArrayList<String>();
    final ArrayList<String>  dist_pic = new ArrayList<String>();
    final ArrayList<String>  stream_name_pic = new ArrayList<String>();
    final ArrayList<String>  stream_owner_pic = new ArrayList<String>();

    private class nearbyPic {
        public String pic_url;
        public String pic_dist;
        public String pic_stream;
        public String pic_stream_owner;

        public nearbyPic(String pic_url, String pic_dist, String pic_stream, String pic_stream_owner){
            this.pic_url = pic_url;
            this.pic_dist = pic_dist;
            this.pic_stream = pic_stream;
            this.pic_stream_owner = pic_stream_owner;
        }
    }

    private class nearPicCompare implements Comparator<nearbyPic>{
        @Override
        public int compare(nearbyPic pic1, nearbyPic pic2){
            Integer dist_pic1 = Integer.parseInt(pic1.pic_dist);
            Integer dist_pic2 = Integer.parseInt(pic2.pic_dist);
            return dist_pic1.compareTo(dist_pic2);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nearby);

        view_nearyby_pre = (Button)findViewById(R.id.nearby_view_previous);
        view_neraby_more = (Button)findViewById(R.id.nearby_view_more);

        view_nearyby_pre.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(view_nearyby_pre.isEnabled()){
                    currentpage--;
                    setupAdapterWrapper();
                }
            }
        });

        view_neraby_more.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(view_neraby_more.isEnabled()){
                    currentpage++;
                    setupAdapterWrapper();
                }
            }
        });

        device_lat = MainActivity.device_lat;
        device_long = MainActivity.device_long;
        usr_email = getIntent().getStringExtra(ViewStreamFragment.LOGIN_USER);

        back_from_nearby = (Button)findViewById(R.id.back_from_nearbypics);
        back_from_nearby.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(nearbyPictures.this, ViewStreams.class);
                intent.putExtra(MainActivity.LOGIN_USER_INFO, usr_email);
                startActivity(intent);
            }
        });

        final String request_url = "http://connexversion3.appspot.com/viewNearby";
        AsyncHttpClient httpClient = new AsyncHttpClient();
        RequestParams params = new RequestParams();
        params.add("device_lat", device_lat);
        params.add("device_long", device_long);

        final List<nearbyPic> nearPic_bundles = new ArrayList<nearbyPic>();



        httpClient.get(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray pics_url = jObject.getJSONArray("pic_url");
                    JSONArray stream_names_of_pic = jObject.getJSONArray("stream_names");
                    JSONArray stream_owner_of_pic = jObject.getJSONArray("stream_owner");
                    JSONArray pic_dist = jObject.getJSONArray("dist_dev2pic");

                    for(int i=0; i<pics_url.length(); i++){
                        // construct the nearbyPic and put to array
                        nearbyPic newPic = new nearbyPic(pics_url.getString(i),
                                                        pic_dist.getString(i),
                                                        stream_names_of_pic.getString(i),
                                                        stream_owner_of_pic.getString(i));
                        nearPic_bundles.add(newPic);
                    }

                    Collections.sort(nearPic_bundles, new nearPicCompare());

                    for(int i=0;i<pics_url.length();i++) {
                        nearbyPic temp = nearPic_bundles.get(i);
                        pic_url.add(temp.pic_url);
                        dist_pic.add(temp.pic_dist);
                        stream_name_pic.add(temp.pic_stream);
                        stream_owner_pic.add(temp.pic_stream_owner);
                    }

                    upbound = pic_url.size()%3 == 0 ? pic_url.size()/3 : pic_url.size()/3 + 1;

                    setupAdapter(pic_url, dist_pic,stream_name_pic,stream_owner_pic,usr_email);
                    //Toast.makeText(nearbyPictures.this, "the dist is "+dist_pic.get(0), Toast.LENGTH_LONG).show();
                }catch(JSONException j){
                    System.out.println("JSON Error");
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }

    private void setupAdapterWrapper(){
        setupAdapter(pic_url, dist_pic,stream_name_pic,stream_owner_pic,usr_email);
    }

    private void setupAdapter(ArrayList<String> imageurllist, ArrayList<String> dist_list,
                              ArrayList<String> stream_name, ArrayList<String> stream_owner, String usr_email){

        GridView mGridView = (GridView)this.findViewById(R.id.nearbypicsGrid);
        if(mGridView == null) return;
        Log.i(TAG,"We are in near by stream adapter");

        boolean has_more = false;
        boolean has_less = false;
        if(currentpage < upbound)
            has_more = true;
        if(currentpage > 1)
            has_less = true;

        if(!has_more){
            // disable the more button
            view_neraby_more.setEnabled(false);
        }else {
            view_neraby_more.setEnabled(true);
        }

        if(has_less){
            // make less button visible
            view_nearyby_pre.setVisibility(View.VISIBLE);
            view_nearyby_pre.setEnabled(true);
        }else {
            view_nearyby_pre.setVisibility(View.INVISIBLE);
            view_nearyby_pre.setEnabled(false);
        }

        int start_index = (currentpage-1)*3;
        int end_index = start_index +3;
        if(end_index > imageurllist.size())
            end_index = imageurllist.size();

        ArrayList<String> url_to_show = new ArrayList<String>(imageurllist.subList(start_index, end_index));
        ArrayList<String> dist_to_show = new ArrayList<String>(dist_list.subList(start_index, end_index));
        ArrayList<String> streamname_to_show = new ArrayList<String>(stream_name.subList(start_index, end_index));
        ArrayList<String> streamowner_to_show = new ArrayList<String>(stream_owner.subList(start_index, end_index));

        mGridView.setAdapter(new CustomAdapter(nearbyPictures.this,
                url_to_show, dist_to_show, streamname_to_show, streamowner_to_show,usr_email,
                this.getLayoutInflater()));
    }
}

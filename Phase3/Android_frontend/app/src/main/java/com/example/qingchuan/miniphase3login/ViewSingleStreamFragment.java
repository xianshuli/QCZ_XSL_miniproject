package com.example.qingchuan.miniphase3login;

import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.GridView;
import android.widget.TextView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Created by Qingchuan on 10/23/2015.
 */
public class ViewSingleStreamFragment extends Fragment {

    private String stream_owner;
    private String login_usr;
    private String stream_name;
    private String TAG  = "View Single Stream";
    private GridView mGridView;

    private Button uploadButton;
    private Button backToStreamButton;
    private Button swithPageButton_more;
    private Button swithPageButton_less;
    private int currentPage = 1;

    ArrayList<String> imageurls = new ArrayList<String>();
    private int upbound = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        stream_owner = getActivity().getIntent().getStringExtra(ViewStreamFragment.STREAM_OWNER);
        login_usr = getActivity().getIntent().getStringExtra(ViewStreamFragment.LOGIN_USER);
        stream_name = getActivity().getIntent().getStringExtra(ViewStreamFragment.STREAM_NAME);
        Log.i(TAG, "Stream owner is " + stream_owner + " login usr is " + login_usr + " stream name is " + stream_name);
        fillStreamInGrid();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View v = inflater.inflate(R.layout.view_singlestream, container, false);
        TextView usr_info = (TextView)v.findViewById(R.id.login_usr);
        TextView textview_stream_name = (TextView)v.findViewById(R.id.view_single_stream_name);
        textview_stream_name.setText(stream_name);
        usr_info.setText(login_usr);
        mGridView = (GridView)v.findViewById(R.id.viewSingleStream);
        uploadButton = (Button)v.findViewById(R.id.upload_button);
        backToStreamButton = (Button)v.findViewById(R.id.back_to_stream_button);
        swithPageButton_more = (Button)v.findViewById(R.id.switch_page_button_more);
        swithPageButton_less = (Button)v.findViewById(R.id.switch_page_button_less);

        Log.i(TAG,"I got login usr = "+login_usr+" and stream owner= "+stream_owner);
        if(!stream_owner.equals(login_usr))
            uploadButton.setEnabled(false);

        uploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getActivity(), ImageUpload.class);
                intent.putExtra(ViewStreamFragment.STREAM_NAME, stream_name);
                intent.putExtra(ViewStreamFragment.LOGIN_USER, login_usr);
                intent.putExtra(ViewStreamFragment.STREAM_OWNER, stream_owner);
                startActivity(intent);
            }
        });

        backToStreamButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getActivity(), ViewStreams.class);
                intent.putExtra(MainActivity.LOGIN_USER_INFO, login_usr);
                startActivity(intent);
            }
        });

        swithPageButton_more.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(swithPageButton_more.isEnabled()){
                    currentPage++;
                    setupAdapter(imageurls);
                }
            }
        });

        swithPageButton_less.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(swithPageButton_less.isEnabled()){
                    currentPage--;
                    setupAdapter(imageurls);
                }
            }
        });


        return v;
    }

    private void setupAdapter(ArrayList<String> imageurllist){
        if(getActivity() == null || mGridView == null) return;
        Log.i(TAG,"We are in single stream adapter");

        boolean has_more = false;
        boolean has_less = false;
        if(currentPage < upbound)
            has_more = true;
        if(currentPage > 1)
            has_less = true;

        if(!has_more){
            // disable the more button
            swithPageButton_more.setEnabled(false);
        }else {
            swithPageButton_more.setEnabled(true);
        }

        if(has_less){
            // make less button visible
            swithPageButton_less.setVisibility(View.VISIBLE);
            swithPageButton_less.setEnabled(true);
        }else {
            swithPageButton_less.setVisibility(View.INVISIBLE);
            swithPageButton_less.setEnabled(false);
        }

        // assemble the images
        int start_index = (currentPage-1)*3;
        int end_index = start_index +3;
        if(end_index > imageurllist.size())
            end_index = imageurllist.size();
        mGridView.setAdapter(new ImageAdapter(getActivity(),
                new ArrayList<String>(imageurllist.subList(start_index, end_index)),
                getActivity().getLayoutInflater()));
    }

    private void fillStreamInGrid(){
        final String request_url = "http://connexversion3.appspot.com/mobileViewSingleStream?Stream_id="+stream_name;
        AsyncHttpClient httpClient = new AsyncHttpClient();
        RequestParams params = new RequestParams();
        params.add("usr_launch_search", login_usr);
        httpClient.get(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray images_url = jObject.getJSONArray("image_url");

                    for(int i=0;i<images_url.length();i++) {
                        imageurls.add(images_url.getString(i));
                    }
                    upbound = imageurls.size()%3 == 0 ? imageurls.size()/3 : imageurls.size()/3 + 1;

                    setupAdapter(imageurls);

                    Log.i(TAG, "we get single stream with page bound "+upbound);

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
}

package com.example.qingchuan.miniphase3login;

import android.app.Fragment;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Created by Qingchuan on 10/23/2015.
 */
public class ViewStreamFragment extends Fragment {
    private String usr_email = null;
    private String TAG  = "View all streams";
    public static final String STREAM_OWNER = "com.example.qingchuan.miniphase3login.stream_owner";
    public static final String STREAM_NAME = "com.example.qingchuan.miniphase3login.stream_name";
    public static final String LOGIN_USER = "com.example.qingchuan.miniphase3login.loginusr";
    public static final String DEVICE_LAT = "com.example.qingchuan.miniphase3login.devicelat";
    public static final String DEVICE_LONG = "com.example.qingchuan.miniphase3login.devicelong";
    public static final String SEARCH_KEY = "com.example.qingchuan.miniphase3login.searchkey";
    GridView mGridView;
    Button viewNearBy;
    Button viewSubscribe;
    Button launchSearchButton;
    TextView helloView;
    EditText searchField;
    ArrayList<String> mItems = new ArrayList<String>();
    private String searchKeywords = "";

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        usr_email = getActivity().getIntent().getStringExtra(MainActivity.LOGIN_USER_INFO);
        fillStreamInGrid();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View v = inflater.inflate(R.layout.fragment_viewstreams, container, false);

        mGridView = (GridView)v.findViewById(R.id.viewStreams);
        viewNearBy = (Button)v.findViewById(R.id.view_near_by);
        viewSubscribe = (Button)v.findViewById(R.id.view_subscribe);
        helloView = (TextView)v.findViewById(R.id.helloViewStreams);
        searchField = (EditText)v.findViewById(R.id.search_filed_onViewAll);
        launchSearchButton = (Button)v.findViewById(R.id.search_button_onViewAll);

        if(usr_email != null){
            viewSubscribe.setEnabled(true);
            helloView.setText(usr_email);
        }else {
            viewSubscribe.setEnabled(false);
        }

        searchField.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(count > 0){
                    launchSearchButton.setEnabled(true);
                    searchKeywords = s.toString();
                }else{
                    launchSearchButton.setEnabled(false);
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        launchSearchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getActivity(), searchEngine.class);
                intent.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                intent.putExtra(ViewStreamFragment.SEARCH_KEY, searchKeywords);
                startActivity(intent);
            }
        });

        viewNearBy.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getActivity(), nearbyPictures.class);
                intent.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                startActivity(intent);
            }
        });

        viewSubscribe.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), ViewSubscribe.class);
                intent.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                startActivity(intent);
            }
        });

        return v;
    }

    private void setupAdapter(ArrayList<String> coverurllist, ArrayList<String> stream_name,
                                ArrayList<String> stream_owner){
        if(getActivity() == null || mGridView == null) return;
        Log.i(TAG,"We are in adapter");
        //mGridView.setAdapter(new ArrayAdapter<String>(getActivity(),
        //        android.R.layout.simple_gallery_item, mItems));
       // mGridView.setAdapter(new ImageAdapter(getActivity(),coverurllist,getActivity().getLayoutInflater()));

        mGridView.setAdapter(new MyAdapter(getActivity(),coverurllist, stream_name, stream_owner,
                usr_email, getActivity().getLayoutInflater()
                ));
    }

    private void fillStreamInGrid(){
        final String request_url = "http://connexversion3.appspot.com/viewAllStreams";
        final ArrayList<String> imageURLs = new ArrayList<String>();
        final ArrayList<String> streamOwner = new ArrayList<String>();
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray stream_names = jObject.getJSONArray("displayImages_name");
                    JSONArray stream_coverurl = jObject.getJSONArray("displayImages_coverurl");
                    JSONArray stream_owner = jObject.getJSONArray("stream_owner");



                    for(int i=0;i<stream_names.length();i++) {
                        mItems.add(stream_names.getString(i));
                        imageURLs.add(stream_coverurl.getString(i));
                        streamOwner.add(stream_owner.getString(i));
                    }

                    setupAdapter(imageURLs, mItems, streamOwner);

                    /*
                    mGridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                        @Override
                        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                            String thisStreamOwner = streamOwner.get(position);
                            Intent i = new Intent(getActivity(), ViewSingleStream.class);
                            i.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                            i.putExtra(ViewStreamFragment.STREAM_OWNER, thisStreamOwner);
                            i.putExtra(ViewStreamFragment.STREAM_NAME, mItems.get(position));
                            startActivity(i);
                        }
                    });*/

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

package com.example.qingchuan.miniphase3login;

import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.GridView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Created by Qingchuan on 10/25/2015.
 */
public class ViewSubscribeFragment extends Fragment  {
    private String usr_email = null;
    private String TAG  = "View subscribe";
    private Button back_to_viewall;
    GridView mGridView;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        usr_email = getActivity().getIntent().getStringExtra(ViewStreamFragment.LOGIN_USER);
        fillStreamInGrid();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View v = inflater.inflate(R.layout.fragment_viewsubscribe, container, false);
        mGridView = (GridView)v.findViewById(R.id.viewSubStreamsGridView);
        back_to_viewall = (Button)v.findViewById(R.id.back_from_viewsub);
        back_to_viewall.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), ViewStreams.class);
                intent.putExtra(MainActivity.LOGIN_USER_INFO, usr_email);
                startActivity(intent);
            }
        });
        return v;
    }

    private void setupAdapter(ArrayList<String> coverurllist){
        if(getActivity() == null || mGridView == null) return;
        Log.i(TAG,"We are in adapter");
        //mGridView.setAdapter(new ArrayAdapter<String>(getActivity(),
        //        android.R.layout.simple_gallery_item, mItems));
        mGridView.setAdapter(new ImageAdapter(getActivity(), coverurllist, getActivity().getLayoutInflater()));
    }

    private void fillStreamInGrid(){
        final String request_url = "http://connexversion3.appspot.com/mobileViewSubscribe";
        final ArrayList<String> imageURLs = new ArrayList<String>();
        final ArrayList<String> streamOwner = new ArrayList<String>();
        final ArrayList<String> streamName = new ArrayList<String>();

        RequestParams params = new RequestParams();
        params.add("usr_email", usr_email);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, params, new AsyncHttpResponseHandler() {

            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray stream_names = jObject.getJSONArray("stream_names");
                    JSONArray stream_owners = jObject.getJSONArray("stream_owners");
                    JSONArray cover_urls = jObject.getJSONArray("cover_url");
                    boolean has_substream = jObject.getBoolean("hasSubStream");

                    Log.i(TAG, usr_email + " has sub " + has_substream);

                    for(int i=0;i<stream_names.length();i++) {
                        streamName.add(stream_names.getString(i));
                        imageURLs.add(cover_urls.getString(i));
                        streamOwner.add(stream_owners.getString(i));
                    }

                    setupAdapter(imageURLs);

                    mGridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                        @Override
                        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                            Intent i = new Intent(getActivity(), ViewSingleStream.class);
                            i.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                            i.putExtra(ViewStreamFragment.STREAM_OWNER, streamOwner.get(position));
                            i.putExtra(ViewStreamFragment.STREAM_NAME, streamName.get(position));
                            startActivity(i);
                        }
                    });

                } catch (JSONException j) {
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

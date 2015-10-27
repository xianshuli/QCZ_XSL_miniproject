package com.example.qingchuan.miniphase3login;

import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
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
 * Created by Qingchuan on 10/25/2015.
 */
public class SearchEngineFragment extends Fragment  {

    private String TAG  = "Search Engine";
    private String usr_email = null;
    private String searchKeywords = "";
    private String searchKeywords_fromhere = "";
    boolean find_match = false;
    boolean search_result;
    private int upbound = 1;
    private int currentpage = 1;

    TextView search_result_tag;
    Button back_to_viewAll;
    Button launchSearchButton;
    Button prevButton;
    Button moreButton;
    EditText searchField;

    final ArrayList<String> pic_url = new ArrayList<String>();
    final ArrayList<String>  stream_name_pic = new ArrayList<String>();
    final ArrayList<String>  stream_owner_pic = new ArrayList<String>();

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        usr_email = getActivity().getIntent().getStringExtra(ViewStreamFragment.LOGIN_USER);
        searchKeywords = getActivity().getIntent().getStringExtra(ViewStreamFragment.SEARCH_KEY);
        find_match = launch_search(searchKeywords);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.searchengine_fragment, container, false);
        search_result_tag = (TextView)v.findViewById(R.id.search_result_tag);
        back_to_viewAll = (Button)v.findViewById(R.id.back_from_search);
        launchSearchButton = (Button)v.findViewById(R.id.search_button_onSearch);
        searchField = (EditText)v.findViewById(R.id.search_filed_onSearch);

        back_to_viewAll.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getActivity(), ViewStreams.class);
                intent.putExtra(MainActivity.LOGIN_USER_INFO, usr_email);
                startActivity(intent);
            }
        });

        searchField.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (count > 0) {
                    launchSearchButton.setEnabled(true);
                    searchKeywords_fromhere = s.toString();
                } else {
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
                Intent intent = new Intent(getActivity(), searchEngine.class);
                intent.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                intent.putExtra(ViewStreamFragment.SEARCH_KEY, searchKeywords_fromhere);
                startActivity(intent);
            }
        });

        prevButton = (Button)v.findViewById(R.id.prev_button);
        moreButton = (Button)v.findViewById(R.id.more_button);

        prevButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(prevButton.isEnabled()){
                    currentpage--;
                    setupAdapterWrapper();
                }
            }
        });

        moreButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(moreButton.isEnabled()){
                    currentpage++;
                    setupAdapterWrapper();
                }
            }
        });

        Log.i(TAG, "Do we found anything "+find_match);


        return v;
    }

    private void setupAdapterWrapper(){
        setupAdapter(pic_url, stream_name_pic,stream_owner_pic,usr_email);
    }

    private boolean launch_search(String keyword){
        final String request_url = "http://connexversion3.appspot.com/mobileSearch";
        AsyncHttpClient httpClient = new AsyncHttpClient();
        RequestParams params = new RequestParams();
        params.add("search_key", keyword);
        params.add("usr_launch_search", usr_email);
        search_result = false;

        httpClient.get(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    String echo_key = jObject.getString("keyword");
                    search_result = jObject.getBoolean("hasResult");
                    JSONArray pic_URL = jObject.getJSONArray("cover_url");
                    JSONArray stream_NAME = jObject.getJSONArray("stream_names");
                    JSONArray stream_OWNER = jObject.getJSONArray("stream_owners");

                    if(pic_URL.length() > 0)
                        search_result = true;

                    for(int i=0; i<pic_URL.length(); i++){
                        pic_url.add(pic_URL.getString(i));
                        stream_name_pic.add(stream_NAME.getString(i));
                        stream_owner_pic.add(stream_OWNER.getString(i));
                    }

                    upbound = pic_url.size()%3 == 0 ? pic_url.size()/3 : pic_url.size()/3 + 1;

                    setupAdapter(pic_url,stream_name_pic,stream_owner_pic,usr_email);

                    Log.i(TAG, "echo key = "+echo_key+" search result is "+search_result);
                } catch (JSONException j) {
                    System.out.println("JSON Error");
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });

        return search_result;
    }

    private void setupAdapter(ArrayList<String> imageurllist,
                              ArrayList<String> stream_name, ArrayList<String> stream_owner, String usr_email){
        GridView mGridView = (GridView)getActivity().findViewById(R.id.searchViewResults);
        if(mGridView == null) return;
        Log.i(TAG,"We are in search adapter");
        if(search_result)
            search_result_tag.setText(pic_url.size()+"result(s) for "+searchKeywords+"\nClick on image to view Stream");
        else
            search_result_tag.setText("No search result");

        boolean has_more = false;
        boolean has_less = false;
        if(currentpage < upbound)
            has_more = true;
        if(currentpage > 1)
            has_less = true;

        if(!has_more){
            // disable the more button
            moreButton.setEnabled(false);
        }else {
            moreButton.setEnabled(true);
        }

        if(has_less){
            // make less button visible
            prevButton.setVisibility(View.VISIBLE);
            prevButton.setEnabled(true);
        }else {
            prevButton.setVisibility(View.INVISIBLE);
            prevButton.setEnabled(false);
        }

        int start_index = (currentpage-1)*3;
        int end_index = start_index +3;
        if(end_index > imageurllist.size())
            end_index = imageurllist.size();

        ArrayList<String> url_to_show = new ArrayList<String>(imageurllist.subList(start_index, end_index));
        ArrayList<String> streamname_to_show = new ArrayList<String>(stream_name.subList(start_index, end_index));
        ArrayList<String> streamowner_to_show = new ArrayList<String>(stream_owner.subList(start_index, end_index));

        mGridView.setAdapter(new MyAdapter(getActivity(),
                url_to_show, streamname_to_show, streamowner_to_show,usr_email,
                getActivity().getLayoutInflater()));
    }
}

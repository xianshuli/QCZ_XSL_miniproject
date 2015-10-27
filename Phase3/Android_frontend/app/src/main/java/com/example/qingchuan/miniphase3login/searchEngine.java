package com.example.qingchuan.miniphase3login;

import android.app.Fragment;

/**
 * Created by Qingchuan on 10/25/2015.
 */
public class searchEngine extends SingleFragmentActivity {
    @Override
    public Fragment createFragment(){
        return new SearchEngineFragment();
    }
}

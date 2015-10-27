package com.example.qingchuan.miniphase3login;

import android.app.Fragment;

/**
 * Created by Qingchuan on 10/23/2015.
 */
public class ViewSingleStream extends SingleFragmentActivity {
    @Override
    public Fragment createFragment(){
        return new ViewSingleStreamFragment();
    }
}

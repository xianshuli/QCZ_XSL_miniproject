package com.example.qingchuan.miniphase3login;

/**
 * Created by Qingchuan on 10/23/2015.
 */
import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.os.Bundle;

/**
 * Created by Qingchuan on 8/4/2015.
 */
public abstract class SingleFragmentActivity extends Activity{
    protected abstract Fragment createFragment();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fragment);
        FragmentManager fm = getFragmentManager();
        Fragment mFragment = fm.findFragmentById(R.id.fragmentContainer);
        if(mFragment == null){
            mFragment = createFragment();
            fm.beginTransaction().add(R.id.fragmentContainer,mFragment).commit();
        }
    }
}

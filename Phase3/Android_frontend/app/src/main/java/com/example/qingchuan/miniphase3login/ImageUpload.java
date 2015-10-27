package com.example.qingchuan.miniphase3login;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.ActionBarActivity;
import android.util.Base64;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;

/**
 * Created by Qingchuan on 10/24/2015.
 */
public class ImageUpload extends ActionBarActivity {
    private static final int PICK_IMAGE = 1;
    Context context = this;
    private String stream_name;
    private String stream_owner;
    private String usr_email;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_upload);
        stream_name = getIntent().getStringExtra(ViewStreamFragment.STREAM_NAME);
        stream_owner = getIntent().getStringExtra(ViewStreamFragment.STREAM_OWNER);
        usr_email = getIntent().getStringExtra(ViewStreamFragment.LOGIN_USER);
        // Choose image from library
        Button chooseFromLibraryButton = (Button) findViewById(R.id.choose_from_library);
        Button takefromCamera = (Button) findViewById(R.id.use_camera);

        takefromCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (checkCameraHardware(ImageUpload.this) == true) {
                    Intent intent = new Intent(ImageUpload.this, CameraActivity.class);
                    intent.putExtra(ViewStreamFragment.LOGIN_USER,usr_email);
                    startActivityForResult(intent, 2);
                }
            }
        });

        chooseFromLibraryButton.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        // To do this, go to AndroidManifest.xml to add permission
                        Intent galleryIntent = new Intent(Intent.ACTION_PICK,
                                android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                        // Start the Intent
                        startActivityForResult(galleryIntent, PICK_IMAGE);
                    }
                }
        );
    }

    private boolean checkCameraHardware(Context context) {
        if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            // this device has a camera
            return true;
        } else {
            // no camera on this device
            return false;
        }
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_IMAGE && data != null && data.getData() != null) {
            Uri selectedImage = data.getData();

            // User had pick an image.

            String[] filePathColumn = {MediaStore.Images.ImageColumns.DATA};
            Cursor cursor = getContentResolver().query(selectedImage, filePathColumn, null, null, null);
            cursor.moveToFirst();

            // Link to the image

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String imageFilePath = cursor.getString(columnIndex);
            cursor.close();

            // Bitmap imaged created and show thumbnail

            ImageView imgView = (ImageView) findViewById(R.id.thumbnail);
            final Bitmap bitmapImage = BitmapFactory.decodeFile(imageFilePath);
            imgView.setImageBitmap(bitmapImage);

            // Enable the upload button once image has been uploaded

            Button uploadButton = (Button) findViewById(R.id.upload_to_server);

            uploadButton.setClickable(true);

            uploadButton.setOnClickListener(
                    new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {

                            // Get photo caption

                            EditText text = (EditText) findViewById(R.id.upload_message);
                            String photoCaption = text.getText().toString();

                            ByteArrayOutputStream baos = new ByteArrayOutputStream();
                            bitmapImage.compress(Bitmap.CompressFormat.JPEG, 50, baos);
                            byte[] b = baos.toByteArray();
                            byte[] encodedImage = Base64.encode(b, Base64.DEFAULT);
                            String encodedImageStr = encodedImage.toString();

                            getUploadURL(b, photoCaption);
                        }
                    }
            );

        }
        else if (requestCode == 2) {
            if (resultCode != 0) {
                final String imageFilePath = data.getStringExtra("imageFile");
                System.out.println(imageFilePath);
                ImageView imgView = (ImageView) findViewById(R.id.thumbnail);

                Bitmap bitmapImage = BitmapFactory.decodeFile(imageFilePath);
                Matrix matrix = new Matrix();
                matrix.postRotate(90);
                final Bitmap rotated = Bitmap.createBitmap(bitmapImage, 0, 0, bitmapImage.getWidth(), bitmapImage.getHeight(), matrix, true);

                imgView.setImageBitmap(rotated);


                final Button uploadButton = (Button) findViewById(R.id.upload_to_server);
                uploadButton.setClickable(true);
                uploadButton.setOnClickListener(
                        new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                EditText text = (EditText) findViewById(R.id.upload_message);
                                String photoCaption = text.getText().toString();
                                //System.out.println(photoCaption);

                                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                                rotated.compress(Bitmap.CompressFormat.JPEG, 50, baos);
                                byte[] b = baos.toByteArray();
                                byte[] encodedImage = Base64.encode(b, Base64.DEFAULT);

                                String encodedImageStr = encodedImage.toString();
                                System.out.println(encodedImageStr);

                                //String location = mLocationClient.getLastLocation().getLatitude() + "_" + mLocationClient.getLastLocation().getLongitude();
                                getUploadURL(b, photoCaption);
                            }
                        }
                );
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private void getUploadURL(final byte[] encodedImage, final String photoCaption){
        String request_url="http://connexversion3.appspot.com/mobileGetUploadUrl";
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            String upload_url;

            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {

                try {
                    JSONObject jObject = new JSONObject(new String(response));

                    upload_url = jObject.getString("upload_url");
                    postToServer(encodedImage,stream_name , upload_url);

                } catch (JSONException j) {
                    System.out.println("JSON Error");
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e("Get_serving_url", "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }

    private void postToServer(byte[] encodedImage,String stream_id, String upload_url){
        RequestParams params = new RequestParams();
        params.put("file",new ByteArrayInputStream(encodedImage));
        params.put("stream_id", stream_id);
        params.put("pic_lat",MainActivity.device_lat);
        params.put("pic_long",MainActivity.device_long);
        AsyncHttpClient client = new AsyncHttpClient();
        client.post(upload_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                String pic_long = "";
                String pic_lat = "";
                String stream_id = "";
                try {
                    JSONObject jObject = new JSONObject(new String(response));

                    pic_lat = jObject.getString("pic_lat");
                    pic_long = jObject.getString("pic_long");
                    stream_id = jObject.getString("stream_id");

                } catch (JSONException j) {
                    System.out.println("JSON Error");
                }
                Toast.makeText(context, "location recorded lat= "+pic_lat+" long= "+pic_long, Toast.LENGTH_LONG).show();
                Log.w("async", "success!!!! write stream "+stream_id +" with pic pos: "+pic_lat+" : "+pic_long);
                Intent i = new Intent(ImageUpload.this, ViewSingleStream.class);
                i.putExtra(ViewStreamFragment.LOGIN_USER, usr_email);
                i.putExtra(ViewStreamFragment.STREAM_OWNER, stream_owner);
                i.putExtra(ViewStreamFragment.STREAM_NAME, stream_name);
                startActivity(i);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e("Posting_to_blob", "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.image_upload, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}

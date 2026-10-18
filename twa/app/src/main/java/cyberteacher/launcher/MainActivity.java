package cyberteacher.launcher;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // TWA launch is handled by com.google.androidbrowserhelper.trusted.LauncherActivity
        // declared in AndroidManifest.xml. This activity is a placeholder.
        finish();
    }
}

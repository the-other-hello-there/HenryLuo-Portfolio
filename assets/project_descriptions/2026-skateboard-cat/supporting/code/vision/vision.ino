#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "REPLACE_WITH_YOUR_VALUE";
const char* password = "REPLACE_WITH_YOUR_VALUE";

const int BRIGHTNESS_THRESHOLD = 240;
const framesize_t FRAME_SIZE = FRAMESIZE_QQVGA;

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

WebServer server(80);

struct DetectionResult {
  int brightest;
  int x;
  int y;
  bool aboveThreshold;
  unsigned long lastUpdateMs;
};

DetectionResult lastResult = {0, -1, -1, false, 0};

DetectionResult detectBrightest(camera_fb_t* fb) {
  DetectionResult result;
  result.brightest = 0;
  result.x = -1;
  result.y = -1;
  result.aboveThreshold = false;
  result.lastUpdateMs = millis();

  if (!fb || fb->format != PIXFORMAT_GRAYSCALE) {
    return result;
  }

  int width = fb->width;
  int height = fb->height;
  uint8_t* pixels = fb->buf;

  for (int y = 0; y < height; y++) {
    int row = y * width;
    for (int x = 0; x < width; x++) {
      uint8_t b = pixels[row + x];
      if (b > result.brightest) {
        result.brightest = b;
        result.x = x;
        result.y = y;
      }
    }
  }

  result.aboveThreshold = (result.brightest >= BRIGHTNESS_THRESHOLD);
  return result;
}

void handleRoot() {
  String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ESP32-CAM Laser Tracker</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; background: #111; color: #eee; }
    .box { margin-top: 15px; padding: 14px; background: #1d1d1d; border-radius: 8px; max-width: 420px; }
    .hit { color: #00ff88; font-weight: bold; }
    .miss { color: #ff6666; font-weight: bold; }
    .mono { font-family: Consolas, monospace; }
  </style>
</head>
<body>
  <h2>Laser Tracker</h2>
  <div class="box">
    <div>Brightest value: <span id="val" class="mono">-</span></div>
    <div>X: <span id="x" class="mono">-</span></div>
    <div>Y: <span id="y" class="mono">-</span></div>
    <div>Status: <span id="status">-</span></div>
    <div>Age (ms): <span id="age" class="mono">-</span></div>
  </div>

  <script>
    const val = document.getElementById('val');
    const xOut = document.getElementById('x');
    const yOut = document.getElementById('y');
    const status = document.getElementById('status');
    const age = document.getElementById('age');

    async function refreshData() {
      try {
        const r = await fetch('/brightest?ts=' + Date.now(), { cache: 'no-store' });
        const j = await r.json();

        val.textContent = j.brightest;
        xOut.textContent = j.x;
        yOut.textContent = j.y;
        age.textContent = j.ageMs;

        if (j.aboveThreshold) {
          status.textContent = 'BRIGHT SPOT DETECTED';
          status.className = 'hit';
        } else {
          status.textContent = 'below threshold';
          status.className = 'miss';
        }
      } catch (e) {
        status.textContent = 'read error';
        status.className = 'miss';
      }
    }

    setInterval(refreshData, 100);
    refreshData();
  </script>
</body>
</html>
)rawliteral";

  server.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  server.sendHeader("Pragma", "no-cache");
  server.sendHeader("Expires", "0");
  server.send(200, "text/html", html);
}

void handleBrightest() {
  unsigned long ageMs = millis() - lastResult.lastUpdateMs;

  String json = "{";
  json += "\"brightest\":" + String(lastResult.brightest) + ",";
  json += "\"x\":" + String(lastResult.x) + ",";
  json += "\"y\":" + String(lastResult.y) + ",";
  json += "\"aboveThreshold\":" + String(lastResult.aboveThreshold ? "true" : "false") + ",";
  json += "\"ageMs\":" + String(ageMs);
  json += "}";

  server.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  server.sendHeader("Pragma", "no-cache");
  server.sendHeader("Expires", "0");
  server.send(200, "application/json", json);
}

bool initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 10000000;
  config.pixel_format = PIXFORMAT_GRAYSCALE;
  config.frame_size = FRAME_SIZE;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }

  sensor_t* s = esp_camera_sensor_get();
  if (s) {
    s->set_framesize(s, FRAME_SIZE);
    s->set_brightness(s, 0);
    s->set_contrast(s, 2);
    s->set_saturation(s, -2);
    s->set_special_effect(s, 2);
    s->set_whitebal(s, 0);
    s->set_awb_gain(s, 0);
    s->set_exposure_ctrl(s, 0);
    s->set_aec2(s, 0);
    s->set_ae_level(s, -1);
    s->set_gain_ctrl(s, 0);
    s->set_agc_gain(s, 0);
    s->set_hmirror(s, 0);
    s->set_vflip(s, 0);
  }

  return true;
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(false);
  Serial.println();
  Serial.println("Booting...");

  if (!initCamera()) {
    Serial.println("Camera init failed");
    while (true) {
      delay(1000);
    }
  }

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Open this in your browser: http://");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/brightest", HTTP_GET, handleBrightest);
  server.begin();

  lastResult.lastUpdateMs = millis();
}

void loop() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (fb) {
    lastResult = detectBrightest(fb);
    esp_camera_fb_return(fb);
  }

  server.handleClient();
}
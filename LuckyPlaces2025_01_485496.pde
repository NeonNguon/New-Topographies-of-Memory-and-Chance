// Use a six-digit input string.
// Digits 1-3 control colors.
// All 6 digits control the 6 independent rotation axes.
String input = "485496"; 
color fg1, fg2, bg; // 3-color system
int rot1X, rot1Y, rot1Z; // Rotation directions for Image 1
int rot2X, rot2Y, rot2Z; // Rotation directions for Image 2

PImage img1, img2;
// Tile count is kept low for performance. 
int tilesX = 1200; 
int tilesY = 800;

// This example uses the "Vietnamese Lottery" palette.
// --- Palette: Refined Vietnamese Lottery (Swapped) ---
// fg1 and fg2 palettes have been switched.

// --- Palette: Vietnamese Lottery (Blue Focus - Swapped) ---
// fg1 and fg2 palettes have been switched.

color[] fg1Palette = {
  #6D4C41, // Coffee Brown
  #78909C, // Slate Gray
  #26A69A, // Teal
  #FBC02D, // Yellow
  #AFB42B, // Lime Green
  #D84315, // Burnt Orange
  #5E35B1, // Deep Violet
  #689F38, // Muted Green
  #8D6E63, // Taupe
  #546E7A  // Dark Slate Gray
};

color[] fg2Palette = {
  #0096C7, // Bright Blue
  #00B4D8, // Sky Blue
  #48CAE4, // Light Sky Blue
  #E53935, // Strong Red
  #FDD835, // Vibrant Yellow
  #023E8A, // Deep Blue
  #FB8C00, // Bright Orange
  #43A047, // Bright Green
  #C2185B, // Hot Pink
  #0077B6  // Cerulean Blue
};

color[] bgPalette = {
  #E3F2FD, // Pale Blue
  #E0F7FA, // Light Cyan
  #FFF8E1, // Pale Yellow
  #FCE4EC, // Light Pink
  #F1F8E9, // Pale Green
  #FAFAFA, // Off-white
  #FFFDE7, // Lighter Yellow
  #E8EAF6, // Lavender
  #FFF3E0, // Pale Orange
  #ECEFF1  // Very Light Gray
};


void setup() {
  size(1200, 800, P3D);
  colorMode(RGB, 255);
  sphereDetail(8); // Use low-poly spheres for better performance

  // Load & size your images
  try {
    img1 = loadImage("485496.jpg"); // Placeholder name
    img2 = loadImage("bee (48).png"); // Placeholder name
  } catch (Exception e) {
    println("Error loading images. Make sure they are in the 'data' folder.");
    img1 = createImage(64, 64, RGB);
    img2 = createImage(64, 64, ARGB);
  }

  img1.resize(tilesX, tilesY);
  float aspectRatio = float(img2.width) / float(img2.height);
  img2.resize(int(tilesY * aspectRatio), tilesY);

  // Parse 6 digits from the input string
  if (input.length() < 6) {
    println("Input string must be 6 digits long. Using default '012345'.");
    input = "012345";
  }
  // Digits 1-6
  int d1 = constrain(input.charAt(0) - '0', 0, 9);
  int d2 = constrain(input.charAt(1) - '0', 0, 9);
  int d3 = constrain(input.charAt(2) - '0', 0, 9);
  int d4 = constrain(input.charAt(3) - '0', 0, 9);
  int d5 = constrain(input.charAt(4) - '0', 0, 9);
  int d6 = constrain(input.charAt(5) - '0', 0, 9);

  // Assign colors from the first 3 digits
  fg1 = fg1Palette[d1];
  fg2 = fg2Palette[d2];
  bg = bgPalette[d3];
  
  // Assign rotation directions for all 6 axes from all 6 digits
  // Even number = positive rotation (1), Odd number = negative rotation (-1)
  rot1X = (d1 % 2 == 0) ? 1 : -1;
  rot1Y = (d2 % 2 == 0) ? 1 : -1;
  rot1Z = (d3 % 2 == 0) ? 1 : -1;
  
  rot2X = (d4 % 2 == 0) ? 1 : -1;
  rot2Y = (d5 % 2 == 0) ? 1 : -1;
  rot2Z = (d6 % 2 == 0) ? 1 : -1;
}

void draw() {
  background(bg);
  
  noStroke();
  rectMode(CENTER);

  float tileW = (float)width / tilesX;
  float tileH = (float)height / tilesY;
  
  float rotationAngle = frameCount * 3.6; // 100 frames for a full rotation

  // First image with its own 3-axis rotation
  push();
  translate(width / 2, height / 2);
  scale(1);
  rotateX(radians(rotationAngle * rot1X));
  rotateY(radians(rotationAngle * rot1Y));
  rotateZ(radians(rotationAngle * rot1Z));
  fill(fg1);
  drawImageTiles(img1, tileW, tileH);
  pop();

  // Second image with its own independent 3-axis rotation
  push();
  translate(width / 2, height / 2, 75); // Adds a small push forward on the Z-axis
  scale(1);
  rotateX(radians(rotationAngle * rot2X));
  rotateY(radians(rotationAngle * rot2Y));
  rotateZ(radians(rotationAngle * rot2Z));
  fill(fg2);
  drawImageTiles(img2, tileW, tileH);
  pop();
  
  // ADD THIS LINE HERE
  saveFrame("output/frame_####.png");

  // Automatically stop after 100 frames
  if (frameCount >= 100) {
    noLoop();
    println("100 frames rendered. Animation stopped.");
  }
}

// This function remains the same
void drawImageTiles(PImage img, float tileW, float tileH) {
  float imageGridWidth = img.width * tileW;
  float imageGridHeight = img.height * tileH;

  for (int x = 0; x < img.width; x++) {
    for (int y = 0; y < img.height; y++) {
      float b = brightness(img.get(x, y));
      
      float s = map(b, 0, 255, 1.2, 0); 
      float z = map(b, 0, 255, -200, 200);

      push();
      translate(x * tileW - imageGridWidth / 2, y * tileH - imageGridHeight / 2, z);
      sphere(tileW * s * 0.8); // Using low-poly sphere for organic look and speed
      pop();
    }
  }
}

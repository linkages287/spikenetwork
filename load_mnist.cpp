#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdint>
#include <algorithm>
#include <cmath>
#include <random>
#include <cstdlib>

// MNIST data loader for C++
// Loads MNIST dataset from original binary format or CSV

class MNISTLoader {
public:
    struct Sample {
        std::vector<double> data;  // 784 pixels (28x28)
        int label;                 // Digit label (0-9)
    };
    
    // Load MNIST from CSV format (easier to work with)
    static std::vector<Sample> load_from_csv(const std::string& filename) {
        std::vector<Sample> dataset;
        std::ifstream file(filename);
        
        if (!file.is_open()) {
            std::cerr << "Error: Could not open " << filename << "\n";
            std::cerr << "MNIST CSV files can be downloaded from:\n";
            std::cerr << "  https://www.kaggle.com/datasets/oddrationale/mnist-in-csv\n";
            return dataset;
        }
        
        std::string line;
        bool first_line = true;
        
        while (std::getline(file, line)) {
            if (first_line) {
                first_line = false;
                continue; // Skip header
            }
            
            std::stringstream ss(line);
            std::string item;
            
            Sample s;
            bool first = true;
            
            while (std::getline(ss, item, ',')) {
                if (first) {
                    s.label = std::stoi(item);
                    first = false;
                } else {
                    // Normalize pixel values from 0-255 to 0-1
                    double pixel_value = std::stod(item) / 255.0;
                    s.data.push_back(pixel_value);
                }
            }
            
            dataset.push_back(s);
        }
        
        return dataset;
    }
    
    // Generate synthetic MNIST-like data for testing (if real MNIST not available)
    static std::vector<Sample> generate_synthetic_mnist(int samples_per_digit = 100) {
        std::vector<Sample> dataset;
        int image_size = 28;
        int total_pixels = image_size * image_size; // 784
        
        for (int digit = 0; digit < 10; ++digit) {
            for (int sample = 0; sample < samples_per_digit; ++sample) {
                Sample s;
                s.label = digit;
                s.data.resize(total_pixels, 0.0);
                
                // Create digit pattern in 28x28 grid
                create_mnist_digit_pattern(digit, s.data, image_size, sample);
                
                dataset.push_back(s);
            }
        }
        
        return dataset;
    }
    
    
private:
    static void create_mnist_digit_pattern(int digit, std::vector<double>& pattern, 
                                          int image_size, int variation) {
        std::mt19937 gen(digit * 10000 + variation);
        std::uniform_real_distribution<double> noise(-0.1, 0.1);
        
        // Create base pattern in center region
        int center_x = image_size / 2;
        int center_y = image_size / 2;
        
        switch (digit) {
            case 0: // Circle
                draw_circle(pattern, image_size, center_x, center_y, 10.0, 1.0);
                break;
            case 1: // Vertical line
                draw_line(pattern, image_size, center_x, 4, center_x, image_size - 4, 1.0);
                break;
            case 2: // S-shape
                draw_s_curve(pattern, image_size, center_x, center_y);
                break;
            case 3: // Three horizontal bars
                draw_three_bars(pattern, image_size, center_x, center_y);
                break;
            case 4: // L-shape
                draw_l_shape(pattern, image_size, center_x, center_y);
                break;
            case 5: // S-shape variant
                draw_five_shape(pattern, image_size, center_x, center_y);
                break;
            case 6: // Circle with tail
                draw_circle(pattern, image_size, center_x, center_y + 3, 9.0, 1.0);
                draw_line(pattern, image_size, center_x - 8, center_y, center_x - 8, center_y + 8, 1.0);
                break;
            case 7: // Diagonal + horizontal
                draw_line(pattern, image_size, 4, 4, image_size - 4, 4, 1.0);
                draw_line(pattern, image_size, image_size - 4, 4, center_x, image_size - 4, 1.0);
                break;
            case 8: // Two circles
                draw_circle(pattern, image_size, center_x, center_y - 4, 6.0, 1.0);
                draw_circle(pattern, image_size, center_x, center_y + 4, 6.0, 1.0);
                break;
            case 9: // Inverted 6
                draw_circle(pattern, image_size, center_x, center_y - 3, 9.0, 1.0);
                draw_line(pattern, image_size, center_x + 8, center_y - 8, center_x + 8, center_y, 1.0);
                break;
        }
        
        // Add noise
        for (size_t idx = 0; idx < pattern.size(); ++idx) {
            pattern[idx] += noise(gen);
            if (pattern[idx] < 0) pattern[idx] = 0;
            if (pattern[idx] > 1) pattern[idx] = 1;
        }
    }
    
    static void draw_line(std::vector<double>& pattern, int size, 
                         int x1, int y1, int x2, int y2, double value) {
        int dx = std::abs(x2 - x1);
        int dy = std::abs(y2 - y1);
        int steps = std::max(dx, dy);
        
        for (int i = 0; i <= steps; ++i) {
            double t = (steps > 0) ? (double)i / steps : 0;
            int x = (int)(x1 + t * (x2 - x1));
            int y = (int)(y1 + t * (y2 - y1));
            
            if (x >= 0 && x < size && y >= 0 && y < size) {
                pattern[y * size + x] = value;
            }
        }
    }
    
    static void draw_circle(std::vector<double>& pattern, int size,
                           int cx, int cy, double radius, double value) {
        for (int y = 0; y < size; ++y) {
            for (int x = 0; x < size; ++x) {
                double dx = x - cx;
                double dy = y - cy;
                double dist = sqrt(dx*dx + dy*dy);
                if (fabs(dist - radius) < 1.0) {
                    pattern[y * size + x] = value;
                }
            }
        }
    }
    
    static void draw_s_curve(std::vector<double>& pattern, int size, int cx, int cy) {
        draw_line(pattern, size, cx - 10, cy - 8, cx + 10, cy - 8, 1.0);
        draw_line(pattern, size, cx + 10, cy - 8, cx + 10, cy, 1.0);
        draw_line(pattern, size, cx + 10, cy, cx - 10, cy, 1.0);
        draw_line(pattern, size, cx - 10, cy, cx - 10, cy + 8, 1.0);
        draw_line(pattern, size, cx - 10, cy + 8, cx + 10, cy + 8, 1.0);
    }
    
    static void draw_three_bars(std::vector<double>& pattern, int size, int cx, int cy) {
        draw_line(pattern, size, cx - 10, cy - 8, cx + 10, cy - 8, 1.0);
        draw_line(pattern, size, cx - 10, cy, cx + 10, cy, 1.0);
        draw_line(pattern, size, cx - 10, cy + 8, cx + 10, cy + 8, 1.0);
        draw_line(pattern, size, cx + 10, cy - 8, cx + 10, cy + 8, 1.0);
    }
    
    static void draw_l_shape(std::vector<double>& pattern, int size, int cx, int cy) {
        draw_line(pattern, size, cx - 10, cy - 8, cx - 10, cy, 1.0);
        draw_line(pattern, size, cx - 10, cy, cx + 10, cy, 1.0);
        draw_line(pattern, size, cx + 10, cy - 8, cx + 10, cy + 8, 1.0);
    }
    
    static void draw_five_shape(std::vector<double>& pattern, int size, int cx, int cy) {
        draw_line(pattern, size, cx + 10, cy - 8, cx - 10, cy - 8, 1.0);
        draw_line(pattern, size, cx - 10, cy - 8, cx - 10, cy, 1.0);
        draw_line(pattern, size, cx - 10, cy, cx + 10, cy, 1.0);
        draw_line(pattern, size, cx + 10, cy, cx + 10, cy + 8, 1.0);
        draw_line(pattern, size, cx + 10, cy + 8, cx - 10, cy + 8, 1.0);
    }
};


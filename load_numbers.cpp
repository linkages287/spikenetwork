#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <random>
#include <cmath>

// Simple number data loader
// Creates synthetic digit patterns (0-9) as input vectors
class NumberDataLoader {
public:
    struct Sample {
        std::vector<double> data;  // Input pattern (flattened image)
        int label;                 // Digit label (0-9)
    };
    
    // Generate synthetic digit patterns
    // Each digit is represented as a simple pattern in a grid
    static std::vector<Sample> generate_synthetic_data(int samples_per_digit = 10) {
        std::vector<Sample> dataset;
        
        // Create patterns for digits 0-9
        // Each digit is a 7x7 grid (49 pixels)
        int grid_size = 7;
        int total_pixels = grid_size * grid_size;
        
        for (int digit = 0; digit < 10; ++digit) {
            for (int sample = 0; sample < samples_per_digit; ++sample) {
                Sample s;
                s.label = digit;
                s.data.resize(total_pixels, 0.0);
                
                // Create pattern based on digit
                create_digit_pattern(digit, s.data, grid_size, sample);
                
                dataset.push_back(s);
            }
        }
        
        return dataset;
    }
    
    // Load from CSV file (format: label,pixel1,pixel2,...,pixel49)
    static std::vector<Sample> load_from_csv(const std::string& filename) {
        std::vector<Sample> dataset;
        std::ifstream file(filename);
        
        if (!file.is_open()) {
            std::cerr << "Warning: Could not open " << filename 
                      << ". Using synthetic data instead.\n";
            return generate_synthetic_data();
        }
        
        std::string line;
        while (std::getline(file, line)) {
            std::stringstream ss(line);
            std::string item;
            
            Sample s;
            bool first = true;
            while (std::getline(ss, item, ',')) {
                if (first) {
                    s.label = std::stoi(item);
                    first = false;
                } else {
                    s.data.push_back(std::stod(item));
                }
            }
            dataset.push_back(s);
        }
        
        return dataset;
    }
    
private:
    static void create_digit_pattern(int digit, std::vector<double>& pattern, 
                                     int grid_size, int variation) {
        // Add some randomness for variation
        std::mt19937 gen(digit * 1000 + variation);
        std::uniform_real_distribution<> noise(-0.1, 0.1);
        
        // Define patterns for each digit (simplified representations)
        switch (digit) {
            case 0: // Circle/zero
                draw_circle(pattern, grid_size, 3, 3, 2.5, 1.0);
                break;
            case 1: // Vertical line
                draw_line(pattern, grid_size, 3, 1, 3, 5, 1.0);
                break;
            case 2: // S-shape
                draw_line(pattern, grid_size, 1, 1, 5, 1, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 3, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 1, 5, 1.0);
                draw_line(pattern, grid_size, 1, 5, 5, 5, 1.0);
                break;
            case 3: // Two horizontal lines with vertical
                draw_line(pattern, grid_size, 1, 1, 4, 1, 1.0);
                draw_line(pattern, grid_size, 1, 3, 4, 3, 1.0);
                draw_line(pattern, grid_size, 1, 5, 4, 5, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 5, 1.0);
                break;
            case 4: // L-shape
                draw_line(pattern, grid_size, 1, 1, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 5, 1.0);
                break;
            case 5: // S-shape variant
                draw_line(pattern, grid_size, 5, 1, 1, 1, 1.0);
                draw_line(pattern, grid_size, 1, 1, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 3, 5, 5, 1.0);
                draw_line(pattern, grid_size, 5, 5, 1, 5, 1.0);
                break;
            case 6: // Circle with tail
                draw_circle(pattern, grid_size, 3, 4, 2.0, 1.0);
                draw_line(pattern, grid_size, 1, 3, 1, 5, 1.0);
                break;
            case 7: // Diagonal + horizontal
                draw_line(pattern, grid_size, 1, 1, 5, 1, 1.0);
                draw_line(pattern, grid_size, 5, 1, 3, 5, 1.0);
                break;
            case 8: // Two circles
                draw_circle(pattern, grid_size, 3, 2, 1.5, 1.0);
                draw_circle(pattern, grid_size, 3, 5, 1.5, 1.0);
                break;
            case 9: // Inverted 6
                draw_circle(pattern, grid_size, 3, 3, 2.0, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 3, 1.0);
                break;
        }
        
        // Add noise
        for (auto& p : pattern) {
            p += noise(gen);
            if (p < 0) p = 0;
            if (p > 1) p = 1;
        }
    }
    
    static void draw_line(std::vector<double>& pattern, int grid_size, 
                         int x1, int y1, int x2, int y2, double value) {
        int dx = abs(x2 - x1);
        int dy = abs(y2 - y1);
        int steps = std::max(dx, dy);
        
        for (int i = 0; i <= steps; ++i) {
            double t = (steps > 0) ? (double)i / steps : 0;
            int x = (int)(x1 + t * (x2 - x1));
            int y = (int)(y1 + t * (y2 - y1));
            
            if (x >= 0 && x < grid_size && y >= 0 && y < grid_size) {
                pattern[y * grid_size + x] = value;
            }
        }
    }
    
    static void draw_circle(std::vector<double>& pattern, int grid_size,
                           int cx, int cy, double radius, double value) {
        for (int y = 0; y < grid_size; ++y) {
            for (int x = 0; x < grid_size; ++x) {
                double dx = x - cx;
                double dy = y - cy;
                double dist = sqrt(dx*dx + dy*dy);
                if (fabs(dist - radius) < 0.5) {
                    pattern[y * grid_size + x] = value;
                }
            }
        }
    }
};


CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
TARGET = spike_network
EXPORT_TARGET = export_network
TRAIN_TARGET = train_numbers
SIMULATE_TARGET = simulate_spiking
TRAIN_ANIM_TARGET = train_with_animation
SOURCES = main.cpp neuron.cpp network.cpp
EXPORT_SOURCES = export_network.cpp neuron.cpp network.cpp
TRAIN_SOURCES = train_numbers.cpp neuron.cpp network.cpp
SIMULATE_SOURCES = simulate_spiking.cpp neuron.cpp network.cpp
TRAIN_ANIM_SOURCES = train_with_animation.cpp neuron.cpp network.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXPORT_OBJECTS = $(EXPORT_SOURCES:.cpp=.o)
TRAIN_OBJECTS = $(TRAIN_SOURCES:.cpp=.o)
SIMULATE_OBJECTS = $(SIMULATE_SOURCES:.cpp=.o)
TRAIN_ANIM_OBJECTS = $(TRAIN_ANIM_SOURCES:.cpp=.o)

all: $(TARGET) $(EXPORT_TARGET) $(TRAIN_TARGET) $(SIMULATE_TARGET) $(TRAIN_ANIM_TARGET)

$(TARGET): main.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.o neuron.o network.o

$(EXPORT_TARGET): export_network.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(EXPORT_TARGET) export_network.o neuron.o network.o

$(TRAIN_TARGET): train_numbers.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(TRAIN_TARGET) train_numbers.o neuron.o network.o

$(SIMULATE_TARGET): simulate_spiking.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(SIMULATE_TARGET) simulate_spiking.o neuron.o network.o

$(TRAIN_ANIM_TARGET): train_with_animation.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(TRAIN_ANIM_TARGET) train_with_animation.o neuron.o network.o

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(EXPORT_OBJECTS) $(TRAIN_OBJECTS) $(SIMULATE_OBJECTS) $(TRAIN_ANIM_OBJECTS) $(TARGET) $(EXPORT_TARGET) $(TRAIN_TARGET) $(SIMULATE_TARGET) $(TRAIN_ANIM_TARGET)
	rm -rf data/json/*.json

run: $(TARGET)
	./$(TARGET)

export: $(EXPORT_TARGET)
	./$(EXPORT_TARGET) data/json/network_state.json 10

setup-venv:
	@echo "Setting up Python virtual environment..."
	@./setup_visualization.sh

visualize: export
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python visualize_network.py data/json/network_state.json_step0.json; \
	else \
		echo "Virtual environment not found. Run 'make setup-venv' first."; \
		python3 visualize_network.py data/json/network_state.json_step0.json; \
	fi

demo: setup-venv export_network
	@./demo_visualization.sh

train: $(TRAIN_TARGET)
	./$(TRAIN_TARGET)

visualize-3d: data/json/trained_network.json
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python visualize_3d.py data/json/trained_network.json; \
	else \
		python3 visualize_3d.py data/json/trained_network.json; \
	fi

animate-spiking: $(SIMULATE_TARGET)
	@./$(SIMULATE_TARGET) data/json/trained_network.json 0 30
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python animate_3d_spiking.py data/json/spike_animation_step0.json; \
	else \
		python3 animate_3d_spiking.py data/json/spike_animation_step0.json; \
	fi

animate-training: $(TRAIN_ANIM_TARGET)
	@./$(TRAIN_ANIM_TARGET) 3 0.01
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python animate_training.py data/json/training_epoch0_test_digit0_step0.json; \
	else \
		python3 animate_training.py data/json/training_epoch0_test_digit0_step0.json; \
	fi

.PHONY: all clean run export visualize setup-venv demo train visualize-3d animate-spiking animate-training


CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
TARGET = spike_network
EXPORT_TARGET = export_network
SOURCES = main.cpp neuron.cpp network.cpp
EXPORT_SOURCES = export_network.cpp neuron.cpp network.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXPORT_OBJECTS = $(EXPORT_SOURCES:.cpp=.o)

all: $(TARGET) $(EXPORT_TARGET)

$(TARGET): main.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.o neuron.o network.o

$(EXPORT_TARGET): export_network.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(EXPORT_TARGET) export_network.o neuron.o network.o

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(EXPORT_OBJECTS) $(TARGET) $(EXPORT_TARGET) *.json

run: $(TARGET)
	./$(TARGET)

export: $(EXPORT_TARGET)
	./$(EXPORT_TARGET) network_state.json 10

setup-venv:
	@echo "Setting up Python virtual environment..."
	@./setup_visualization.sh

visualize: export
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python visualize_network.py network_state.json_step0.json; \
	else \
		echo "Virtual environment not found. Run 'make setup-venv' first."; \
		python3 visualize_network.py network_state.json_step0.json; \
	fi

demo: setup-venv export_network
	@./demo_visualization.sh

.PHONY: all clean run export visualize setup-venv demo


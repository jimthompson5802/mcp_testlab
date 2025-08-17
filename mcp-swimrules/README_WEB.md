# Swim Rules Agent Web Application

A web-based interface for USA Swimming rules analysis and violation checking, built with FastAPI and modern web technologies.

## Features

- **Intuitive Web Interface**: Clean, responsive design for easy scenario input and analysis
- **Real-time Analysis**: Fast scenario analysis with confidence scoring
- **Rule Citations**: Detailed rule citations with categorized references
- **Example Scenarios**: Built-in examples for different violation types
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Offline Support**: Basic offline functionality with service worker

## User Interface Components

### Scenario Input
- Multi-line text area with 2000 character limit
- Real-time character counter with warnings
- Placeholder text with example scenarios
- Input validation and error handling

### Analysis Results
- **Decision Banner**: Color-coded results (ALLOWED/DISQUALIFICATION)
- **Confidence Score**: AI-generated confidence percentage
- **Detailed Rationale**: Comprehensive explanation of the decision
- **Rule Citations**: Organized by category (Primary, Supporting, Related)

### Interactive Features
- **Example Scenarios**: Modal with categorized violation examples
- **Keyboard Shortcuts**: Ctrl/Cmd+Enter to analyze
- **Error Handling**: User-friendly error messages
- **Loading Indicators**: Visual feedback during analysis

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements_web.txt
   ```

2. **Start the Server**
   ```bash
   python start_server.py
   ```
   
   Or manually:
   ```bash
   uvicorn app_server:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Open Your Browser**
   Navigate to: `http://localhost:8000`

## Usage

### Analyzing Scenarios

1. **Enter Scenario**: Type or paste a swimming scenario description in the text area
2. **Click Analyze**: Press the "Analyze" button or use Ctrl/Cmd+Enter
3. **Review Results**: View the decision, rationale, and rule citations
4. **Load Examples**: Use the "Load Example" button to try sample scenarios

### Example Scenarios

The application includes pre-loaded examples in three categories:

- **Stroke Violations**: Technique and touch requirements
- **Starting Violations**: False starts and relay violations  
- **General Violations**: Lane interference and equipment issues

### Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Analyze current scenario
- `Escape`: Close modals and error messages

## API Endpoints

### `POST /api/analyze`
Analyze a swimming scenario for rule violations.

**Request Body:**
```json
{
  "scenario": "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn"
}
```

**Response:**
```json
{
  "decision": "DISQUALIFICATION",
  "confidence": 95.0,
  "rationale": "The described scenario constitutes a violation...",
  "rule_citations": [
    {
      "rule_number": "101.2.2",
      "rule_title": "Breaststroke Turn Requirements",
      "rule_category": "Stroke Technique"
    }
  ]
}
```

### `GET /api/scenario-examples`
Retrieve example scenarios for testing.

**Response:**
```json
{
  "stroke_violations": ["Example 1", "Example 2"],
  "starting_violations": ["Example 3", "Example 4"],
  "general_violations": ["Example 5", "Example 6"]
}
```

### `GET /health`
Health check endpoint.

## File Structure

```
mcp-swimrules/
├── app_server.py           # FastAPI application server
├── start_server.py         # Startup script
├── requirements_web.txt    # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── styles.css         # CSS styling
    ├── script.js          # JavaScript functionality
    └── sw.js             # Service worker
```

## Development

### Code Style
- Follows PEP 8 conventions
- 120-character line length limit
- Type hints for all functions
- Comprehensive error handling

### Testing
Run the development server with auto-reload:
```bash
uvicorn app_server:app --reload --host 0.0.0.0 --port 8000
```

### Customization
- **Styling**: Modify `static/styles.css` for visual changes
- **Functionality**: Update `static/script.js` for frontend behavior
- **API Logic**: Edit `app_server.py` for backend changes

## Future Enhancements

- **MCP Integration**: Connect to actual MCP server with swim rules tools
- **User Authentication**: Add user accounts and session management
- **Advanced Search**: Implement full-text search across rule database
- **Offline Mode**: Enhanced offline functionality with cached rules
- **Mobile App**: Native mobile application development
- **Print Support**: Optimized printing for official documentation

## Technical Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom CSS with responsive design
- **Icons**: Unicode emojis for cross-platform compatibility
- **Offline**: Service Worker for basic offline functionality

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project follows the same license as the parent MCP Testlab project.

## Contributing

1. Follow the coding style guidelines in `.github/copilot-instructions.md`
2. Test all changes thoroughly
3. Ensure responsive design works on all screen sizes
4. Update documentation for any new features

# Visualization Integration Specification

## 1. Core Visualization Structure

Every visualization object MUST follow this basic structure:
```json
{
    "source": string,      // Source of the visualization (e.g., "nounproject", "colors", "openai")
    "name": string,        // Identifier for the visualization
    "image": string,       // Primary image reference
    "images"?: string[],   // Optional array for multiple images (e.g., color schemes)
    "properties"?: {       // Optional visualization-specific properties
        string: any
    }
}
```

## 2. Visualization Placement

Visualizations can be integrated at multiple levels:

### 2.1 Object Level
- Object modifiers should have visualizations representing their values
- Alternatives should include their own visualizations
```json
{
    "name": "method",
    "value": "post",
    "visualization": {
        "source": "nounproject",
        "name": "http_post",
        "image": "post_method.svg"
    }
}
```

### 2.2 Type Level
- Type components should have visualizations representing their category
```json
{
    "name": "illustration",
    "category": "visual",
    "visualization": {
        "source": "nounproject",
        "name": "art_palette",
        "image": "palette.svg"
    }
}
```

### 2.3 Artifact Level
- Main artifact visualization (e.g., final image, UI component)
- Attribute visualizations
- Relationship visualizations
```json
{
    "visualization": {
        "source": "openai",
        "name": "final_output",
        "image": "result.png",
        "properties": {
            "layout": "vertical"
        }
    }
}
```

## 3. Visualization Sources

### 3.1 Noun Project (`"source": "nounproject"`)
- Used for: Icons, symbols, conceptual representations
- Required properties: None
- Optional properties: `"attribution"`, `"license"`

### 3.2 Colors (`"source": "colors"`)
- Used for: Color schemes, palettes, themes
- Required properties: `"images"` array with color SVGs
- Optional properties: `"palette_name"`, `"color_space"`

### 3.3 OpenAI (`"source": "openai"`)
- Used for: Generated images, complex visualizations
- Required properties: None
- Optional properties: `"model"`, `"prompt"`

### 3.4 Custom (`"source": "custom"`)
- Used for: Project-specific visualizations
- Required properties: None
- Optional properties: Based on implementation

## 4. Metadata Configuration

Every example MUST include visualization configuration in metadata:
```json
{
    "metadata": {
        "visualization_config": {
            "theme": string,          // e.g., "technical", "artistic", "data"
            "layout": string,         // e.g., "hierarchical", "vertical", "grid"
            "icon_size": string,      // e.g., "small", "medium", "large"
            "show_relationships": boolean
        }
    }
}
```

## 5. Example Type-Specific Requirements

### 5.1 UI Components
- Must include interactive state visualizations
- Should show component hierarchy
- Include accessibility-related icons

### 5.2 Data Analysis
- Must include chart type icons
- Show data flow relationships
- Include database and processing icons

### 5.3 Code Generation
- Include language/framework icons
- Show architectural relationships
- Include API/endpoint icons

### 5.4 Visual Content
- Include style/mood icons
- Show color scheme visualizations
- Include composition/layout icons

### 5.5 Question/Answer
- Include topic/category icons
- Show knowledge domain relationships
- Include interaction flow icons 